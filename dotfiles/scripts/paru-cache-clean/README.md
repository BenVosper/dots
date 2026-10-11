# paru-cache-clean

Weekly trim of paru's AUR build cache (`~/.cache/paru/clone`):

- keeps the newest 2 built versions of each installed package
- removes built packages that are no longer installed
- removes downloaded source `*.tar.gz` files older than 30 days
- deletes clone dirs whose packages are all uninstalled

Needs `pacman-contrib` (for `paccache`).

## Install (per machine)

Symlink the units so a `git pull` keeps them up to date:

```sh
mkdir -p ~/.config/systemd/user
ln -s ~/scripts/paru-cache-clean/paru-cache-clean.{service,timer} ~/.config/systemd/user/
systemctl --user daemon-reload
systemctl --user enable --now paru-cache-clean.timer
```

## Useful commands

```sh
# run it now
systemctl --user start paru-cache-clean.service

# next scheduled run / past output
systemctl --user list-timers paru-cache-clean.timer
journalctl --user -u paru-cache-clean
```
