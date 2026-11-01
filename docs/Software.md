[Home](../README.md) · [Getting Started](Getting_Started.md) · [Cluster Guide](Cluster_Guide.md) · [Troubleshooting](Troubleshooting.md) · [About](About.md)


<img src="img/icons/software.svg" width="96" height="96" alt=""/>


# Software

A Raspberry Pi needs an operating system (OS) on its microSD card, just as a laptop needs Windows, macOS or Linux.

The official one is **Raspberry Pi OS**, a version of Debian Linux built for the Pi. It was called *Raspbian* until 2020, and older tutorials still use that name. The current release is based on Debian 13 ("Trixie").

<img src="img/diagrams/os-editions.svg" width="100%" alt="Raspberry Pi OS Desktop, a full graphical desktop, next to Raspberry Pi OS Lite, a command line only edition suited to cluster nodes managed over SSH."/>

* [Which edition to use](#which-edition-to-use)
* [How you install it](#how-you-install-it)
* [Versions](#versions)


## Which edition to use

Use **Raspberry Pi OS Lite (64-bit)** on every node.

- **Lite** has no desktop, which leaves more memory for Hadoop and Spark. You manage the nodes over SSH from your own computer.
- **64-bit** lets Java use the board's full memory, and Hadoop publishes ready-made 64-bit ARM builds.

The Desktop edition works too, but the desktop uses a few hundred megabytes of memory on every node for no benefit in a cluster.

Other operating systems, such as Ubuntu Server, also run on the Pi and can be picked in Raspberry Pi Imager. This guide assumes Raspberry Pi OS; commands may differ elsewhere.


## How you install it

Use **Raspberry Pi Imager**, the official tool for writing an OS to a card. It downloads the OS, writes it, and lets you set each node's hostname, user and SSH access before the first boot. [Install OS](Install_OS.md) walks through it.

NOOBS, the older installer that earlier versions of this guide recommended, is no longer maintained. Imager replaces it.


## Versions

Java, Hadoop and Spark must work together, so the guide pins one combination that their documentation lists as compatible. Use these versions on **every** node.

| Component | Version | Why this one |
|:--|:--|:--|
| Raspberry Pi OS Lite (64-bit) | Debian 13 "Trixie" based | Current release; 64-bit for Java memory and Hadoop's ARM builds |
| Java | Eclipse Temurin **17** | Hadoop 3.5 requires Java 17 on the server side ([Hadoop 3.5.0 docs](https://hadoop.apache.org/docs/r3.5.0/)); Spark 4 needs Java 17 or newer. Debian 13 doesn't package Java 17, so it comes from [Adoptium](https://adoptium.net/installation/linux) |
| Hadoop | **3.5.0**, `aarch64` build | First release with full Java 17 support ([release notes](https://hadoop.apache.org/release/3.5.0.html)) |
| Spark | **4.2.1**, pre-built for Hadoop 3 | Bundles Hadoop 3.5 client libraries; supports Java 17 |
| Python | 3.13, from Raspberry Pi OS | Same version on every node, which PySpark requires |
| Python packages | See [`workload/requirements.txt`](../workload/requirements.txt) | Installed in one virtual environment, `/opt/pyenv`, on every node |

Versions chosen on 30 October 2026. Newer patch releases (3.5.x, 4.2.x) should work the same; for anything else, check the release notes of each project before upgrading one piece on its own.

Download links in this guide use [Apache's download CDN](https://dlcdn.apache.org/), which only keeps current releases. If a link stops working, the same file is in the [Apache archive](https://archive.apache.org/dist/) under the same path.

---

Back to the [Cluster Guide](Cluster_Guide.md)
