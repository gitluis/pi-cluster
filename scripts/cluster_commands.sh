# ------------------- #
# Pi-Cluster Commands #
# ------------------- #
# Source this file from ~/.bashrc:  source ~/.scripts/cluster_commands.sh
#
# Nodes are read from the "# pi-cluster network" block in /etc/hosts:
#   # pi-cluster network
#   192.168.0.100    master
#   192.168.0.101    worker1
#   ...
#   # end pi-cluster network

# common user across all nodes (do NOT use USER: it is a standard shell variable)
CLUSTER_USER="${CLUSTER_USER:-$(id -un)}"
CLUSTER_HOSTS_FILE="${CLUSTER_HOSTS_FILE:-/etc/hosts}"
CLUSTER_SSH_OPTS=(-o BatchMode=yes -o ConnectTimeout=5)


# print the lines of the pi-cluster block in /etc/hosts (IP + hostname)
function nodes {
  awk '/^# pi-cluster network/{f=1; next} /^# end pi-cluster network/{f=0} f && /^[0-9]/ {print $1"\t"$2}' \
    "$CLUSTER_HOSTS_FILE"
}


# return the common user across all nodes in the cluster
function cluster-user {
  echo "$CLUSTER_USER"
}


# return only the hostname of each worker in the cluster
function workers {
  nodes | awk '$2 ~ /^worker[0-9]+$/ {print $2}'
}


# return which nodes are currently up
function nodes-up {
  local host
  for host in $(nodes | awk '{print $2}'); do
    if ping -c 1 -W 2 "$host" > /dev/null 2>&1; then
      echo "$host: up"
    else
      echo "$host: DOWN"
    fi
  done
}


# run a command on every worker (not on master)
function master-cmd {
  local worker
  for worker in $(workers); do
    echo "==> $worker: $*"
    # shellcheck disable=SC2029  # expanding here is intended: the command runs remotely as one string
    ssh "${CLUSTER_SSH_OPTS[@]}" "$CLUSTER_USER@$worker" "$*" \
      || echo "!! $worker: command failed (exit $?)" >&2
  done
}


# run a command on every worker, then on master (master last so reboot/shutdown reach the workers)
function cluster-cmd {
  master-cmd "$@"
  echo "==> $(hostname): $*"
  bash -c "$*"
}


# reboot / shut down all nodes (workers first, master last)
function cluster-reboot   { cluster-cmd "sudo shutdown -r now"; }
function cluster-shutdown { cluster-cmd "sudo shutdown -h now"; }


# copy a file or directory to the same path on every worker
#   cluster-scp ~/.bashrc
#   cluster-scp ~/.scripts            (directories are copied recursively)
#   cluster-scp ./data.csv /tmp/      (optional destination)
function cluster-scp {
  local src="$1" dest="${2:-$1}" worker
  if [[ -z "$src" ]]; then
    echo "usage: cluster-scp <path> [dest]" >&2
    return 1
  fi
  # copy a directory into its parent, so ~/.scripts lands at ~/.scripts, not ~/.scripts/.scripts
  if [[ -d "$src" && -z "$2" ]]; then
    dest="$(dirname "$(realpath "$src")")/"
  fi
  for worker in $(workers); do
    echo "==> $worker: $src -> $dest"
    scp -r -q "${CLUSTER_SSH_OPTS[@]}" "$src" "$CLUSTER_USER@$worker:$dest" \
      || echo "!! $worker: copy failed" >&2
  done
}


# kept for backward compatibility with the guide
function cluster-scpr { cluster-scp "$@"; }
