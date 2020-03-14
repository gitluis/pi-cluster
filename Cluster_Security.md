[Background](Background.md) / [Purpose](Purpose.md) / [Getting Started](Getting_Started.md) / [Cluster Guide](Cluster_Guide.md)


<img src="https://image.flaticon.com/icons/svg/719/719184.svg" width="100px" height="100px"/>


# Cluster Security

"The security of your Raspberry Pi is important. Gaps in security leave your Raspberry Pi open to hackers who can then use it without your permission." - [The Raspberry Pi Foundation](https://www.raspberrypi.org/documentation/configuration/security.md)

Here we take some extra-security measurements for our cluster to avoid any suspicious or unknown incoming traffic to our cluster and keep our cluster secured.

* [Change Pi default password](#change-pi-default-password)
* [Change default username](#change-default-username)
    * [Add new user](#add-new-user)
    * [Remove `pi` user](#remove-pi-user)
    * [Edit cluster commands!](#edit-cluster-commands)
* [Key-based Authentication](#key-based-authentication)
    * [Disable Password Login](#disable-password-login)
* [Install `fail2ban`](#install-fail2ban)
* [Install Uncomplicated Firewall](#install-uncomplicated-firewall)



# Change Pi default password

The default password is `raspberry`.

Keep in mind you have a cluster, meaning more than one Raspberry Pi. Our recommendation is to construct something easy you will not forget as your password for each node. We will setup [key-based authentication](#key-based-authentication) later, thus your password may not need to be strong.

Open a new terminal window (`Ctrl+Alt+T`)
```cli
passwd
```

Follow the prompts.

**Reminder:** You will have to do this manually on each Raspberry Pi.


# Change default username

The default username is `pi`. You add another security layer to your Raspberry Pi by changing the default username so that nobody knows your username.

**Note(s):**
1. Although `root` is a user, you cannot login as `root` to your Raspberry Pi. That is why the user `pi` must use `sudo` or `su -` to perform commands with administrative privileges.
2. You will have to change the username manually on each Raspberry Pi.

## Add new user

Add new user
```cli
sudo adduser alice
```

Add new user to the `sudo` group
```cli
sudo usermod -a -G adm,dialout,cdrom,sudo,audio,video,plugdev,games,users,input,netdev,gpio,i2c,spi alice
```

Verify user belongs to the `sudo` group
```cli
sudo su - alice
```

If you are now `root`, then `alice` belongs to the `sudo` group, as expected.

A new home directory for `alice` will be created at `/home/alice`.


## Remove `pi` user

Close the `pi` process
```cli
sudo pkill -u pi
```

Delete `pi` user
```cli
sudo deluser -remove-home pi
```

**Note:** If you have data in `/home/pi/` make sure to move it somewhere else before running the command above.


## Edit cluster commands

**NOT TESTED YET!!!**

Remember that our [Cluster Commands](Cluster-Commands) were all constructed based on a `pi` user. Therefore, if you created a new user `alice`, you need to perform the steps below.

Steps:
1. [Add new user](#add-new-user) `alice` in each node to ensure the same user exists across the cluster
2. [Setup Cluster Keys](The_Pi_Network.md#setup-cluster-keys) for all nodes logged in as `alice`
3. [Add commands to `~/.bashrc`](Cluster_Commands.md#add-commands-to-bashrc) in the master node
4. Edit `cluster_commands.sh`
```cli
nano ~/.scripts/cluster_commands.sh
```

5. Replace `USER="pi"` with `USER="alice"` and save the file
6. Copy over work done to all workers
```cli
cluster-scp ~/.bashrc
cluster-scpr ~/.scripts/
cluster-cmd source ~/.bashrc
```

Having these commands under the user's `home` directory (`/home/<user>`) is very useful because it allows you to have multiple users in your cluster all with keys separated from each other and still provides full communication between the nodes and their users. Same applies with cluster commands, each user may have their own defined commands.


# Key-based Authentication

We learned about SSH Keys in section [Generate SSH Keys](The_Pi_Network.md#generate-ssh-keys).

Since we have already created keys for each node in the cluster and they can communicate with each other we simply need to enforce authentication through key-pairs only.


## Disable Password Login

Edit `/etc/ssh/sshd_config` file
```cli
sudo nano /etc/ssh/sshd_config
```

Modify the following lines to `no`
```text
ChallengeResponseAuthentication no
PasswordAuthentication no
UsePAM no
```

Reboot the Pi
```cli
shutdown -r now
```


# Install `fail2ban`

"If you are using your Raspberry Pi as some sort of server, for example an `ssh` or a webserver, your firewall will have deliberate 'holes' in it to let the server traffic through. In these cases, [Fail2ban](www.fail2ban.org) can be useful. Fail2ban, written in Python, is a scanner that examines the log files produced by the Raspberry Pi, and checks them for suspicious activity. It catches things like multiple brute-force attempts to log in, and can inform any installed firewall to stop further login attempts from suspicious IP addresses. It saves you having to manually check log files for intrusion attempts and then update the firewall (via `iptables`) to prevent them." - [The Raspberry Pi Foundation](https://www.raspberrypi.org/documentation/configuration/security.md)

Install fail2ban
```cli
sudo apt install fail2ban
```

Enable fail2ban and take a look at rules for SSH
```cli
sudo /etc/fail2ban/jail.conf /etc/fail2ban/jail.local
sudo nano /etc/fail2ban/jail.local
```

Look for section named `[ssh]` that look as follows
```configuration
[ssh]
enabled  = true
port     = ssh
filter   = sshd
logpath  = /var/log/auth.log
maxretry = 6
```

This section let's you know that `fail2ban` will examine the SSH port, filter it using `/etc/fail2ban/filter.d/sshd.conf` parameters, parse `/var/log/auth.log` for malicious activity and allow 6 connection attempt retries before detection threshold is reached.

The default ban action is
```configuration
# Default banning action (e.g. iptables, iptables-new,
# iptables-multiport, shorewall, etc) It is used to define
# action_* variables. Can be overridden globally or per
# section within jail.local file
banaction = iptables-multiport
```

`iptables-multiport` means that the Fail2ban system will run the `/etc/fail2ban/action.d/iptables-multiport.conf` file when the detection threshold is reached.

To permanently ban an IP address after 4 failed attempts, change `bantime` to -1
```configuration
[ssh]
enabled  = true
port     = ssh
filter   = sshd
logpath  = /var/log/auth.log
maxretry = 4
bantime = -1
```

You can find more on Fail2Ban at [this tutorial](https://www.digitalocean.com/community/tutorials/how-fail2ban-works-to-protect-services-on-a-linux-server).


## Install Uncomplicated Firewall

If your cluster will continuously be exposed (connected) to the Internet, you will need to setup [fail2ban](#install-fail2ban) previously discussed along with firewall.

A firewall is a software that provides network security by filtering incoming and outgoing network traffic (packets) based on user-defined rules. The idea is to reduce unwanted network traffic while allowing legitimate communication.

We can use [ufw](https://www.linux.com/tutorials/introduction-uncomplicated-firewall-ufw/) which is the default firewall tool in Ubuntu.

Install the firewall
```cli
sudo apt install ufw
```

To enable the firewall, use
```cli
sudo ufw enable
```

To disable the firewall, use
```cli
sudo ufw disable
```

To list the firewall current settings
```cli
sudo ufw status
```

To limit login attempts on SSH port (22) using TCP
```cli
sudo ufw limit ssh/tcp
```

To limit login attempts on SSH port (22) using UDP
```cli
sudo ufw limit ssh/udp
```

The last two configurations denies connection if an IP address has attempted to connect six or more times in the last 30 seconds.

Deny access to port 30 from IP address 192.168.2.1
```cli
sudo ufw deny from 192.168.2.1 port 30
```

Resources:
* [Securing your Raspberry Pi](https://www.raspberrypi.org/documentation/configuration/security.md)
* [An Introduction to Uncomplicated Firewall](https://www.linux.com/tutorials/introduction-uncomplicated-firewall-ufw/)
