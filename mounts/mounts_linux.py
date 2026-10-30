import subprocess
import json

def names():

    mount_list = []

    # wywołanie komendy listującej zamontowane dyski, zwraca sie w formacie jsona
    x = subprocess.run(["lsblk", "-J", "-o", "NAME,TRAN,RM,MOUNTPOINTS,TYPE"], capture_output=True, text=True)

    y = json.loads(x.stdout).get('blockdevices')    # wyciąga potrzebną nam liste mount-ów

    for elem in y:
        if elem.get("tran") == "usb":   # sprawdza czy mount jest pendrive-m

            iterate_mountpoints(elem, mount_list)


    return mount_list


def iterate_mountpoints(elem, mount_list):

    if elem.get("children"):

        for child in elem.get("children"):      # jeżeli urządzenie posiada dzieci to wchodzimy głębiej w rekurencje
            iterate_mountpoints(child, mount_list)


    for mount in elem.get("mountpoints") or []:

        if mount is not None:                   # itreuje po zamontowanych partycjach (pendrive-a/dziecka)

            mount_list.append(mount)

            




# print(names())