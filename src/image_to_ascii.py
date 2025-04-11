from PIL import Image, ImageOps
import os

# input the image and resize it
new_width = 200
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
        f.write("\n")
        for j in range(new_width):

            #gets pixel value
            pixel = im.getpixel((j,i))

            #make each pixel an ascii char 0(black)-255(white)
            f.write(ascii_chars[int(pixel/255*(len(ascii_chars)-1))])
    f.close()
    print("Outputted ascii text file")