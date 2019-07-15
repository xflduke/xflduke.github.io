# Passthrough egpu on manjaro

* [前言](#前言)
* [环境准备 Prepare your environment](#环境准备-prepare-you-environment)
  * [CPU支持intel-VT-d 或者 AMD-d](#cpu支持intel-vt-d-或者-amd-d)
  * [主板IOMMU支持](#主板支持iommu)
  * [UEFI支持（非必须）](#uefi支持非必须)
* [Linux主机屏蔽egpu](#linux主机上屏蔽egpu)
* [加载模块管理里面屏蔽egpu所在组的IOMMUid](#加载模块管理里面屏蔽egpu所在组的IOMMUid)
* [配置libvirt](#配置libvirt)
* [安装guestOS](#安装guestos)
* [配置PCI Passthrough](#配置pci-passthrough)
* [完成图](#完成图)

## 前言

基于Manjaro linux下的KVM虚拟机的egpu passthrough

- 检证环境(具体要求参照下面的环境准备)
- 
  - NUC8iBEH（__i5-8259u__）
  - __egpu__ AORUS Nvida GTX 1080
  - Manjaro Linux（Kernel __4.19.49-1__）
  - qumu 4.0.0-2
  - libvirt 5.4.0-1
  - ovmf 1
- 以下基于上面的检证环境，具体由于BIOS/UEFI,Linux版本不同会有一定差异
  [有不明白的地方多看看Arch Linux Wiki](https://wiki.archlinux.org/index.php/PCI_passthrough_via_OVMF)

- Manjaro Linux安装参照 [Manjaro Install Guide](https://manjaro.org/support/firststeps/#install-manjaro)

- 需要的linux包请自行通过pacman或者界面管理器安装

## 环境准备 Prepare you environment

### CPU支持intel-VT-d 或者 AMD-d

- 设置方法

  - 开机进入BIOS（DEL，F2之类按键的其中一个，具体看主板）
  - 设置VT-x，VT-d（AMD CPU设置AMD-v）  
- 验证方法
  - `cat /proc/cpuinfo | grep vm`
    在结果里面查看下面关键字
     Intel：vmx，AMD：svm

### 主板IOMMU支持

- 设置方法
  - Kernel启动参数里面追加
    1. grub2引导的按照以下顺序追加
     `sudo vi /etc/default/grub`
     在命令行参数中加入intel_iommu=on
     `GRUB_CMDLINE_LINUX="intel_iommu=on"`
    2. 重新生成grup.conf
     `sudo grub-mkconfig -o /boot/grub/grub.cfg`
    3. `reboot`

- 验证方法
  - `dmesg | grep -i -e DMAR -e IOMMU` 
     关键字：OMMU: enabled

- 查看IOMMU分组

  ```bash
  #!/bin/bash
  shopt -s nullglob
  for g in /sys/kernel/iommu_groups/*; do
  echo "IOMMU Group ${g##*/}:"
      for d in $g/devices/*; do
          echo -e "\t$(lspci -nns ${d##*/})"
      done;
  done;
  ```

- 记住显卡所在分组，并确保没有其他设备和显卡在同一分组。
  如不在同一分组，可能需要打内核补丁隔离

### UEFI支持（非必须）

- 设置方法
  - 略

## Linux主机屏蔽egpu

因为需要passthrough，主机不能占有egpu，所以需要明确屏蔽掉egpu，实现是stub方式

## 加载模块管理里面屏蔽egpu所在组的IOMMUid

- 设置方法
  - 配置文件
    1. `sudo vi /etc/modprobe.d/vfio.conf`
    没有的话创建新文件，并添加以下部分（10de:13c2,10de:0fbb 替换成IOMMU分组里面的egpu所在的全部id）
    1. `options vfio-pci ids=10de:13c2,10de:0fbb`
  - 初期化配置
    1. `sudo vi /etc/mkinitcpio.conf`
    在文件中的MODULES和HOOKS里面分别添加以下模块

    ```bash
    MODULES=(... vfio_pci vfio vfio_iommu_type1 vfio_virqfd ...) 
    HOOKS=(... modconf ...)
    ```

  - 重新生成initramfs
    1. `sudo mkinitcpio -c /etc/mkinitcpio.conf -g /boot/linux-custom.img`
    2. 用生成的img替换掉系统默认的img，或者在grup启动脚本里添加这个内核的启动项
  
  - reboot

  - 验证方法
    - `sudo dmesg | grep -i vfio`
    有类似下面的日志，dmesg日志缓冲区大小有限，建议reboot之后立即确认

      ```bash
      [    0.329224] VFIO - User Level meta-driver version: 0.3
      [    0.341372] vfio_pci: add [10de:13c2[ffff:ffff]] class 0x000000/00000000
      [    0.354704] vfio_pci: add [10de:0fbb[ffff:ffff]] class 0x000000/00000000
      [    2.061326] vfio-pci 0000:06:00.0: enabling device (0100 -> 0103)
      ```

## 配置libvirt

- 添加ovmf固件
  1. `sudo vi /etc/libvirt/qemu.conf`
  2. 添加以下设定
  `nvram = ["/usr/share/ovmf/x64/OVMF_CODE.fd:/usr/share/ovmf/x64/OVMF_VARS.fd"]`
  3. 启动服务

  ```bash
  sudo systemctl enable libvirtd.service
  sudo systemctl start libvirtd.service
  sudo systemctl enable virtlogd
  sudo systemctl start virtlogd
  ```

## 安装guestOS

- 安装方法：略 （验证中用的名字：guest）
- 配置方法：参照自己实际的CPU，MEM，SSD配置来决定

## 配置PCI Passthrough

- 按照egpu所在的IOMMU组里面的设备添加
- 修改配置文件
  1. `sudo virsh edit guest` REM guest是创建虚拟机实体的名字
  2. 在`<features>/<hyperv>`块中的最后添加
   `<vendor_id state='on' value='123456789ab'/>` REM value任意，建议12位
  3. 在`<features>/<hyperv>`的块后面添加

  ```bash
    <kvm>
      <hidden state='on'/>
    </kvm>
  ```

## 完成图
![IMG](images/egpu_passthrough.png)