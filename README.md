# Automated Firmware Analysis(AFA)

Automated Firmware Analysis(AFA) 是Linux平台下针对固件分析的集成化命令行工具，在QEMU和AFL++的基础上进行设计实习。可以对多种类型和架构的固件完成静态分析、动态仿真、功能模块模糊测试以及敏感信息搜集，并保存相应报告结果。

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

其中`<input_floder>`是用于存放测试输入的文件夹路径，`<output_floder>` 是用于存放测试输出的文件夹路径

#### 标准输入模糊测试

```sh
./afa.py -f -i <input_floder> -o <output_floder> -- <elf_path>
```

#### 文件输入模糊测试

利用`@@`替换命令行运行时的`argv`传入参数
```sh
./afa.py -f -i <input_floder> -o <output_floder> -- <elf_path> @@
```




