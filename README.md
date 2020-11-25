## Raspberry Pi Control

This is just a Tkinter-based GUI for controlling multiple Raspberry Pis which are running our usual experimental optogenetic protocols. It includes timers for each well and a history of commands issued. It's ugly but it works. Soon to be added: log of experiments and commands, video streaming. 

------
You can run it on OS X by just clicking the file in "dist"
------


Description of commands:

**Flashing Lights**: Specify a frequency and pulse width for regular and repeated pulses of light *ad infinitum*.

**Paired Pulse**: A protocol for producing two pulses of light of pre-determined duration and relative timing.

**Blocks**: (we don't really use this protocol anymore), but runs Flashing Lights but with a slower "envelope", i.e. there are periods in which it will periodically flash the lights like Flashing Lights and periods in which it won't turn the lights on at all


Notes for installing a new Raspberry Pi:
-- Assemble the behavior box, installing the camera, screen, ethernet, etc.
-- Download the Raspian build here: https://downloads.raspberrypi.org/raspbian/images/raspbian-2017-12-01/
-- Unzip the image and place it onto an SD card as described here, depending on the OS you'll use to write the image: https://www.raspberrypi.org/documentation/installation/installing-images/
-- Boot the raspberry pi from the SD card.
-- Use apt-get to install gstreamer on the Raspberry Pi (Debian) as described here: https://gstreamer.freedesktop.org/documentation/installing/on-linux.html?gi-language=c
  -- In our lab, it's necessary to add a specific configuration file to /etc/apt to allow it to navigate the institution's firewall / network. Otherwise all apt commands fail.
-- Install MP4Box as described here: https://www.raspberrypi.org/documentation/usage/camera/raspicam/raspivid.md
-- Enable SSH and the camera module.
-- From another Pi, copy .py files from /home/pi and /home/pi/stimuli.
  -- If using a custom configuration also, copy /home/pi/config.
  -- This can be done manually or with the scp command.
-- Restart the Pi.

Note: it is also necessary to load custom code onto the Arduino to control the lights. This Raspberry Pi Control will automatically work with the arduino.

