import os
from time import sleep
import mounts.mounts_linux as mounts_linux
import mounts.mounts_windows as mounts_windows
import threading


def scan_usb(mounts, event):

    def walk_error_handler(error):
        print(error)                # handles error thrown by os.walk
        print(event.is_set())

    for a, _, files in os.walk(mounts, onerror=walk_error_handler): 

        for i in files:

            if event.is_set():                      # iteration through files on USB device
                return
            
            print(os.path.join(a, i)) 
            
            if event.wait(3):
                return # used to debug (front panel USB-s dont work)

def usb_manager_main():
    
    showed = set()
    stop_events = {}

    if os.name == "nt":
        system_mount = mounts_windows      # checks if system is linux/windows
    else:
        system_mount = mounts_linux

    while True:                                             

        current = set(system_mount.get_usb_mounts())  # retrives list of connected devices via USB

        for mounts in current:
            
            if mounts in showed:    # checks if content of device was iterated or is it getting itreated
                continue

            event = threading.Event()
            stop_events[mounts] = event
            threading.Thread(target=scan_usb, daemon=True, args=(mounts, event, )).start()  # every device has its own thread for iteration

        for mount in showed - current:

            stop_events.pop(mount).set()    # deletes disconnected devices from memory

        showed = current
        sleep(0.5)

if __name__ == "__main__":
    usb_manager_main()