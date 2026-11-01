[Home](../README.md) · [About](About.md) · [Getting Started](Getting_Started.md) · [Cluster Guide](Cluster_Guide.md) · [Troubleshooting](Troubleshooting.md)


<img src="img/icons/security.svg" width="96" height="96" alt=""/>


# Cluster Security

**Goal:** only you can log in to the nodes, failed login attempts get blocked, and each node accepts network traffic only from the cluster and your computer.

**Run on:** `master`, using the [cluster commands](Cluster_Commands.md), unless a step says otherwise.

Do the steps **in order**. Two of them can lock you out of a node if done early, and each step says how to check it before moving on. If you're ever locked out of a node with no monitor, put its card in your computer, reflash it with [Install OS](Install_OS.md), and repeat the setup for that node.

* [What Imager already did](#what-imager-already-did)
* [Allow cluster-reboot without a password](#allow-cluster-reboot-without-a-password)
* [Turn off password logins](#turn-off-password-logins)
* [Block repeated failed logins with fail2ban](#block-repeated-failed-logins-with-fail2ban)
* [Firewall](#firewall)
* [Old installs with a `pi` user](#old-installs-with-a-pi-user)


# What Imager already did

If you flashed the cards as described in [Install OS](Install_OS.md), each node already has:

- **No default user.** Your own username replaces the old `pi`/`raspberry` pair that attackers try first.
- **A strong password**, still needed for `sudo`. Use a real password, not an easy one: it protects every administrative command.
- **Key-only SSH**, if you chose public-key authentication.

**Check** that password logins over SSH are off on every node:

```bash
cluster-cmd 'sudo sshd -T | grep -E "^(passwordauthentication|kbdinteractiveauthentication) "'
```

Each node should print `passwordauthentication no` and `kbdinteractiveauthentication no`. If any prints `yes`, do [Turn off password logins](#turn-off-password-logins).


# Allow cluster-reboot without a password

`cluster-reboot` and `cluster-shutdown` run `sudo shutdown` on each node over SSH, where nobody can type a password. Check whether your user already has passwordless `sudo`:

```bash
cluster-cmd 'sudo -n true 2>/dev/null && echo "passwordless sudo" || echo "password required"'
```

If nodes print `password required`, allow passwordless `sudo` for `shutdown` only. Run this on each node over SSH (`ssh -t worker1`), since `sudo` asks for your password this one time:

```bash
echo "$USER ALL=(root) NOPASSWD: /usr/sbin/shutdown" | sudo tee /etc/sudoers.d/010-cluster-shutdown
sudo chmod 440 /etc/sudoers.d/010-cluster-shutdown
sudo visudo -c
```

`visudo -c` must print `parsed OK` for every file. A broken sudoers file can block `sudo` entirely; if it reports an error, remove the file with `sudo rm /etc/sudoers.d/010-cluster-shutdown` before closing your session.

If nodes print `passwordless sudo`, your user can run anything as root without a password, which the rest of this guide relies on for `cluster-cmd sudo ...`. That's convenient on a home network. To tighten it later, remove the rule in `/etc/sudoers.d/` that grants it and add the `shutdown` rule above.


# Turn off password logins

Skip this if the check in [What Imager already did](#what-imager-already-did) printed `no` on every node.

1. **Make sure key login works first.** From your computer, in a new terminal, run `ssh alice@worker1.local` for every node. Each must log you in **without** asking for a password. If one asks, fix its keys ([The Pi Network](The_Pi_Network.md#ssh-keys-from-master-to-every-node)) before going on.

2. Add a small settings file instead of editing the main SSH configuration, then check it and restart SSH:

    ```bash
    cluster-cmd "printf 'PasswordAuthentication no\nKbdInteractiveAuthentication no\n' | sudo tee /etc/ssh/sshd_config.d/10-cluster.conf"
    cluster-cmd 'sudo sshd -t && sudo systemctl restart ssh'
    ```

    `sshd -t` checks the settings and only lets the restart happen if they're valid. Restarting SSH doesn't end sessions that are already open.

3. **Check** with the command in [What Imager already did](#what-imager-already-did), then open a new SSH session from your computer to confirm you still get in.

Older guides also set `ChallengeResponseAuthentication no` (renamed `KbdInteractiveAuthentication` in OpenSSH 8.7) and `UsePAM no`. Leave `UsePAM` alone: turning it off breaks parts of the login process on Debian and adds no protection here.


# Block repeated failed logins with fail2ban

[fail2ban](https://github.com/fail2ban/fail2ban) watches the login log and blocks addresses that fail to log in several times. With key-only SSH on a home network it's a second layer, not a necessity; it matters most if a node is ever reachable from the internet.

1. Install it on every node:

    ```bash
    cluster-cmd sudo apt install -y fail2ban python3-systemd
    ```

2. Write the settings for the SSH jail. Current Raspberry Pi OS keeps logs in the systemd journal instead of `/var/log/auth.log`, so fail2ban must read the journal (`backend = systemd`):

    ```bash
    cluster-cmd "printf '[sshd]\nenabled  = true\nbackend  = systemd\nmaxretry = 4\nfindtime = 10m\nbantime  = 1h\nignoreip = 127.0.0.1/8 ::1 192.168.0.0/24\n' | sudo tee /etc/fail2ban/jail.d/sshd.local"
    cluster-cmd 'sudo systemctl enable --now fail2ban && sudo systemctl restart fail2ban'
    ```

    | Setting | Meaning |
    | --- | --- |
    | `maxretry = 4`, `findtime = 10m` | Block an address after 4 failed logins within 10 minutes |
    | `bantime = 1h` | Unblock it after 1 hour. Avoid `-1` (forever): a few typos would lock out your own computer for good |
    | `ignoreip` | Never block the cluster's own network. Change `192.168.0.0/24` to yours |

**Check:**

```bash
cluster-cmd 'sudo fail2ban-client status sshd | head -4'
```

Each node prints `Status for the jail: sshd`. To unblock an address early: `sudo fail2ban-client set sshd unbanip <address>`.


# Firewall

A firewall drops network traffic you didn't allow. [ufw](https://help.ubuntu.com/community/UFW) (Uncomplicated Firewall) makes the rules easy to write.

**Order matters:** if you turn the firewall on before allowing SSH, it cuts off your session and every new one. The rules below allow the cluster's network first.

Hadoop and Spark talk between nodes on many ports, some chosen at random. Rather than list them all, allow everything from the cluster's own network, and rate-limit SSH from anywhere else.

1. **Try it on one worker first.** On `master`:

    ```bash
    ssh worker1 'sudo apt install -y ufw && sudo ufw default deny incoming && sudo ufw default allow outgoing && sudo ufw allow from 192.168.0.0/24 && sudo ufw limit ssh && sudo ufw --force enable'
    ```

    Replace `192.168.0.0/24` with your network.

2. **Check** that you can still log in to `worker1` from `master` and from your computer, and that `ssh worker1 sudo ufw status verbose` lists the rules:

    ```
    Status: active
    Logging: on (low)
    Default: deny (incoming), allow (outgoing), disabled (routed)
    New profiles: skip

    To                         Action      From
    --                         ------      ----
    Anywhere                   ALLOW IN    192.168.0.0/24
    22/tcp                     LIMIT IN    Anywhere
    22/tcp (v6)                LIMIT IN    Anywhere (v6)
    ```

3. Then do every node:

    ```bash
    cluster-cmd 'sudo apt install -y ufw && sudo ufw default deny incoming && sudo ufw default allow outgoing && sudo ufw allow from 192.168.0.0/24 && sudo ufw limit ssh && sudo ufw --force enable'
    ```

`ufw limit ssh` blocks an address that opens 6 or more SSH connections within 30 seconds. SSH uses TCP only, so there's no need for a UDP rule. If your computer is on a different network from the cluster, add a rule for it before enabling, such as `sudo ufw allow from 192.168.50.0/24 to any port 22 proto tcp`.

To block one address: `sudo ufw deny from 192.168.0.250`. To turn the firewall off while troubleshooting: `sudo ufw disable`.


# Old installs with a `pi` user

Cards flashed before April 2022, or set up with the username `pi`, still have that well-known user. Replace it with your own on each such node. Stay logged in as `pi` in one session the whole time, so you can undo anything.

1. Create the new user and give it the same groups `pi` had:

    ```bash
    sudo adduser alice
    for g in $(id -Gn pi); do [ "$g" != pi ] && sudo usermod -aG "$g" alice; done
    ```

2. Copy your SSH keys to it:

    ```bash
    sudo mkdir -p /home/alice/.ssh
    sudo cp ~/.ssh/authorized_keys /home/alice/.ssh/
    sudo chown -R alice:alice /home/alice/.ssh
    sudo chmod 700 /home/alice/.ssh
    ```

3. **Check** from your computer, in a new terminal: `ssh alice@<node>` logs in without a password, and `sudo -v` there accepts the new user's password.

4. From that `alice` session, remove `pi`:

    ```bash
    sudo pkill -u pi
    sudo deluser --remove-home pi
    ```

    Move anything you need out of `/home/pi` first.

Repeat on every node, then redo [SSH keys from master](The_Pi_Network.md#ssh-keys-from-master-to-every-node) as `alice` and set `CLUSTER_USER=alice` if your [cluster commands](Cluster_Commands.md) were set up under `pi`.


Resources:
* [Securing your Raspberry Pi](https://www.raspberrypi.com/documentation/computers/configuration.html)
* [UFW on Ubuntu's community wiki](https://help.ubuntu.com/community/UFW)

---

**Step 5 of 9** · ← Step 4: [Cluster Commands](Cluster_Commands.md) · Step 6: [Single Node Setup](Single_Node_Setup.md) →
