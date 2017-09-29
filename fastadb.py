#!/usr/bin/python3

import sys
import subprocess

def pullfile(inText):
    filelists = listfile(inText).split('\n')
    
    for each in filelists:
        if each and each != ' ':
            result = subprocess.run(['adb','pull',each],stdout=subprocess.PIPE)
            print(result.stdout.decode('utf-8'))

def pushfile(inText):
    pass
    
def listfile(inText):
    result = subprocess.run(['adb','shell','ls -1',inText],stdout=subprocess.PIPE)
    filelists = result.stdout.decode('utf-8') #.split('\n')
    return filelists


if __name__ == "__main__":
    #sys.argv格式为 x.py pull /sdcard/DCIM/Camera/
    #sys.argv格式为 0    1    2+  
    if sys.argv[1:]:
        if sys.argv[2:]:
            inText = ' '.join(sys.argv[2:])
            if sys.argv[1] == 'pull':
                print("正在将对应文件传输至本地……")
                c = pullfile(inText)
                outText = ''
            #elif sys.argv[1] == 'push':
            #    print("正在将对应文件推送至设备……")
            #    c = pushfile(inText)
            #    outText = ''
            elif sys.argv[1] == 'list':
                print("正在列出匹配的文件……")
                outText = listfile(inText)
            else:
                print("用法: fastadb.py [pull][list] strings")
                outText = ''
        else:
            print("正在列出匹配的文件……")
            inText = ' '.join(sys.argv[1:])
            outText = listfile(inText)
    else:
        print("用法: fastadb.py [pull][list] strings")
        outText = ''
        
    print(outText)
