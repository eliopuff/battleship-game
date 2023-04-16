
##############################################################################
#                                   Imports                                  #
##############################################################################
from ex5_helper import *
from typing import Optional
import copy
import math
import sys

##############################################################################
#                                  Functions                                 #
##############################################################################


def separate_channels(image: ColoredImage) -> List[SingleChannelImage]:
    '''this function receives a 3-d list of rows x columns x channels, 
    representing three tones of an image, and converts it to a 3d-list 
    of three lists in seperate channel (channels x columns x rows). 
    in other words, splits an image (list) into three single-hued images (lists)'''
    separated_channels = []
    for k in range(len(image[0][0])):
        column = []
        for i in range(len(image)):
            row = []
            for j in range(len(image[0])):
                row.append(image[i][j][k])
            column.append(row)
        separated_channels.append(column)
    return separated_channels



def combine_channels(channels: List[SingleChannelImage]) -> ColoredImage:
    '''this function reverses what separate_channels() does, turning a 3d list 
    from separated by channels (channels x columns x rows) to separated 
    by rows (rows x columns x channels). in other words, turns an image 
    back to full-coloured (pardon my british english)'''
    combined_channels = []
    for i in range(len(channels[0])):
        column = []
        for j in range(len(channels[0][0])):
            row = []
            for k in range(len(channels)):
                row.append(channels[k][i][j])
            column.append(row)
        combined_channels.append(column)
    return combined_channels



def RGB2grayscale(colored_image: ColoredImage) -> SingleChannelImage:
    '''this function receives a list of lists representing a colored image
     - in RGB - and "grayscales" it. the RGB hues for each pixel are toned 
     (multiplied) and averaged to recieve (per pixel) one grayscaled pixel'''
    grayscaled = []
    for i in range(len(colored_image)):
        row = []
        for j in range(len(colored_image[0])):
            red: float = colored_image[i][j][0] * 0.299
            green: float = colored_image[i][j][1] * 0.587
            blue: float = colored_image[i][j][2] * 0.114
            gray_pixel: int = round(red + blue + green)
            row.append(gray_pixel)
        grayscaled.append(row)
    return grayscaled



def blur_kernel(size: int) -> Kernel:
    '''this function receives an integer size and returns
     a blur kernel - a square of size - int x int. the integer
    is necessarily whole, uneven and larger than 0. it is used to
    scan an image and blur its pixels with the kernel, by averaging 
    all neighbouring pixels'''
    kernel = []
    for i in range(size):
        row: list = []
        for j in range(size):
            row.append((1/(size*size)))
        kernel.append(row)
    return kernel
    ...



def apply_kernel(image: SingleChannelImage, kernel: Kernel) -> SingleChannelImage:
    '''this function receives a list of lists representing a single channel 
    image, and a square kernel of uneven size. the function creates a blurred 
    copy of the image by applying the kernel to each pixel and averaging the values 
    of pixels. the edges are treated differently: pixels that do not "exist" 
    bordering the pixels at the edges are made to have the same value as the 
    pixel in question (pixel at the centre of the kernel).'''
    blurred_image = []
    for i in range(len(image)):
        row = []
        for j in range(len(image[0])):
            new_pixel = blur_pixel(image, kernel, (i, j))
            row.append(new_pixel)
        blurred_image.append(row)
    return blurred_image
        



def blur_pixel(image: SingleChannelImage, kernel: Kernel, pixel: tuple) -> int:
    '''this function receives a single channel image (list of lists), 
    a blur kernel and a pixel coordinate. it applies the kernel to the 
    kernel-sized area around the pixel and returns the new value of the 
    blurred pixel. non-existing values are filled in to be the same as the pixel'''
    half_kernel =  len(kernel)//2 #this is the distance between the centre 
    #of the kernel and its edge
    blur_val = kernel[0][0] #our blur kernels use the same value for all pixels 
    #falling under the kernel at any point, so this move is safe
    blur_sum = 0
    y, x = pixel
    for i in range(y-half_kernel, y + half_kernel + 1):
        for j in range(x-half_kernel, x + half_kernel + 1):
            if i < 0 or j < 0 or i >= len(image) or j >= len(image[0]): 
                #these are out of the image, thus will be counted as the pixel itself
                blur_sum += blur_val * image[y][x]
            else:
                blur_sum += blur_val * image[i][j]
    final_blur_sum = blur_sum_check(round(blur_sum))
    return final_blur_sum


def blur_sum_check(blur_sum):
    '''this function checks whether the resulting sum of a blurred 
    pixel is over 255 or under 0, and neutralizes these conditions 
    (as a pixel cannot physically be these).'''
    if blur_sum < 0:
        return 0
    elif blur_sum > 255:
        return 255
    else:
        return blur_sum #no harm done




