[Home](../README.md) · [Cluster Guide](Cluster_Guide.md) · [Troubleshooting](Troubleshooting.md)


<img src="img/icons/hardware-list.svg" width="96" height="96" alt=""/>


# Hardware List

**Goal:** buy everything the cluster needs before you start.

This list is for one `master` and four workers, as in the rest of the guide. Quantities scale with the number of nodes.

| Component | Qty | Priority | Notes |
|:--|:-:|:--|:--|
| Raspberry Pi 5 | 5 | Required | **4 GB minimum, 8 GB recommended**, the same on every node. A Pi 4 also works ([Pi 4 notes](#raspberry-pi-4)). Workers run an HDFS DataNode, a Spark executor and Python at once; `master` runs the NameNode, the Spark master and your driver program |
| Raspberry Pi 27 W USB-C power supply | 5 | Required | One per Pi, 5 V 5 A. See [Power](#power) |
| USB-C cable | 5 | Required | Only if your supply has no built-in cable |
| microSD card, 32 GB, A2 | 5 | Required | Or an NVMe SSD with the M.2 HAT+ instead (recommended for HDFS). See [Storage](#storage) |
| microSD card reader | 1 | Required | For flashing the cards from your computer |
| 8-port gigabit network switch | 1 | Required | 5 ports for the Pis + 1 uplink to your router. A 5-port switch is one port short |
| Ethernet cable, Cat 5e or better | 6 | Required | 5 Pis + 1 uplink |
| Raspberry Pi Active Cooler | 5 | Required | Clips onto the Pi 5. The cluster runs at full load for hours. See [Cooling](#cooling) |
| Cluster case (stacking plates with standoffs) | 1 | Recommended | Keeps boards apart for airflow. Check there is room above each board for the Active Cooler, and the M.2 HAT+ if you use one |
| Keyboard, mouse, monitor | 1 each | Optional | Not needed when you set up SSH while flashing ([Install OS](Install_OS.md)) |
| Micro-HDMI to HDMI cable | 1 | Optional | The Pi 5 has micro-HDMI ports; match the other end to your monitor |

Prices change often, so check current ones on the [Raspberry Pi 5 product page](https://www.raspberrypi.com/products/raspberry-pi-5/) and your local reseller.


## Power

A Raspberry Pi 5 is designed for the official 27 W supply, 5 V at up to 5 A ([product page](https://www.raspberrypi.com/products/raspberry-pi-5/)). Five boards can draw up to 25 A together, more than any ordinary multi-port USB charger delivers.

With too little power, the Pis see a voltage drop under load, slow themselves down, and can corrupt their cards. That defeats the point of the cluster, which is to train faster.

Good options:

- One official 27 W supply per Pi, on a power strip.
- A PoE+ HAT made for the Pi 5 on each board, with a PoE+ switch, so one cable carries both network and power. HATs made for the Pi 4 don't fit the Pi 5.

**Check:** after the cluster is running, every node should print `throttled=0x0`:

```bash
cluster-cmd vcgencmd get_throttled
```

Anything else means a power or heat problem. `0x50005`, for example, means under-voltage and throttling are happening now and have happened since boot. Fix power before tuning anything else.


## Cooling

A Raspberry Pi 5 starts slowing its CPU down at 80 °C, and drops to about 1.5 GHz above 85 °C. Without cooling, it reaches that within minutes of training a model on all four cores. The official **Active Cooler** keeps it around 60 °C under load, and its fan speeds up on its own as the board warms ([Raspberry Pi: heating and cooling Raspberry Pi 5](https://www.raspberrypi.com/news/heating-and-cooling-raspberry-pi-5/)).

**Check** the temperature of every node while a job runs:

```bash
cluster-cmd vcgencmd measure_temp
```

Under about 70 °C at full load is comfortable.


## Storage

microSD cards are slow at random writes and wear out with heavy writing. HDFS writes data blocks and logs constantly, so:

- **Good:** A2 rated microSD cards from a known brand, 32 GB or larger.
- **Better:** an NVMe SSD on each Pi 5, using the official [M.2 HAT+](https://www.raspberrypi.com/documentation/accessories/m2-hat-plus.html). It takes 2230 or 2242 size drives and fits over the Active Cooler (the *Compact* version doesn't). Flash the SSD with Raspberry Pi Imager through a USB adapter, the same way you flash a card. With no card inserted, the Pi 5 boots from the SSD.


## Raspberry Pi 4

The original cluster ran on five Raspberry Pi 4 Model B boards with 2 GB each, and a Pi 4 still works with every step in this guide. It is two to three times slower than a Pi 5 at training. If you use Pi 4 boards:

- Power each with the official 15.3 W (5.1 V 3 A) supply.
- Use heatsinks and a fan, or a case with fans, instead of the Active Cooler.
- Use a microSD card or a USB 3 SSD (the Pi 4 has no PCIe connector for the M.2 HAT+).
- With 2 GB boards, use the 2 GB rows in [Spark](Spark.md#configure-spark).
- Choose *Raspberry Pi 4* as the device when [flashing the cards](Install_OS.md#flash-each-card).

---

**Step 1 of 9** · Step 2: [Install OS](Install_OS.md) →
