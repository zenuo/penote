#!/bin/bash
nohup /usr/bin/python3.6 -m penote.app > /dev/null 2>&1 &
tail --retry -f -n 0 ./logs/info.log ./logs/error.log
