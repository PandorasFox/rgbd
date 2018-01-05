# RGBD

I'm writing a daemon for controlling my ws2812B RGB LED strips with my raspberry pi. Security is something of a concern, so this is written so as to never actually require root.

The main purpose behind most of this is so that I can easily dim the brightness on the lights (or change the lighting patterns/mood) from my phone, in my bed. Really.

Uses [rpi\_ws281x](https://github.com/jgarff/rpi_ws281x) and [colour](https://pypi.python.org/pypi/colour).

You *must* be controlling your pi over SPI for this, so it can run as a non-root user. Specifically, you'll probably need to modify your `/boot/config.txt` as outlined in `rpi\_ws281x`'s readme.

DBUS is used for passing messages from the ctl script to the daemon. If you don't have a dbus session bus (i.e. from an X session), I've included some systemd unit files.

## Wiring

My wiring setup is as follows:

* Single pin connector from SPI 0 (GPIO 10) to DIN on the LED Strip
* Raspi ground to ground on the LED Strip
* Positive from a power supply to the 5V power line on the strip
* Ground back into the negative on the power supply.

A 3.3V -> 5V voltage step is not required for the WS2812B, since (most) 2812B strips take 3.3-5V DIN, since DIN and power have been decoupled and no longer need to be run at the same voltage.

## Setup

Install [rpi\_ws281x](https://github.com/jgarff/rpi_ws281x) and [colour](https://pypi.python.org/pypi/colour) (not strictly needed, but handy for animations). Make sure to follow the instructions for SPI as given in the `rpi_ws281x` repo.

Currently, the upstream version of `rpi_ws281x` has a bug that prevents using SPI as non-root; I've fixed the bug [here](https://github.com/pandorasfox/rpi_ws281x). Once it gets merged, this will no longer be needed.

## Installing

```
git clone https://github.com/pandorasfox/rgbd && cd rgbd
chmod +x ./installer
./installer install
```

You can specify a variety of options to the installer for where files get installed to.

To use `lightctl`, make sure its install dir is in your `$PATH`. By default, it installs to `~/.local/bin`.

You must be a member of the `gpio` group in order to run this code.

## Usage

After installing the files, you should be able to just `systemctl --user enable --now rgbd`. You may need to tweak your config file.

## This project and root/sudo

A big part of why I wrote this daemon is so that animations can be dynamically loaded, and for good dynamic control of my lights. If something is going to be dynamically loading and executing script files, _it should not be doing that as root_.

This left me with a few options:

* Run the animation scripts in a separate downgraded process, with limited shared resources. Pretty workable, but difficult to rig up animation timings.
* Disallow dynamic config loading (boo).
* Set up a root daemon we can control (less performant/communication is hard)
* Run everything as our own user.

The last option was the best, but required a decent amount of setup to get right.

If you want the script to persist beyond your session, then you _will_ need `sudo` rights to set some loginctl stuff, but that's it. For all regular usage, it can just stay running as a user daemon without any need for elevated permissions, ever.
