# 10 names
# 5 people
# who gets what?
from __future__ import annotations

import random
from typing import List, Tuple

from PIL import Image, ImageDraw, ImageFont
from PIL.ImageFont import FreeTypeFont


def check_taken(roller_name: str, taken):
    taken_count = 0
    for e in taken.values():
        if e == 2:
            taken_count += 1
    return taken_count


# roll to get new names
def roll(roller_name: str, untaken: List[str]):
    c1 = list(filter(lambda it: it != roller_name, untaken))
    first_choice = random.choice(c1)
    c2 = list(filter(lambda it: it != first_choice, c1))
    second_choice = random.choice(c2)
    untaken.remove(first_choice)
    untaken.remove(second_choice)

    return first_choice, second_choice


def draw_centered(draw: ImageDraw, message: str, x: float, y: float, font: FreeTypeFont,
                  color: Tuple[int, int, int] = (255, 0, 0)):
    _, _, w, h = draw.textbbox((0, 0), message, font=font)
    draw.text(((x - (w / 2)), (y - (h / 2))), message, font=font, fill=color)


def generate_image(title, subtitle, note):
    img: Image = Image.open('sscard.png')
    pen = ImageDraw.Draw(img)
    draw_centered(pen, title, img.width * .5, img.height * .4, ImageFont.truetype('MAIAN.TTF', 90), color=(0, 0, 0))
    draw_centered(pen, subtitle, img.width * .5, img.height * 0.6, ImageFont.truetype('MAIAN.TTF', 60), color=(0, 0, 0))

    draw_centered(pen, note, img.width * .5, img.height * 0.7, ImageFont.truetype('MAIAN.TTF', 30), color=(0, 0, 0))
    return img


def generate(data: dict):
    names = [i[0] for i in data['participants']]
    untaken = names + names
    values = {name: [] for name in names}
    for i in names:
        try:
            values[i] = first, second = roll(i, untaken)
        except IndexError as e:
            return generate(data)

    return values
