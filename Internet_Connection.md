[Background](Background.md) / [Purpose](Purpose.md) / [Getting Started](Getting_Started.md) / [Cluster Guide](Cluster_Guide.md)


<img src="https://image.flaticon.com/icons/svg/2526/2526509.svg" width="100px" height="100px"/>


# Internet Connection

This section covers different methods on how-to set up and connect to the internet on your Raspberry Pi.

**Ethernet** is the preferred and easiest method.

* [Ethernet Connection](#ethernet-connection)
* [WiFi Connection](#wifi-connection)
* [Setting WiFi Network via CLI](#setting-wifi-network-via-the-cli)
    * [Using raspi-config](#using-raspi-config)
    * [Getting WiFi network details](#getting-wifi-network-details)
    * [Adding network details to Raspberry Pi](#adding-network-details-to-raspberry-pi)


# Ethernet Connection

Requirements:
* <img src="https://image.flaticon.com/icons/svg/361/361390.svg" width="20px" height="20px"/> Internet access (router)
* <img src="https://image.flaticon.com/icons/svg/403/403084.svg" width="20px" height="20px"/> An Ethernet cable

Steps to connect:
1. Make sure that your router is connected to the internet.
2. Connect one (1) Ethernet cable end to your Raspberry Pi and the other end to your router.
3. Access [https://github.com/gitluis/rpi-cluster](https://github.com/gitluis/rpi-cluster) through the web browser.
4. If page shows up, you have successfully connected your board to the internet.
6. Done!

Troubleshooting:
* Refer to [How to Fix Your Internet Connection: 15 Steps (with Pictures)](https://www.wikihow.com/Fix-Your-Internet-Connection).


# WiFi Connection

Requirements:
* <img src="https://image.flaticon.com/icons/svg/361/361390.svg" width="20px" height="20px"/> Internet access (router)

Steps to connect:
1. If you are using the command-line interface, refer to the next section for details on how to set up WiFi through the command line.
1. If you are using the Raspberry Pi Desktop or another Desktop Environment, you can set up wireless networking by going to the network icon at the right-hand end of the menu bar. See [image reference here](https://www.raspberrypi.org/documentation/configuration/wireless/desktop.md).

Troubleshooting:
* Refer to Raspberry Pi Foundation's [wireless connectivity guide](https://www.raspberrypi.org/documentation/configuration/wireless/desktop.md).


# Setting WiFi Network via CLI

How-to configure WiFi Protected Access (WPA) based wireless network interfaces manually on Linux-based operating systems via the Command Line Interface (CLI).


## Using raspi-config

1. Run `sudo raspi-config`
1. Select the **Network Options** item from the menu
1. Select **Wi-fi** option
1. Set the network SSID and the passphrase for the network

If you do not know the SSID of the network, the next section details how to list all available networks prior to running `raspi-config` command.


## Getting WiFi network details

To scan and list all available WiFi networks along with other useful information, run the following command in a terminal window
```cli
sudo iwlist wlan0 scan
```

Retrieve the following information from your WiFi Network:
* `'ESSID:"testing"'` which is the name of the WiFi network
* `'IE:IEEE 802.11i/WPA2 Version 1'` which is the authentication method that such network uses
* The password for the wireless network (commonly found in the back of the router)

Try [using raspi-config](#Using-raspi-config) after writing down the network details. If `raspi-config` fails to connect the Pi to the desired network, the next section covers how to manually add such network to the Pi and connect to it.


## Adding network details to Raspberry Pi

Create a `wpa-supplicant` configuration file
```cli
sudo nano /etc/wpa_supplicant/wpa_supplicant.conf
```

Generate an encrypted pre-shared key (psk)
```cli
wpa_passphrase "<network ssid>" >> /etc/wpa_supplicant/wpa_supplicant.conf
```

Enter the network SSID and WPA password or keyphrase then hit Enter again.

Here is how `wpa_supplicant.conf` should look like so far:
```conf
network={
    ssid="network ssid"
    psk="encrypted pre-shared key"
    key_mgmt=WPA-PSK
}
```

Add the following information at the top of the `wpa_supplicant.conf` file
```conf
ctrl_interface=DIR=/var/run/wpa_supplicant GROUP=netdev
update_config=1
country=<country-code-here>
```

Refer to [en.wikipedia.org/wiki/ISO_3166-1](https://en.wikipedia.org/wiki/ISO_3166-1) for your specific country code.

Re-configure the network interface
```cli
wpa_cli -i wlan0 reconfigure
```

Verify whether the Raspberry Pi has successfully connected to the internet using:
```cli
ifconfig wlan0
```

If `inet addr` displays an IP address beside it, the Raspberry PI is connected to the internet. Otherwise, please refer to the Raspberry Pi Foundation's [guide](https://www.raspberrypi.org/documentation/configuration/wireless/wireless-cli.md) on how to connect to WiFi via command line.
