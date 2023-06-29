#!/usr/bin/env python3

import os
import os.path
import pexpect
import sys
import argparse


def printTable():
    print('\n\n\n')
    print('      _        ________        _       ')
    print('     / \      |_   __  |      / \      ')
    print('    / _ \       | |_ \_|     / _ \     ')
    print('   / ___ \      |  _|       / ___ \    ')
    print(' _/ /   \ \_   _| |_      _/ /   \ \_  ')
    print('|____| |____| |_____|    |____| |____| ')
    print('\n')
    print('****************************************')
    print('           Welcome to AFA!!!            ')
    print('****************************************')
    
                                       

def searchInfo():
    rootfs_path = sys.argv[1] 
    filename = sys.argv[2]
    payload = "scripts/infosearcher.sh " + rootfs_path + " report/info-report/"+filename
    os.system(payload)

def checkArgc(cnt):
    match cnt:
        case 1:
            return 'no argv'
        case 3:
            return 'search'
        



def main():
    
    mode = checkArgc(len(sys.argv))
    if mode == 'no argv':
        print("usage: please use ./afa.py <rootfs_path> <file>")
        exit()
        
    printTable()
    if mode == 'search':
        searchInfo()
    else:
        print("usage: please use ./afa.py <rootfs_path> <file>")
        exit()
    
    # print('argc:'+str(len(sys.argv)))
    
    
    
if __name__ == "__main__":
    main()