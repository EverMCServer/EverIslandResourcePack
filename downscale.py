
from PIL import Image
import sys

if len(sys.argv) != 2:
    print('Usage: python downscale.py <image>')
    sys.exit(0)

f = sys.argv[1]

with Image.open(f) as im:
    im = im.resize((32,32), Image.LANCZOS)
    im.save(f)
