[Background](Background.md) / [Purpose](Purpose.md) / [Getting Started](Getting_Started.md) / [Cluster Guide](Cluster_Guide.md)


<img src="https://image.flaticon.com/icons/svg/2482/2482403.svg" width="100px" height="100px"/>
<img src="https://image.flaticon.com/icons/svg/888/888929.svg" width="100px" height="100px"/>


# Front-end Desktop

There is a wide variety of linux distribution desktop environments. While you can search and install the ones you prefer the most, we wanted to complete this section by adding how to install some of the most common desktop environments in the Linux world.

# Ubuntu Desktop Environment

The Ubuntu desktop environments are very well known and most common due to Ubuntu's different flavors across Linux-based systems. These shall work on any linux-based OS, although that may not be the case for **Raspbian**.

**Note**: These commands **do not work** on a Raspberry Pi with Raspbian installed.

## Installing a Desktop Environment

Use one of the following commands to install a desired Ubuntu desktop environment
```cli
sudo apt install ubuntu-desktop
sudo apt install ubuntu-bungie-desktop
sudo apt install lubuntu-desktop
sudo apt install xubuntu-desktop
```

**Note**: If it asks for a display manager, select the bottom or last option.

Reboot board
```cli
shutdown -r now
```

If desktop GUI does not starts upon boot, start it manually as follows
```cli
startx
```

Upon boot, at the login screen and **select the desktop session you just installed**.
