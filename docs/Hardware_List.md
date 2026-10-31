[Home](../README.md) · [Cluster Guide](Cluster_Guide.md) · [Troubleshooting](Troubleshooting.md)


<img src="img/icons/hardware-list.svg" width="96" height="96" alt=""/>


# Hardware List

**Goal:** buy everything the cluster needs before you start.

This list is for one `master` and four workers, as in the rest of the guide. Quantities scale with the number of nodes.

The guide supports the **Raspberry Pi 5** and the **Raspberry Pi 4 Model B**. The Pi 5 is about two to three times faster at training; the Pi 4 is cheaper and is what the original cluster ran on. Pick one model and use it on all five nodes. Where the two boards need different parts, the table has a column for each.

| Component | Raspberry Pi 5 | Raspberry Pi 4 | Qty | Priority |
|:--|:--|:--|:-:|:--|
| Board | Raspberry Pi 5, **4 GB minimum, 8 GB recommended** | Raspberry Pi 4 Model B, **2 GB minimum, 4 GB recommended** | 5 | Required |
| Power supply | Official 27 W USB-C (5 V 5 A) | Official 15.3 W USB-C (5.1 V 3 A) | 5 | Required |
| Cooling | Raspberry Pi Active Cooler | Heatsinks and a fan, or a case with fans | 5 | Required |
| Storage | 32 GB A2 microSD card, or an NVMe SSD on the M.2 HAT+ | 32 GB A2 microSD card, or a USB 3 SSD | 5 | Required |
| microSD card reader | same | same | 1 | Required |
| 8-port gigabit network switch | same | same | 1 | Required |
| Ethernet cable, Cat 5e or better | same | same | 6 | Required |
| Cluster case (stacking plates with standoffs) | Room above each board for the Active Cooler, and the M.2 HAT+ if used | Room for heatsinks and fans | 1 | Recommended |
| PoE+ HAT, instead of power supplies | A HAT made for the Pi 5 | A HAT made for the Pi 4 | 5 | Optional |
| Keyboard, mouse, monitor | same | same | 1 each | Optional |
| Micro-HDMI to HDMI cable | same | same | 1 | Optional |

Notes:

- **RAM:** workers run an HDFS DataNode, a Spark executor and Python at once; `master` runs the NameNode, the Spark master and your driver program. More RAM gives Spark more room; [Spark](Spark.md#configure-spark) has memory settings for every size. The original cluster worked on 2 GB Pi 4 boards.
- **Switch:** 5 ports for the Pis plus 1 uplink to your router. A 5-port switch is one port short.
- **Keyboard, mouse, monitor:** not needed when you set up SSH while flashing ([Install OS](Install_OS.md)).

Prices change often, so check current ones on the [Raspberry Pi 5](https://www.raspberrypi.com/products/raspberry-pi-5/) and [Raspberry Pi 4](https://www.raspberrypi.com/products/raspberry-pi-4-model-b/) product pages and your local reseller.


## Power

Use the official supply for your board on every Pi:

| Board | Official supply | Five boards can draw up to |
|:--|:--|:--|
| Raspberry Pi 5 | 27 W, 5 V at up to 5 A ([product page](https://www.raspberrypi.com/products/raspberry-pi-5/)) | 25 A |
| Raspberry Pi 4 | 15.3 W, 5.1 V at up to 3 A ([specifications](https://www.raspberrypi.com/products/raspberry-pi-4-model-b/specifications/)) | 15 A |

With too little power, the Pis see a voltage drop under load, slow themselves down, and can corrupt their cards. That defeats the point of the cluster, which is to train faster. A multi-port USB charger rarely delivers full current on every port at once, so avoid one unless its spec sheet says it does.

Good options:

- One official supply per Pi, on a power strip.
- A PoE+ HAT on each board with a PoE+ switch, so one cable carries both network and power. HATs are made for one model: Pi 4 HATs don't fit the Pi 5.

**Check:** after the cluster is running, every node should print `throttled=0x0`:

```bash
cluster-cmd vcgencmd get_throttled
```

Anything else means a power or heat problem. `0x50005`, for example, means under-voltage and throttling are happening now and have happened since boot. Fix power before tuning anything else.


## Cooling

Both boards start slowing their CPU down at 80 °C, and slow further at 85 °C (a Pi 5 drops to about 1.5 GHz). Without cooling, they reach that within minutes of training a model on all four cores.

- **Raspberry Pi 5:** the official **Active Cooler** keeps it around 60 °C under load, and its fan speeds up on its own as the board warms ([Raspberry Pi: heating and cooling Raspberry Pi 5](https://www.raspberrypi.com/news/heating-and-cooling-raspberry-pi-5/)).
- **Raspberry Pi 4:** heatsinks alone help; heatsinks with a fan, or a case with fans, keep the CPU at full speed.

**Check** the temperature of every node while a job runs:

```bash
cluster-cmd vcgencmd measure_temp
```

Under about 70 °C at full load is comfortable.


## Storage

microSD cards are slow at random writes and wear out with heavy writing. HDFS writes data blocks and logs constantly, so:

- **Good, either board:** A2 rated microSD cards from a known brand, 32 GB or larger.
- **Better, Raspberry Pi 5:** an NVMe SSD on the official [M.2 HAT+](https://www.raspberrypi.com/documentation/accessories/m2-hat-plus.html). It takes 2230 or 2242 size drives and fits over the Active Cooler (the *Compact* version doesn't). With no card inserted, the Pi 5 boots from the SSD.
- **Better, Raspberry Pi 4:** a USB 3 SSD in one of the blue USB 3 ports. The Pi 4 has no PCIe connector, so the M.2 HAT+ doesn't fit it.

Flash an SSD with Raspberry Pi Imager the same way you flash a card, using a USB adapter for an NVMe drive.

---

**Step 1 of 9** · Step 2: [Install OS](Install_OS.md) →
