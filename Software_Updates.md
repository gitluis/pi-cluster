[Background](Background.md) / [Purpose](Purpose.md) / [Getting Started](Getting_Started.md) / [Cluster Guide](Cluster_Guide.md)


<img src="https://image.flaticon.com/icons/svg/1857/1857091.svg" width="100px" height="100px"/>
<img src="https://image.flaticon.com/icons/svg/2562/2562026.svg" width="100px" height="100px"/>


# Software Updates

After the OS is installed in your Raspberry Pi, both, hardware and software may need to be updated and possibly upgraded to any recent firmware and operating system updates (if any).

Your Raspberry Pi will need to be connected to the internet via Ethernet or WiFi.

## How-to Update & Upgrade

Open a Terminal window (Ctrl+Alt+T) and run the following commands
```cli
sudo apt update -y
sudo apt full-upgrade -y
```

**Note**: These commands work only for debian-based linux distributions. If you are using a different linux distro you will have to search the software package manager that such distro uses to install software from the command line. The same applies with Windows operating systems.