def bilinear_interpolation(image: SingleChannelImage, y: float, x: float) -> int:
    '''this function works with image resizing. it receives an image and 
    a relative coordinate in desired resized image, and returns the value 
    of the pixel - depending on where the spot of the coordinate lands in 
    the original image. there is a given bilinear interpolation formula, 
    and we will plug in the values and relative distances from the pixels 
    around the relative spot. a, b, c, d will be the short names for the 
    four closest pixels to our target pixel'''
    y1 = math.floor(y) #four nearest pixel values
    y2 = math.ceil(y)
    x1 = math.floor(x)
    x2 = math.ceil(x)
    delta_y = y%1 #the fraction distance
    delta_x = x%1
    a = image[y1][x1] #four nearest pixels
    b = image[y2][x1]
    c = image[y1][x2]
    d = image[y2][x2]
    new_pixel = a*(1 - delta_x)*(1 - delta_y) + b*delta_y*(1 - delta_x) \
    + c*delta_x*(1-delta_y) + d*delta_x*delta_y #the grand calculation
    return round(new_pixel)

    ...

def is_corner(new_height: int, new_width: int, y: int, x: int):
    '''this function receives as input height, width and coordinates. 
    it determines whether coordinates (i, j) in a photo are corners 
    of the photo of these coordinates, and returns true if they are'''
    if y == 0 and x == 0:
        return True
    elif y == 0 and x == (new_width - 1):
        return True
    elif y == (new_height - 1) and x == 0:
        return True
    elif y == (new_height - 1) and x == (new_width - 1):
        return True
    return False
    
def which_corner(image: SingleChannelImage, y: int, x: int) -> int:
    '''this function receives as input and image, and coordinates 
    of a pixel in a resized version of said image. the function receives 
    coordinates of only corners, and returns the value of the pixel 
    in the image - destined to be placed in the corner of the resized 
    image, in accordance with the following function resize()'''
    image_length: int = len(image) - 1
    image_width: int = len(image[0]) - 1
    if y == 0 and x == 0:
        return image[0][0]
    elif y == 0 and x != 0:
        return image[0][image_width]
    elif y != 0 and x == 0:
        return image[image_length][0]
    elif y != 0 and x != 0:
        return image[image_length][image_width]

    

def resize(image: SingleChannelImage, new_height: int, new_width: int)\
     -> SingleChannelImage:
    '''this function receives an single-channel image (list of lists) 
    and resize dimensions, and returns the image in the new dimensions. 
    the four corner pixels are kept and the rest have a value based off 
    of the calculations in the bilinear interpolation function, according 
    to relative position. the function returns a single-channel image in 
    required dimensions'''
    resized_image = []
    image_height = len(image) - 1 #original image dimensions, for later use
    image_length = len(image[0]) - 1
    for i in range(new_height):
        row = []
        for j in range(new_width):
            if is_corner(new_height, new_width, i, j) == True:
                row.append(which_corner(image, i, j))
            else:
                y, x = i, j
                rel_height = y*image_height/(new_height - 1)
                rel_width = x*image_length/(new_width - 1)
                row.append(bilinear_interpolation(image, rel_height, rel_width))
        resized_image.append(row)
    return resized_image
    ...

def rotated_RGB(image: Image, direction: str):
    '''this function receives as input an image, 3D list 
    representing an RGB image, and returns the image rotated in 
    the desired direction'''
    seperated = separate_channels(image) #a list of three 2D images, 
    #seperated to channels R, G, B
    red = seperated[0]
    green = seperated[1]
    blue = seperated[2]
    red_rotate = rotated_single_channel(red, direction)#rotated for each
    green_rotate = rotated_single_channel(green, direction)
    blue_rotate = rotated_single_channel(blue, direction)
    combined = combine_channels([red_rotate, green_rotate, blue_rotate])
    return combined



def rotated_single_channel(image: Image, direction: str):
    '''this function receives as input an image, list of 
    lists (2D) representing a single-channel image, and 
    returns the image rotated in the desired direction'''
    rotated_image = []
    for i in range(len(image[0])):
        rotated_image.append([x[i] for x in image])
    if direction == 'L':
        return rotated_image[::-1]
    elif direction == 'R':
        rotated_image_right = [i[::-1] for i in rotated_image]
        return rotated_image_right



