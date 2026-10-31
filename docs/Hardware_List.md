[Home](../README.md) · [Cluster Guide](Cluster_Guide.md) · [Troubleshooting](Troubleshooting.md)


<img src="img/icons/hardware-list.svg" width="96" height="96" alt=""/>


# Hardware List

**Goal:** buy everything the cluster needs before you start.

This list is for one `master` and four workers, as in the rest of the guide. Quantities scale with the number of nodes.

| Component | Qty | Priority | Notes |
|:--|:-:|:--|:--|
| Raspberry Pi 4 Model B or Raspberry Pi 5 | 5 | Required | Same model on every node if you can. 2 GB works with smaller memory settings; **4 GB or more recommended**. Workers run an HDFS DataNode, a Spark executor and Python at once; `master` runs the NameNode, the Spark master and your driver program |
| Official power supply | 5 | Required | One per Pi: the 15.3 W (5.1 V 3 A) supply for a Pi 4, or the 27 W (5 V 5 A) supply for a Pi 5. See [Power](#power) |
| USB-C cable | 5 | Required | Only if your supply has no built-in cable |
| microSD card, 32 GB, A1 or A2 | 5 | Required | A2 cards are faster at small reads and writes. See [Storage](#storage) for an SSD option |
| microSD card reader | 1 | Required | For flashing the cards from your computer |
| 8-port gigabit network switch | 1 | Required | 5 ports for the Pis + 1 uplink to your router. A 5-port switch is one port short |
| Ethernet cable, Cat 5e or better | 6 | Required | 5 Pis + 1 uplink |
| Heatsinks and fan, or a case with fans | 5 | Required | The cluster runs at full load for hours. A Pi 5 needs the Active Cooler or a case fan. See [Cooling](#cooling) |
| Cluster case (stacking plates with standoffs) | 1 | Recommended | Keeps boards apart for airflow; many include fans |
| Keyboard, mouse, monitor | 1 each | Optional | Not needed when you set up SSH while flashing ([Install OS](Install_OS.md)) |
| Micro-HDMI to HDMI cable | 1 | Optional | The Pi 4 and Pi 5 have micro-HDMI ports; match the other end to your monitor |

Prices change often, so check current ones on the [Raspberry Pi product page](https://www.raspberrypi.com/products/raspberry-pi-4-model-b/) and your local reseller.


## Power

Each Raspberry Pi 4 needs 5.1 V at up to 3 A ([specifications](https://www.raspberrypi.com/products/raspberry-pi-4-model-b/specifications/)), so five boards can draw up to 15 A together. A Raspberry Pi 5 is rated for 5 V at up to 5 A with its official 27 W supply ([product page](https://www.raspberrypi.com/products/raspberry-pi-5/)).

A multi-port USB charger rated 2.4 A *in total* is far below that. Under load the Pis see a voltage drop, slow themselves down, and can corrupt their SD cards. That defeats the point of the cluster, which is to train faster.

Good options:

- One official 5.1 V 3 A supply per Pi, on a power strip.
- A multi-port USB-C charger only if it can deliver 3 A on **every** port at the same time. Most chargers share their total between ports; check the spec sheet.
- PoE+ HATs on each Pi with a PoE+ switch, so one cable carries both network and power. The Pi 4 and Pi 5 need different HATs.

**Check:** after the cluster is running, every node should print `throttled=0x0`:

```bash
cluster-cmd vcgencmd get_throttled
```

Anything else means a power or heat problem. `0x50005`, for example, means under-voltage and throttling are happening now and have happened since boot. Fix power before tuning anything else.


## Cooling

A Raspberry Pi slows its CPU down as it nears 80 to 85 °C. Bare boards reach that within minutes of training a model on all four cores. Heatsinks alone help; heatsinks with a fan keep the CPU at full speed.

**Check** the temperature of every node while a job runs:

```bash
cluster-cmd vcgencmd measure_temp
```

Under about 70 °C at full load is comfortable.


## Storage

microSD cards are slow at random writes and wear out with heavy writing. HDFS writes data blocks and logs constantly, so:

- Use A1 or A2 rated cards from a known brand, 32 GB or larger.
- For heavier use, boot each Pi from an SSD instead: a USB 3 SSD on a Pi 4 or Pi 5, or an NVMe SSD on a Pi 5 with an M.2 HAT. Flash it with Raspberry Pi Imager the same way you flash a card.


## Raspberry Pi 4 or Raspberry Pi 5?

The Raspberry Pi 5 is the newest model and about two to three times faster than a Pi 4, which shortens training directly. It costs more and needs the 27 W supply and an active cooler, so budget for both. The Pi 4 is cheaper and is what the first build used. Both follow the same steps; [Hardware](Hardware.md) compares them.

---

**Step 1 of 9** · Step 2: [Install OS](Install_OS.md) →
