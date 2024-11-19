from PIL import Image, ImageOps
# input the image and resize it
new_width = 57
inputname = input("name of image inc .jpg or .png:")
with Image.open(inputname) as im:
    width, height = im.size
    new_height = int(height/width * new_width *0.5)
    im = im.resize((new_width, new_height))
    
    #convert to grayscale
    im = ImageOps.grayscale(im)


    #ascii define white to black
    ascii_chars = "@%#*+=-:. "

    #opens the text file
    f = open(inputname[0:-4]+".txt","w")

    #goes thorugh each pixel
    for i in range(new_height):
        f.write("\n")
        for j in range(new_width):

            #gets pixel value
            pixel = im.getpixel((j,i))

            #make each pixel an ascii char 0(black)-255(white)
            f.write(ascii_chars[int(pixel/255*(len(ascii_chars)-1))])
    print("Outputted ascii text file")
