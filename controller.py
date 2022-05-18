import psutil
import docker
from time import sleep


# client = docker.from_env()
# print(client.containers.run("alpine", ["echo", "hello", "world"]))
# client.containers.run("anakli/parsec:splash2x-fft-native-reduced", \
#     ["./bin/parsecmgmt", "-a", "run", "-p", "splash2x.fft", "-i", "native", "-n", "1"], \
#     cpuset_cpus="0", \
#     detach=True, \
#     remove=True, \
#     name="parsec-fft")

# container_fft = client.containers.get("parsec-fft")
# container_fft.pause()
# container_fft.unpause()
# container_fft.update()


# print(psutil.cpu_times())
# print(psutil.cpu_percent(interval=1))
# print(psutil.cpu_percent(interval=1, percpu=True))

def run(client, name):
  if name == 'fft':
    client.containers.run("anakli/parsec:splash2x-fft-native-reduced", \
      ["./bin/parsecmgmt", "-a", "run", "-p", "splash2x.fft", "-i", "native", "-n", "1"], \
      cpuset_cpus="0", \
      detach=True, \
      remove=True, \
      name=name)
  else:
    client.containers.run("anakli/parsec:" + name + "-native-reduced", \
      ["./bin/parsecmgmt", "-a", "run", "-p", name, "-i", "native", "-n", "1"], \
      cpuset_cpus="0", \
      detach=True, \
      remove=True, \
      name=name)

def pause(client, name):
  client.containers.get(name).pause()

def unpause(client, name):
  client.containers.get(name).unpause()

if __name__ == '__main__':
  client = docker.from_env()

  ready = ["fft", "blackscholes", "canneal", "dedup", "ferret", "freqmine"]
  running = []
  paused = []
  completed = []

  # run(client, ready[0])
  # pause(client, ready[0])
  while len(ready) != 0 or len(paused) != 0 or len(running) != 0:
    # update completed tasks

    # check cpu usage

    # pause/unpause
    
    sleep(0.01)