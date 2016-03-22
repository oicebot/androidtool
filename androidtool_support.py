#! /usr/bin/env python
#
# Support module generated by PAGE version 4.7
# In conjunction with Tcl version 8.6
#    Mar 21, 2016 01:59:48 PM


import sys
import os
from subprocess import check_output, STDOUT, CalledProcessError


try:
    from Tkinter import *
except ImportError:
    from tkinter import *

try:
    import ttk
    py3 = 0
except ImportError:
    import tkinter.ttk as ttk
    py3 = 1


def set_Tk_var():
    # These are Tk variables used passed to Tkinter and must be
    # defined before the widgets using them are created.
    global combobox
    global current_device, device_info, file_path, files_list
    global device_file_path, device_files, found_devices
    current_device = ''
    files_list = []
    device_files = {}
    file_path = os.path.dirname(os.path.abspath(__file__))
    device_file_path= '/sdcard/Download'

    combobox = StringVar()
    combobox.set('Please Select:')

    device_info = StringVar()
    device_info.set('Device info:')

    found_devices = 0


def install_apk():
    print('androidtool_support.install_apk')
    global files_list
    global file_path
    global device_files
    global current_device
    global device_file_path
    global found_devices
    try:
        clicked = w.List_local.curselection()[0]
        if clicked == 0:
            print 'This cannot be installed!'
            return

        local_file = os.path.join(file_path, files_list[clicked - 1])
        if os.path.isdir(local_file):
            print 'Target is a dir!'
            return
        if local_file.endswith(('.apk')):
            if found_devices > 1:
                cmd = ["adb", "-s%s" % current_device, "install", local_file, ]
            else:
                cmd = ["adb", "install", local_file, ] #.replace(' ','\ '), ]

            print cmd
            out = check_output(cmd, STDOUT)
            info = out.split('\r\n')
            print info
        else:
            print 'Target is not apk!'

    except CalledProcessError as e:
        t = e.returncode, e.message
        print t

    sys.stdout.flush()


def pull_file():
    print('androidtool_support.pull_file')
    global files_list
    global file_path
    global device_files
    global current_device
    global device_file_path
    global found_devices
    try:
        clicked = w.List_device.curselection()[0]
        if clicked == 0:
            print 'This cannot be pulled!'
            return
        device_file = os.path.join(device_file_path,
                                   device_files[device_file_path][clicked - 1])

        if found_devices > 1:
            cmd = ["adb", "-s%s" % current_device, "pull",
             device_file, file_path, ] #.replace(' ','\ '), ]
        else:
            cmd = ["adb", "pull", device_file, file_path, ]
        print cmd
        out = check_output(cmd, STDOUT)
        info = out.split('\r\n')

        print info

    except CalledProcessError as e:
        t = e.returncode, e.message
        print t

    refresh_list()

    sys.stdout.flush()


def push_file():
    print('androidtool_support.push_file')

    global files_list
    global file_path
    global device_files
    global current_device
    global device_file_path
    global found_devices
    try:
        clicked = w.List_local.curselection()[0]
        if clicked == 0:
            print 'This cannot be pushed!'
            return

        local_file = os.path.join(file_path, files_list[clicked - 1])
        if os.path.isdir(local_file):
            local_file = local_file + '/'

        if found_devices > 1:
            cmd = ["adb", "-s%s" % current_device, "push", local_file, device_file_path, ]
        else:
            cmd = ["adb", "push", local_file, device_file_path, ]

        print cmd
        out = check_output(cmd, STDOUT)
        info = out.split('\r\n')

        print info

    except CalledProcessError as e:
        t = e.returncode, e.message
        print t


    sys.stdout.flush()


def refresh_devices():
    print('androidtool_support.refresh_devices')
    global found_devices
    try:
        out = check_output(["adb", "devices"])
        devices = []
        for i in out.split('\n')[1:]:
            if i:
                devices.append(i)
        w.TC_devices['values'] = devices
        found_devices = len(devices)

        print 'Devices found:', found_devices

    except CalledProcessError as e:
        t = e.returncode, e.message
        print t

    sys.stdout.flush()


