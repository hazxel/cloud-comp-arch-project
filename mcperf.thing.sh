# ssh login
gcloud compute ssh --ssh-key-file ~/.ssh/cloud-computing ubuntu@client-agent-b-6f7c \
                     --zone europe-west3-a

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
           --noload -T 16 -C 4 -D 4 -Q 1000 -c 4 -t 5 \
           --scan 5000:55000:5000

# MEMCACHED_IP is from the output of kubectl get pods -o wide above and INTERNAL_AGENT_IP is from the Internal IP of the client-agent node from the output of kubectl get nodes -o wide.
# You should look at the output of ./mcperf -h to understand the different flags in the above com- mands.