import sys
from PIL import Image

if(len(sys.argv) < 2):
    print("Invoke using: python main.py {paths to image files}", file=sys.stderr)
    exit(1)

for infile in sys.argv[1:]:
    try:
        with Image.open(infile) as image:

            dimension_tuple = image.size
            image_width = dimension_tuple[0]
            image_height = dimension_tuple[1]
            
            print(f"Loaded {infile} with size {image_width}x{image_height}")
    except OSError:
        pass

