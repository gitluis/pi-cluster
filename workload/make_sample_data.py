#!/usr/bin/env python3
"""Make a sample data set shaped like the guide's workload.

One row per series per day: series_id, date, y. The values mimic daily
transaction amounts per location: a base level, a weekly cycle, spikes
around the 1st and 15th of the month, a slow trend, and noise.

    python3 make_sample_data.py --series 300 --days 1095 --out sample.parquet

Then copy it to HDFS:

    hdfs dfs -put sample.parquet /user/$USER/sample.parquet
"""
import argparse

import numpy as np
import pandas as pd


def make(series: int, days: int, seed: int) -> pd.DataFrame:
    rng = np.random.default_rng(seed)
    dates = pd.date_range("2023-01-01", periods=days, freq="D")
    dow = dates.day_of_week.to_numpy()
    dom = dates.day.to_numpy()
    t = np.arange(days)

    frames = []
    for i in range(series):
        base = rng.uniform(2_000, 20_000)
        weekly = rng.uniform(0.05, 0.25) * np.sin(2 * np.pi * (dow + rng.integers(7)) / 7)
        payday = rng.uniform(0.2, 0.6) * (np.isin(dom, [1, 2, 15, 16]))
        trend = rng.uniform(-0.15, 0.25) * t / days
        noise = rng.normal(0, rng.uniform(0.03, 0.10), days)
        y = base * (1 + weekly + payday + trend + noise)
        # plain dates (not nanosecond timestamps), which Spark reads from Parquet without extra settings
        frames.append(pd.DataFrame({"series_id": f"S{i:04d}", "date": dates.date, "y": y.round(2)}))
    return pd.concat(frames, ignore_index=True)


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument("--series", type=int, default=300, help="number of series (models) to generate")
    parser.add_argument("--days", type=int, default=1095, help="days of history per series")
    parser.add_argument("--seed", type=int, default=42)
    parser.add_argument("--out", default="sample.parquet")
    args = parser.parse_args()

    df = make(args.series, args.days, args.seed)
    df.to_parquet(args.out, index=False)
    print(f"wrote {len(df):,} rows for {args.series} series to {args.out}")


if __name__ == "__main__":
    main()
