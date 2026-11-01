import subprocess
import json

def get_usb_mounts():

    mount_list = []

    # commands returns data about all mounted USB devices in json format
    command = """ConvertTo-Json -InputObject @(
    Get-Disk |
    Where-Object { $_.BusType -eq "USB" } |
    Get-Partition |
    Where-Object { $_.DriveLetter } |
    Select-Object DiskNumber, PartitionNumber, DriveLetter
    )"""

    x = subprocess.run(["powershell", "-NoProfile", "-Command", command], capture_output=True, text=True, check=True)


    y = json.loads(x.stdout)    # returns parsed mounts list

    for i in y:
        holder = i.get("DriveLetter")           # iterates through mounts lists and fixes their paths
        mount_list.append(f"{holder}:\\")


    return mount_list


if __name__ == "__main__":
    get_usb_mounts()