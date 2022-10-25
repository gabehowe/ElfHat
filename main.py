# 10 names
# 5 people
# who gets what?
import datetime
import os
import os.path as ospath
import sys
from random import randint
from typing import Tuple

from PIL import Image, ImageDraw, ImageFont
from PIL.ImageFont import FreeTypeFont

# initialize names
names = ['Thomas', 'Katie', 'Sammy', 'Gabe', 'Dahlia']
taken = {'Thomas': 0, 'Katie': 0, 'Sammy': 0, 'Gabe': 0, 'Dahlia': 0}
values = {'Thomas': [], 'Katie': [], 'Sammy': [], 'Gabe': [], 'Dahlia': []}


def check_taken(roller_name: str):
    taken_count = 0
    for e in taken.values():
        if e == 2:
            taken_count += 1
    return taken_count


# roll to get new names
def roll(roller_name: str):
    while True:
        first_name = names[randint(0, len(names) - 1)]
        second_name = names[randint(0, len(names) - 1)]
        # if names are equal or any of the names are the same as the roller's name, continue
        taken_count = check_taken(roller_name)
        if first_name == second_name or first_name == roller_name or second_name == roller_name and taken_count == len(
                names) - 3:
            return None
        if first_name != second_name and first_name != roller_name and second_name != roller_name:
            # if the names are already taken continue
            if taken[second_name] == 2 or taken[first_name] == 2:
                continue
            # if the names aren't taken, and none of the three names are equal, increment taken
            taken[second_name] += 1
            taken[first_name] += 1
            # return the checked first and second name
            return [first_name, second_name]


def draw_centered(draw: ImageDraw, message: str, x: float, y: float, font: FreeTypeFont,
                  color: Tuple[int, int, int] = (255, 0, 0)):
    _, _, w, h = draw.textbbox((0, 0), message, font=font)
    draw.text(((x - (w / 2)), (y - (h / 2))), message, font=font, fill=color)


def generate_image(title: str, subtitle: str, location: os.path):
    if not ospath.isdir('./values'):
        os.mkdir('./values')
    img = Image.open('./template.png')
    drawer = ImageDraw.Draw(img)
    a_bold = ImageFont.truetype('./arialbd.ttf', 50)
    a_reg = ImageFont.truetype('./arial.ttf', 30)
    a_bold_big = ImageFont.truetype('./arialbd.ttf', 100)
    color = (255, 255, 255)
    draw_centered(drawer, subtitle, img.width / 2, img.height / 2,
                  a_bold, color)
    draw_centered(drawer, title, img.width / 2, img.height * 0.3, a_bold_big, color)
    drawer.text((img.width * 0.05, img.height * 0.86),
                f'Generated on {datetime.datetime.now().utcnow().strftime("%B %d, %Y at %H:%M:%S")}',
                font=a_reg, fill=color)
    drawer.text((img.width * 0.05, img.height * 0.9),
                f'Powered by ElfHat, an open source project by Gabriel Howe.',
                font=a_reg, fill=color)

    img.save(location)


def main():
    while True:
        for i in names:
            rolled = roll(i)
            if rolled is None:
                for o in taken.keys():
                    taken[o] = 0
                for a in values.keys():
                    values[a] = 0
                break

            first_name, second_name = rolled
            values[i] = [first_name, second_name]
            if i == names[-1]:
                for p in values.keys():
                    first, second = values[p]
                    path = f'./values/{p}.png'
                    generate_image(p, f'Your people are {first} and {second}', path)

            sys.exit()


if __name__ == '__main__':
    main()
