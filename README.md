# Automated Firmware Analysis(AFA)

Automated Firmware Analysis(AFA) 是Linux平台下针对固件分析的集成化命令行工具，在QEMU和AFL++的基础上进行设计实现。可以对多种类型和架构的固件完成静态分析、动态仿真、功能模块模糊测试以及敏感信息搜集，并保存相应报告结果。

Automated Firmware Analysis(AFA) is a command-line tool for the Linux platform, based on QEMU and AFL++. It can perform static analysis，simulation of firmware for different types and architectures of devices, fuzz functional modules, and automatically generate report files.

## Install

```sh
 ./setup.sh
```

## usage

### 环境模拟（仍在施工）

​	输入：固件文件路径、固件类型

​	输出：可供调试的固件仿真环境

### 敏感信息搜集

```sh
./afa.py -s <firmware_path> <report.txt>
```

- 固件和分解的文件系统都在目录images下
- 报告默认保存在Report/info-report/<report.txt>

### 固件功能模块测试

我们在AFL++的基础上进行改进，增添了对使用socket进行数据传输的二进制程序的模糊测试功能。其中`mode`共有三个模式：

- `local server`模式

    **local server**模式指在本地对二进制server服务进行模糊测试，需要保证server程序可以在本机运行，使用方式如下：
    
    ```sh
    sudo su
    ./afa.py -f -i <input_floder> -m local-sever -- <srv_elf_path> <ip> <remote>
    ```
    **注意：使用此功能时请保证root权限，防止端口开启出现问题**

- `remote server`模式

    **remote server**模式可以直接对远端正在运行的服务进行模糊测试，只需要服务对应的ip和port即可，使用方式
    
    ```sh
    ./afa.py -f -i <input_floder> -m remote-sever -- <ip> <remote>
    ```

    **注意：由于模糊测试可能会导致服务crash，所以对在运行服务测试时，必须获得被测试方授权同意，此外被测试服务应有自动重启功能，以免影响正常运营。使用本工具导致的违法违规行为，皆与本工具无关。**

- `normal`模式
    
    **normal**模式，为传统的AFL++功能，可以从STDIN和文件中进行读入，使用方式如下：
    ```sh
    ./afa.py -f -i <input_floder> -m normal -- <elf_path>       #标准输入模式
    ./afa.py -f -i <input_floder> -m normal -- <elf_path> @@    #文件读入模式
    ```




