from PIL import Image, ImageOps
import os

# input the image and resize it
new_width = 100
if (new_width > 100):
    print("Warning: new_width is too large for the terminal, it might not display correctly.")

inputname = input("name of image inc .jpg or .png:")
with Image.open(inputname) as im:
    width, height = im.size
    new_height = int(height/width * new_width *0.5)
    im = im.resize((new_width, new_height))
    
    #convert to grayscale
    im = ImageOps.grayscale(im)


    #ascii define white to black
    ascii_chars = "@%#*+=-:. "

    #goes to the output directory 
    output_dir = os.path.join(os.path.dirname(__file__), "../output")

    #makes the output directory if it does not exist
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)
    
    #gets the filename without the extension and path just the name ex. src/image.png -> image
    filename = os.path.basename(os.path.splitext(inputname)[0])
    output_path = os.path.join(output_dir, filename+ "_ascii.txt")

    #opens the text file
    f = open(output_path,"w")

    #goes through each pixel
    for i in range(new_height):
        line = ""

        for j in range(new_width):

            #gets pixel value
            pixel = im.getpixel((j,i))

            #make each pixel an ascii char 0(black)-255(white)
            char = ascii_chars[int(pixel/255*(len(ascii_chars)-1))]
            line += char
            
        line = line +"\n"
        f.write(line )
        print("\r" + line,end="",flush=True) #ensure clean output using Carriage Return
    f.close()
    print("\n")
    print("Outputted ascii text file")