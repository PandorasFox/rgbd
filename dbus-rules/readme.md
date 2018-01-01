# dbus rules

I placed this file in `/etc/dbus-1/system.d/rgbd.conf`. The specific location may vary depending on your system.

The system bus is used because (at least on my pi), there's no X session and thus no session bus.

If in the future, I can get the daemon to run as a regular non-root user, I'll see about it managing its own dbus session.
