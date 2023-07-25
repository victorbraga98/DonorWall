#! /usr/bin/env python3

__author__ = "Victor Braga"
__copyright__ = "Copyright 2023, Victor Braga"
__credits__ = []
__license__ = "MIT"
__version__ = "1.0.0"
__maintainer__ = "Victor Braga"
__email__ = "victorbraga98@gmail.com"
__status__ = "Production"

from PIL import Image, ImageDraw, ImageFont
import csv
import math
import textwrap
import time
from datetime import datetime
import itertools

# Top row text height start
TR_text_height_start = 290
# Bottom row text height start
BR_text_height_start = 1180

# Column Starts (x, y) values
positions = [[490, TR_text_height_start], [470, BR_text_height_start], [1330, TR_text_height_start], [1330, BR_text_height_start], [2510, TR_text_height_start], [2510, BR_text_height_start], [3350, TR_text_height_start], [3350, BR_text_height_start]]



# Configuration
image_path = 'bg_4k.png'
output_directory = './output/'
csv_path = 'names.csv'

# Text Configuration
font_size = 55
line_spacing = 90  # Set the distance between each line in pixels
text_color = (0, 0, 0)  # Set text color in RGB Values: Black

# Create a font object
font = ImageFont.truetype('LinikSans-Bold.ttf', font_size)



# Number of columns per slide
names_per_top_column = 8
names_per_bottom_column = 10

print("Loading input image...")


def GenerateGraphic(dataset, output_count):
    columns = []
    indiv_colsT = []
    indiv_colsB = []

    def divide_chunks(l):
        subsets = []
        i = 0
        while i < len(l):
            if len(subsets) % 2 == 0:
                subset = l[i:i + names_per_top_column]
                i += 8
            else:
                subset = l[i:i + names_per_bottom_column]
                i += 10
            subsets.append(subset)
        return subsets

    columns = (divide_chunks(dataset))
    
    # Define drawers:
    img = Image.open(image_path)
    draw = ImageDraw.Draw(img)

    # Set columns and column data, paste it on image
    count = 0
    for sets in columns:
        text_y = positions[count][1] 
        for names in sets:
            text_width, text_height = draw.textsize(names, font=font)
            text_x = positions[count][0] - (text_width/2)
            draw.text((text_x, text_y), names, font=font, fill=text_color)
            text_y += line_spacing
        count += 1
    
    # Add page number to top right of image
    page_count_font = ImageFont.truetype('LinikSans-Bold.ttf', 25)
    # Set page number to a double digit number
    page_number = str(output_count).zfill(2)
    draw.text((3645, 100), page_number, font=page_count_font, fill=(84, 84, 84))


    # Get date and time for file output
    now = datetime.now()
    dt_string = now.strftime("%m-%d-%Y_%H%M%S")
    img.save(f'./output/{dt_string}.png')

# Load donor names from the CSV file
individuals = []
with open(csv_path, 'r', encoding='utf-8-sig') as csvfile:
    reader = csv.reader(csvfile)
    for row in reader:
        if len(row) > 0:
            individuals.append(row[0])  # Assign a count ID to each name
        else:
            print("Empty row encountered.")

print(f"There are {len(individuals)} unique names in this CSV file.")
total_prints = math.ceil(len(individuals)/72)

nested_set = []

# Create sublists with a max of 72 names
for i in range(0, len(individuals), 72):
    sublist = individuals[i:i+72]
    nested_set.append(sublist)



printed = 1
for sets in nested_set:
    print(f"Generating image {printed} of {total_prints}")
    GenerateGraphic(sets, printed)
    printed +=1
