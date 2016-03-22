#Android Tool

##Intro
This is an alpha test project for using ADB to transfer files into mobile devices in Linux.

TKGUI build with [PAGE](http://page.sourceforge.net/), and code wrote in [UliPad](https://github.com/limodou/ulipad)

Currently works:

* List devices, and select between different devices.
* List files/dirs from target device.
* Push/Pull files into/out of the device
* `adb install` selected apk file

##Disclaimer
I'm not responsible for any damaged devices / bricked devices / nuclear wars caused by using this tool. I installed it on my computer and work with my phone with no problems. But since those codes are still in alpha development, please use with care.

##Requirement
This code has been tested under:

* Ubuntu 14.04 lts
* Python 2.7.6 ( GCC 4.8.2 on Linux2)
* Tkinter / TTK
* Android Debug Bridge version 1.0.32
* Device: Nexus 7(2013) and Nexus 6P

##Installation
Download the files and put in any folder, then run `python androidtool.py`

##TODO:
1. long serial numbers, such as Nexus 6P wasn't detected properly when using code like: `"adb -s %s shell ls /sdcard/" % device_ID`
2. add fool-proof
3. maybe add some waiting information while loading device file lists.
