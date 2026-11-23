#!/bin/sh
# Junta vídeo mudo + mix final.  Uso: sh mux.sh video_mudo.mp4 mix.wav saida.mp4
ffmpeg -y -v error -i "$1" -i "$2" -map 0:v -map 1:a -c:v copy -c:a aac -b:a 320k -shortest -movflags +faststart "$3" && echo "ok $3"
