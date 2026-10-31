[Home](../README.md) · [Cluster Guide](Cluster_Guide.md) · [Troubleshooting](Troubleshooting.md)


<img src="img/icons/workload.svg" width="96" height="96" alt=""/>


# Workload

**Goal:** train one XGBoost model per series (300 of them) across the cluster, **one model at a time on each worker**, and measure whether the cluster beats training on one computer.

**Run on:** `master`.

**Before you start:** HDFS and Spark are running ([Spark](Spark.md)).

* [How the work is split](#how-the-work-is-split)
* [Python on every node](#python-on-every-node)
* [Put the data in HDFS](#put-the-data-in-hdfs)
* [Train the models](#train-the-models)
* [Use a trained model](#use-a-trained-model)
* [Benchmark](#benchmark)


# How the work is split

The 300 models don't depend on each other: each one learns from its own series only. So the job splits naturally by series, and Spark's job is just to hand series out to workers.

| Setting | Value | Effect |
| --- | --- | --- |
| `spark.executor.cores` | 4 ([Spark](Spark.md#configure-spark)) | One executor per worker, with all 4 cores |
| `spark.task.cpus` | 4 (set by the script) | Each task reserves all 4 cores, so an executor runs **one task at a time** |
| One series per task | set by the script | Each task trains exactly one model |
| XGBoost `nthread` | 4 (set by the script) | The model uses all 4 cores of its worker |

With four workers, four models train at once, and each worker picks up the next series as soon as it finishes one. The script reports the most models that ran at the same moment on each worker, so you can confirm it's 1.

The code is in [`workload/train_models.py`](../workload/train_models.py). It uses Spark's `groupBy(...).applyInPandas(...)`: Spark groups the rows by series, sends each group to a worker as a pandas DataFrame, and the function trains and returns that series' model.


# Python on every node

The workers run the training code in Python, so every node needs the same Python packages at the same path.

1. Create a virtual environment at `/opt/pyenv` on every node and install the pinned packages from [`workload/requirements.txt`](../workload/requirements.txt):

    ```bash
    cluster-cmd 'sudo apt install -y python3-venv'
    cluster-cmd 'sudo mkdir -p /opt/pyenv && sudo chown "$USER": /opt/pyenv && python3 -m venv /opt/pyenv'
    mkdir -p ~/pi-cluster && cd ~/pi-cluster
    for f in requirements.txt make_sample_data.py train_models.py; do
      wget -q -O $f https://raw.githubusercontent.com/gitluis/pi-cluster/master/workload/$f
    done
    cluster-scp ~/pi-cluster
    cluster-cmd '/opt/pyenv/bin/pip install -r ~/pi-cluster/requirements.txt'
    ```

    The install downloads ready-built ARM packages and takes a few minutes per node.

2. Tell Spark to use that Python, then restart Spark:

    ```bash
    echo 'export PYSPARK_PYTHON=/opt/pyenv/bin/python' >> $SPARK_HOME/conf/spark-env.sh
    cluster-scp /opt/spark/conf
    $SPARK_HOME/sbin/stop-all.sh && $SPARK_HOME/sbin/start-all.sh
    ```

**Check:** every node prints the same XGBoost version:

```bash
cluster-cmd '/opt/pyenv/bin/python -c "import xgboost; print(xgboost.__version__)"'
```


# Put the data in HDFS

The script expects Parquet with one row per series per day: a series ID, a date and the value to predict.

**To try the cluster first**, make a sample data set with the same shape: 300 series of three years of daily values.

```bash
cd ~/pi-cluster
/opt/pyenv/bin/python make_sample_data.py --series 300 --days 1095 --out sample.parquet
hdfs dfs -put -f sample.parquet /user/$USER/sample.parquet
```

**To use your own data**, export it to Parquet with those three columns and copy it the same way. If your columns have other names, pass them to the script with `--series-col`, `--date-col` and `--target-col`.

If the data comes from work, check your employer's data-handling rules before copying it to a home cluster.


# Train the models

1. **Quick test** with 8 series, to catch problems in a minute or two:

    ```bash
    cd ~/pi-cluster
    spark-submit train_models.py --input /user/$USER/sample.parquet --output /user/$USER/models_test --limit 8
    ```

2. **The full run:**

    ```bash
    spark-submit train_models.py --input /user/$USER/sample.parquet --output /user/$USER/models 2> train.log
    ```

    Spark's progress messages go to `train.log`; the summary prints on screen at the end. Follow the job on the Spark master's web page, `http://master.local:8080`.

**Check** the summary. It should look like this, with your own times and roughly 75 models per worker:

```
Trained 300 models in ... min (wall clock)
Median time per model: ... s; median RMSE: ...

Per worker: models trained, most models training at the same moment
  worker1        75 models   max concurrent: 1
  worker2        76 models   max concurrent: 1
  worker3        74 models   max concurrent: 1
  worker4        75 models   max concurrent: 1
```

`max concurrent: 1` on every worker confirms one model at a time per worker. A worker with fewer models than the others is usually slower: check its temperature and power with `vcgencmd` ([Power](Hardware_List.md#power)).

The results are in HDFS at `/user/$USER/models`: one row per series with its error on the last 56 days (`rmse`, `mae`), how long it took, which worker trained it, and the model itself.

To change the model, edit `PARAMS`, `ROUNDS`, `LAGS` or `TEST_DAYS` at the top of `train_models.py`, copy it to the workers with `cluster-scp ~/pi-cluster`, and run again.


# Use a trained model

The models are stored in XGBoost's own format. To load one, for example in `pyspark` on `master`:

```python
import xgboost as xgb

row = (spark.read.parquet(f"/user/{spark.sparkContext.sparkUser()}/models")
       .where("series_id = 'S0042'").first())
model = xgb.Booster()
model.load_model(bytearray(row["model"]))
```

`model.predict(...)` then takes the same features the script builds in its `features()` function.


# Benchmark

The [goal](Purpose.md) is to beat about 7 hours for 300 models on one computer. Measure both sides with the same script, the same data and the same settings.

1. **One computer, no Spark.** On your computer, with the same `requirements.txt` installed:

    ```bash
    python3 train_models.py --local --input sample.parquet --output laptop_metrics.csv
    ```

    `--local` trains the models one after another using all of the computer's cores. Add `--limit 20` for a quicker estimate and multiply by 15.

2. **One Pi**, to know what a single worker can do:

    ```bash
    ssh worker1 'cd ~/pi-cluster && hdfs dfs -get -f /user/$USER/sample.parquet . && /opt/pyenv/bin/python train_models.py --local --input sample.parquet --limit 8 --threads 4'
    ```

3. **The cluster:** the full run above.

| Run | Time for 300 models | Median per model |
| --- | --- | --- |
| Your computer (`--local`) | | |
| One Pi worker (`--limit 8`, ×37.5) | | |
| Cluster, 4 workers | | |

Fill in your own numbers. The cluster's time is about 75 rounds of "one model per worker", so expect roughly 75 × the median per model on one Pi. To beat 7 hours, a single model must train on one Pi in under about 5½ minutes (7 h ÷ 75).

A Raspberry Pi 4 core is several times slower than a current laptop core, so the cluster won't always win against a fast computer. Its advantage is that it runs on its own while your computer stays free, and it scales: each extra worker adds another model in parallel.

If your computer's run uses all its cores, you can also compare **per model**: the cluster wins when one Pi's time per model is less than 4 times your computer's time per model, since four Pis train at once.

---

**Step 9 of 9** · ← Step 8: [Spark](Spark.md) · Done! Back to the [Cluster Guide](Cluster_Guide.md)
