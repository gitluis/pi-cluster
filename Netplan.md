[Background](Background.md) / [Purpose](Purpose.md) / [Getting Started](Getting_Started.md) / [Cluster Guide](Cluster_Guide.md)


<img src="https://image.flaticon.com/icons/svg/2526/2526509.svg" width="100px" height="100px"/>


# Netplan

As of Ubuntu 18.04 LTS, ubuntu has switched to [Netplan](https://netplan.io/) for configuring network interfaces. Netplan is a [YAML](https://en.wikipedia.org/wiki/YAML)-based configuration system that makes the process of configuring a network simple and very straightforward.

* [Install Netplan](#install-netplan)
* [Getting network details](#getting-network-details)
* [Set up network via DHCP](#set-up-network-via-dhcp)
* [Set up a static network](#set-up-a-static-network)
* [Set up an open wireless network (WiFi)](#set-up-an-open-wireless-network-wifi)
* [Set up a WPA-based wireless network](#set-up-a-wpa-based-wireless-network-wifi)
* [Network configuration](#network-configuration)

## Install Netplan

For those not using Ubuntu 18.04 LTS, you will have to manually install netplan
```cli
sudo apt update -y
sudo apt install netplan
```

By default, it may be disabled, thus we have to enable it
```cli
echo "ENABLED=1" | sudo tee /etc/default/netplan
```

Reboot the system
```cli
sudo reboot
```


### How can I install Netplan without an internet connection?

Keep in mind that if you are not using Ubuntu 18.04 LTS which comes with Netplan installed by default then you will have to install Netplan first. However, if you are not or cannot connect to the internet via Ethernet, _how will you download and install Netplan?_

For such specific cases I would recommend attempting to configure your network with the previous guides (above). If none of them worked out for you, I would suggest to stick to Raspbian with Desktop in which network can be set up easily or switch to Ubuntu 18.04 LTS or a newer version.


## Getting network details

List all network interfaces
```cli
ip a
```

You typically have two (2) or more network interfaces:
* First one is always **lo** which stands for loopback interface. This is a network interface that identifies the device and points to the local IP address of your system, most well known as 127.0.0.0/8 and also called **localhost**.
* The second is the network interface we're looking for to configure whose name may vary between _eth0_, _ens33_, among others depending on your operating system.


## Set up network via DHCP

To set up a network interface named `eth0` via Ethernet to get an automatically IP address assigned via DHCP, create a `eth0-config.yaml` configuration file with the following:
```yaml
network:
  version: 2
  renderer: networkd
  ethernets:
    eth0:
      dhcp4: true
```

Now refer to [Network configuration](#network-configuration) to apply the new configuration.


## Set up a static network

To set up a network interface named `eth0` via Ethernet to have a static IP address assigned to it, create a `eth0-config.yaml` configuration file with the following:
```yaml
network:
  version: 2
  renderer: networkd
  ethernets:
    eth0:
      addresses:
        - 192.168.0.25/24
      gateway4: 192.168.0.1
      nameservers:
        addresses: [192.168.0.1, 8.8.8.8]
```

For your IP address mask value, e.g. your `Subnet Mask` is `255.255.255.0` then the IP address mask is `xxx.xxx.xxx.xxx/24` as specified above, refer to [this guide here](https://www.aelius.com/njh/subnet_sheet.html) for more details.

Now refer to [Network configuration](#network-configuration) to apply the new configuration.


## Set up an open wireless network (WiFi)

To set up a network interface named `wlan0` and connect to a open wireless connection (public WiFi), create a `wlan0-config.yaml` configuration file with the following:
```yaml
network:
  version: 2
  wifis:
    wlan0:
      access-points:
        opennetwork: {}
      dhcp4: yes
```

Now refer to [Network configuration](#network-configuration) to apply the new configuration.


## Set up a WPA-based wireless network (WiFi)

To set up a network interface named `wlan0` and connect to a private wireless connection (WPA/WPA2 WiFi), create a `wlan0-config.yaml` configuration file with the following:
```yaml
network:
  version: 2
  renderer: networkd
  wifis:
    wlan0:
      dhcp4: no
      dhcp6: no
      addresses: [192.168.0.25/24]
      gateway4: 192.168.0.1
      nameservers:
        addresses: [192.168.0.1, 8.8.8.8]
      access-points:
        "network_ssid_name":
          password: "**********"
```

For your IP address mask value, e.g. your `Subnet Mask` is `255.255.255.0` then the IP address mask is `xxx.xxx.xxx.xxx/24` as specified above, refer to [this guide here](https://www.aelius.com/njh/subnet_sheet.html) for more details.

Don't forget to replace `"network_ssid_name"` with your network SSID and `"**********"` with your network's passphrase key or pre-shared key password.

Now refer to [Network configuration](#network-configuration) to apply the new configuration.


## Network configuration

Save your configuration files under `/etc/netplan/` with the `.yaml` extension, e.g. `/etc/netplan/eth0-config.yaml`.

Apply the new configuration
```cli
sudo netplan apply
```
The configuration will be written to disk under `/etc/netplan/` and will persist between reboots if accepted and properly configured.

Verify you are connected to the internet
```cli
ping google.com
```
You should start seeing data being received constantly, meaning you are downloading packets from google.com as a test. Type `Ctrl+C` to interrupt.
