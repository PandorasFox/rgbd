Install these to `~/.local/share/systemd/user/`

If you want the daemon to run after (or before) you log out, do: `sudo loginctl enable-linger $(whoami)`.

That _should_ be the only `sudo` needed for this entire project, from `git clone` to having your RGB strip painting your walls with a rainbow.
