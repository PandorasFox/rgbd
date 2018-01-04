# RGBD

I'm writing a daemon for controlling my ws2812B RGB LED strips with my raspberry pi.

The main purpose behind most of this is so that I can easily dim the brightness on the lights (or change the lighting patterns/mood) from my phone, in my bed. Really.

The eventual goals are outlined in spec.txt. They're subject to change.

Uses [rpi\_ws281x](https://github.com/jgarff/rpi_ws281x) and [colour](https://pypi.python.org/pypi/colour).

You *must* be controlling your pi over SPI for this, so it can run as a non-root user. Specifically, you'll probably need to modify your `/boot/config.txt` as outlined in `rpi\_ws281x`'s readme.

DBUS is used for passing messages from the ctl script to the daemon. A sample dbus conf file is included; daemon details are still being fleshed out for where it will run from/etc.

## Wiring

My wiring setup is as follows:

* Single pin connector from SPI 0 (GPIO 10) to DIN on the LED Strip
* Raspi ground to ground on the LED Strip
* Positive from a power supply to the 5V power line on the strip
* Ground back into the negative on the power supply.

A 3.3V -> 5V voltage step is not required for the WS2812B, since (most) 2812B strips take 3.3-5V DIN, since DIN and power have been decoupled and no longer need to be run at the same voltage.

## Setup

Install [rpi\_ws281x](https://github.com/jgarff/rpi_ws281x) and [colour](https://pypi.python.org/pypi/colour). Make sure to follow the instructions for SPI as given in the `rpi_ws281x` repo.

Currently, the upstream version of `rpi_ws281x` has a bug that prevents using SPI as non-root; I've fixed the bug [here](https://github.com/pandorasfox/rpi_ws281x). Once it gets merged, this will no longer be needed.

## Usage

For now, the only part of this entire project that requires `sudo` is placing the `dbus` conf file in `dbus-rules` into `/etc/dbus-1/system.d/`.

After that, you can copy the included `config.json` to `~/.config/rgbd/config.json`, and copy the animations directory to `~/.local/share/rgbd/animations/`.

You can then run `rgbd` by invoking `./lightctl start`.

Systemd unit files are planned on being included, as is an installer script.

I also need to figure out how to fully decouple lightctl from the scripts - they need to be importable somehow (or I just need to install to ~/.local/share).

I also need to look into the dbus session bus and launching that ourselves.
