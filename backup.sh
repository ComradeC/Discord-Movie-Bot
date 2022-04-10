#!/bin/sh
cd ..
if [ ! -d "backup" ]; then
  mkdir backup
fi
cd Discord-Movie-Bot
cp golden_quotes.json ../backup/golden_quotes.json
cp movie_list.json ../backup/movie_list.json