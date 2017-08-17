#!/bin/bash

url='http://unixmanga.nl/onlinereading/manga-lists.html'

path="$(pwd)"
path="$path/manga"

if [ $# -gt 0 ]
then
    path="$1"
fi

list=$(wget -O- "$url" 2>/dev/null | grep '^<a href="http://unixmanga.nl/onlinereading/' | sed -r 's/.+(http:.+html).+/\1/')

for i in $list
do
    echo "Start downloading $i"
    ../manga.py -p -i -d "$path" -u "$i"
done
