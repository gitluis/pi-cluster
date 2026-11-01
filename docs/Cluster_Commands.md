[Home](../README.md) · [Getting Started](Getting_Started.md) · [Cluster Guide](Cluster_Guide.md) · [Troubleshooting](Troubleshooting.md) · [About](About.md)


<img src="img/icons/cluster-commands.svg" width="96" height="96" alt=""/>


# Cluster Commands

**Goal:** run a command, copy a file, or reboot every node with one command from `master`.

**Run on:** `master` (the script is then copied to the workers).

These are shell functions defined in [`scripts/cluster_commands.sh`](../scripts/cluster_commands.sh). Many thanks to [Andrew and his guide](https://dev.to/awwsmm/building-a-raspberry-pi-hadoop-spark-cluster-8b2) for the idea.

They read the node list from the `# pi-cluster network` block in `/etc/hosts`, so finish [The Pi Network](The_Pi_Network.md#mapping-the-hostname) first. SSH keys must also be set up, because the functions log in to each worker without a password.

* [Install the commands](#install-the-commands)
* [Command reference](#command-reference)
* [Clock sync](#clock-sync)


# Install the commands

1. Back up your `~/.bashrc` in case you need to undo this:

    ```bash
    cp ~/.bashrc ~/.bashrc.bak
    ```

2. Download the script into a hidden `~/.scripts` folder:

    ```bash
    mkdir -p ~/.scripts
    wget -O ~/.scripts/cluster_commands.sh \
      https://raw.githubusercontent.com/gitluis/pi-cluster/master/scripts/cluster_commands.sh
    ```

3. Load it from `~/.bashrc` and reload your shell:

    ```bash
    printf '\n# pi-cluster commands\nsource ~/.scripts/cluster_commands.sh\n' >> ~/.bashrc
    source ~/.bashrc
    ```

4. Copy the script and the updated `~/.bashrc` to every worker:

    ```bash
    cluster-scp ~/.scripts
    cluster-scp ~/.bashrc
    ```

**Check:** `workers` lists `worker1` to `worker4`, each once.

To undo, run `cp ~/.bashrc.bak ~/.bashrc` and `source ~/.bashrc`.


# Command reference

| Command | What it does |
| --- | --- |
| `cluster-user` | Print the user the commands log in as (your own username by default) |
| `nodes` | Print the IP address and hostname of every node |
| `workers` | Print only the worker hostnames |
| `nodes-up` | Ping every node and report `up` or `DOWN` |
| `master-cmd <command>` | Run a command on every worker, not on `master` |
| `cluster-cmd <command>` | Run a command on every worker, then on `master` |
| `cluster-scp <path> [dest]` | Copy a file or folder to the same path on every worker |
| `cluster-reboot` | Reboot all nodes, `master` last |
| `cluster-shutdown` | Shut down all nodes, `master` last |

The commands log in as your own user. To use a different user, set `CLUSTER_USER` before the `source` line in `~/.bashrc`, for example `CLUSTER_USER=alice`. The variable is deliberately not called `USER`, which is a standard shell variable that other programs read.


## `nodes`

```console
$ nodes
192.168.0.100	master
192.168.0.101	worker1
192.168.0.102	worker2
192.168.0.103	worker3
192.168.0.104	worker4
```


## `workers`

```console
$ workers
worker1
worker2
worker3
worker4
```


## `nodes-up`

```console
$ nodes-up
master: up
worker1: up
worker2: up
worker3: DOWN
worker4: up
```

Each node gets one ping with a 2-second timeout. `DOWN` means no reply: the node is off, still booting, or not on the network.


## `master-cmd` and `cluster-cmd`

```console
$ cluster-cmd date
==> worker1: date
Fri 30 Oct 2026 08:31:47 PM AST
==> worker2: date
Fri 30 Oct 2026 08:31:47 PM AST
==> worker3: date
Fri 30 Oct 2026 08:31:48 PM AST
==> worker4: date
Fri 30 Oct 2026 08:31:48 PM AST
==> master: date
Fri 30 Oct 2026 08:31:48 PM AST
```

Use `master-cmd` when only the workers should run something, and `cluster-cmd` when every node should.

Quote commands that contain pipes, redirects or `;`, so they run on each node instead of on `master`:

```bash
cluster-cmd 'df -h / | tail -1'
```

`cluster-cmd` runs on the workers first and on `master` last. That order matters for `reboot` and `shutdown`: if `master` went first, it would turn off before it could reach the workers.

If a worker is down or refuses the login, you see a `!! worker3: command failed` line and the loop moves on to the next worker after 5 seconds, instead of hanging.


## `cluster-scp`

```console
$ cluster-scp ~/.bashrc
==> worker1: /home/alice/.bashrc -> /home/alice/.bashrc
==> worker2: /home/alice/.bashrc -> /home/alice/.bashrc
==> worker3: /home/alice/.bashrc -> /home/alice/.bashrc
==> worker4: /home/alice/.bashrc -> /home/alice/.bashrc
```

With one argument, the file lands at the same path on every worker and overwrites what is there. A folder is copied with its contents, so `cluster-scp ~/.scripts` creates or updates `~/.scripts` on each worker. Give a second argument to choose a different destination, for example `cluster-scp data.csv /tmp/`.

`cluster-scpr` still works as an alias of `cluster-scp`, for older notes that use it.


## `cluster-reboot` and `cluster-shutdown`

```bash
cluster-reboot
cluster-shutdown
```

These run `sudo shutdown` over SSH, which only works if your user can use `sudo` without typing a password. Check on any node:

```bash
sudo -n true && echo "passwordless sudo: yes"
```

If it prints nothing, see [Cluster Security](Cluster_Security.md#allow-cluster-reboot-without-a-password) for a narrow rule that allows only `shutdown`.


# Clock sync

Nodes must agree on the time: logs, scheduled jobs and HDFS all compare timestamps across nodes. Raspberry Pi OS already syncs the clock over the internet with `systemd-timesyncd`, so normally there is nothing to install.

Check every node:

```bash
cluster-cmd timedatectl show -p NTPSynchronized --value
```

Each node should print `yes`. Set the same time zone everywhere too, for example:

```bash
cluster-cmd sudo timedatectl set-timezone America/Puerto_Rico
```

If a node prints `no`, it usually can't reach the internet. Fix its network first ([The Pi Network](The_Pi_Network.md)), then check again with `timedatectl timesync-status`.

---

**Step 4 of 9** · ← Step 3: [The Pi Network](The_Pi_Network.md) · Step 5: [Cluster Security](Cluster_Security.md) →
