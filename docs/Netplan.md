[Background](Background.md) / [Purpose](Purpose.md) / [Getting Started](Getting_Started.md) / [Cluster Guide](Cluster_Guide.md)


<img src="img/icons/netplan.svg" width="96" height="96" alt=""/>


# Netplan

**Most readers can skip this page.** On Raspberry Pi OS, use [`nmcli`](The_Pi_Network.md#option-b-set-a-static-address-on-each-pi) instead. This page is for nodes running **Ubuntu Server**, where [Netplan](https://netplan.io/) is the standard way to set up the network.

Netplan describes network settings in YAML files under `/etc/netplan/` and hands them to a backend (`systemd-networkd` on Ubuntu Server, NetworkManager on desktops) that does the actual work.

**On Raspberry Pi OS, don't hand-edit `/etc/netplan/`.** Current Raspberry Pi OS also uses Netplan under the hood, but NetworkManager rewrites those files with its own settings, so manual edits can be lost ([Raspberry Pi: cloud-init on Raspberry Pi OS](https://www.raspberrypi.com/news/cloud-init-on-raspberry-pi-os/)).

* [Find the interface name](#find-the-interface-name)
* [DHCP address](#dhcp-address)
* [Static address](#static-address)
* [Wi-Fi with a password](#wi-fi-with-a-password)
* [Apply the configuration](#apply-the-configuration)


## Find the interface name

```bash
ip a
```

`lo` is the loopback interface (the machine talking to itself, `127.0.0.1`). The wired interface is the other one, usually `eth0` on a Raspberry Pi.


## DHCP address

Save as `/etc/netplan/60-eth0.yaml`:

```yaml
network:
  version: 2
  renderer: networkd
  ethernets:
    eth0:
      dhcp4: true
```


## Static address

Save as `/etc/netplan/60-eth0.yaml`, using the node's address from the [network lookup table](The_Pi_Network.md#network-lookup-table):

```yaml
network:
  version: 2
  renderer: networkd
  ethernets:
    eth0:
      dhcp4: false
      addresses:
        - 192.168.0.101/24
      routes:
        - to: default
          via: 192.168.0.1
      nameservers:
        addresses: [192.168.0.1, 1.1.1.1]
```

`/24` matches the subnet mask `255.255.255.0`. Older examples use `gateway4:`, which Netplan has deprecated; `routes` with `to: default` replaces it.


## Wi-Fi with a password

Save as `/etc/netplan/60-wlan0.yaml`, replacing the network name and password:

```yaml
network:
  version: 2
  renderer: networkd
  wifis:
    wlan0:
      dhcp4: true
      regulatory-domain: "US"
      access-points:
        "Your Network":
          password: "your-password"
```

Set `regulatory-domain` to your [two-letter country code](https://en.wikipedia.org/wiki/ISO_3166-1_alpha-2).


## Apply the configuration

The files contain passwords and Netplan warns if others can read them, so restrict them first:

```bash
sudo chmod 600 /etc/netplan/*.yaml
```

Then test the configuration. `netplan try` applies it and rolls back automatically after 120 seconds unless you press Enter, which saves you if a mistake cuts off your SSH session:

```bash
sudo netplan try
```

**Check:** `ip -4 addr show eth0` shows the expected address, and `ping -c 3 ubuntu.com` gets replies.
