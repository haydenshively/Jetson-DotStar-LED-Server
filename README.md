# Jetson-DotStar-LED-Server

I wrote this code so that IFTTT and Google Assisstant could control the LEDs on a shelf I built.
The server itself is pretty simple (and not very professional) but it works.

When I set all of this up, the only way to enable the Jetson Nano's SPI interface was to manipulate
an Excel sheet provided by NVIDIA, run a macro that generated config files, and re-flash the device
with those files in a special directory of the SD card. This was not a simple process and it took
many tries to get right, but since then it seems Nvidia has made things easier --
[see here](https://www.jetsonhacks.com/2020/05/04/spi-on-jetson-using-jetson-io/).

[This](https://www.jetsonhacks.com/nvidia-jetson-nano-j41-header-pinout/) pinout mapping for
the J41 header will also prove useful if you're trying to replicate this project.

## Requirements

You'll need to install Adafruit's `dotstar` library, but other than that everything is standard Python.

## Running

If you have a firewall enabled (such as `ufw`, make sure to open the HTTP port. Modify the paths and IPs
in the `start.sh` and `start_with_tmux.sh` files, `chmod +x` them, and you should be good to go. Since
I don't have a static IP, I've designed this to SSH into a GCP machine (which does have a static IP) and
forward the ports. You may not want/need to do that.
