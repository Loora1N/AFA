# Automated Firmware Analysis(AFA)

Automated Firmware Analysis(AFA) is a command-line tool for the Linux platform, based on QEMU and AFL++. It can perform static analysis，simulation of firmware for different types and architectures of devices, fuzz functional modules, and automatically generate report files.

## Install

```sh
 ./setup.sh
```

## 使用方式

#### 环境模拟

​	输入：固件文件路径、固件类型

​	输出：可供调试的固件仿真环境

#### 敏感信息搜集

​	输入：固件文件路径

​	输出：敏感信息报告

#### 固件功能模块测试

​	输入：固件功能模块路径、模块测试输入用例

​	输出：模糊测试结果报告
