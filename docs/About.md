[Home](../README.md) · [Cluster Guide](Cluster_Guide.md) · [Troubleshooting](Troubleshooting.md)


<img src="img/icons/about.svg" width="96" height="96" alt=""/>


# About

Why this cluster exists, what Hadoop and Spark are, and the history of the build.

* [Purpose](#purpose)
* [Background: Hadoop and Spark](#background-hadoop-and-spark)
* [Builds](#builds)


# Purpose

The main reason for building and configuring this cluster is to leverage Hadoop and Spark's distributed storage and processing capabilities to build, train, test and assess Machine Learning models in parallel for projects at work and also to demonstrate you may not need to invest in full-powered computers or servers to build a cluster.

I found myself training about 300 XGBoost models on time-series financial data that would take about 7 hours to train total. As a result, the **goal** here is to at least reduce the amount of time it takes to train all models. By having a separate cluster, I allow myself to continue working on other tasks while the cluster takes the load. That is when the idea of a Raspberry Pi cluster kicked in.


## Design

The 300 models are independent: each learns from its own series. The cluster therefore splits the work by series and trains **one model at a time on each worker**, with all four of the worker's cores working on that one model. Four workers train four models at once.

Hadoop's file system (HDFS) stores the data and the trained models, and Spark hands out the series to the workers. Learning Hadoop and Spark on real hardware is part of the point of this project, alongside the speed-up.


## Measuring success

Success means training all 300 models in less than the 7-hour baseline, measured with the same script and data on both sides. A Raspberry Pi core is slower than a laptop core, especially on a Pi 4, so this isn't guaranteed: the cluster wins when a single Pi trains one model in under about 5½ minutes. [Workload](Workload.md#benchmark) shows how to measure it.

Even when a fast computer is quicker, the cluster still frees that computer for other work while the models train.


# Background: Hadoop and Spark

We live in a digital world full of data. Whether that is un-, semi- or structured data, there are many things we can do with it if we make use of Machine Learning (ML). More specifically, supervised, unsupervised or reinforcement learning algorithms are used to build models that learn (train) and discover patterns from historical data to predict an outcome. There are numerous applications of ML such as weather forecast (prediction), storm tracking models, among others.

- [**Hadoop**](https://hadoop.apache.org) is a software framework for storing and processing large data sets across a cluster of computers. This guide uses its file system, **HDFS**, which splits files into blocks and keeps copies of each block on several machines.
- [**MapReduce**](https://www.tutorialspoint.com/hadoop/hadoop_mapreduce.htm) is Hadoop's original way of processing data in parallel: a *map* step works on each block where it's stored, and a *reduce* step combines the results. Here it is counting the words in a file:

  <img src="img/diagrams/mapreduce-word-count.svg" width="100%" alt="MapReduce counting words in a file. Split: HDFS stores the file as three blocks on worker1 to worker3. Map: each worker turns every word in its own block into a word-and-1 pair. Shuffle: the pairs are grouped by word. Reduce: each group adds up its 1s, giving pi 4, spark 2, data 1. Output: the counts are written back to HDFS as a new file."/>

- [**Spark**](https://spark.apache.org/) is a newer engine for large-scale data processing. It keeps data in memory between steps, which makes it much faster than MapReduce, and you can drive it from Python.

It all sounds similar, so here is how the pieces fit together on this cluster:

<img src="img/diagrams/hadoop-spark-stack.svg" width="100%" alt="How Hadoop and Spark fit together: your work runs on Spark, which gets CPU and memory from its own standalone scheduler and reads data from HDFS. MapReduce with YARN is optional. The master runs the HDFS NameNode and the Spark master; each worker runs a DataNode and a Spark worker."/>

The cluster lets you extract, transform and load (ETL) data and train models with Spark, while HDFS stores the data. Analysis and visualization of the results are up to you.


# Builds

The cluster was first built in 2020 on Raspberry Pi 4 boards and ran Hadoop and Spark successfully. The guide has since been updated for current software and for the **Raspberry Pi 5**, the newest model, while keeping full support for the **Raspberry Pi 4**. Where the two boards need different parts or settings, the guide shows both.

| Build | When | Boards | Operating system | Result |
| --- | --- | --- | --- | --- |
| Original build | 2020 | 5 × Raspberry Pi 4 Model B, 2 GB | Raspbian (2020 release) | **Worked**, including HDFS and Spark. The Hadoop and Spark pages were written later, in the 2026 update |
| 2026 update | October 2026 | Written for 5 × Raspberry Pi 5 or 5 × Raspberry Pi 4 | Raspberry Pi OS Lite 64-bit (Debian 13) | Not built on hardware. Steps updated from the original build; the training job was tested on a Spark 4.2 cluster on a regular computer |

Built it with these steps? Please [open an issue](https://github.com/gitluis/pi-cluster/issues) with your boards, RAM, OS image date and [benchmark](Workload.md#benchmark) time, or if a step didn't work for you.

---

Back to the [Cluster Guide](Cluster_Guide.md)
