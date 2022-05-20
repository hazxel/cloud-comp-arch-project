from pydoc import cli
import psutil
import docker
from time import sleep

def run(client, name):
  if name == 'fft':
    client.containers.run("anakli/parsec:splash2x-fft-native-reduced", \
      ["./bin/parsecmgmt", "-a", "run", "-p", "splash2x.fft", "-i", "native", "-n", "1"], \
      cpuset_cpus="3", \
      detach=True, \
      remove=True, \
      name=name)
  else:
    client.containers.run("anakli/parsec:" + name + "-native-reduced", \
      ["./bin/parsecmgmt", "-a", "run", "-p", name, "-i", "native", "-n", "4"], \
      cpuset_cpus="0-3", \
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

  # print(psutil.cpu_times())
  # print(psutil.cpu_percent(interval=1))
  # print(psutil.cpu_percent(interval=1, percpu=True))

  while ready or paused or running:
    # update completed tasks
    for container in running:
      try:
        client.containers.get(container)
      except:
        running.remove(container)
        completed.append(container)

    # check cpu usage and pause/unpause
    if psutil.cpu_percent(interval=1) < 50:
      if paused:
        run_this = paused.pop()
        unpause(client, run_this)
        running.append(run_this)
      elif ready:
        run_this = ready.pop()
        run(client, run_this)
        running.append(run_this)
    elif psutil.cpu_percent(interval=1) > 70 and running:
      pause_this = running.pop()
      pause(client, pause_this)
      paused.append(pause_this)

    sleep(1)
    print(ready, running, paused, completed)