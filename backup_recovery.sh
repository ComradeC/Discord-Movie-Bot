#!/bin/sh
cd ..
if [ ! -d "backup" ]; then
  cp ./backup/golden_quotes.json ./Discord-Movie-Bot/golden_quotes.json
  cp ./backup/movie_list.json ./Discord-Movie-Bot/movie_list.json
fi
