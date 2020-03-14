[Background](Background.md) / [Purpose](Purpose.md) / [Getting Started](Getting_Started.md) / [Cluster Guide](Cluster_Guide.md)


<img src="https://image.flaticon.com/icons/svg/2126/2126739.svg" width="100px" height="100px"/>


# Clone OS

We will use Raspbian for this quick-guide on how to install an operating system and then clone that image so that you avoid repeating steps.


## Install Raspbian

1. Install Raspbian
1. Update Raspbian
1. Upgrade Raspbian

Refer to the [Installing Raspbian](Installing_Raspbian.md) page to install Raspbian into one of your micro SD cards.


## Clone Image

After you have successfully installed, updated and upgraded a clean Raspbian OS image, we need to do the following:
1. Turn off your Raspberry Pi
```
sudo shutdown now
```
2. Insert the micro SD card into your laptop or computer (not the raspberry pi)
3. Read the Raspbian pre-installed image ([How-to Read Images](Read_Write_OS_Images.md#read-images))
4. Save the image as `raspbian-preinstalled-cluster.img`

Now for each micro SD card you have (excluding the one with Raspbian on it), we do the following:
1. Insert micro SD card into your laptop or computer (not the Raspberry Pi)
1. Format the micro SD card ([How-to Format SD Cards](Formatting_SD_Cards.md#format-sd-card))
1. Write the `raspbian-preinstalled.img` to the micro SD card ([How-to Write Images](Read_Write_OS_Images.md#write-custom-images))

That's it, you are done!
