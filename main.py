from PIL import Image, ImageOps
# load and resize the image to 100 by x with thumbnail doing the reize calc
size = [100,50]
inputname = input("name of image inc .jpg or .png:")
with Image.open(inputname) as im:
    
    im.thumbnail(size,Image.LANCZOS)
    
    #convert to grayscale
    im = ImageOps.grayscale(im)
    width, height = im.size

    #ascii define white to black
    ascii_chars = "#@%*+=-:. "
    
    #opens the text file
    f = open(inputname[0:-4]+".txt","w")

    #goes thorugh each pixel
    for i in range(height):
        f.write("\n")
        for j in range(width):

            #gets pixel value
            pixel = im.getpixel((j,i))

            #make each pixel an ascii char 0(black)-255(white)
            f.write(ascii_chars[round(pixel/255*len(ascii_chars))])
