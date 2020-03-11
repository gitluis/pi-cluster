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
