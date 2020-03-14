[Background](Background.md) / [Purpose](Purpose.md) / [Getting Started](Getting_Started.md) / [Cluster Guide](Cluster_Guide.md)


<img src="https://image.flaticon.com/icons/svg/2535/2535492.svg" width="100px" height="100px"/>


# Cluster Commands

The following are user-defined cluster command functions that will also facilitate communication across the cluster network. Many thanks to [Andrew and his guide](https://dev.to/awwsmm/building-a-raspberry-pi-hadoop-spark-cluster-8b2) for coming up with this idea.

All of these `functions` are to be defined in each Pi's `~/.bashrc` file and note that some of these depend on having the IP addresses mapped to each hostname in the `/etc/hosts` file.

* [Back-up file `~/.bashrc`](#back-up-file-bashrc)
* [Add commands to `~/.bashrc`](#add-commands-to-bashrc)
* [All commands (`cluster_commands.sh`)](#all-commands)
    * [Define cluster user](#define-cluster-user)
    * [`cluster-user` command explained](#cluster-user-command-explained)
    * [`nodes` command explained](#nodes-command-explained)
    * [`nodes-up` command explained](#nodes-up-command-explained)
    * [`workers` command explained](#workers-command-explained)
    * [`master-cmd` command explained](#master-cmd-command-explained)
    * [`cluster-cmd` command explained](#cluster-cmd-command-explained)
        * [`date` sync](#date-sync)
    * [`cluster-reboot` command explained](#cluster-reboot-command-explained)
    * [`cluster-shutdown` command explained](#cluster-shutdown-command-explained)
    * [`cluster-scp` command explained](#cluster-scp-command-explained)
    * [`cluster-scpr` command explained](#cluster-scpr-command-explained)


# Back-up file `~/.bashrc`

Before we proceed, let's back up current `~/.bashrc` file in every Pi just in case
```cli
cp ~/.bashrc ~/.bashrc.bak
```

If you mess up the file, you can always revert back your changes using
```cli
cp ~/.bashrc.bak ~/.bashrc
source ~/.bashrc
```


# Add commands to `~/.bashrc`

Download our cluster_command.sh` script to a hidden `scripts` directory
```cli
mkdir -p ~/.scripts
cd ~/.scripts
wget https://raw.githubusercontent.com/gitluis/pi-cluster/master/scripts/cluster_commands.sh
```

Edit `~/.bashrc` file to include `cluster_commands.sh` file
```cli
sudo nano ~/.bashrc
```

Append the following lines at the bottom
```shell
...

# including pi-cluster commands
source ~/.scripts/cluster_commands.sh
```

Source for changes to take effect
```cli
source ~/.bashrc
```

Copy over the `~/.bashrc` file to all workers
```cli
cluster-scp ~/.bashrc
```

**Note:** For these commands to work, you must have had mapped each Raspberry Pi's IP address to its hostname as specified in [The Pi Network](The_Pi_Network.html#mapping-the-hostname).


# All commands

`cluster_commands.sh`
```shell
# ------------------- #
# Pi-Cluster Commands #
# ------------------- #


# define cluster user
USER="pi"


# return the common user across all nodes in the cluster
function cluster-user {
  echo $USER
}


# return the IP address and mapped hostname of each node in the cluster
function nodes {
  grep "master" /etc/hosts | awk '{print $0}' && \
  grep "worker" /etc/hosts | awk '{print $0}'
}


# return which nodes are currently up and running
function nodes-up {
  echo "Pinging master..."
  ping master -c 1 | grep "packet loss"

  for worker in $(workers)
  do
    echo "Pinging $worker..."
    ping $worker -c 1 | grep "packet loss"
  done
}


# return only the hostname of each worker in the cluster
function workers {
  grep "worker" /etc/hosts | awk '{print $2}'
}


# send a command to be executed by all workers in the cluster
function master-cmd {
  for worker in $(workers)
  do
    echo "Executing '$@' in $worker as $USER..."
    ssh $USER@$worker "$@"
  done
}


# send a command to be executed by all nodes in the cluster
function cluster-cmd {
  master-cmd $@
  echo "Executing '$@' in master as $USER..."
  $@
}


# reboot all nodes in the cluster at the same time
function cluster-reboot {
  cluster-cmd sudo shutdown -r now
}


# shutdown all nodes in the cluster at the same time
function cluster-shutdown {
  cluster-cmd sudo shutdown now
}


# transfer files from one node to all other nodes
function cluster-scp {
  for worker in $(workers)
  do
    echo "Executing 'scp $1 $USER@$worker:$2' in $worker as $USER..."
    scp $1 $USER@$worker:$2
  done
}


# transfer directories from one node to all other nodes
function cluster-scpr {
  for worker in $(workers)
  do
    echo "Executing 'scp -r $1 $USER@$worker:$2' in $worker as $USER..."
    scp -r $1 $USER@$worker:$2
  done
}
```


# Define cluster user

Define a common user across all nodes in the cluster.

```shell
# define cluster user
USER="pi"
```


# `cluster-user` command explained

Return the common user across all nodes in the cluster.

Usage example
```cli
$ cluster-user
pi
```


# `nodes` command explained

Return the IP address and mapped hostname of each node in the cluster.

Usage example
```cli
$ nodes
192.168.0.100	master
192.168.0.101	worker1
192.168.0.102	worker2
192.168.0.103	worker3
192.168.0.104	worker4
```


# `nodes-up` command explained

Return which nodes are currently up and running.

Usage example
```cli
$ nodes-up
Pinging master...
1 packets transmitted, 1 received, 0% packet loss, time 0ms
Pinging worker1...
1 packets transmitted, 1 received, 0% packet loss, time 0ms
Pinging worker2...
1 packets transmitted, 1 received, 0% packet loss, time 0ms
Pinging worker3...
1 packets transmitted, 1 received, 0% packet loss, time 0ms
Pinging worker4...
1 packets transmitted, 1 received, 0% packet loss, time 0ms
```

`0%` packet loss reflects that such node is up and running. In the case of a node being down, it will display a `100%` packet loss, meaning all packets sent were not received.


# `workers` command explained

Return only the hostname of each worker in the cluster.

Usage example
```cli
$ workers
worker1
worker2
worker3
worker4
```


# `master-cmd` command explained

Send a command to be executed by all workers in the cluster.

Usage example
```cli
$ master-cmd date
Executing 'date' in worker1 as pi...
Wed 11 Mar 2020 08:31:47 PM AST
Executing 'date' in worker2 as pi...
Wed 11 Mar 2020 08:31:47 PM AST
Executing 'date' in worker3 as pi...
Wed 11 Mar 2020 08:31:48 PM AST
Executing 'date' in worker4 as pi...
Wed 11 Mar 2020 08:31:48 PM AST
```


# `cluster-cmd` command explained

Send a command to be executed by all nodes in the cluster.

The difference between these `master-cmd` and `cluster-cmd` is that sometimes you want workers to do something but not the master, for that case you can use `master-cmd`. And for the case in which you want all nodes in the cluster to do something, you use `cluster-cmd` instead.

Usage example
```cli
$ cluster-cmd date
Executing 'date' in worker1 as pi...
Wed 11 Mar 2020 10:38:56 PM AST
Executing 'date' in worker2 as pi...
Wed 11 Mar 2020 08:32:11 PM AST
Executing 'date' in worker3 as pi...
Wed 11 Mar 2020 06:22:40 PM AST
Executing 'date' in worker4 as pi...
Wed 11 Mar 2020 09:47:10 PM AST
Executing 'date' in master as pi...
Wed 11 Mar 2020 12:12:58 PM AST
```

**Note**: The reason for `$@` being after `master-cmd $@` is so that the command is executed in the workers first and then in the master node. If a `reboot` or `shutdown` command is passed and was to be executed in the master node first then the master would be halted before it can tell the workers what they were supposed to do, thus rebooting/shutting down the master but not the workers.


## `date` sync

As you may have seen, each Pi's date and time may not be synchronized. It may not be a problem now, but for those people who intend on creating "crontab" jobs, which are nothing more but scheduled job or tasks, it could be a critical issue.

First, we need to make sure `htpdate` is installed on all of our Pi boards
```cli
cluster-cmd "sudo apt install htpdate -y > /dev/null 2&1"
```

That will align the nodes within +/- 10 seconds.

A more reliable and robust way is to have them synchronized using a remote server such as `time.nist.gov`
```cli
cluster-cmd sudo htpdate -a -l time.nist.gov
```

This may take a few minutes before it finished yet it will sync all clocks. Being off by less than 5 seconds is good enough.


# `cluster-reboot` command explained

Reboot all nodes in the cluster at the same time.

Usage example
```cli
cluster-reboot
```


# `cluster-shutdown` command explained

Shutdown all nodes in the cluster at the same time.

Usage example
```cli
cluster-shutdown
```


# `cluster-scp` command explained

Transfer (secure copy) files from one node to all other nodes.

Usage example
```cli
$ cluster-scp ~/.bashrc
Executing 'scp /home/pi/.bashrc pi@worker1:' in worker1 as pi...
.bashrc                                       100% 3594     2.3MB/s   00:00    
Executing 'scp /home/pi/.bashrc pi@worker2:' in worker2 as pi...
.bashrc                                       100% 3594     2.1MB/s   00:00    
Executing 'scp /home/pi/.bashrc pi@worker3:' in worker3 as pi...
.bashrc                                       100% 3594     2.5MB/s   00:00    
Executing 'scp /home/pi/.bashrc pi@worker4:' in worker4 as pi...
.bashrc                                       100% 3594     2.2MB/s   00:00
```

This overwrites the `/home/pi/.bashrc` file to the same `path` in all workers.


# `cluster-scpr` command explained

Transfer (secure copy) directories from one node to all other nodes.

Usage example
```cli
$ cluster-scpr ~/.scripts/
Executing 'scp -r /home/pi/.scripts/ pi@worker1:' in worker1 as pi...
cluster_commands.sh                           100% 1805     1.5MB/s   00:00    
Executing 'scp -r /home/pi/.scripts/ pi@worker2:' in worker2 as pi...
cluster_commands.sh                           100% 1805     1.7MB/s   00:00    
Executing 'scp -r /home/pi/.scripts/ pi@worker3:' in worker3 as pi...
cluster_commands.sh                           100% 1805     1.7MB/s   00:00    
Executing 'scp -r /home/pi/.scripts/ pi@worker4:' in worker4 as pi...
cluster_commands.sh                           100% 1805     1.1MB/s   00:00
```

This overwrites the `/home/pi/.scripts` directory and its contents to the same `path` in all workers.

**Note:** You must ensure that the preceding `/` at the end is specified for all contents to be transferred over.
