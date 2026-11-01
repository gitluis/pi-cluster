[Home](../README.md) · [About](About.md) · [Getting Started](Getting_Started.md) · [Cluster Guide](Cluster_Guide.md) · [Troubleshooting](Troubleshooting.md)


<img src="img/icons/cluster-setup.svg" width="96" height="96" alt=""/>


# Cluster Setup

**Goal:** HDFS spread across the cluster: `master` runs the NameNode, and the four workers store the data.

**Run on:** `master`.

**Before you start:** [Single Node Setup](Single_Node_Setup.md) works and HDFS is stopped (`stop-dfs.sh`).

* [Clear the test data](#clear-the-test-data)
* [Point HDFS at the workers](#point-hdfs-at-the-workers)
* [Copy Hadoop to the workers](#copy-hadoop-to-the-workers)
* [Format and start HDFS](#format-and-start-hdfs)
* [Start and stop the cluster](#start-and-stop-the-cluster)
* [Optional: YARN and MapReduce](#optional-yarn-and-mapreduce)


# Clear the test data

The single-node test stored blocks on `master`, which won't be a DataNode anymore. Start from an empty file system:

```bash
rm -rf /opt/hadoop_data/*
```


# Point HDFS at the workers

1. List the workers as DataNodes:

    ```bash
    workers > $HADOOP_CONF_DIR/workers
    cat $HADOOP_CONF_DIR/workers
    ```

    It should list `worker1` to `worker4`.

2. Keep **2 copies** of every block, so losing one worker or one card loses no data. In `$HADOOP_CONF_DIR/hdfs-site.xml`, change the `dfs.replication` value from `1` to `2`:

    ```bash
    sed -i 's|<value>1</value>|<value>2</value>|' $HADOOP_CONF_DIR/hdfs-site.xml
    grep -A1 dfs.replication $HADOOP_CONF_DIR/hdfs-site.xml
    ```

    Three copies is Hadoop's usual default, but on four small cards two is a better balance between safety and space.


# Copy Hadoop to the workers

Copying the archive and unpacking it on each worker is much faster than copying thousands of small files.

```bash
master-cmd 'sudo mkdir -p /opt/hadoop /opt/hadoop_data && sudo chown "$USER": /opt/hadoop /opt/hadoop_data'
cluster-scp /tmp/hadoop-3.5.0-aarch64.tar.gz
master-cmd 'tar -xzf /tmp/hadoop-3.5.0-aarch64.tar.gz -C /opt/hadoop --strip-components=1 && rm /tmp/hadoop-3.5.0-aarch64.tar.gz'
```

Then copy the configuration and environment from `master`, so every node uses identical settings:

```bash
cluster-scp /opt/hadoop/etc/hadoop
cluster-scp ~/.cluster_env
cluster-scp ~/.bashrc
```

**Check:** every worker has the same Hadoop version and sees the same workers file:

```bash
master-cmd 'hadoop version | head -1; cat $HADOOP_CONF_DIR/workers | tr "\n" " "; echo'
```

Whenever you change a file in `/opt/hadoop/etc/hadoop` on `master`, copy it again with `cluster-scp /opt/hadoop/etc/hadoop`.


# Format and start HDFS

```bash
hdfs namenode -format
start-dfs.sh
```

`start-dfs.sh` starts the NameNode and SecondaryNameNode on `master`, then logs in to each worker over SSH to start its DataNode.

**Check:**

```bash
hdfs dfsadmin -report | grep "Live datanodes"
cluster-cmd jps
```

The report must say `Live datanodes (4)`. `jps` should show `DataNode` on each worker, and `NameNode` and `SecondaryNameNode` on `master`.

Store a file and confirm HDFS kept two copies of it on different workers:

```bash
hdfs dfs -mkdir -p /user/$USER
echo "hello from the pi cluster" | hdfs dfs -put - /user/$USER/hello.txt
hdfs fsck /user/$USER/hello.txt -files -blocks -locations | grep -o "DatanodeInfoWithStorage\[[^,]*"
```

The last command prints two different worker addresses.

The NameNode web page, `http://master.local:9870`, shows the same under *Datanodes*.


# Start and stop the cluster

After every power-on, start the services in this order; stop them in the reverse order before shutting down.

| Step | Start | Stop |
| --- | --- | --- |
| 1. HDFS | `start-dfs.sh` | `stop-dfs.sh` |
| 2. Spark ([Spark](Spark.md)) | `$SPARK_HOME/sbin/start-all.sh` | `$SPARK_HOME/sbin/stop-all.sh` |

To shut everything down safely:

```bash
$SPARK_HOME/sbin/stop-all.sh
stop-dfs.sh
cluster-shutdown
```

Stopping HDFS first lets the NameNode save its state. Pulling the power on a running NameNode can leave HDFS needing repair on the next start.

Use Spark's scripts by their full path. Hadoop also has a `start-all.sh`, and the one on your `PATH` is Hadoop's.


# Optional: YARN and MapReduce

YARN is Hadoop's own scheduler; MapReduce is Hadoop's original way of processing data. **This guide doesn't use either.** Spark runs its own lightweight scheduler instead ([Spark](Spark.md)), which leaves more memory for training models on 2 to 4 GB boards.

Set up YARN only if you want to try MapReduce, and **stop it before running Spark jobs** so the two don't compete for memory.

1. Replace `yarn-site.xml`. Each worker offers YARN 1.5 GB of memory and its 4 cores:

    ```bash
    cat > $HADOOP_CONF_DIR/yarn-site.xml <<'EOF'
    <?xml version="1.0" encoding="UTF-8"?>
    <configuration>
      <property><name>yarn.resourcemanager.hostname</name><value>master</value></property>
      <property><name>yarn.nodemanager.aux-services</name><value>mapreduce_shuffle</value></property>
      <property><name>yarn.nodemanager.resource.memory-mb</name><value>1536</value></property>
      <property><name>yarn.nodemanager.resource.cpu-vcores</name><value>4</value></property>
      <property><name>yarn.scheduler.minimum-allocation-mb</name><value>256</value></property>
      <property><name>yarn.scheduler.maximum-allocation-mb</name><value>1536</value></property>
      <property><name>yarn.nodemanager.vmem-check-enabled</name><value>false</value></property>
      <property>
        <name>yarn.nodemanager.env-whitelist</name>
        <value>JAVA_HOME,HADOOP_COMMON_HOME,HADOOP_HDFS_HOME,HADOOP_CONF_DIR,CLASSPATH_PREPEND_DISTCACHE,HADOOP_YARN_HOME,HADOOP_HOME,PATH,LANG,TZ,HADOOP_MAPRED_HOME</value>
      </property>
    </configuration>
    EOF
    ```

2. Replace `mapred-site.xml`, giving each MapReduce task 512 MB:

    ```bash
    cat > $HADOOP_CONF_DIR/mapred-site.xml <<'EOF'
    <?xml version="1.0" encoding="UTF-8"?>
    <configuration>
      <property><name>mapreduce.framework.name</name><value>yarn</value></property>
      <property><name>yarn.app.mapreduce.am.resource.memory-mb</name><value>512</value></property>
      <property><name>mapreduce.map.memory.mb</name><value>512</value></property>
      <property><name>mapreduce.reduce.memory.mb</name><value>512</value></property>
      <property><name>yarn.app.mapreduce.am.env</name><value>HADOOP_MAPRED_HOME=/opt/hadoop</value></property>
      <property><name>mapreduce.map.env</name><value>HADOOP_MAPRED_HOME=/opt/hadoop</value></property>
      <property><name>mapreduce.reduce.env</name><value>HADOOP_MAPRED_HOME=/opt/hadoop</value></property>
    </configuration>
    EOF
    ```

3. Limit the YARN services' own memory, copy the configuration to the workers and start YARN:

    ```bash
    printf 'export YARN_RESOURCEMANAGER_OPTS="-Xmx256m"\nexport YARN_NODEMANAGER_OPTS="-Xmx256m"\n' >> $HADOOP_CONF_DIR/yarn-env.sh
    cluster-scp /opt/hadoop/etc/hadoop
    start-yarn.sh
    ```

4. **Check** with the example job that estimates pi, then stop YARN:

    ```bash
    yarn node -list
    hadoop jar $HADOOP_HOME/share/hadoop/mapreduce/hadoop-mapreduce-examples-3.5.0.jar pi 4 1000
    stop-yarn.sh
    ```

    `yarn node -list` shows 4 nodes, and the job ends with `Estimated value of Pi is 3.14...`. The ResourceManager's web page is `http://master.local:8088` while YARN runs.

---

**Step 7 of 9** · ← Step 6: [Single Node Setup](Single_Node_Setup.md) · Step 8: [Spark](Spark.md) →
