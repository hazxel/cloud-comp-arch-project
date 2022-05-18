import psutil
import docker

client = docker.from_env()
# print(client.containers.run("alpine", ["echo", "hello", "world"]))
client.containers.run("anakli/parsec:splash2x-fft-native-reduced", \
    ["./bin/parsecmgmt", "-a", "run", "-p", "splash2x.fft", "-i", "native", "-n", "1"], \
    cpuset_cpus="0", \
    detach=True, \
    remove=True, \
    name="parsec-fft")

container_fft = client.containers.get("parsec-fft")
container_fft.pause()
container_fft.unpause()
# container_fft.update()


print(psutil.cpu_times())
print(psutil.cpu_percent(interval=1))