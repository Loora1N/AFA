#!/usr/bin/env python3

import os
import os.path
import sys
import time


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
    print('\n')
    print('starting...')
    time.sleep(2)
    
def printHelp():
    print('AFA based on qemu and AFL++ by Loora1N and Cube!!!')
    print('\n')
    print('information search:')
    print('./afa.py -s <firmware_path> <report.txt>\n')
    print('module fuzz:')
    print('./afa.py -f -i <input_floder> -o <output_floder> -- <elf_path>\n')

                                       

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
    
    
def startFuzz(cnt):
    inputPath = sys.argv[3]
    outputPath = sys.argv[5]
    elfPath = sys.argv[7]
    if cnt == 8:
        payload = "afl-fuzz -i "+ inputPath + " -o " + outputPath + " -Q -- " + elfPath
    elif cnt == 9:
        payload = "afl-fuzz -i "+ inputPath + " -o " + outputPath + " -Q -- " + elfPath + ' @@'
    else:
        return 1
    os.system(payload)

    

def checkArgc(cnt):
    if cnt > 2:
        if sys.argv[1] == '-f':
            if cnt == 8:
                if sys.argv[2] == '-i':
                    if sys.agv[4] == '-o':
                        if sys.argv[6] == '--':
                            return 'fuzz'
            if cnt == 9:
                if sys.argv[2] == '-i':
                    if sys.agv[4] == '-o':
                        if sys.argv[6] == '--':
                            if sys.argv[8] == '@@':
                                return 'fuzz'
            return 'Usahe -f'
        
        elif sys.argv[1] == '-s':
            if cnt == 4:
                return 'search'
            else:
                return 'Usage -s'
    elif cnt == 2:
        if sys.argv[1] == '-h' or sys.argv[1] == '--help':
            return 'help'
    return 'no argv'    



def start():
    
    mode = checkArgc(len(sys.argv))
    if mode == 'no argv':
        print("please use './afa.py --help/-h' for more information!")
        exit()
        
    elif mode == 'search':
        printTable()
        searchInfo()
        
    elif mode == 'fuzz':
        printTable()
        startFuzz(len(sys.argv))
        
    elif mode =='Usage -s':
        print("usage: please use ./afa.py -s <firmware_path> <report.txt>")
        exit()
        
    elif mode =='Usage -f':
        print("usage: please use ./afa.py -f -i <input_floder> -o <output_floder> -- <elf_path>")
        exit()
        
    elif mode =='help':
        printHelp()
        exit()
    
    else:
        print("Error: this function does not finished yet!!")
        print("please use './afa.py --help/-h' for more information!")
        exit()
    
    
    
if __name__ == "__main__":
    start()