[Background](Background.md) / [Purpose](Purpose.md) / [Getting Started](Getting_Started.md) / [Cluster Guide](Cluster_Guide.md)


<img src="img/icons/cluster.svg" width="96" height="96" alt=""/>


# Cluster Guide

The following set of sections cover all required information to build a cluster of Raspberry Pi's from hardware to software, installation, configuration and test of applications.

1. [Hardware List](Hardware_List.md) - List of hardware required for the cluster
2. [Install OS](Install_OS.md) - Flash every card with Raspberry Pi Imager, ready for SSH
3. [The Pi Network](The_Pi_Network.md) - Fixed addresses, the hostname map and SSH keys
4. [Cluster Commands](Cluster_Commands.md) - Run commands and copy files on every node at once
5. [Cluster Security](Cluster_Security.md) - Key-only logins, fail2ban and a firewall
6. [Versions](Versions.md) - The Java, Hadoop and Spark versions this guide uses
7. [Single Node Setup](Single_Node_Setup.md) - Java on every node, HDFS on master alone
8. [Cluster Setup](Cluster_Setup.md) - HDFS across all nodes; starting and stopping the cluster
9. [Spark](Spark.md) - Spark in standalone mode, one executor per worker
10. [Workload](Workload.md) - Train the 300 models, one per worker at a time, and benchmark the cluster
