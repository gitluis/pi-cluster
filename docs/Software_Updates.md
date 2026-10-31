[Home](../README.md) · [Cluster Guide](Cluster_Guide.md) · [Troubleshooting](Troubleshooting.md)


<img src="img/icons/updates.svg" width="96" height="96" alt=""/>


# Software Updates

**Goal:** keep the OS, packages and firmware on every node current and identical.

**Run on:** `master`, using the [cluster commands](Cluster_Commands.md). Before those are set up, run the same commands on each node over SSH.

The nodes need internet access through your router.


## Update packages

```bash
cluster-cmd sudo apt update
cluster-cmd sudo apt full-upgrade -y
```

`apt update` refreshes the list of available packages; `full-upgrade` installs the new versions. Updating all nodes at the same time keeps their software versions identical, which Hadoop and Spark expect.

Then reboot any node that needs it:

```bash
cluster-cmd 'test -f /run/reboot-required && echo "reboot needed" || echo "ok"'
cluster-reboot
```


## Update firmware

The Raspberry Pi 4 and Pi 5 keep their bootloader in a small chip on the board (the EEPROM). Check whether an update is available:

```bash
cluster-cmd sudo rpi-eeprom-update
```

If any node reports an update, apply it and reboot:

```bash
cluster-cmd sudo rpi-eeprom-update -a
cluster-reboot
```


## When to update

- Before installing Hadoop or Spark.
- Every month or so afterwards, when no job is running.
- Stop HDFS and Spark first (see [Cluster Setup](Cluster_Setup.md#start-and-stop-the-cluster)), so a reboot doesn't interrupt a job.

---

Back to the [Cluster Guide](Cluster_Guide.md)
