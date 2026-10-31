[Home](../README.md) · [Cluster Guide](Cluster_Guide.md) · [Troubleshooting](Troubleshooting.md)


<img src="img/icons/getting-started.svg" width="96" height="96" alt=""/>


# Getting Started

**Goal:** know what you need and how the guide works, before you buy anything.


## What you need

- **Hardware:** five Raspberry Pi 4 boards plus power, cooling, cards, a switch and cables. [Hardware List](Hardware_List.md) has the full list.
- **A computer** running Windows, macOS or Linux, with a microSD card reader. You use it to flash the cards and to log in to the cluster.
- **A router** with a free Ethernet port, for the cluster's internet access.
- **Comfort with a terminal:** typing commands, editing a file with `nano`, and reading error messages. No Hadoop or Spark experience is needed.


## How the guide works

- The [Cluster Guide](Cluster_Guide.md) is the path: nine steps in order. Each step relies on the ones before it.
- Every step page starts with its **Goal** and where to **Run on** (your computer, `master`, or every node), and has **Check** points that tell you whether it worked.
- Commands that start with `cluster-cmd`, `master-cmd` or `cluster-scp` act on several nodes at once. They're set up in step 4, [Cluster Commands](Cluster_Commands.md).
- Examples use the username `alice` and the addresses `192.168.0.100` to `192.168.0.104`. Replace them with your own wherever they appear.
- Reference pages, such as [Hardware](Hardware.md) or [Software Updates](Software_Updates.md), explain a topic in more depth. The steps link to them when they're needed.


## Why a cluster

[Background](Background.md) explains what Hadoop and Spark are and how they fit together. [Purpose](Purpose.md) explains what this cluster is for: training 300 forecasting models faster than one computer can.

Ready? Start with [step 1: Hardware List](Hardware_List.md).

---

Back to the [Cluster Guide](Cluster_Guide.md)