def rotate_90(image: Image, direction: str) -> Image:
    '''this function receives an image in the form of a list 
    of lists (grayscale or RGB) and rotates it 90 degrees left 
    or right (depending on imput). the function itself creates 
    a new list of lists describing the image, but rotated with 
    all pixels displaced accordingly. '''
    if type(image[0][0]) == int:
        rotated_image = rotated_single_channel(image, direction)
    else:
        rotated_image = rotated_RGB(image, direction)
    return rotated_image
    ...



def get_edges(image: SingleChannelImage, blur_size: \
    int, block_size: int, c: float) -> SingleChannelImage:
    '''this function receives a single-channel image as input 
    and returns a version of the image containing only the 
    outlines of objects, in black. it first blurs the image 
    and after find the edges by averaging each pixel and 
    determining whether it is an edge - turning it black, 
    or not - turning it white'''
    blurred_image = apply_kernel(image, blur_kernel(blur_size))
    edges_image = []
    for i in range(len(image)):
        row = []
        for j in range(len(image[0])):
            threshold = get_threshold(blurred_image, block_size, c, i, j)
            if threshold > blurred_image[i][j]:
                row.append(0)
            else:
                row.append(255)
        edges_image.append(row)
    return edges_image
    ...

def get_threshold(image: SingleChannelImage, block_size: int, \
c: float, y: int, x: int) -> int:
    '''this function assissts above function for creating an image 
    representing edges, by calculating the desired threshold 
    value for the image. the calculation is technical, based 
    off an average of a block-size parameter square around each 
    pixel. if parts of the square are out of range, they are 
    'replaced' by a pixel of the same value as the one at the centre'''
    r_val = block_size//2
    sum = 0
    for i in range(y - r_val, y + r_val + 1):
        for j in range(x - r_val, x + r_val + 1):
            if i < 0 or j < 0 or i >= len(image) or j >= len(image[0]):
                sum += image[y][x]
            else:
                sum += image[i][j]
    average_sum = sum/(block_size**2)
    return average_sum - c #we end our calculation and return the sum
    


def quantize(image: SingleChannelImage, N: int) -> SingleChannelImage:
    '''this function receives a single-channel image and an int N, 
    and utilizes this to create a 'quantized' version of the image, 
    where only a certain amount of colours in the image (the amount 
    given by N) are kept. this is calculated through a specific sum 
    for finding these values. the function returns the quantized image'''
    quantized_image = []
    for i in range(len(image)):
        row = []
        for j in range(len(image[0])):
            quant_pixel = round((math.floor(image[i][j] * N/256))\
                 * (255/(N - 1)))
            row.append(quant_pixel)
        quantized_image.append(row)
    return quantized_image
    ...


def quantize_colored_image(image: ColoredImage, N: int) -> ColoredImage:
    '''similar to the quantize, this function receives an image 
    it must quantize to a specific parameter of N colours, but 
    this time the image is 3D. it will seperate the various channels, 
    quantize each by N, and return a 3D quantized image with colours 
    N to the power of #channels.'''
    seperated = separate_channels(image)
    list_of_channels = []
    for channel in seperated:
        quant = quantize(channel, N)
        list_of_channels.append(quant)
    combined = combine_channels(list_of_channels)
    return combined


#from here start the functions assissting the run of main

def main_menu():
    #this function represents the main menu of our 'main()' 
    # image editing program. it prints the menu, and checks the 
    # input is appropriate.
    menu = 'This is an image-editing program. List of operations:\n' + \
    '1 - grayscale\n2 - blur\n3 - resize\n4 - rotate 90 degrees\n' + \
    '5 - create edges image\n6 - image quantization\n7 - display image.\n' + \
    '8 - Exit.\nPlease enter the number corresponding to the operation' + \
    'of your choice:'
    error = 'Invalid operation.\n'
    while True: #haven't gotten suitable input yet, until output
        user_input = input(menu)
        if user_input.isdigit() == False:
            print(error)
        else:
            if float(user_input) not in range(1, 9):
                print(error)
            else:
                return int(user_input)

def is_grayscale(image) -> bool:
    #this function determines whether a list of list representing an 
    # image is RGB or grayscale, returns True if grayscale, otherwise False.
    if type(image[0][0]) == int:
        return True
    else:
        return False



def main_grayscale(image):
    #this function, as part of 'main', executes the grayscale operation
    if is_grayscale(image) == True:
        print('Your image is already grayscale.')
        return image
    else:
        return RGB2grayscale(image)

