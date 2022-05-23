import docker
import psutil
import time
from datetime import datetime

fft = {
    'image': 'anakli/parsec:splash2x-fft-native-reduced',
    'command': './bin/parsecmgmt -a run -p splash2x-fft -i native -n 1',
    'cpuset_cpus': '0',
    'detach': True,
    'name': 'splash2x-fft',
    'remove': False
}

freqmine = {
    'image': 'anakli/parsec:freqmine-native-reduced',
    'command': './bin/parsecmgmt -a run -p freqmine -i native -n 3',
    'cpuset_cpus': '0-3',
    'detach': True,
    'name': 'freqmine',
    'remove': False
}

ferret = {
    'image': 'anakli/parsec:ferret-native-reduced',
    'command': './bin/parsecmgmt -a run -p ferret -i native -n 3',
    'cpuset_cpus': '0-3',
    'detach': True,
    'name': 'ferret',
    'remove': False
}

canneal = {
    'image': 'anakli/parsec:canneal-native-reduced',
    'command': './bin/parsecmgmt -a run -p canneal -i native -n 1',
    'cpuset_cpus': '1',
    'detach': True,
    'name': 'canneal',
    'remove': False
}

dedup = {
    'image': 'anakli/parsec:dedup-native-reduced',
    'command': './bin/parsecmgmt -a run -p dedup -i native -n 1',
    'cpuset_cpus': '2',
    'detach': True,
    'name': 'dedup',
    'remove': False
}

blackscholes = {
    'image': 'anakli/parsec:blackscholes-native-reduced',
    'command': './bin/parsecmgmt -a run -p blackscholes -i native -n 3',
    'cpuset_cpus': '0-3',
    'detach': True,
    'name': 'blackscholes',
    'remove': False
}

t3_configs = [freqmine, ferret, blackscholes]
t1_configs = [fft, canneal, dedup]

client = docker.from_env()
f = open('log.txt', 'w')

psutil.cpu_percent(percpu=True)

def log(content):
    output = datetime.now().strftime('[%H:%M:%S] ') + content
    f.write(output + '\n')
    print(output)

def create_container(config):
    container = client.containers.run(
        config['image'], config['command'],
        cpuset_cpus=config['cpuset_cpus'],
        detach=config['detach'],
        name=config['name'],
        remove=config['remove']
    )
    log(config['name'] + ' created')
    container.reload()
    return container
    
def remove_container(container):
    container.remove()
    log(container.name + ' removed')

def main():
    for config in t3_configs:
        container = create_container(config)
        while True:
            container.reload()
            if container.status == 'exited':
                remove_container(container)
                break
            else:
                utilizations = psutil.cpu_percent(percpu=True)
                if utilizations[3] > 75:
                    container.update(cpuset_cpus='0-2')
                elif utilizations[3] < 50:
                    container.update(cpuset_cpus='0-3')
            time.sleep(1)

    t1_containers = []
    for config in t1_configs:
        t1_containers.append(create_container(config))
    
    while len(t1_containers):
        remotions = []
        for container in t1_containers:
            container.reload()
            if container.status == 'exited':
                remove_container(container)
                remotions.append(container)
        for container in remotions:
            t1_containers.remove(container)
        time.sleep(1)

    print('----- The End -----')

if __name__ == '__main__':
    main()