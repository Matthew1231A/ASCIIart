import sys
from PIL import Image

POST_PROCESS_NAME_APPEND = "_ASCII_modified"
LUMINOSITY_COEFF_ARRAY = [0.21, 0.72, 0.07]
BRIGHTNESS_CHAR_STRING = "`^\",:;Il!i~+_-?][}{1)(|\\/tfjrxnuvczXYUJCLQ0OZmwqpdbkhao*#MW&8%B@$"
BRIGHTNESS_CHAR_STRING_LENGTH = len(BRIGHTNESS_CHAR_STRING)
OUTPUT_FILE_TYPE = ".txt"
BASE_HEIGHT = 60

# Given a path to an image file, return the path in a form where POST_PROCESS_NAME_APPEND is inserted before the final period (which determines the file type


def strip_file_type(path: str) -> str:
    periodIndex = path.rfind(".")

    stripped_path = path[:periodIndex]
    path_file_type = OUTPUT_FILE_TYPE

    return stripped_path + POST_PROCESS_NAME_APPEND + path_file_type

# Computes the dot product of 2 lists. Stops computation at the minimum length of the 2 lists


def compute_dot(v1: list, v2: list) -> float:
    sum = 0.0

    for index in range(min(len(v1), len(v2))):
        sum += v1[index] * v2[index]

    return sum

# Scales an image to have a constate height of BASE_HEIGHT so the resulting file isn't insanely large but also still understandable.


def normalize_image_dimensions(width: int, height: int) -> tuple:
    # Determine scale from current height to 100
    # e.g. 300 becomes 100 with a scale of 3
    normalize_scale = float(height)/BASE_HEIGHT

    # Set height to be the BASE_HEIGHT
    height = BASE_HEIGHT
    # Scale the width by the ratio calculated above
    width = int(float(width)/normalize_scale)

    return (width, height)


# __name__ guard
if __name__ == "__main__":

    # Ensure that at least one image filename is provided
    if(len(sys.argv) < 2):
        print(
            "Invoke using: python main.py {paths to image files}", file=sys.stderr)
        exit(1)

    # For every file after the invocation
    for infile in sys.argv[1:]:
        try:
            with Image.open(infile) as image:
                image_width, image_height = image.size

                print(
                    f"Loaded {infile} with size {image_width}x{image_height}")

                #Scale the image down
                new_dimensions = normalize_image_dimensions(
                    image_width, image_height)
                resized = image.resize(new_dimensions)

                #Update the width and height to that of the resized image
                image_width, image_height = resized.size

                print(
                    f"Resized to {image_width}x{image_height}")

                #Load the pixels from the resized image 
                pixels = resized.load()

                #Remove the extension from the original image, add the modified tag and reappend the type
                try:
                    f = open(strip_file_type(infile), "w")
                except:
                    continue

                #Loop through the rows then columns of the image (like in a book)
                for y in range(image_height):

                    #Buffer the chars of the current line
                    buffer = ""
                    for x in range(image_width):

                        #Get the RGB values at that pixel
                        pixel = pixels[x, y]
                        luminosity = compute_dot(pixel, LUMINOSITY_COEFF_ARRAY)

                        # Normalize brightness model then map across string
                        brightness_string_index = int(
                            (luminosity/255.0) * (BRIGHTNESS_CHAR_STRING_LENGTH - 1))
                        
                        #Append to the buffer 2 of the selected characters (to preserve the ratio)
                        buffer += (
                            BRIGHTNESS_CHAR_STRING[brightness_string_index]*2)
                    f.write(buffer + "\n")
                f.close

        except OSError:
            pass
