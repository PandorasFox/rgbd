# RGBD

I'm writing a daemon for controlling my ws2812B RGB LED strips with my raspberry pi.

The main purpose behind most of this is so that I can easily dim the brightness on the lights (or change the lighting patterns/mood) from my phone, in my bed. Really.

The eventual goals are outlined in spec.txt. They're subject to change.

Uses [rpi\_ws281x](https://github.com/jgarff/rpi_ws281x), [colour](https://pypi.python.org/pypi/colour), and [python-daemon](https://pypi.python.org/pypi/python-daemon/).

For a more performant version of `python-daemon`, please run the following command:

`sudo pip3 install git+https://github.com/PandorasFox/python-daemon`. 

You *must* be controlling your pi over SPI for this, so it can run as a non-root user. Specifically, you'll probably need to modify your `/boot/config.txt` as outlined in `rpi\_ws281x`'s readme.

DBUS is used for passing messages from the ctl script to the daemon. A sample dbus conf file is included; daemon details are still being fleshed out for where it will run from/etc.