def main_blur(image):
    #as part of main, this function is in charge of the blurring operation
    user_input = input('Enter kernel size:')
    if user_input.isdigit() == True and float(user_input)%1 == 0:
        if int(user_input) > 0 and int(user_input)%2 != 0:
            if is_grayscale(image) == True: #grayscale, simple one-channel blur
                return apply_kernel(image, blur_kernel(int(user_input)))
            else: #more complex, we blur each channel alone and unify
                separate = separate_channels(image)
                r_blur = apply_kernel(separate[0], blur_kernel(int(user_input)))
                g_blur = apply_kernel(separate[1], blur_kernel(int(user_input)))
                b_blur = apply_kernel(separate[2], blur_kernel(int(user_input)))
                return combine_channels([r_blur, g_blur, b_blur])
    return None, image #back to main menu.

def main_resize(image):
    #function part of main responsible for the operation of resizing an image
    user_input = input('Enter new height and width, separated with a comma:')
    if ',' not in user_input:
        return None, image
    separated_input = user_input.split(',')
    if len(separated_input) != 2:
        return None, image
    height, width = user_input.split(',')
    if height.isdigit() == True and float(height)%1 == 0 and width.isdigit()\
         == True and float(width)%1 == 0:
        height, width = int(height), int(width)
        if is_grayscale(image) == True:
            return resize(image, height, width)
        else:
            separate = separate_channels(image)
            r_resize = resize(separate[0], height, width)
            g_resize = resize(separate[1], height, width)
            b_resize = resize(separate[2], height, width)
            return combine_channels([r_resize, g_resize, b_resize])
    return None, image


def main_rotate(image):
    #this function, as part of main, is responsible for the operation of 
    # rotating an image
    user_input = input('Enter L/R for rotation direction:')
    if user_input != 'L' and user_input != 'R':
        return None, image
    else:
        return rotate_90(image, user_input)


def main_edges(image):
    #this function, as part of main, is responsible for the operation of 
    # creating an edges image of the original image
    user_input = input('Enter blur size, block size and coefficient c' + 
    'separated by a comma:')
    if ',' not in user_input:
        return None, image
    separated_input = user_input.split(',')
    if len(separated_input) != 3:
        return None, image
    blur_size, block_size, c = separated_input
    if are_variables_numbers(blur_size, block_size, c) == False:
        return None, image
    if edges_variable_checker(float(blur_size), float(block_size), float(c))\
         == True:
        if is_grayscale(image) == True:
            return get_edges(image, int(blur_size), int(block_size), float(c))
        else:
            grayscale = RGB2grayscale(image)
            return get_edges(grayscale, int(blur_size), int(block_size), float(c))
    return None, image

def are_variables_numbers(blur_size, block_size, c):
    #his function will validate whether the inputs for blur size, block size and 
    # c are valid numbers
    if (blur_size + block_size).isdigit() == False:
        return False
    if '.' in c:
        if (''.join(c.split('.'))).isdigit() == False:
            return False
    elif '.' not in c:
        if (c).isdigit() == False:
            return False
    return True

    


def edges_variable_checker(blur_size, block_size, c):
    #since there are a lot of parameters to check with these variables, 
    # i decided to separate this into another function
    if blur_size%1 == 0 and blur_size > 0 and blur_size%2 != 0:
        if block_size%1 == 0 and block_size > 0 and block_size%2 != 0:
            if c >= 0:
                return True
    return False




def main_quantize(image):
     #this function, as part of main, is responsible for the operation of 
     # creating a quantized image of the original image
    user_input = input('Enter number of colors you want to keep:')
    if user_input.isdigit() == True:
        if float(user_input)%1 == 0 and float(user_input) > 1:
            if is_grayscale(image) == True:
                return quantize(image, int(user_input))
            else:
                return quantize_colored_image(image, int(user_input))
    return None, image




if __name__ == '__main__': 
    #the 'main' here brings together all functions above in an ultimate 
    # concoction of an image-editing program! it is run on an arg1 given by user
    if len(sys.argv) != 2:
        print("Invalid amount of arguments.")
        program_running = False #program can't run
    else:
        edited_image = load_image(sys.argv[1])
        program_running = True #we start our program with it running
    while program_running == True:
        operation = main_menu() #start with main menu, continue to all options
        if operation == 1:
            edited_image = main_grayscale(edited_image)
        elif operation == 2:
            edited_image = main_blur(edited_image)
        elif operation == 3:
            edited_image = main_resize(edited_image)
        elif operation == 4:
            edited_image = main_rotate(edited_image)
        elif operation == 5:
            edited_image = main_edges(edited_image)
        elif operation == 6:
            edited_image = main_quantize(edited_image)
        elif operation == 7:
            show_image(edited_image)
        else:
            program_running == False
            filename = input('Choose file location to save your image:')
            save_image(edited_image, filename)
            print('Saved!')
            break
        if type(edited_image) == tuple:
            if edited_image[0] == None:
                print('Invalid input.')
                edited_image = edited_image[1]
                continue #back to top of loop
