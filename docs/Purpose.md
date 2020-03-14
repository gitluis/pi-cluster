[Background](Background.md) / [Purpose](Purpose.md) / [Getting Started](Getting_Started.md) / [Cluster Guide](Cluster_Guide.md)


<img src="https://image.flaticon.com/icons/svg/2103/2103658.svg" width="100px" height="100px"/>


# Purpose

The main reason for building and configuring this cluster is to leverage Hadoop and Spark's distributed storage and processing capabilities to build, train, test and assess Machine Learning models in-parallel for projects at work and also to demonstrate you may not need to invest in full-powered computers or servers to build a cluster.

I found myself training about 300 XGBoost models on time-series financial data that would take about 7 hours to train total. As a result, the **goal** here is to at least reduce the amount of time it takes to train all models. By having a separate cluster, I allow myself to continue working on other tasks while the cluster takes the load. That is when the idea of Raspberry Pi's kicked in.
