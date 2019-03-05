#!/usr/bin/env python3
from cscore import CameraServer, UsbCamera
from networktables import NetworkTables


def main():
    # Use cscore (Camera Server Core, I think) to send camera feed automatically.
    cs = CameraServer.getInstance()
    # Make cscore show output in the driverstation console.
    cs.enableLogging()

    # Get both USB cameras plugged in, and tell cscore to start sending them to the driverstation.
    # You might wish to name these based on what part of the robot they're on, i.e. 'bottom_camera' etc.
    usb0 = cs.startAutomaticCapture(dev=0)
    usb1 = cs.startAutomaticCapture(dev=1)

    cs.waitForever()


# Automatically run main function when this file runs
if __name__ == '__main__':
    main()
