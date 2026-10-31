[Home](../README.md) · [Cluster Guide](Cluster_Guide.md) · [Troubleshooting](Troubleshooting.md)


<img src="img/icons/hardware.svg" width="96" height="96" alt=""/>


# Hardware

This guide supports two boards: the **Raspberry Pi 5**, the newest and fastest model, and the **Raspberry Pi 4 Model B**, which the original cluster ran Hadoop and Spark on (see [Builds](../README.md#builds)). Every step works on both; where they differ, the page shows both.

Use the same model and the same amount of RAM on all five nodes if you can. Mixing works, but the memory settings in [Spark](Spark.md#configure-spark) have to suit the smallest board, and slower workers finish fewer models.

The table shows which boards suit a Hadoop/Spark cluster.

| Board | RAM options | Power supply | Fit for this cluster |
|:--|:--|:--|:--|
| [Raspberry Pi 5](https://www.raspberrypi.com/products/raspberry-pi-5/) | 1, 2, 4, 8 or 16 GB | 5 V 5 A USB-C (27 W) | **Supported, fastest.** About two to three times as fast as a Pi 4 at training. 4 GB minimum, 8 GB recommended. Needs the Active Cooler under sustained load |
| [Raspberry Pi 4 Model B](https://www.raspberrypi.com/products/raspberry-pi-4-model-b/) | 1 to 8 GB | 5.1 V 3 A USB-C (15.3 W) | **Supported.** The original cluster ran on 2 GB boards. 2 GB minimum, 4 GB recommended. Needs heatsinks and a fan under sustained load |
| [Raspberry Pi 3 Model B+](https://www.raspberrypi.com/products/raspberry-pi-3-model-b-plus/) | 1 GB | 5.1 V 2.5 A micro-USB | No: 1 GB is too little for Hadoop and Spark together |
| [Raspberry Pi Zero 2 W](https://www.raspberrypi.com/products/raspberry-pi-zero-2-w/) | 512 MB | 5.1 V 2.5 A micro-USB | No: too little memory and no Ethernet port |

Use the 64-bit edition of Raspberry Pi OS on every board. Java, Hadoop and Spark all need it to use more than a few gigabytes of memory efficiently, and Hadoop publishes ARM 64-bit builds.

See [Hardware List](Hardware_List.md) for everything else to buy.


# Overclocking (optional)

**Skip this unless your cluster already runs cool and stable.** Overclocking adds heat and power draw, and a cluster under hours of full load is the worst case for both. Get `vcgencmd get_throttled` to report `throttled=0x0` first ([Power](Hardware_List.md#power)).

Overclocking needs good cooling: heatsinks **and** a fan.

**Raspberry Pi 5:** don't overclock a Pi 5 cluster. It already runs at 2.4 GHz, and under hours of full load the gain is small compared with the extra heat and the risk of an unstable node. If you want to try anyway, its settings go in a `[pi5]` section; see the official [overclocking options](https://www.raspberrypi.com/documentation/computers/config_txt.html#overclocking-options).

**Raspberry Pi 4:** overclocking gives a Pi 4 a more noticeable boost. The values and steps below are for the Pi 4, as used in the original build.


## Known values for the Raspberry Pi 4

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


## `over_voltage` limits

Each step of `over_voltage` adds 0.025 V. For example, `over_voltage=3` adds 0.075 V (75 mV).

Values above 6 are only allowed together with `force_turbo=1`, and that combination permanently sets a bit in the chip that **voids your warranty**. Stay at 6 or below. Details are in the official [overclocking options](https://www.raspberrypi.com/documentation/computers/config_txt.html#overclocking-options).


## How to overclock the CPU and GPU

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

Back to the [Cluster Guide](Cluster_Guide.md)
