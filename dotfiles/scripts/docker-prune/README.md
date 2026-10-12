# docker-prune

Weekly cleanup of docker state unused for 30 days (override with `DAYS=`):

- removes stopped containers that last ran more than 30 days ago (by
  `State.FinishedAt`, not creation time like `docker container prune`)
- removes unused images older than 30 days
- removes **all** volumes not attached to a container — so a volume lives as
  long as its container does, but anything orphaned (e.g. after
  `docker compose down`) goes on the next run. Don't keep data in volumes.
- leaves networks alone: they cost nothing, and shared `external` ones (e.g.
  `unmade`) look unused whenever their containers are stopped
- removes build cache not used in 30 days

Runs as the user via the `docker` group; no root needed.

## Install (per machine)

Symlink the units so a `git pull` keeps them up to date:

```sh
mkdir -p ~/.config/systemd/user
ln -s ~/scripts/docker-prune/docker-prune.{service,timer} ~/.config/systemd/user/
systemctl --user daemon-reload
systemctl --user enable --now docker-prune.timer
```

## Useful commands

```sh
# see which containers would go
~/scripts/docker-prune/docker-prune -n

# run it now
systemctl --user start docker-prune.service

# next scheduled run / past output
systemctl --user list-timers docker-prune.timer
journalctl --user -u docker-prune
```
