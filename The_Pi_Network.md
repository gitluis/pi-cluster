[Background](Background.md) / [Purpose](Purpose.md) / [Getting Started](Getting_Started.md) / [Cluster Guide](Cluster_Guide.md)


<img src="https://image.flaticon.com/icons/svg/2004/2004693.svg" width="100px" height="100px"/>


# The Pi Network

The so called [Local Area Network (LAN)](https://www.howtogeek.com/353283/what-is-a-local-area-network-lan/). In order for the cluster to communicate, we need to set up a LAN switch so that each Pi board knows where to send and receive data, commands, and output results.

* [Network Lookup Table](#network-lookup-table)
* [Assign a static IP address](#assign-a-static-ip-address)
* [Change Hostname](#change-hostname)
    * [Rename the hostname](#rename-the-hostname)
    * [Mapping the hostname](#mapping-the-hostname)
    * [Reboot the Pi](#reboot-the-pi)
* [Enable Secure Shell (SSH)](#enable-secure-shell-ssh)
    * [Enable SSH](#enable-ssh)
        * [Enable via Terminal](#enable-via-terminal)
        * [Enable via Desktop](#enable-via-desktop)
        * [Enable via raspi-config](#enable-via-raspi-config)
    * [Start SSH](#start-ssh)
* [Remote Log-in](#remote-log-in)
    * [Generate SSH Keys](#generate-ssh-keys)
        * [How to Generate Keys](#how-to-generate-keys)
    * [Setup Cluster Keys](#setup-cluster-keys)

# Network Lookup Table

Let's enumerate each Pi and outline the network configuration for reference.

| Pi Number | Interface | IP Address    | Hostname |
|:---------:|:----------|:--------------|:---------|
|     0     | eth0      | 192.168.0.100 | master   |
|     1     | eth0      | 192.168.0.101 | worker1  |
|     2     | eth0      | 192.168.0.102 | worker2  |
|     3     | eth0      | 192.168.0.103 | worker3  |
|     4     | eth0      | 192.168.0.104 | worker4  |

You guessed right! There is a "master" node that will oversee and control the cluster while each "worker" executes whatever command the master issued.


# Assign a static IP address

To facilitate communication between the cluster, let's assign a static local IP address to each Raspberry Pi board in the network switch.

Edit file `/etc/dhcpcd.conf`
```cli
sudo nano /etc/dhcpcd.conf
```

Uncomment the following lines and add `X`
```conf
interface eth0
static ip_address=192.168.0.10X/24
```
Where `X` represents the Pi Number in the [Network Lookup Table](#network-lookup-table).

**Reminder**: You have to edit this file manually on each Raspberry Pi.


# Change Hostname

Raspbian by default, sets the `hostname` of each Pi to `raspberrypi`. Such hostname is not mapped to the IP address given it can change via DHCP but since we assigned a static IP address we can map it. Mapping the hostname to the static IP will ease communication between the network.


## Rename the hostname

By changing the hostname to `master` and `workerX` you will be able to distinguish between the nodes.

Edit file `/etc/hostname` and replace `raspberrypi` with each the Pi's hostname
```cli
sudo nano /etc/hostname
```

Each Pi's hostname is specified in the [Network Lookup Table](#network-lookup-table).

**Reminder**: You have to change the hostname manually on each Raspberry Pi.


## Mapping the hostname

All of your Raspberry Pi's must have each of their IP addresses mapped to their hostnames in the `/etc/hosts` file so that each Pi can fully communicate with each other.

Edit file `/etc/hosts` and add the following:
```
# pi-cluster network
192.168.0.100    master
192.168.0.101    worker1
192.168.0.102    worker2
192.168.0.103    worker3
192.168.0.104    worker4
```

Reboot system for changes to take effect
```cli
shutdown -r now
```

**Reminder**: You have to do this manually on each Raspberry Pi.


# Enable Secure Shell (SSH)

SSH is a network protocol for operating network services **securely** such as log into a remote computer, execute commands, tunneling, forwarding TCP ports and transfer files (via secure copy or scp).

We need SSH for each Pi to communicate with each other and be able to execute commands coming from the Master node.


## Enable SSH

SSH is disabled by default as of latest Raspbian versions. Thus, we need to enable it but first, you must change your default password.

To change your default password, simply open a terminal window, type in `passwd`, press enter and follow the prompts. We suggest something easy while configuring the cluster, we will discuss [Cluster Security](Cluster_Security.md) measurements later.


### Enable via Terminal

Open a terminal window and type in
```cli
sudo systemctl enable ssh
```


### Enable via Desktop

1. Go to `Preferences` menu and open `Raspberry Pi Configuration`
1. Head over to the `Interfaces` tab
1. Select `Enabled` right next to `SSH`
1. Click `OK`
1. Start the service


### Enable via `raspi-config`

1. Open a terminal window and type in `sudo raspi-config`
1. Select `Interfacing Options`
1. Navigate to `SSH` and select it
1. Choose `Yes`
1. Select `Ok`
1. Choose `Finish`


## Start SSH

To start up the SSH service, run the following command
```cli
sudo systemctl start ssh
```


# Remote Log-in

With the `hostname` mapped to each IP address on each Pi and SSH enabled, remote login becomes easier
```cli
ssh pi@worker3
```

If that is your first time remotely logging in to `worker3`, it will ask you if you trust the destination, type in `yes` and press enter.

The **problem** here is that every time you log in remotely to any other Pi, it will ask you for that Pi's password.


## Generate SSH Keys

To avoid typing in the password of the computer we're trying to remotely log in to, we create what is called **private** and **public** key-pairs.

The private key is solely for the computer in which the key is being generated (**not to be shared**) while the public key can be shared among other computers for these to be able to securely login remotely without entering a password.


### How to Generate Keys

To generate private/public keys, run this command
```cli
ssh-keygen -t ed25519
```

Press Enter three (3) times.

That will generate a private and public key-pair within the `~/.ssh` hidden directory. The private key is stored in file `~/.ssh/id_ed25519` and the public key is in file `~/.ssh/id_ed25519.pub`. **DO NOT modify or share the private key file!**


## Setup Cluster Keys

1. Login to master node and generate keys for it
```cli
ssh-keygen -t ed25519
```

Press Enter three (3) times.

2. Append master's public key to its own SSH authorized keys file
```cli
cat ~/.ssh/id_ed22519.pub >> ~/.ssh/authorized_keys
```

3. Login to worker `X` node and generate keys for it
```cli
ssh-keygen -t ed25519
```

Press Enter three (3) times.

4. Append worker `X`'s public key to the master's SSH authorized keys file
```cli
cat ~/.ssh/id_ed22519.pub | ssh pi@master 'cat >> ~/.ssh/authorized_keys'
```

Enter the `master`'s password if prompted.

**Note:** If the destination username (master's username) is different from `pi`, change it accordingly in the command above.

5. Repeat steps 3-4 for each worker specified in the [Network Lookup Table](#network-lookup-table)
6. Login to master node
6. Overwrite the master's SSH authorized keys file to each worker `X`
```cli
scp ~/.ssh/authorized_keys pi@workerX:~/.ssh/authorized_keys
```

Where `X` represents the Pi Number in the [Network Lookup Table](#network-lookup-table).

**Note:** If the destination username (master's username) is different from `pi`, change it accordingly in the command above.

7. Repeat step 6 for each worker specified in the [Network Lookup Table](#network-lookup-table)
8. Done

You should now be able to log in remotely to any Pi on the network from any other Pi.
