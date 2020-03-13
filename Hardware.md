[Background](Background.md) / [Purpose](Purpose.md) / [**Getting Started**](Getting_Started.md) / [Cluster Guide](Cluster_Guide.md)

1. [**Hardware**](Hardware.md) - General Pi hardware information, specifications, costs and overclocking
2. [Software](Software.md) - High-level operating system and software information
3. [Formatting SD Cards](Formatting_SD_Cards.md) - A quick-guide on how to format SD cards
4. [Read & Write Images](Read_Write_OS_Images.md) - A quick-guide on how to flash, write, and read operating system images
5. [Installing NOOBS](Installing_NOOBS.md) - A guide on how to install the NOOBS operating system installer
6. [Installing Raspbian](Installing_Raspbian.md) - A guide on how to install Raspbian into your Pi
7. [Internet Connection](Internet_Connection.md) - Information on how to connect your Pi to the internet
8. [Software Updates](Software_Updates.md) - How to update and upgrade operating system, software and hardware
9. [Miscellaneous](Miscellaneous.md) - Other "good-to-know" information

#  

<img src="https://image.flaticon.com/icons/svg/2422/2422428.svg" width="100px" height="100px"/>


# Hardware

The following table show the latest Raspberry Pi computer boards along with some extra information about each of them.

| Board Model                                                                                  | RAM                | Cost            | Full Specifications                                                                       |
|----------------------------------------------------------------------------------------------|--------------------|-----------------|-------------------------------------------------------------------------------------------|
| [Raspberry Pi 4 Model B](https://www.raspberrypi.org/products/raspberry-pi-4-model-b/)       | 1 GB / 2 GB / 4 GB | $35 / $45 / $55 | [Click Here](https://www.raspberrypi.org/products/raspberry-pi-4-model-b/specifications/) |
| [Raspberry Pi 3 Model B+](https://www.raspberrypi.org/products/raspberry-pi-3-model-b-plus/) | 1 GB               | $35             | [Click Here](https://www.raspberrypi.org/products/raspberry-pi-3-model-b-plus/)           |
| [Raspberry Pi Zero W](https://www.raspberrypi.org/products/raspberry-pi-zero-w/)             | 512 MB             | $10             | [Click Here](https://www.raspberrypi.org/products/raspberry-pi-zero-w/)                   |

You can buy any of the Rapsberry Pi boards at [canakit.com](https://www.canakit.com/raspberry-pi/raspberry-pi-boards).


# Overclocking

```
OVERCLOCK AT YOUR OWN RISK !!!!!!
```


## Requirements
* CPU, RAM & USB Heatsinks
* Small Fan (mounted on top of raspberry pi)

**Note**: Heat sinks and fan "hats" may vary for each Raspberry Pi version.


## Known Information

| Status         | CPU Speed | GPU Speed | Over Voltage |
|:---------------|:----------|:----------|:-------------|
| Default        | 1500 MHz  | 500 MHz   | =0           |
| Max. Overclock | 2147 MHz  | 750 MHz   | =6           |


## `over_voltage` Limitations

Values above 6 are only allowed when `force_turbo` is specified: this sets the warranty bit if `over_voltage_*` is also set. This means that if `force_turbo` is specified (whether it is 0 or 1) and the `over_voltage` is set **above 6** then the `warranty` bit is set, thus **voiding your Raspberry Pi warranty**. For more information, please refer to [Overclocking options in config.txt](https://www.raspberrypi.org/documentation/configuration/config-txt/overclocking.md).


## How-to Overclock CPU/GPU

1. Connect your micro SD card to a PC
2. Open file `boot/config.txt` inside the micro SD card
3. Modify the file by adding the following under your corresponding Raspberry Pi version (mine is a Pi 4):
```python
[pi4]
over_voltage=6
arm_freq=2000
gpu_freq=600
```

Truth is, you can start with `over_voltage=2` (+0.05 V) then increase it by a step of 1 until the Raspberry Pi boots up properly without exceeding `over_voltage=6`.

**Note:** Every `over_voltage` increase represents a voltage-load increase of `over_voltage * 0.025 V`. For instance, when `over_voltage=3`, total voltage load increases by 0.075 V (or 75 mV).
