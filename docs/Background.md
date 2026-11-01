[Home](../README.md) · [Cluster Guide](Cluster_Guide.md) · [Troubleshooting](Troubleshooting.md)


<img src="img/icons/background.svg" width="96" height="96" alt=""/>


# Background

We live in a digital world full of data. Whether that is un-, semi- or structured data, there are many things we can do with it if we make use of Machine Learning (ML). More specifically, supervised, unsupervised or reinforcement learning algorithms are used to build models that learn (train) and discover patterns from historical data to predict an outcome. There are numerous applications of ML such as weather forecast (prediction), storm tracking models, among others.

- [**Hadoop**](https://hadoop.apache.org) is a software framework for storing and processing large data sets across a cluster of computers. This guide uses its file system, **HDFS**, which splits files into blocks and keeps copies of each block on several machines.
- [**MapReduce**](https://www.tutorialspoint.com/hadoop/hadoop_mapreduce.htm) is Hadoop's original way of processing data in parallel: a *map* step works on each block where it's stored, and a *reduce* step combines the results. Here it is counting the words in a file:

  <img src="img/diagrams/mapreduce-word-count.svg" width="100%" alt="MapReduce counting words in a file. Split: HDFS stores the file as three blocks on worker1 to worker3. Map: each worker turns every word in its own block into a word-and-1 pair. Shuffle: the pairs are grouped by word. Reduce: each group adds up its 1s, giving pi 4, spark 2, data 1. Output: the counts are written back to HDFS as a new file."/>

- [**Spark**](https://spark.apache.org/) is a newer engine for large-scale data processing. It keeps data in memory between steps, which makes it much faster than MapReduce, and you can drive it from Python.

It all sounds similar, so here is how the pieces fit together on this cluster:

<img src="img/diagrams/hadoop-spark-stack.svg" width="100%" alt="How Hadoop and Spark fit together: your work runs on Spark, which gets CPU and memory from its own standalone scheduler and reads data from HDFS. MapReduce with YARN is optional. The master runs the HDFS NameNode and the Spark master; each worker runs a DataNode and a Spark worker."/>

The cluster lets you extract, transform and load (ETL) data and train models with Spark, while HDFS stores the data. Analysis and visualization of the results are up to you.

---

Back to the [Cluster Guide](Cluster_Guide.md)
