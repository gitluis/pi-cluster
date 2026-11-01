[Home](../README.md) · [About](About.md) · [Getting Started](Getting_Started.md) · [Cluster Guide](Cluster_Guide.md) · [Troubleshooting](Troubleshooting.md)


<img src="img/icons/hardware-list.svg" width="96" height="96" alt=""/>


# Hardware List

**Goal:** buy everything the cluster needs before you start.

* [Choosing a board](#choosing-a-board)
* [What to buy](#what-to-buy)
* [Power](#power)
* [Cooling](#cooling)
* [Storage](#storage)
* [Overclocking (optional)](#overclocking-optional)


## Choosing a board

This guide supports two boards: the **Raspberry Pi 5**, the newest and fastest model, and the **Raspberry Pi 4 Model B**, which the original cluster ran Hadoop and Spark on (see [Builds](About.md#builds)). Every step works on both; where they differ, the guide shows both.

The table shows which boards suit a Hadoop/Spark cluster.

| Board | RAM options | Power supply | Fit for this cluster |
|:--|:--|:--|:--|
| [Raspberry Pi 5](https://www.raspberrypi.com/products/raspberry-pi-5/) | 1, 2, 4, 8 or 16 GB | 5 V 5 A USB-C (27 W) | **Supported, fastest.** About two to three times as fast as a Pi 4 at training. 4 GB minimum, 8 GB recommended. Needs the Active Cooler under sustained load |
| [Raspberry Pi 4 Model B](https://www.raspberrypi.com/products/raspberry-pi-4-model-b/) | 1 to 8 GB | 5.1 V 3 A USB-C (15.3 W) | **Supported.** The original cluster ran on 2 GB boards. 2 GB minimum, 4 GB recommended. Needs heatsinks and a fan under sustained load |
| [Raspberry Pi 3 Model B+](https://www.raspberrypi.com/products/raspberry-pi-3-model-b-plus/) | 1 GB | 5.1 V 2.5 A micro-USB | No: 1 GB is too little for Hadoop and Spark together |
| [Raspberry Pi Zero 2 W](https://www.raspberrypi.com/products/raspberry-pi-zero-2-w/) | 512 MB | 5.1 V 2.5 A micro-USB | No: too little memory and no Ethernet port |

Pick one model and use the same amount of RAM on all five nodes if you can. Mixing works, but the memory settings in [Spark](Spark.md#configure-spark) have to suit the smallest board, and slower workers finish fewer models.

Use the 64-bit edition of Raspberry Pi OS on every board. Java, Hadoop and Spark all need it to use more than a few gigabytes of memory efficiently, and Hadoop publishes ARM 64-bit builds.


## What to buy

This list is for one `master` and four workers, as in the rest of the guide. Quantities scale with the number of nodes. Where the two boards need different parts, the table has a column for each.

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


## Overclocking (optional)

**Skip this unless your cluster already runs cool and stable.** It's not part of building the cluster: come back to it once the cluster runs. Overclocking adds heat and power draw, and a cluster under hours of full load is the worst case for both. Get `vcgencmd get_throttled` to report `throttled=0x0` first ([Power](#power)).

Overclocking needs good cooling: heatsinks **and** a fan.

**Raspberry Pi 5:** don't overclock a Pi 5 cluster. It already runs at 2.4 GHz, and under hours of full load the gain is small compared with the extra heat and the risk of an unstable node. If you want to try anyway, its settings go in a `[pi5]` section; see the official [overclocking options](https://www.raspberrypi.com/documentation/computers/config_txt.html#overclocking-options).

**Raspberry Pi 4:** overclocking gives a Pi 4 a more noticeable boost. The values and steps below are for the Pi 4, as used in the original build.


### Known values for the Raspberry Pi 4

| Setting | Default | Reported stable maximum |
|:--|:--|:--|
| CPU (`arm_freq`) | 1500 MHz on early boards, 1800 MHz on newer ones | 2147 MHz |
| GPU (`gpu_freq`) | 500 MHz | 750 MHz |
| `over_voltage` | 0 | 6 |

Check what your board runs at today:

```bash
vcgencmd get_config arm_freq
```

The maximum values come from [Tom's Hardware's overclocking tests](https://www.tomshardware.com/reviews/raspberry-pi-4-b-overclocking,6188.html); not every board reaches them.


### `over_voltage` limits

Each step of `over_voltage` adds 0.025 V. For example, `over_voltage=3` adds 0.075 V (75 mV).

Values above 6 are only allowed together with `force_turbo=1`, and that combination permanently sets a bit in the chip that **voids your warranty**. Stay at 6 or below. Details are in the official [overclocking options](https://www.raspberrypi.com/documentation/computers/config_txt.html#overclocking-options).


### How to overclock the CPU and GPU

1. Open the boot configuration file on the Pi:

    ```bash
    sudo nano /boot/firmware/config.txt
    ```

    (On your computer, it's `config.txt` on the card's `bootfs` partition.)

2. Add these lines under the `[pi4]` section, or add the section if it's missing:

    ```ini
    [pi4]
    over_voltage=2
    arm_freq=2000
    gpu_freq=600
    ```

3. Reboot with `sudo reboot`.

4. **Check** that the new speed applied and that the board isn't throttling under load:

    ```bash
    vcgencmd measure_clock arm
    vcgencmd measure_temp
    vcgencmd get_throttled
    ```

If the Pi doesn't boot or `get_throttled` is not `0x0`, raise `over_voltage` by 1 (up to 6) or lower `arm_freq`. If a Pi won't boot at all, put its card in your computer and remove the lines from `config.txt` on the `bootfs` partition.

---

**Step 1 of 9** · Step 2: [Install OS](Install_OS.md) →
