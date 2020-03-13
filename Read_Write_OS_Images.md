[Background](Background.md) / [Purpose](Purpose.md) / [**Getting Started**](Getting_Started.md) / [Cluster Guide](Cluster_Guide.md)

1. [Hardware](Hardware.md) - General Pi hardware information, specifications, costs and overclocking
2. [Software](Software.md) - High-level operating system and software information
3. [Formatting SD Cards](Formatting_SD_Cards.md) - A quick-guide on how to format SD cards
4. [**Read & Write Images**](Read_Write_OS_Images.md) - A quick-guide on how to flash, write, and read operating system images
5. [Installing NOOBS](Installing_NOOBS.md) - A guide on how to install the NOOBS operating system installer
6. [Installing Raspbian](Installing_Raspbian.md) - A guide on how to install Raspbian into your Pi
7. [Internet Connection](Internet_Connection.md) - Information on how to connect your Pi to the internet
8. [Software Updates](Software_Updates.md) - How to update and upgrade operating system, software and hardware
9. [Miscellaneous](Miscellaneous.md) - Other "good-to-know" information

#  

<img src="https://image.flaticon.com/icons/svg/2305/2305882.svg" width="100px" height="100px"/> <img src="https://image.flaticon.com/icons/svg/1126/1126863.svg" width="100px" height="100px"/> <img src="https://image.flaticon.com/icons/svg/337/337931.svg" width="100px" height="100px"/>


# Read & Write OS Images

Operating system images are similar but different from zipped files. Similar because contents are "compressed" but different because an image cannot be extracted like a zip file.

It is worth mentioning that sometimes images can come in zip format. The reason for that is to compress the image even further and have a lighter file.

* [Read Images](#read-images)
* [Write Custom Images](#write-custom-images)


## Read Images

[Win32 Disk Imager](https://sourceforge.net/projects/win32diskimager/) is strictly for Windows operating system.

1. Download [Win32 Disk Imager](https://sourceforge.net/projects/win32diskimager/)
1. Install Win32 Disk Imager
1. Open Win32 Disk Imager
1. Write the Image file destination path (blue folder to browse)
    * Make sure file name ends with ".img"
    * Image will be stored in the folder location specified with the file name given
        * Example: `C:\Users\gitluis\Desktop\your-image-file-name.img`
1. Select the Device (micro SD drive)
1. Click on Read
1. Done


## Write Custom Images

1. Format your micro SD card ([how-to](Formatting-SD-Cards))
2. Download [Raspberry Pi Imager](Formatting-SD-Cards#raspberry-pi-imager-downloads)
3. Install Raspberry Pi Imager in your computer
4. Open Raspberry Pi Imager
5. Click on `Choose OS`

<img src="https://i.ibb.co/YX9fHVk/format-sd-card-1.png" width="600px" height="400px"/>

6. Select `Use custom`

<img src="https://i.ibb.co/dLsRmsB/format-sd-card-2.png" width="600px" height="400px"/>

7. Navigate to your `image.img` file and open it (images supported: *.img, *.zip, *.gz, *.xz)

<img src="https://i.ibb.co/qDTKwjm/format-sd-card-3.png" width="600px" height="400px"/>

8. Click on `Choose SD Card`

<img src="https://i.ibb.co/g7LRvG2/format-sd-card-4.png" width="600px" height="400px"/>

9. Select your micro SD card

<img src="https://i.ibb.co/KFdTMV4/format-sd-card-5.png" width="600px" height="400px"/>

10. Click on `Write`

<img src="https://i.ibb.co/1K0m4Sc/format-sd-card-6.png" width="600px" height="400px"/>

10. The image will start being written to the micro SD card and verify its contents
11. Wait until it finish
12. Done
