#!/bin/env python3

import subprocess
import os
import time
import glob

container = "fireflyiii-spectre"
script_path = os.path.dirname(os.path.realpath(__file__))


# start container
p = subprocess.Popen(["docker", "start", container])
p.wait()
if p.poll() != 0:
    print(f"> failed to start container {container}")
    exit(1)


command = ["docker", "exec", container, "php", "artisan", "importer:import"]

files = [os.path.split(p)[-1] for p in glob.glob(f'{script_path}/configs/*.json')]

processes = set()
max_processes = 6

for name in files:
    processes.add(subprocess.Popen([*command, f"/configs/{name}"],
#        stdout=subprocess.DEVNULL,
#        stderr=subprocess.STDOUT,
        ))
    if len(processes) >= max_processes:
        os.wait()
        processes.difference_update([p for p in processes if p.poll() is not None])

for f, p in zip(files, processes):
    p.wait()

print("===============================")

# Check if all the child processes were closed
for f, p in zip(files, processes):
    print(f"{f}: {p.poll()}")

# stop container
p = subprocess.Popen(["docker", "stop", container])
p.wait()
if p.poll() != 0:
    print(f"> failed to stop container {container}")
    exit(1)

