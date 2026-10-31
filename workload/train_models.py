#!/usr/bin/env python3
"""Train one XGBoost model per series, one model at a time on each worker.

On the cluster (from master):

    spark-submit train_models.py --input /user/$USER/sample.parquet --output /user/$USER/models

Baseline on one computer, no Spark (for the benchmark):

    python3 train_models.py --local --input sample.parquet

How "one model per worker" works: each worker has one Spark executor with 4 cores
(spark.executor.cores=4, set in spark-defaults.conf), and this job asks for 4 cores
per task (spark.task.cpus=4). So each executor runs one task at a time, and each task
trains one series' model with XGBoost using all 4 cores.

Input: Parquet with one row per series per day: --series-col, --date-col, --target-col.
Output: Parquet with one row per series: metrics, timing, the worker that trained it,
and the model itself (XGBoost UBJSON bytes).
"""
import argparse
import os
import socket
import time

import numpy as np
import pandas as pd
import xgboost as xgb

LAGS = (1, 7, 14, 28)
TEST_DAYS = 56
PARAMS = {
    "objective": "reg:squarederror",
    "eta": 0.05,
    "max_depth": 6,
    "subsample": 0.8,
    "colsample_bytree": 0.8,
    "seed": 42,
}
ROUNDS = 300

RESULT_SCHEMA = (
    "series_id string, rows long, rmse double, mae double, train_seconds double, "
    "started double, finished double, host string, model binary"
)


def features(df: pd.DataFrame, date_col: str, target_col: str) -> pd.DataFrame:
    """Calendar features plus lagged and rolling values of the target, for one series."""
    df = df.sort_values(date_col).reset_index(drop=True)
    when = pd.to_datetime(df[date_col])
    out = pd.DataFrame({
        "dow": when.dt.day_of_week,
        "dom": when.dt.day,
        "month": when.dt.month,
    })
    y = df[target_col].astype("float64")
    for lag in LAGS:
        out[f"lag_{lag}"] = y.shift(lag)
    out["mean_7"] = y.shift(1).rolling(7).mean()
    out["mean_28"] = y.shift(1).rolling(28).mean()
    out["y"] = y
    return out.dropna().reset_index(drop=True)


def train_one(pdf: pd.DataFrame, series_col: str, date_col: str, target_col: str, threads: int) -> dict:
    """Train and evaluate one series' model. Returns one result row."""
    started = time.time()
    series_id = str(pdf[series_col].iloc[0])
    data = features(pdf, date_col, target_col)
    train, test = data.iloc[:-TEST_DAYS], data.iloc[-TEST_DAYS:]
    x_cols = [c for c in data.columns if c != "y"]

    booster = xgb.train(
        {**PARAMS, "nthread": threads},
        xgb.DMatrix(train[x_cols], label=train["y"]),
        num_boost_round=ROUNDS,
    )
    pred = booster.predict(xgb.DMatrix(test[x_cols]))
    err = test["y"].to_numpy() - pred
    finished = time.time()
    return {
        "series_id": series_id,
        "rows": len(pdf),
        "rmse": float(np.sqrt(np.mean(err ** 2))),
        "mae": float(np.mean(np.abs(err))),
        "train_seconds": finished - started,
        "started": started,
        "finished": finished,
        "host": socket.gethostname(),
        "model": bytes(booster.save_raw("ubj")),
    }


def max_overlap(intervals) -> int:
    """Largest number of intervals running at the same moment."""
    intervals = list(intervals)
    events = sorted([(s, 1) for s, _ in intervals] + [(f, -1) for _, f in intervals], key=lambda e: (e[0], e[1]))
    running = peak = 0
    for _, delta in events:
        running += delta
        peak = max(peak, running)
    return peak


def summarize(results: pd.DataFrame, wall_seconds: float) -> None:
    print(f"\nTrained {len(results)} models in {wall_seconds / 60:.1f} min (wall clock)")
    print(f"Median time per model: {results['train_seconds'].median():.1f} s; "
          f"median RMSE: {results['rmse'].median():,.2f}")
    print("\nPer worker: models trained, most models training at the same moment")
    for host, group in results.groupby("host"):
        overlap = max_overlap(zip(group["started"], group["finished"]))
        print(f"  {host:<12} {len(group):>4} models   max concurrent: {overlap}")


def run_local(args) -> None:
    pdf = pd.read_parquet(args.input)
    series = sorted(pdf[args.series_col].unique())[: args.limit or None]
    threads = args.threads or os.cpu_count()
    start = time.time()
    rows = [
        train_one(pdf[pdf[args.series_col] == s], args.series_col, args.date_col, args.target_col, threads)
        for s in series
    ]
    results = pd.DataFrame(rows)
    summarize(results, time.time() - start)
    if args.output:
        results.drop(columns="model").to_csv(args.output, index=False)
        print(f"\nMetrics written to {args.output}")


def run_spark(args) -> None:
    from pyspark.sql import SparkSession
    from pyspark.sql import functions as F

    cores = args.threads or 4
    spark = (
        SparkSession.builder.appName("train-one-model-per-worker")
        # one task per executor at a time: a task takes all the executor's cores
        .config("spark.task.cpus", str(cores))
        # keep one series per task, so the work spreads evenly across workers
        .config("spark.sql.adaptive.coalescePartitions.enabled", "false")
        # XGBoost's threads sleep instead of spinning while they wait; without this,
        # training slows down many times over if anything else needs the CPU
        .config("spark.executorEnv.OMP_WAIT_POLICY", "PASSIVE")
        .getOrCreate()
    )
    data = spark.read.parquet(args.input)
    if args.limit:
        keep = data.select(args.series_col).distinct().orderBy(args.series_col).limit(args.limit)
        data = data.join(keep, args.series_col)
    n_series = data.select(args.series_col).distinct().count()
    spark.conf.set("spark.sql.shuffle.partitions", str(n_series))
    print(f"Training {n_series} models, {cores} cores per model")

    def train_group(pdf: pd.DataFrame) -> pd.DataFrame:
        return pd.DataFrame([train_one(pdf, args.series_col, args.date_col, args.target_col, cores)])

    start = time.time()
    (
        data.groupBy(args.series_col)
        .applyInPandas(train_group, schema=RESULT_SCHEMA)
        .write.mode("overwrite")
        .parquet(args.output)
    )
    wall = time.time() - start

    metrics = spark.read.parquet(args.output).drop("model").toPandas()
    summarize(metrics, wall)
    print(f"\nModels and metrics written to {args.output}")
    spark.stop()


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument("--input", required=True, help="Parquet file or folder (HDFS path on the cluster)")
    parser.add_argument("--output", help="where to write results (required on the cluster)")
    parser.add_argument("--series-col", default="series_id")
    parser.add_argument("--date-col", default="date")
    parser.add_argument("--target-col", default="y")
    parser.add_argument("--threads", type=int, help="cores per model (default: 4 on the cluster, all locally)")
    parser.add_argument("--limit", type=int, help="train only the first N series, for a quick test")
    parser.add_argument("--local", action="store_true", help="run without Spark, one model after another")
    args = parser.parse_args()

    if args.local:
        run_local(args)
    else:
        if not args.output:
            parser.error("--output is required on the cluster")
        run_spark(args)


if __name__ == "__main__":
    main()
