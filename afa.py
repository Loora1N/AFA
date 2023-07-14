#!/usr/bin/env python3
import os
import os.path
import sys
import time
import threading


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
    print('./afa.py -f -i <input_floder> -o <output_floder> -- <elf_path> <IPaddress> <port>\n')                               

def searchInfo():
    
    firm_path = sys.argv[2] 
    filename = sys.argv[3]
    
    #TODO: extract file system
    firmFilename = os.path.basename(firm_path)
    os.system('cp '+firm_path+' images/')
    os.system('cd images/ && binwalk -eM '+firmFilename)
    
    #TODO: info searcher and save file
    firmFloder = 'images/_'+firmFilename+'.extracted'    
    payload = "python3 scripts/infosearch.py " + firmFloder + " Report/info-report/"+filename
    os.system(payload)
    payload = "rm -rf "  + firmFloder
    os.system(payload)
    
    #TODO: create a report

# thread restart   
def restart_target(path):
    print(path+"\n")
    t_startsrv = threading.Thread(target=start_target,args=(path,))
    t_startsrv.daemon = True
    t_startsrv.start()
    # t_startsrv.join()

# thread check
def check_fuzz_target(target_path):
    while True:
        tmp_file = './corn.lock'
        tmp_path = "sh -c "+ target_path
        os.system('''ps -ef | grep "%s" | grep -v grep > %s'''%(tmp_path,tmp_file))
        if not(os.path.getsize(tmp_file)):
            restart_target(target_path)
        else:
            f = open(tmp_file,"r+")
            f.truncate(0)
        time.sleep(2)

#start service        
def start_target(target_path):
    os.system(target_path)
    
#start fuzz
def fuzz_target(payload):
    os.system(payload)
    
def startLocalTcpFuzz(cnt):
    inputPath = sys.argv[3]
    outputPath = 'Report/fuzzreport'
    elfPath = sys.argv[7]
    IPaddress = sys.argv[8]
    port = sys.argv[9]
    if cnt == 10:
        payload = "afl-fuzz -i "+ inputPath + " -o " + outputPath + \
            " -Q -- ./source/fuzzentry/fuzzentry" + " " + IPaddress + " " + port
    else:
        return 1
    # start sevice thread
    print("starting service......\n")
    restart_target(elfPath)
    time.sleep(2)
    
    # start check thread
    print("starting check thread......\n")
    t_check = threading.Thread(target = check_fuzz_target,args=(elfPath,))
    t_check.daemon = True
    t_check.start()
    time.sleep(2)
    #start fuzz thread
    t_fuzz = threading.Thread(target = fuzz_target,args=(payload,))
    t_fuzz.daemon = True
    t_fuzz.start()
    t_fuzz.join()

    

def checkArgc(cnt):
    if cnt > 2:
        if sys.argv[1] == '-f':
            if sys.argv[2] == '-i':
                if sys.argv[4] == '-M':
                    if sys.argv[6] == '--':
                        if sys.argv[5] == 'local-server':
                            if cnt == 10:
                                return 'fuzz-local-tcp'
                        if sys.argv[5] == 'remote-server':
                            if cnt == 9:
                                return 'fuzz-remote-server'
                        if sys.argv[5] == 'normal':
                                return 'fuzz-normal'
            return 'Usage -f'   
        
        elif sys.argv[1] == '-s':
            if cnt == 4:
                return 'search'
            else:
                return 'Usage -s'
    elif cnt == 2:
        if sys.argv[1] == '-h' or sys.argv[1] == '--help':
            return 'help'
    return 'no argv'    

#TODO: REMOTE FUZZ
def startRemoteTcpFuzz(cnt):
    inputPath = sys.argv[3]
    outputPath = 'Report/fuzzreport'
    IPaddress = sys.argv[7]
    port = sys.argv[8]
    if cnt == 9 :
        payload = "afl-fuzz -i "+ inputPath + " -o " + outputPath + \
            " -Q -- ./source/fuzzentry/fuzzentry" + " " + IPaddress + " " + port
        os.system(payload)
    else :
        return 1

def startNormalFuzz():
    inputPath = sys.argv[3]
    outputPath = 'Report/fuzzreport'
    elfPath = sys.argv[7]
    # file input
    if sys.argv[8] == '@@':
        payload = "afl-fuzz -i "+ inputPath + " -o " + outputPath + \
            " -Q -- "+ elfPath +" @@"
    # stdin input
    else:
        payload = "afl-fuzz -i "+ inputPath + " -o " + outputPath + \
            " -Q -- "+ elfPath
    os.system(payload)
    return 


#TODO 仿真模式
def qemu_firm():
    return 


def start():
    
    mode = checkArgc(len(sys.argv))
    if mode == 'no argv':
        print("please use './afa.py --help/-h' for more information!")
        exit()
        
    elif mode == 'search':
        printTable()
        searchInfo()
        
    elif mode == 'fuzz-local-tcp':
        printTable()
        startLocalTcpFuzz(len(sys.argv))
    
    elif mode == 'fuzz-remote-server':
        printTable()
        startRemoteTcpFuzz(len(sys.argv))
        
    elif mode == 'fuzz-normal':
        printTable()
        startNormalFuzz(len(sys.argv))
    
        
    elif mode == 'firmqemu':
        printTable()
        qemu_firm()
    
    elif mode =='Usage -s':
        print("usage: please use ./afa.py -s <firmware_path> <report.txt>")
        exit()
        
    elif mode =='Usage -f':
        print("usage: please use ./afa.py -f -i <input_floder> -M <option> -- [elf_path] [IPaddress] [port]")
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