# run memcached
kubectl create -f memcache-t1-cpuset.yaml
kubectl expose pod some-memcached --name some-memcached-11211  --type LoadBalancer --port 11211 --protocol TCP
sleep 60
kubectl get service some-memcached-11211
kubectl get pods -o wide

# ssh login
gcloud compute ssh --ssh-key-file ~/.ssh/cloud-computing ubuntu@client-agent-cqjq --zone europe-west3-a
gcloud compute ssh --ssh-key-file ~/.ssh/cloud-computing ubuntu@client-agent-b-5slm --zone europe-west3-a
gcloud compute ssh --ssh-key-file ~/.ssh/cloud-computing ubuntu@client-measure-x4db --zone europe-west3-a
gcloud compute ssh --ssh-key-file ~/.ssh/cloud-computing ubuntu@memcache-server-ft7h --zone europe-west3-a

sudo apt-get update
sudo apt-get install libevent-dev libzmq3-dev git make g++ --yes
sudo cp /etc/apt/sources.list /etc/apt/sources.list~
sudo sed -Ei 's/^# deb-src /deb-src /' /etc/apt/sources.list
sudo apt-get update
sudo apt-get build-dep memcached --yes
cd && git clone https://github.com/shaygalon/memcache-perf.git
cd memcache-perf
make

# agent
./mcperf -T 16 -A

# measure
./mcperf -s MEMCACHED_IP --loadonly
./mcperf -s MEMCACHED_IP -a INTERNAL_AGENT_IP  \
           --noload -T 6 -C 4 -D 4 -Q 1000 -c 4 -t 20 \
           --scan 30000:30500:10

# MEMCACHED_IP is from the output of kubectl get pods -o wide above and INTERNAL_AGENT_IP is from the Internal IP of the client-agent node from the output of kubectl get nodes -o wide.
# You should look at the output of ./mcperf -h to understand the different flags in the above com- mands.

# clean






# TASK 4

sudo apt update
sudo apt install -y memcached libmemcached-tools
sudo systemctl status memcached
sudo vim /etc/memcached.conf # -m 1024 -t 1 -l MEMCACHE_SERVER_INTERNAL_IP

sudo systemctl restart memcached

sudo apt install python3-pip
python3 -m pip install docker psutil
git clone https://github.com/hazxel/cloud-comp-arch-project.git
cd cloud-comp-arch-project

#measure
sudo apt-get update
sudo apt-get install libevent-dev libzmq3-dev git make g++ --yes
sudo apt-get build-dep memcached --yes
git clone https://github.com/eth-easl/memcache-perf-dynamic.git
cd memcache-perf-dynamic
make

# agent
./mcperf -T 16 -A

# measure
./mcperf -s INTERNAL_MEMCACHED_IP --loadonly
$ ./mcperf -s INTERNAL_MEMCACHED_IP -a INTERNAL_AGENT_IP  \
           --noload -T 16 -C 4 -D 4 -Q 1000 -c 4 -t 10 \
           --qps_interval 2 --qps_min 5000 --qps_max 100000