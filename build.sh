#!/bin/bash

rm -rf build
rm -rf twemoji
mkdir build
git clone https://github.com/twitter/twemoji.git --depth 1
cd twemoji
git fetch origin gh-pages:gh-pages --depth=1
git checkout gh-pages
cp -r v/latest/72x72 ../build/twemoji
cd ..
cd build/twemoji
for i in `find -name "*-*"`; do rm $i; done
cd ../..
python3 build.py
cd build/twemoji
for i in *; do 
    python3 ../../downscale.py $i
    mv $i ../EverIslandResources/assets/minecraft/textures/font/twemoji_$i
done
cd ../..
cp twemoji/LICENSE build/EverIslandResources/assets/minecraft/textures/font/LICENSE_twemoji
rm -rf twemoji

VERSION="v0.9"
for i in 7,"MC 1.17+" 6,"MC 1.16.2-1.16.5" 5,"MC 1.15-1.16.2" 4,"MC 1.13-1.14"; do IFS=","; set -- $i;
    color1="green"
    color2="light_purple"
    if [ "$1" -ge "6" ]; then
        color1="#3DFFB5"
        color2="#edc1fb"
    fi
    python3 build.py -v $1 -d "{\"text\":\"\",\"extra\":[{\"text\":\"EverMC\",\"color\":\"$color1\"},{\"text\":\" 资源包\",\"color\":\"$color2\"},{\"text\":\" $VERSION\",\"color\":\"white\"},{\"text\":\" ($2)\",\"color\":\"gray\"}]}"
    cd build/EverIslandResources
    zip -r ../EverMCResources-$2.zip ./*
    cd ../..
done
