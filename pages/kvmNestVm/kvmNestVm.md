# purpose : kvm nested virtualization

<a href="https://xflduke.github.io/">Back to Index</a>

- [purpose : kvm nested virtualization](#purpose--kvm-nested-virtualization)
  - [环境](#%e7%8e%af%e5%a2%83)
  - [注意事项](#%e6%b3%a8%e6%84%8f%e4%ba%8b%e9%a1%b9)
  - [配置](#%e9%85%8d%e7%bd%ae)

## 环境

- L0主机：manjaro
- L1虚拟机：centos7.0

## 注意事项

- Intel，AMD的对照表在下面,后面的记述都是基于IntelCPU说明
  - CPU硬件虚拟化技术支持：intel VT-d <-> AMD-v (确认方法:BIOS)
  - CPU命令集：vmx <-> svm （确认方法：`cat /proc/cpuinfo | grep -E "(vmx|svm)"`）

- 目前支持虚拟机嵌套的有主要有KVM,XEN,VMwareESiX,Hyper-v(201907)

## 配置

- 修改虚拟机域配置的cpu模式为passthrough
  - 列出配置的虚拟机
  - `sudo virsh list`
  - 在里面找到要配置的虚拟机
  - `sudo virsh edit <虚拟机域名>`
  - 更改cpu模式为passthrough
  - `<cpu mode='host-passthrough'>`
- 修改KVM设定打开cpu nested支持
  - 切换到root用户
  - `su`
  - 添加modprobe配置文件
  - `echo options kvm_intel nested=1 >> /etc/modprobe.d/kvm-nested.conf`
  - 重新加载kvm intel(注意：在这一步操作之前需要首先停止虚拟机)
  - `modprobe -r kvm_intel`
  - `modprobe kvm_intel`
  - 确认修改结果（Y：有效）
  - `cat /sys/module/kvm_intel/parameters/nested`
- 启动虚拟机确认
  - `cat /proc/cpuinfo | grep -E "(vmx|svm)"`
  - 看到cpu指令集多出来很多，其中有虚拟化的指令即可

<a href="https://xflduke.github.io/">Back to Index</a>
