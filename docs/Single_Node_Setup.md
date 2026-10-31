[Background](Background.md) / [Purpose](Purpose.md) / [Getting Started](Getting_Started.md) / [Cluster Guide](Cluster_Guide.md)


<img src="img/icons/single-node.svg" width="96" height="96" alt=""/>


# Single Node Setup

**Goal:** Java on every node, and Hadoop's file system (HDFS) running on `master` alone, so you can confirm Hadoop works before adding the workers.

**Run on:** `master`. Java goes to every node with `cluster-cmd`.

**Before you start:** [The Pi Network](The_Pi_Network.md), [Cluster Commands](Cluster_Commands.md) and [Cluster Security](Cluster_Security.md) are done, and `nodes-up` shows every node `up`. Versions are listed in [Versions](Versions.md).

* [Install Java 17 on every node](#install-java-17-on-every-node)
* [Download Hadoop](#download-hadoop)
* [Set environment variables](#set-environment-variables)
* [Configure HDFS](#configure-hdfs)
* [Start HDFS and test it](#start-hdfs-and-test-it)


# Install Java 17 on every node

Hadoop 3.5 needs Java 17 exactly. Raspberry Pi OS offers Java 21 and 25 but not 17, so install Eclipse Temurin 17 from the Adoptium repository.

```bash
cluster-cmd 'sudo apt install -y wget gpg'
cluster-cmd 'wget -qO- https://packages.adoptium.net/artifactory/api/gpg/key/public | sudo gpg --dearmor --yes -o /usr/share/keyrings/adoptium.gpg'
cluster-cmd 'echo "deb [signed-by=/usr/share/keyrings/adoptium.gpg] https://packages.adoptium.net/artifactory/deb $(. /etc/os-release && echo $VERSION_CODENAME) main" | sudo tee /etc/apt/sources.list.d/adoptium.list'
cluster-cmd 'sudo apt update && sudo apt install -y temurin-17-jdk'
```

**Check:**

```bash
cluster-cmd 'ls -d /usr/lib/jvm/temurin-17-jdk-*'
```

Every node should print `/usr/lib/jvm/temurin-17-jdk-arm64`. That folder is `JAVA_HOME` below.

If `apt update` says the repository has no `Release` file for your OS codename, Adoptium hasn't published that codename yet: replace it with the previous Debian codename (`bookworm`) in `/etc/apt/sources.list.d/adoptium.list` and run the last command again.


# Download Hadoop

Download the ARM 64-bit build and its checksum, then check that the download is complete and unmodified:

```bash
cd /tmp
wget https://dlcdn.apache.org/hadoop/common/hadoop-3.5.0/hadoop-3.5.0-aarch64.tar.gz
wget https://downloads.apache.org/hadoop/common/hadoop-3.5.0/hadoop-3.5.0-aarch64.tar.gz.sha512
sha512sum -c hadoop-3.5.0-aarch64.tar.gz.sha512
```

The last command must print `hadoop-3.5.0-aarch64.tar.gz: OK`.

Unpack it into `/opt/hadoop`, owned by your user so Hadoop can write its logs there:

```bash
sudo mkdir -p /opt/hadoop /opt/hadoop_data
sudo chown "$USER": /opt/hadoop /opt/hadoop_data
tar -xzf hadoop-3.5.0-aarch64.tar.gz -C /opt/hadoop --strip-components=1
```

Keep the `.tar.gz` in `/tmp` for now: [Cluster Setup](Cluster_Setup.md) copies it to the workers.


# Set environment variables

Put the cluster's settings in their own file, `~/.cluster_env`:

```bash
cat > ~/.cluster_env <<'EOF'
# pi-cluster environment
export JAVA_HOME=/usr/lib/jvm/temurin-17-jdk-arm64
export HADOOP_HOME=/opt/hadoop
export HADOOP_CONF_DIR=$HADOOP_HOME/etc/hadoop
export SPARK_HOME=/opt/spark
export PATH=$PATH:$JAVA_HOME/bin:$HADOOP_HOME/bin:$HADOOP_HOME/sbin:$SPARK_HOME/bin
EOF
```

Load it from the **first** line of `~/.bashrc`:

```bash
sed -i '1i [ -f ~/.cluster_env ] && . ~/.cluster_env' ~/.bashrc
source ~/.bashrc
```

It must go at the top, not the bottom. `~/.bashrc` on Raspberry Pi OS stops early for commands sent over SSH (like `cluster-cmd hdfs ...`), so anything below that point wouldn't apply to them.

**Check:** `hadoop version` prints `Hadoop 3.5.0`.


# Configure HDFS

HDFS keeps two kinds of data:

- The **NameNode**, on `master`, records which file is made of which blocks and where each block is stored.
- The **DataNodes** store the blocks themselves. For this test, `master` is its own DataNode; in [Cluster Setup](Cluster_Setup.md) the workers take over.

All Hadoop settings live in `$HADOOP_CONF_DIR` (`/opt/hadoop/etc/hadoop`).

1. **Java and memory.** Append to `hadoop-env.sh`:

    ```bash
    cat >> $HADOOP_CONF_DIR/hadoop-env.sh <<'EOF'

    # pi-cluster
    export JAVA_HOME=/usr/lib/jvm/temurin-17-jdk-arm64
    export HDFS_NAMENODE_OPTS="-Xmx512m"
    export HDFS_SECONDARYNAMENODE_OPTS="-Xmx256m"
    export HDFS_DATANODE_OPTS="-Xmx256m"
    EOF
    ```

    Hadoop gives each service up to a quarter of the machine's memory by default. These limits keep the services small so Spark and your models get the rest.

2. **Where HDFS lives.** Replace `core-site.xml`:

    ```bash
    cat > $HADOOP_CONF_DIR/core-site.xml <<'EOF'
    <?xml version="1.0" encoding="UTF-8"?>
    <configuration>
      <property>
        <name>fs.defaultFS</name>
        <value>hdfs://master:9000</value>
      </property>
      <property>
        <name>hadoop.tmp.dir</name>
        <value>/opt/hadoop_data/tmp</value>
      </property>
    </configuration>
    EOF
    ```

3. **Where data is stored, and how many copies.** Replace `hdfs-site.xml`:

    ```bash
    cat > $HADOOP_CONF_DIR/hdfs-site.xml <<'EOF'
    <?xml version="1.0" encoding="UTF-8"?>
    <configuration>
      <property>
        <name>dfs.namenode.name.dir</name>
        <value>file:///opt/hadoop_data/namenode</value>
      </property>
      <property>
        <name>dfs.datanode.data.dir</name>
        <value>file:///opt/hadoop_data/datanode</value>
      </property>
      <property>
        <name>dfs.replication</name>
        <value>1</value>
      </property>
    </configuration>
    EOF
    ```

    `dfs.replication` is how many copies of each block HDFS keeps. With a single DataNode, only 1 is possible.

4. **Which nodes are DataNodes.** For now, only `master`:

    ```bash
    echo master > $HADOOP_CONF_DIR/workers
    ```


# Start HDFS and test it

1. Format the NameNode. This creates an empty file system; do it **once**, since formatting again erases everything HDFS stores:

    ```bash
    hdfs namenode -format
    ```

    Look for `has been successfully formatted` near the end.

2. Start HDFS:

    ```bash
    start-dfs.sh
    ```

3. **Check** the running services with `jps`. It should list `NameNode`, `DataNode` and `SecondaryNameNode`. If one is missing, its log in `/opt/hadoop/logs/` says why.

4. Store a file and read it back:

    ```bash
    hdfs dfs -mkdir -p /user/$USER
    echo "hello from the pi cluster" | hdfs dfs -put - /user/$USER/hello.txt
    hdfs dfs -cat /user/$USER/hello.txt
    ```

5. **Check** the report shows one live DataNode:

    ```bash
    hdfs dfsadmin -report | grep "Live datanodes"
    ```

You can also open the NameNode's web page from your computer at `http://master.local:9870`.

A warning such as `Unable to load native-hadoop library` is harmless: Hadoop falls back to Java code.

Stop HDFS before moving on:

```bash
stop-dfs.sh
```

Next: [Cluster Setup](Cluster_Setup.md).
