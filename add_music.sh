#!/bin/sh
# Add music to the generated animation video file
IN=anim/anim.mp4
OUT=anim/animm.mp4
MUSIC=music/elevator-music-stretched.mp3
ffmpeg -i $IN -i $MUSIC -c:v copy -c:a aac -strict experimental $OUT
