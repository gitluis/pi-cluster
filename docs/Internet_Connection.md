[Home](../README.md) · [Cluster Guide](Cluster_Guide.md) · [Troubleshooting](Troubleshooting.md)


<img src="img/icons/internet.svg" width="96" height="96" alt=""/>


# Internet Connection

**Goal:** each Pi can reach the internet, for software updates and downloads.

**Ethernet is the recommended connection** for a cluster: it's faster and steadier than Wi-Fi, and the nodes already need it to talk to each other.

* [Ethernet](#ethernet)
* [Wi-Fi](#wi-fi)
* [Check the connection](#check-the-connection)


# Ethernet

You need:

* <img src="img/icons/router.svg" width="20" height="20" alt=""/> A router with internet access
* <img src="img/icons/ethernet.svg" width="20" height="20" alt=""/> An Ethernet cable from the Pi to your switch, and one from the switch to the router

There is nothing to configure: Raspberry Pi OS asks the router for an address automatically (DHCP) as soon as the cable is plugged in. To give each node a fixed address, see [The Pi Network](The_Pi_Network.md#give-each-node-a-fixed-address).


# Wi-Fi

Only use Wi-Fi for a single Pi you're testing, or if the cluster can't be wired to your router. The Raspberry Pi 4 and Pi 5 have built-in Wi-Fi.

**Easiest:** set the network name (SSID), password and Wi-Fi country in Raspberry Pi Imager's customization step when you flash the card ([Install OS](Install_OS.md#flash-each-card)).

**On a running Pi:** Raspberry Pi OS manages networks with NetworkManager.

1. List nearby networks:

    ```bash
    nmcli device wifi list
    ```

2. Connect, replacing the name and password:

    ```bash
    sudo nmcli device wifi connect "Your Network" password "your-password"
    ```

    The connection is saved and reconnects after a reboot.

If you prefer menus, `sudo nmtui` opens a text interface for the same settings. If Wi-Fi is turned off, set your country first in `sudo raspi-config` under *Localisation Options*, then *WLAN Country*: Wi-Fi stays blocked until a country is set.

Older guides edit `/etc/wpa_supplicant/wpa_supplicant.conf`. Current Raspberry Pi OS ignores that file.


# Check the connection

```bash
ip -4 addr show eth0      # or wlan0 for Wi-Fi
ping -c 3 raspberrypi.com
```

The first command should show an `inet` line with an address such as `192.168.0.101/24`. The second should show three replies. If there's an address but no replies, the problem is between your router and the internet; if there's no address, check the cable, the switch lights and the router.

---

Back to the [Cluster Guide](Cluster_Guide.md)
