[Home](../README.md) · [Cluster Guide](Cluster_Guide.md) · [Troubleshooting](Troubleshooting.md)


<img src="img/icons/purpose.svg" width="96" height="96" alt=""/>


# Purpose

The main reason for building and configuring this cluster is to leverage Hadoop and Spark's distributed storage and processing capabilities to build, train, test and assess Machine Learning models in parallel for projects at work and also to demonstrate you may not need to invest in full-powered computers or servers to build a cluster.

I found myself training about 300 XGBoost models on time-series financial data that would take about 7 hours to train total. As a result, the **goal** here is to at least reduce the amount of time it takes to train all models. By having a separate cluster, I allow myself to continue working on other tasks while the cluster takes the load. That is when the idea of a Raspberry Pi cluster kicked in.


## Design

The 300 models are independent: each learns from its own series. The cluster therefore splits the work by series and trains **one model at a time on each worker**, with all four of the worker's cores working on that one model. Four workers train four models at once.

Hadoop's file system (HDFS) stores the data and the trained models, and Spark hands out the series to the workers. Learning Hadoop and Spark on real hardware is part of the point of this project, alongside the speed-up.


## Measuring success

Success means training all 300 models in less than the 7-hour baseline, measured with the same script and data on both sides. A Raspberry Pi core is slower than a laptop core, especially on a Pi 4, so this isn't guaranteed: the cluster wins when a single Pi trains one model in under about 5½ minutes. [Workload](Workload.md#benchmark) shows how to measure it.

Even when a fast computer is quicker, the cluster still frees that computer for other work while the models train.

---

Back to the [Cluster Guide](Cluster_Guide.md)
