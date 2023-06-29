#!/usr/bin/env python3

import os
import os.path
import sys


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
    
    firm_path = sys.argv[2] 
    filename = sys.argv[3]
    
    #TODO: extract file system
    firmFilename = os.path.basename(firm_path)
    os.system('cp '+firm_path+' images/')
    os.system('cd images/ && binwalk -eM '+firmFilename)
    
    #TODO: info searcher and save file
    firmFloder = 'images/_'+firmFilename+'.extracted'    
    payload = "scripts/infosearcher.sh " + firmFloder + " Report/info-report/"+filename
    os.system(payload)
    
    #TODO: create a report
    
    
    

def checkArgc(cnt):
    match cnt:
        #TODO: create a help fuction and more func
        case 1:
            return 'no argv'
        case 4:
            if sys.argv[1] == '-s':
                return 'search'
            return "not yet"
        



def main():
    
    mode = checkArgc(len(sys.argv))
    if mode == 'no argv':
        print("usage: please use ./afa.py -s <firmware_path> <report.txt>")
        exit()
        
    if mode == 'search':
        printTable()
        searchInfo()
    else:
        print("Error: this function does not finished yet!!")
        print("       please use ./afa.py -s <firmware_path> <report.txt>")
        exit()
    
    
    
if __name__ == "__main__":
    main()