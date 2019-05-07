#!/usr/bin/env python

import sys
import json


from subprocess import run

BLOCK_PADDING = 40  # px


def pad_blocks(blocks):
    for block in blocks:
        block["separator_block_width"] = 40
    return blocks


def add_now_playing_block(blocks):
    status = run(["playerctl", "status"], capture_output=True).stdout.decode().strip()
    if status != "Playing":
        return blocks
    process = run(
        ["playerctl", "metadata", "--format", "{{ artist }} - <b><i>{{ title }}</i></b>"],
        capture_output=True
    )
    now_playing = process.stdout.decode().strip()
    now_playing_block = {
        "full_text": f"🎵: {now_playing}" if now_playing else "",
        "name": "Now Playing",
        "markup": "pango"
    }
    return [now_playing_block, *blocks]


def print_line(message):
    """ Non-buffered printing to stdout. """
    sys.stdout.write(message + "\n")
    sys.stdout.flush()


def read_line():
    """ Interrupted respecting reader for stdin. """
    # try reading a line, removing any extra whitespace
    try:
        line = sys.stdin.readline().strip()
        # i3status sends EOF, or an empty line
        if not line:
            sys.exit(3)
        return line
    # exit on ctrl-c
    except KeyboardInterrupt:
        sys.exit()


if __name__ == "__main__":
    # Skip the first line which contains the version header.
    print_line(read_line())

    # The second line contains the start of the infinite array.
    print_line(read_line())

    while True:
        line, prefix = read_line(), ""
        # ignore comma at start of lines
        if line.startswith(","):
            line, prefix = line[1:], ","

        blocks = json.loads(line)
        blocks = add_now_playing_block(blocks)
        blocks = pad_blocks(blocks)
        # and echo back new encoded json
        print_line(prefix + json.dumps(blocks))
