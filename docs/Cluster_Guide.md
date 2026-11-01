[Home](../README.md) · [Cluster Guide](Cluster_Guide.md) · [Troubleshooting](Troubleshooting.md)


<img src="img/icons/cluster.svg" width="96" height="96" alt=""/>


# Cluster Guide

Follow these steps in order, from an empty desk to 300 trained models. Each page starts with its goal and where to run it, and ends with a check that the step worked before you move on.

| Step | Page | At the end you have | Run on |
| :-: | --- | --- | --- |
| 1 | [Hardware List](Hardware_List.md) | Everything bought and assembled, with enough power and cooling | – |
| 2 | [Install OS](Install_OS.md) | Five cards flashed with Raspberry Pi OS Lite, each node reachable over SSH | Your computer |
| 3 | [The Pi Network](The_Pi_Network.md) | Fixed addresses, nodes reachable by name, `master` able to log in everywhere | Your computer, `master` |
| 4 | [Cluster Commands](Cluster_Commands.md) | One command to run or copy anything on every node | `master` |
| 5 | [Cluster Security](Cluster_Security.md) | Key-only logins, fail2ban and a firewall | `master` |
| 6 | [Single Node Setup](Single_Node_Setup.md) | Java on every node; HDFS working on `master` alone | `master` |
| 7 | [Cluster Setup](Cluster_Setup.md) | HDFS across four workers, with two copies of every block | `master` |
| 8 | [Spark](Spark.md) | Spark with one 4-core executor per worker, reading from HDFS | `master` |
| 9 | [Workload](Workload.md) | 300 models trained, one per worker at a time, and a benchmark | `master` |

Stuck? See [Troubleshooting](Troubleshooting.md).


## Reference pages

Read these when a step points to them, or when you need them later.

| Page | Covers |
| --- | --- |
| [About](About.md) | Why this cluster exists, Hadoop and Spark explained, and the build history |
| [Getting Started](Getting_Started.md) | What you need before step 1 |
| [Software](Software.md) | Raspberry Pi OS and which edition to use |
| [Versions](Versions.md) | The Java, Hadoop and Spark versions the guide uses, and why |
| [Internet Connection](Internet_Connection.md) | Ethernet and Wi-Fi |
| [Software Updates](Software_Updates.md) | Updating packages and firmware on every node |
| [Back Up and Restore Cards](Read_Write_OS_Images.md) | Saving a card to an image file; cloning cards |
| [Netplan](Netplan.md) | Network setup for nodes running Ubuntu Server instead |
| [Troubleshooting](Troubleshooting.md) | Symptoms and fixes |
| [References](References.md) | Sources this guide builds on |
