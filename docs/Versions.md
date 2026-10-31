[Background](Background.md) / [Purpose](Purpose.md) / [Getting Started](Getting_Started.md) / [Cluster Guide](Cluster_Guide.md)


<img src="img/icons/references.svg" width="96" height="96" alt=""/>


# Versions

Java, Hadoop and Spark must be compatible with each other, so the guide pins one tested combination. Use these versions on **every** node.

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