def refresh_list():
    print('androidtool_support.refresh_list')
    global file_path
    global files_list
    global device_files
    global current_device
    global device_file_path
    if len(current_device) <= 0:
        return None
    #sort by time if you need
    #files = sorted(os.listdir(file_path),
    #               key=lambda x: os.path.getctime(os.path.join(file_path, x)))
    files = sorted(os.listdir(file_path))

    w.List_local.delete(0, END)
    w.List_local.insert(END, '../')

    files_list = files

    w.TL_localpath.configure(text=file_path)
    w.TL_devicepath.configure(text=device_file_path)

    for i in files:
        if os.path.isfile(os.path.join(file_path, i)):
            w.List_local.insert(END, i)
        else:
            w.List_local.insert(END, i + '/')

    w.List_device.delete(0, END)
    w.List_device.insert(END, '../')

    if device_file_path in device_files.keys():
        for i in device_files[device_file_path]:
            w.List_device.insert(END, i)
    else:
        w.List_device.insert(END, 'Try refresh dir')

    sys.stdout.flush()


def refresh_dir():
    print('androidtool_support.refresh_dir -- this may take some time')
    global files_list
    global device_files
    global current_device
    global device_file_path
    global found_devices
    try:
        if found_devices > 1:
            cmd = ["adb", "-s%s" % current_device, "shell", "ls -R /sdcard/"]
        else:
            cmd = ["adb", "shell", "ls -R /sdcard/"]

        #print cmd
        out = check_output(cmd, STDOUT)
        temp_file_list = out.split('\r\n')

        status = 0
        device_files = {}
        tokens = []
        key = ''
        for i in temp_file_list:

            if i:
                if i.startswith(('/')):
                    status = 1
                    key = i[:-1].replace('/sdcard//', '/sdcard/')
                else:
                    tokens.append(i)
            else:
                if status:
                    status = 0
                    device_files[key] = tokens
                    tokens = []

    except CalledProcessError as e:
        t = e.returncode, e.message
        print t

    refresh_list()
    sys.stdout.flush()


def double_click2(top):
    print('androidtool_support.double_click2')
    global device_file_path
    global device_files

    clicked = w.List_device.curselection()[0]

    print clicked,
    if clicked == 0:
        #Prevent cd to upper level
        if device_file_path == '/sdcard':
            device_file_path = '/sdcard/'
        if device_file_path != '/sdcard/':
            temp_path = os.path.dirname(device_file_path)
            if temp_path == '/sdcard':
                temp_path = '/sdcard/'
            print 'Jump to: ', temp_path
            device_file_path = temp_path
            refresh_list()
    else:
        temp_path = os.path.join(device_file_path,
                                 device_files[device_file_path][clicked - 1])
        if temp_path in device_files.keys():
            print 'Jump to: ', temp_path
            device_file_path = temp_path
            refresh_list()
        else:
            print device_files[device_file_path][clicked - 1]

    sys.stdout.flush()


def double_click(top):
    print('androidtool_support.double_click')
    global file_path
    global files_list

    clicked = w.List_local.curselection()[0]
    #print clicked
    if clicked == 0:
        file_path = os.path.dirname(file_path)
        os.walk(file_path)
        refresh_list()
    elif os.path.isfile(os.path.join(file_path, files_list[clicked - 1])):
        pass
    elif os.path.isdir(os.path.join(file_path, files_list[clicked - 1])):
        file_path = os.path.join(file_path, files_list[clicked - 1])
        os.walk(file_path)
        refresh_list()
    else:
        pass

    sys.stdout.flush()


def newselection(top):
    global current_device
    global device_info
    global found_devices
    print('androidtool_support.newselection')
    current_device = combobox.get().split('\t')[0]
    device_info.set('Found Devices:%d ; Current Device: %s' % (found_devices, current_device))

    refresh_dir()

    sys.stdout.flush()


def init(top, gui, *args, **kwargs):
    global w, top_level, root
    w = gui
    top_level = top
    root = top


def destroy_window():
    # Function which closes the window.
    global top_level
    top_level.destroy()
    top_level = None

if __name__ == '__main__':
    import androidtool
    androidtool.vp_start_gui()
