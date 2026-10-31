[Home](../README.md) · [Cluster Guide](Cluster_Guide.md) · [Troubleshooting](Troubleshooting.md)


<img src="img/icons/troubleshooting.svg" width="96" height="96" alt=""/>


# Troubleshooting

Find the symptom, then try the fix. Most problems show up in a log: Hadoop's are in `/opt/hadoop/logs/` and Spark's in `/opt/spark/logs/`, on the node where the service runs.

* [Logging in and the network](#logging-in-and-the-network)
* [Power and heat](#power-and-heat)
* [HDFS](#hdfs)
* [Spark and the workload](#spark-and-the-workload)


# Logging in and the network

| Symptom | Likely cause | Fix |
| --- | --- | --- |
| `WARNING: REMOTE HOST IDENTIFICATION HAS CHANGED!` | The card was reflashed, so the node has new SSH host keys | On the computer that warns: `ssh-keygen -R worker1`, plus `ssh-keygen -R worker1.local` and the IP if you used those, then connect again |
| `ssh: Could not resolve hostname master.local` | Your network or computer doesn't support `.local` names | Use the node's IP address from your router's device list |
| `Permission denied (publickey)` | Your key isn't on that node | Redo [SSH keys from master](The_Pi_Network.md#ssh-keys-from-master-to-every-node), or reflash with your key in Imager |
| `nodes-up` shows a node `DOWN` | Off, still booting, cable or switch port problem, or a changed IP address | Check the Pi's green light and the switch port light; find its address in the router; [Give each node a fixed address](The_Pi_Network.md#give-each-node-a-fixed-address) |
| `sudo: unable to resolve host worker2` | The node's name is missing from the hosts block | Check `hostname`, then run [`setup_hosts.sh`](The_Pi_Network.md#mapping-the-hostname) again on that node |
| The hosts block disappears after a reboot | Only `/etc/hosts` was edited, and cloud-init rebuilt it from its template | Run `setup_hosts.sh`, which also updates the template |
| `cluster-cmd` prints `!! worker3: command failed` | The command failed there, or SSH couldn't connect within 5 seconds | Run the command on that worker directly (`ssh worker3 '<command>'`) to see its error |
| A `sudo` command fails over `cluster-cmd` with `a password is required` | Your user needs a password for `sudo` | Run it per node with `ssh -t`, or see [Cluster Security](Cluster_Security.md#allow-cluster-reboot-without-a-password) |
| Lost SSH access after turning on the firewall | SSH wasn't allowed before `ufw enable` | Connect a keyboard and monitor and run `sudo ufw disable`, or reflash the card; then follow [Firewall](Cluster_Security.md#firewall) in order |


# Power and heat

| Symptom | Likely cause | Fix |
| --- | --- | --- |
| `vcgencmd get_throttled` isn't `throttled=0x0` | Under-voltage or overheating | See [Power](Hardware_List.md#power) and [Cooling](Hardware_List.md#cooling). If the last hex digit is odd (`1`, `3`, `5`...), the Pi has too little power right now; if the fifth digit from the right is odd, it has had too little since boot |
| Random crashes, corrupted cards, read-only file system | Weak power supply, or a worn card | The official supply for each Pi ([Power](Hardware_List.md#power)); replace the card; consider [an SSD](Hardware_List.md#storage) |
| One worker trains far fewer models than the others | That worker is throttling | `cluster-cmd vcgencmd measure_temp` during a job; improve its cooling |


# HDFS

| Symptom | Likely cause | Fix |
| --- | --- | --- |
| `hdfs dfsadmin -report` shows fewer than 4 live DataNodes | DataNode didn't start, or can't reach `master` | Read the newest `hadoop-*-datanode-*.log` on that worker |
| DataNode log says `Incompatible clusterIDs` | The NameNode was formatted again after the DataNode first joined | On `master`: `stop-dfs.sh`; then `master-cmd 'rm -rf /opt/hadoop_data/datanode'` and `start-dfs.sh`. This deletes all HDFS data |
| DataNode log shows `Connection refused` to `master:9000` | The NameNode listens on the wrong address, or the firewall blocks it | On `master`, `ss -tln \| grep 9000` must show `192.168.0.100:9000`, not `127.0.1.1`. If not, run `setup_hosts.sh` on `master` and restart HDFS. Check that `ufw` allows your subnet |
| `Name node is in safe mode` | Normal for a minute after start, while DataNodes report in | Wait, or check with `hdfs dfsadmin -safemode get`. If it stays on, some DataNodes are missing |
| `JAVA_HOME is not set` or `UnsupportedClassVersionError` | Wrong or missing Java | `cluster-cmd 'ls -d /usr/lib/jvm/temurin-17-jdk-*'`; `JAVA_HOME` in `hadoop-env.sh` must point to it ([Single Node Setup](Single_Node_Setup.md#install-java-17-on-every-node)) |
| `hdfs: command not found` over SSH | `~/.cluster_env` isn't loaded at the top of `~/.bashrc` | Check `head -1 ~/.bashrc` on that node; see [Set environment variables](Single_Node_Setup.md#set-environment-variables) |


# Spark and the workload

| Symptom | Likely cause | Fix |
| --- | --- | --- |
| Spark master page shows 0 or too few workers | Worker can't reach `master:7077`, or didn't start | Read `/opt/spark/logs/*Worker*.out` on that worker; check the firewall and `SPARK_MASTER_HOST` in `spark-env.sh` |
| `Initial job has not accepted any resources` | The job asks for more memory or cores than a worker offers | `spark.executor.memory` must be at most `SPARK_WORKER_MEMORY`, and `spark.executor.cores` at most `SPARK_WORKER_CORES` ([Configure Spark](Spark.md#configure-spark)) |
| `ModuleNotFoundError: No module named 'xgboost'` (or pandas) | Workers use a Python without the packages | Check `PYSPARK_PYTHON=/opt/pyenv/bin/python` in `spark-env.sh` on every node, and the import check in [Python on every node](Workload.md#python-on-every-node) |
| `Python in worker has different version than that in driver` | Nodes run different Python versions | Use the same Raspberry Pi OS release on every node, and the same `/opt/pyenv` |
| `ExecutorLostFailure` or a worker drops out mid-job | Out of memory: Linux stopped a process | `ssh worker1 'sudo dmesg \| grep -i killed'`; use the smaller row in the memory table, or 4 GB boards |
| `max concurrent` is more than 1 on a worker | `spark.executor.cores` and the script's cores per model differ | Keep `spark.executor.cores 4` and run `train_models.py` without `--threads` (it defaults to 4) |
| Training is much slower than the benchmark | Throttling, or more threads than cores | Check temperature and power; don't raise `--threads` above the worker's core count |

---

Back to the [Cluster Guide](Cluster_Guide.md)
