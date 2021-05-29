# -*- coding: utf-8 -*-
from PIL import Image, ImageColor, ImageDraw, ImageOps
from bdfparser import Font
import yaml
import json
from pathlib import Path
import os

font = Font("wenquanyi_10pt.bdf")

def proc(text_string):
    ac = None
    for char in list(text_string):
        if ac == None:
            ac = font.glyph(char).draw()
        else:
            ac = ac.concat(font.glyph(char).draw())
    im = Image.frombytes("RGBA", (ac.width(), ac.height()), ac.tobytes("RGBA", { 0: b'\x00\x00\x00\x00', 1: b'\xff\xff\xff\xff', 2: b'\xff\x00\x00\xff' }))
    return im

def proc_theme1(text_string, rgba1, rgba2):
    im = proc(text_string)
    if (im.height != 14):
        return None
    width = im.width + 3
    image = Image.new("RGBA", (width, 16))
    draw = ImageDraw.Draw(image)
    for i in range(0, width):
        weight = i/(width-1)
        rgba = tuple(map(lambda x, y: int(x + y), tuple(i * weight for i in rgba1), tuple(i * (1-weight) for i in rgba2)))
        draw.line([(i,0),(i,16)], rgba)
    rect = Image.new("RGBA", (width, 16))
    drawrect = ImageDraw.Draw(rect)
    drawrect.rectangle([0,0,width-1,15],fill=None,outline=(0,0,0,30))
    image.paste(rect, (0,0), rect)
    draw.bitmap((2,2), im)
    return image

def proc_theme2(text_string, rgba1, rgba2):
    im = proc(text_string)
    if (im.height != 14):
        return None
    width = im.width + 3
    image = Image.new("RGBA", (width, 16))
    draw = ImageDraw.Draw(image)
    for i in range(0, width):
        weight = i/(width-1)
        rgba = tuple(map(lambda x, y: int(x + y), tuple(i * weight for i in rgba1), tuple(i * (1-weight) for i in rgba2)))
        draw.line([(i,0),(i,16)], rgba)
    im2 = Image.new("RGBA",(width - 2, 14))
    im2.paste(im, (1,1), im)
    r,g,b,a = im2.split()
    image.paste(im2, (1,1), Image.merge("RGBA", (r,g,b,ImageOps.invert(a))))
    return image

def generate(text_string, rgba1, rgba2, code):
    directory = "build/EverIslandResources/assets/minecraft/textures/font"
    Path(directory).mkdir(parents=True, exist_ok=True)
    data = proc_theme1(text_string, rgba1, rgba2)
    data.save(directory + "/acidisland_{:03x}.png".format(code))
    data = proc_theme2(text_string, rgba1, rgba2)
    data.save(directory + "/acidisland_{:03x}.png".format(code + 0x800))

with open('config.yml', 'r', encoding='utf-8') as f:
    icons = yaml.safe_load(f)['icons']
    providers = []
    providers_uniform = []
    for icon in icons:
        color1 = ImageColor.getrgb(icon['color1'])
        color2 = ImageColor.getrgb(icon['color2'])
        text = icon['text']
        code = icon['code']
        generate(text, color1, color2, code)
        providers.append({
            "type": "bitmap",
            "file": "minecraft:font/acidisland_{:03x}.png".format(code),
            "height": 8,
            "ascent": 8,
            "chars": [
                chr(0xe000 + code)
            ]
        })
        providers.append({
            "type": "bitmap",
            "file": "minecraft:font/acidisland_{:03x}.png".format(code + 0x800),
            "height": 8,
            "ascent": 8,
            "chars": [
                chr(0xe800 + code)
            ]
        })
        providers_uniform.append({
            "type": "bitmap",
            "file": "minecraft:font/acidisland_{:03x}.png".format(code),
            "height": 8,
            "ascent": 7,
            "chars": [
                chr(0xe000 + code)
            ]
        })
        providers_uniform.append({
            "type": "bitmap",
            "file": "minecraft:font/acidisland_{:03x}.png".format(code + 0x800),
            "height": 8,
            "ascent": 7,
            "chars": [
                chr(0xe800 + code)
            ]
        })

    dirs = os.listdir("build/twemoji/")
    for file in dirs:
        code = int(file.replace(".png",""), 16)
        providers.append({
            "type": "bitmap",
            "file": "minecraft:font/twemoji_" + file,
            "height": 8,
            "ascent": 7,
            "chars": [
                chr(code)
            ]
        })
        providers_uniform.append({
            "type": "bitmap",
            "file": "minecraft:font/twemoji_" + file,
            "height": 8,
            "ascent": 7,
            "chars": [
                chr(code)
            ]
        })
        
    directory = "build/EverIslandResources/assets/minecraft/font"
    Path(directory).mkdir(parents=True, exist_ok=True)
    data = json.dumps({"providers": providers})
    uni = json.dumps({"providers": providers_uniform})
    f = open(directory + "/default.json", "w")
    f.write(data)
    f.close()
    f = open(directory + "/uniform.json", "w")
    f.write(uni)
    f.close()
    f = open("build/EverIslandResources/pack.mcmeta", "w")
    f.write("{\"pack\": {\"description\": \"EverMC Acidisland Resource Pack\",\"pack_format\": 6}}")
    f.close()
