import os
from time import sleep
from mounts_linux import names

showed = set()

while True:

    current = set(names())

    for monuts in current:

        nazwa = os.path.basename(monuts)
          
        if monuts in showed:
            continue
        
        print(f"Podłączono: {nazwa}")

        for a, b, files in os.walk(monuts):
            for i in files:
                print(os.path.join(a, i))



    for i in showed - current:
        print(f"Odłączono: {os.path.basename(i)}")

    showed = current
    sleep(0.5)


# print(psutil.disk_partitions()