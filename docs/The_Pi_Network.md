[Home](../README.md) · [About](About.md) · [Getting Started](Getting_Started.md) · [Cluster Guide](Cluster_Guide.md) · [Troubleshooting](Troubleshooting.md)


<img src="img/icons/pi-network.svg" width="96" height="96" alt=""/>


# The Pi Network

**Goal:** every node can reach the internet and has a fixed IP address, every node can reach the others by name, and `master` can log in to every node with an SSH key.

**Run on:** your own computer and `master`, as each step says.

The Pis talk to each other over a [local area network (LAN)](https://www.howtogeek.com/353283/what-is-a-local-area-network-lan/): all five plug into the switch, and the switch plugs into your router for internet access.

* [Connect to the internet](#connect-to-the-internet)
* [Network lookup table](#network-lookup-table)
* [Give each node a fixed address](#give-each-node-a-fixed-address)
* [Mapping the hostname](#mapping-the-hostname)
* [SSH keys from master to every node](#ssh-keys-from-master-to-every-node)


# Connect to the internet

Each Pi needs the internet for software updates and downloads. **Ethernet is the recommended connection** for a cluster: it's faster and steadier than Wi-Fi, and the nodes already need it to talk to each other.


## Ethernet

You need:

* <img src="img/icons/router.svg" width="20" height="20" alt=""/> A router with internet access
* <img src="img/icons/ethernet.svg" width="20" height="20" alt=""/> An Ethernet cable from the Pi to your switch, and one from the switch to the router

There is nothing to configure: Raspberry Pi OS asks the router for an address automatically (DHCP) as soon as the cable is plugged in. Fixed addresses come [next](#give-each-node-a-fixed-address).


## Wi-Fi

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


## Check the connection

```bash
ip -4 addr show eth0      # or wlan0 for Wi-Fi
ping -c 3 raspberrypi.com
```

The first command should show an `inet` line with an address such as `192.168.0.101/24`. The second should show three replies. If there's an address but no replies, the problem is between your router and the internet; if there's no address, check the cable, the switch lights and the router.


# Network lookup table

| Pi | Interface | IP address | Hostname | Role |
|:-:|:--|:--|:--|:--|
| 0 | eth0 | 192.168.0.100 | master | Runs the HDFS NameNode and Spark master; sends commands |
| 1 | eth0 | 192.168.0.101 | worker1 | Stores data and runs work |
| 2 | eth0 | 192.168.0.102 | worker2 | Stores data and runs work |
| 3 | eth0 | 192.168.0.103 | worker3 | Stores data and runs work |
| 4 | eth0 | 192.168.0.104 | worker4 | Stores data and runs work |

**Use your router's network, not necessarily these numbers.** Find it on any node:

```bash
ip route | grep default
```

If it prints `default via 192.168.1.1 ...`, your network is `192.168.1.x`: use `192.168.1.100` to `192.168.1.104` and gateway `192.168.1.1` everywhere this guide says `192.168.0.x`. Also pick addresses your router doesn't hand out to other devices (outside its DHCP range, which its admin page shows).

The hostnames were set when you flashed the cards ([Install OS](Install_OS.md)). Check with `hostname` on each node.


# Give each node a fixed address

Hadoop and Spark find nodes by name, and the names below map to fixed addresses. If a node's address changed after a reboot, the cluster would lose it. Pick **one** of these two options.


## Option A: reserve addresses on your router (recommended)

Nothing to change on the Pis, and it survives reflashing a card.

1. Find each node's hardware (MAC) address:

    ```bash
    cat /sys/class/net/eth0/address
    ```

2. In your router's admin page, look for *DHCP reservation*, *static lease* or *address reservation*, and assign each MAC address the IP from the table.
3. Reboot the Pis: `sudo reboot`.

**Check:** `ip -4 addr show eth0` on each node shows its address from the table.


## Option B: set a static address on each Pi

Current Raspberry Pi OS manages the network with NetworkManager, so use `nmcli`. Editing `/etc/dhcpcd.conf`, as older guides say, has no effect anymore.

Run on each node, with that node's address from the table. The first line finds the name of the wired connection, which differs between OS versions:

```bash
CON="$(nmcli -g NAME,DEVICE connection show --active | awk -F: '$2=="eth0"{print $1}')"
sudo nmcli connection modify "$CON" \
  ipv4.method manual \
  ipv4.addresses 192.168.0.101/24 \
  ipv4.gateway 192.168.0.1 \
  ipv4.dns 192.168.0.1
sudo nmcli connection up "$CON"
```

`/24` matches a subnet mask of `255.255.255.0`, which home routers use. The gateway and DNS server are your router.

If you're logged in over SSH, your session freezes when the address changes. Close it and log in again with the new address.

**Check:** reboot, then `ip -4 addr show eth0` shows the new address and `ping -c 3 raspberrypi.com` gets replies.


# Mapping the hostname

Every node needs the same table of names and addresses, so `master` can reach `worker3` by name and the other way around. It lives in `/etc/hosts`.

Current Raspberry Pi OS rebuilds `/etc/hosts` from a template at every boot, so edits made only to `/etc/hosts` disappear after a reboot. The file also maps each node's own name to `127.0.1.1`, which would make Hadoop listen only to itself. [`scripts/setup_hosts.sh`](../scripts/setup_hosts.sh) handles both: it writes the block below to `/etc/hosts` and to the template, and removes the `127.0.1.1` line.

```
# pi-cluster network
192.168.0.100    master
192.168.0.101    worker1
192.168.0.102    worker2
192.168.0.103    worker3
192.168.0.104    worker4
# end pi-cluster network
```

Keep the first and last comment lines exactly as written: the [cluster commands](Cluster_Commands.md) use them to find the node list.

1. On your computer, download the script and edit the addresses at its top if your network differs:

    ```bash
    curl -fsSLO https://raw.githubusercontent.com/gitluis/pi-cluster/master/scripts/setup_hosts.sh
    ```

2. Copy it to every node and run it there (you'll be asked for your password for `sudo` on each):

    ```bash
    for h in master worker1 worker2 worker3 worker4; do
      scp setup_hosts.sh alice@$h.local: && ssh -t alice@$h.local 'sudo bash setup_hosts.sh'
    done
    ```

    If `.local` names don't work on your network, run it once per node with its IP address instead of `$h.local`.

**Check:** on any node, `getent hosts worker3` prints `192.168.0.103 worker3`, and `ping -c 1 master` replies from `192.168.0.100`. Reboot one node and check again: the block must still be there.


# SSH keys from master to every node

Imager already installed your computer's key on every node. `master` needs its own key on every node too, because Hadoop and Spark start their services on the workers by logging in from `master` over SSH. That includes `master` itself.

Your nodes accept keys only, not passwords, so `ssh-copy-id` from `master` won't work. Copy the key through your computer, which can already log in everywhere.

1. Make a key on `master`, without a passphrase so services can start unattended:

    ```bash
    ssh alice@master.local 'ssh-keygen -t ed25519 -N "" -f ~/.ssh/id_ed25519'
    ```

2. From your computer, add `master`'s public key to every node, `master` included:

    ```bash
    KEY="$(ssh alice@master.local 'cat ~/.ssh/id_ed25519.pub')"
    for h in master worker1 worker2 worker3 worker4; do
      ssh alice@$h.local "grep -qxF '$KEY' ~/.ssh/authorized_keys || echo '$KEY' >> ~/.ssh/authorized_keys"
    done
    ```

3. On `master`, connect to every node once so it records their fingerprints:

    ```bash
    for h in master worker1 worker2 worker3 worker4; do
      ssh -o StrictHostKeyChecking=accept-new $h hostname
    done
    ```

**Check:** step 3 prints all five hostnames without asking for a password or confirmation.

The private key `~/.ssh/id_ed25519` on `master` lets anyone who has it into every node. Never copy or share it; only the `.pub` file goes to other machines.

---

**Step 3 of 9** · ← Step 2: [Install OS](Install_OS.md) · Step 4: [Cluster Commands](Cluster_Commands.md) →
