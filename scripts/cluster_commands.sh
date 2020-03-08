# ------------------- #
# Pi-Cluster Commands #
# ------------------- #

# define cluster user
USER="pi"

# return the user common across all nodes in the cluster
function cluster-user {
  echo $USER
}

# return the IP address and mapped hostname of each node in the cluster
function nodes {
  grep "master" /etc/hosts | awk '{print $0}' && \
  grep "worker" /etc/hosts | awk '{print $0}'
}

# return only the hostname of each worker in the cluster
function workers {
  grep "worker" /etc/hosts | awk '{print $2}'
}

# send a command to be executed by all workers in the cluster
function master-cmd {
  for worker in $(workers)
  do
    ssh $USER@$worker "$@"
  done
}

# send a command to be executed by all nodes in the cluster
function cluster-cmd {
  master-cmd $@
  $@
}

# reboot all nodes in the cluster at the same time
function cluster-reboot {
  cluster-cmd shutdown -r now
}

# shutdown all nodes in the cluster at the same time
function cluster-shutdown {
  cluster-cmd shutdown now
}

# transfer files from one node to all other nodes
function cluster-scp {
  for worker in $(workers)
  do
    scp $@ $USER@$worker:$@
  done
}

# transfer directories from one node to all other nodes
function cluster-scpr {
  for worker in $(workers)
  do
    scp -r $@ $USER@$worker:$@
  done
}
