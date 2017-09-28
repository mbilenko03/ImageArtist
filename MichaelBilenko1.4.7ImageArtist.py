import PIL
from PIL import ImageFont
from PIL import Image
from PIL import ImageDraw
import matplotlib.patches as patches
import matplotlib.pyplot as plt # single use of plt is commented out
import os.path  
import PIL.ImageDraw     

# Gets images from directory
def get_images(directory=None):    
    if directory == None:
        directory = os.getcwd()
        
    image_list = []
    file_list = []
    
    directory_list = os.listdir(directory)
    for entry in directory_list:
        absolute_filename = os.path.join(directory, entry)
        try:
            image = PIL.Image.open(absolute_filename)
            file_list += [entry]
            image_list += [image]
        except IOError:
            pass
    return image_list, file_list
    

#Modifies images according to a funciton and user values
def modify_all_images(function):

    directory = os.getcwd()
     
    new_directory = os.path.join(directory, 'modified')
    try:
        os.mkdir(new_directory)
    except OSError:
        pass  
    
    image_list, file_list = get_images(directory)  
    
    if function == 'frame':
        magnitude = int(raw_input("How big do you want your frame to be?"))
        red = int(input("How much red?"))
        green = int(input("How much green?"))
        blue = int(input("How much blue?"))
        
    if function == 'text':
        magnitude = int(raw_input("How big do you want your text to be?"))
        text = raw_input("What text do you want?")
        xPosition = int(raw_input("Where do you want your photo to be positioned on the x axis?"))
        yPosition = int(raw_input("Where do you want your photo to be positioned on the y axis?"))
        red = int(input("How much red?"))
        green = int(input("How much green?"))
        blue = int(input("How much blue?"))

    for n in range(len(image_list)):
        print n
        filename, filetype = os.path.splitext(file_list[n])
        
        #Replace with function
        curr_image = image_list[n]
        
        if function == 'frame':
            new_image = frame_one_image(curr_image, magnitude, red, green, blue) 
        if function == 'text':
            new_image = text_one_image(curr_image, magnitude, text, xPosition, yPosition, red, green, blue)
   
        new_image_filename = os.path.join(new_directory, filename + '.png')
        new_image.save(new_image_filename)  
    

#Function to frame an image
def frame_one_image(original_image, widthOfFrame, red, green, blue):
    width, height = original_image.size
    radius = widthOfFrame

    rectangle_mask = PIL.Image.new('RGBA', (width, height), (0,0,0,0))
    drawing_layer = PIL.ImageDraw.Draw(rectangle_mask)
    
    drawing_layer.polygon([(radius,radius),(width-radius,radius),
                            (width-radius,height-radius),(radius,height-radius)],
                            fill=(127,0,127,255))
    
    result = PIL.Image.new('RGBA', original_image.size, (red,green,blue,255))
    result.paste(original_image, (0,0), mask=rectangle_mask)
    return result


#Function to add text to an image
def text_one_image(original_image, font_size, text, xPosition, yPosition, red, green, blue):
    width, height = original_image.size
    img = original_image
    draw = ImageDraw.Draw(img)
    # font = ImageFont.truetype(<font-file>, <font-size>)
    font = ImageFont.truetype("ComicSansMSBold.ttf", font_size)
    # draw.text((x, y),"Sample Text",(r,g,b))
    draw.text((xPosition, yPosition),text,(red,green,blue),font=font)    
    return img