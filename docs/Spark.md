[Home](../README.md) · [Cluster Guide](Cluster_Guide.md) · [Troubleshooting](Troubleshooting.md)


<img src="img/icons/spark.svg" width="96" height="96" alt=""/>


# Spark

**Goal:** a Spark cluster with `master` as the Spark master and one Spark *executor* on each worker, reading data from HDFS.

**Run on:** `master`.

**Before you start:** [Cluster Setup](Cluster_Setup.md) is done and HDFS is running (`start-dfs.sh`).

* [How Spark uses the cluster](#how-spark-uses-the-cluster)
* [Install Spark on every node](#install-spark-on-every-node)
* [Configure Spark](#configure-spark)
* [Start Spark and test it](#start-spark-and-test-it)


# How Spark uses the cluster

Spark runs in **standalone mode**: it brings its own small scheduler, so it doesn't need Hadoop's YARN.

| Spark piece | Runs on | Job |
| --- | --- | --- |
| Master | `master` | Keeps track of the workers and hands out their cores and memory |
| Driver | `master` | Your program. Splits a job into *tasks* and collects the results |
| Worker | each worker | Starts an executor when a job needs it |
| Executor | each worker | A Java process that runs tasks, plus Python processes for PySpark code |

The settings below give each worker **exactly one executor with all 4 cores**. For ordinary jobs, that executor runs 4 tasks at a time. For training, the [workload](Workload.md) asks for all 4 cores per task, so each worker trains **one model at a time** using all its cores.


# Install Spark on every node

1. Download Spark and its checksum on `master`:

    ```bash
    cd /tmp
    wget https://dlcdn.apache.org/spark/spark-4.2.1/spark-4.2.1-bin-hadoop3.tgz
    wget https://downloads.apache.org/spark/spark-4.2.1/spark-4.2.1-bin-hadoop3.tgz.sha512
    sha512sum spark-4.2.1-bin-hadoop3.tgz
    cat spark-4.2.1-bin-hadoop3.tgz.sha512
    ```

    The two long hexadecimal strings must match.

2. Unpack it on `master`, then copy and unpack it on the workers:

    ```bash
    cluster-cmd 'sudo mkdir -p /opt/spark && sudo chown "$USER": /opt/spark'
    tar -xzf spark-4.2.1-bin-hadoop3.tgz -C /opt/spark --strip-components=1
    cluster-scp /tmp/spark-4.2.1-bin-hadoop3.tgz
    master-cmd 'tar -xzf /tmp/spark-4.2.1-bin-hadoop3.tgz -C /opt/spark --strip-components=1 && rm /tmp/spark-4.2.1-bin-hadoop3.tgz'
    ```

**Check:** `cluster-cmd 'spark-submit --version 2>&1 | grep -m1 version'` shows `version 4.2.1` on every node. `SPARK_HOME` and the `PATH` entry come from `~/.cluster_env`, set in [Single Node Setup](Single_Node_Setup.md#set-environment-variables).


# Configure Spark

Spark's settings live in `/opt/spark/conf`.

1. **Workers.** Spark uses the same list as HDFS:

    ```bash
    workers > $SPARK_HOME/conf/workers
    ```

2. **Memory and cores.** Pick the row for the RAM of your **workers**:

    | Worker RAM | `SPARK_WORKER_MEMORY` | `spark.executor.memory` |
    | --- | --- | --- |
    | 4 GB | `2g` | `1536m` |
    | 8 GB | `5g` | `4g` |
    | 16 GB | `12g` | `8g` |
    | 2 GB (Pi 4, as in the original build) | `640m` | `512m` |

    The rest of each worker's memory goes to the OS, the HDFS DataNode, the Spark worker itself, and the Python processes that train the models. Python memory isn't part of `spark.executor.memory`, which is why the executor gets well under half of a 4 GB board.

    Create `spark-env.sh`, using your row's `SPARK_WORKER_MEMORY`:

    ```bash
    cat > $SPARK_HOME/conf/spark-env.sh <<'EOF'
    export JAVA_HOME=/usr/lib/jvm/temurin-17-jdk-arm64
    export HADOOP_CONF_DIR=/opt/hadoop/etc/hadoop
    export SPARK_MASTER_HOST=master
    export SPARK_WORKER_CORES=4
    export SPARK_WORKER_MEMORY=2g
    export SPARK_DAEMON_MEMORY=256m
    EOF
    ```

    `HADOOP_CONF_DIR` tells Spark where HDFS is, so a path such as `/user/alice/data` means `hdfs://master:9000/user/alice/data`.

3. **Defaults for every job.** Create `spark-defaults.conf`, using your row's `spark.executor.memory`:

    ```bash
    cat > $SPARK_HOME/conf/spark-defaults.conf <<'EOF'
    spark.master             spark://master:7077
    spark.executor.cores     4
    spark.executor.memory    1536m
    spark.driver.memory      512m
    EOF
    ```

    `spark.executor.cores 4` equals `SPARK_WORKER_CORES`, so each worker fits exactly one executor.

4. **Copy the configuration** to the workers:

    ```bash
    cluster-scp /opt/spark/conf
    ```

`master` is the tightest node, especially with 2 or 4 GB of RAM: it runs the NameNode, the Spark master and your driver program at once. Keep `spark.driver.memory` at `512m`, and don't collect large results back to the driver.


# Start Spark and test it

```bash
$SPARK_HOME/sbin/start-all.sh
```

Use the full path: Hadoop also has a `start-all.sh`, and it's the one on your `PATH`.

**Check** that all four workers joined:

```bash
curl -s http://master:8080/json/ | grep -oE '"(aliveworkers|cores)" ?: ?[0-9]+'
```

It should print `"aliveworkers" : 4` and `"cores" : 16`. The same is on the Spark master's web page at `http://master.local:8080`.

Run Spark's example that estimates pi on the cluster:

```bash
spark-submit $SPARK_HOME/examples/src/main/python/pi.py 100 2>/dev/null
```

It prints `Pi is roughly 3.14...`. While it runs, `http://master.local:8080` shows the application with one executor on each worker.

Finally, read the HDFS test file from [Cluster Setup](Cluster_Setup.md#format-and-start-hdfs) through Spark:

```bash
pyspark <<'EOF' 2>/dev/null | grep hello
print(spark.read.text(f"/user/{spark.sparkContext.sparkUser()}/hello.txt").first()[0])
EOF
```

It prints `hello from the pi cluster`.

To stop Spark: `$SPARK_HOME/sbin/stop-all.sh`. See [Start and stop the cluster](Cluster_Setup.md#start-and-stop-the-cluster) for the full order.

---

**Step 8 of 9** · ← Step 7: [Cluster Setup](Cluster_Setup.md) · Step 9: [Workload](Workload.md) →
