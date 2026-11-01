import subprocess
import json

def get_usb_mounts():

    mount_list = []

    # command returns data about all mounted drives in json format
    x = subprocess.run(["lsblk", "-J", "-o", "NAME,TRAN,RM,MOUNTPOINTS,TYPE"], capture_output=True, text=True)

    y = json.loads(x.stdout).get('blockdevices')    # returns parsed mounts list

    for elem in y:
        if elem.get("tran") == "usb":   # checks if mount is USB

            iterate_mountpoints(elem, mount_list)


    return mount_list


def iterate_mountpoints(elem, mount_list):

    if elem.get("children"):

        for child in elem.get("children"):      # checks for children in device, if present goes into recursion
            iterate_mountpoints(child, mount_list)


    for mount in elem.get("mountpoints") or []:

        if mount is not None:                   # itreates through mounted partitions (USB/child)

            mount_list.append(mount)

            
if __name__ == "__main__":
    print(get_usb_mounts())