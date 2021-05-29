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
rm -rf twemoji
cd build/twemoji
for i in `find -name "*-*"`; do rm $i; done
cd ../..
python3 build.py
cd build/twemoji
for i in *; do mv $i ../EverIslandResources/assets/minecraft/textures/font/twemoji_$i;done
