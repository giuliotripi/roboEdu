#!/bin/bash

videoDuration=$(ffprobe -i "/home/yolo/reg.mkv" -show_entries format=duration -v quiet -of csv="p=0")
ffmpeg -ss 0:20:0 -i "/home/yolo/reg.mkv" -t 2 -r 0.5 "/home/yolo/reg.jpg"
python3 "/home/yolo/lezioni-carica-telegram.py" "/home/yolo/reg.mkv" "$1" "$2" "$3" "$4" "$videoDuration" "/home/yolo/reg.jpg"
