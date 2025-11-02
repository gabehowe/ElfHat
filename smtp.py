"""
Simple SMTP script to send create Secret Stanta images based on a template and send to destinations sourced from a JSON file.

usage: source .env && py smtp.py
"""
import io
import json
import os.path
import os
import random
import smtplib, ssl
import string
from copy import copy
from pathlib import Path
from email import encoders
from email.mime.base import MIMEBase
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from typing import List, Tuple
from dotenv import load_dotenv

from PIL import Image, ImageDraw, ImageFont
from PIL.ImageFont import FreeTypeFont
import matplotlib.pyplot as plt

from randler import generate_all_assignments
import networkx as nx

type email = str

class Template(str):
    """Very basic HTML Template generator."""
    def template(self: str, varname, var):
        return Template(self.replace(f'{{%{varname}%}}', var))

template = Template(open('tem.html').read())
data = json.load(open('santa.json'))



def draw_centered(draw: ImageDraw.ImageDraw, message: str, x: float, y: float, font: FreeTypeFont,
                  color: Tuple[int, int, int] = (255, 0, 0)):
    _, _, w, h = draw.textbbox((0, 0), message, font=font)
    draw.text(((x - (w / 2)), (y - (h / 2))), message, font=font, fill=color)


def generate_image(title, subtitle, note):
    img: Image.Image = Image.open('sscard.png')
    pen = ImageDraw.Draw(img)
    draw_centered(pen, title, img.width * .5, img.height * .4, ImageFont.truetype('MAIAN.TTF', 90), color=(0, 0, 0))
    draw_centered(pen, subtitle, img.width * .5, img.height * 0.6, ImageFont.truetype('MAIAN.TTF', 60), color=(0, 0, 0))

    draw_centered(pen, note, img.width * .5, img.height * 0.7, ImageFont.truetype('MAIAN.TTF', 30), color=(0, 0, 0))
    barr = io.BytesIO()
    img.save(barr, format='PNG')
    return barr

def convert_image(img: io.BytesIO) -> Tuple[MIMEBase, str]:
    part = MIMEBase("application", "octet-stream")
    part.set_payload(img.getvalue())
    encoders.encode_base64(part)
    part.add_header('Content-Disposition', f'inline; filename=generated_image.png')
    cid = ''.join(random.choices(string.ascii_letters + string.digits, k=10))
    part.add_header('Content-Id', f'<{cid}>')
    return part, cid

def build_image(path: os.PathLike, title: str, subtitle: str, note: str) -> Tuple[MIMEBase, str]:
    """
    Load an image and place text on it.
    
    Args:
        - path: Source path for the image.
        - title: Text to render in large as a title.
        - subtitle: Text to render under the title.
        - note: Text to render under the subtitle.

    Returns: 
        A tuple pair of octet-stream image with a random content id.
    """

    img = generate_image(title, subtitle, note)
    return convert_image(img)

def create_message(assignments: List[str], amount: str, target: str):
    """ Create a message to place on the image. """
    return f"""\
    You're in charge of {assignments[0]} and {assignments[1]} for secret santa.
    You have {amount} between both of them.
    If you're not {target}, ignore this email entirely.

    Mystery Man
    """

def send_email(to, target, subject, from_, cc, content, server):
    message = MIMEMultipart("alternative")
    message['To'] = target
    message["Subject"] = subject
    message["From"] = from_
    message['CC'] = cc


    for i in content:
        message.attach(i)
    server.sendmail(message['From'], to, message.as_string())


def send_elf_mail(target_email: email, target: str, assignments: List[str], moderators: List[Tuple[str, email]], server):
    """
    Build and send an email containing information about a Secret Santa assignment.

    Args:
        - target_email: Email address of the recipient.
        - target: Name of the recipient.
        - target_santees: Assignments of the recipient.
        - moderators: (name, email) to additionally send the assignment to.

    """
    text = create_message(assignments, data['amount'], target)
    image_part, cid = build_image(Path('sscard.png'), f'For {target}', f'Your people are {assignments[0]} and {assignments[1]}.',
                                 f'You have {data["amount"]} and 25 days.')
    cc = f'{moderators[0][0]} <{moderators[0][1]}>'
    for i in moderators[1:]:
        cc += f', {i[0]} <{i[1]}>'
    text_part = MIMEText(text)

    html = copy(template).template('cid', cid)
    html_part = MIMEText(html, "html")

    to = [target_email] + [i[1] for i in moderators]
    send_email(to, target,  "Your secret santa card is ready...", f'Mystery Man <{os.environ["EMAIL"]}>', cc, [text_part, html_part, image_part], server)

def build_graph_rep(values:List[Tuple[str, Tuple[str, str]]]) -> io.BytesIO:
    graph = {k:list(v) for k,v in values}
    g = nx.DiGraph(graph)
    nx.draw(g, with_labels=True, node_color="green", edge_color="red")
    buf = io.BytesIO()
    plt.savefig(buf, format='png')
    return buf






def send_graph_rep(values: List[Tuple[str, Tuple[str, str]]], moderators: List[Tuple[str, email]], server):
    rep = build_graph_rep(values)
    img_pt, cid = convert_image(rep)
    html = copy(template).template('cid', cid)
    html_part = MIMEText(html, "html")

    to = [i[1] for i in moderators]

    send_email(to, ','.join([f'{ i[0] } <{i[1]}>' for i in moderators]),  "Hey Secret Santa Moderator! Here's an informative graph.", f'Mystery Man <{os.environ["EMAIL"]}>', "", [html_part, img_pt], server)
    

if __name__ == '__main__':
    load_dotenv()
    context = ssl.create_default_context()

    with smtplib.SMTP_SSL(os.environ['SMTP_URL'], int(os.environ['SSL_PORT']), context=context) as server:
        server.login(os.environ['EMAIL'], os.environ['PASSWORD'])
        print('Logged in?')
        values = generate_all_assignments(data)
        emails = {i[0]: i[1] for i in data['participants']}
        for k, v in values:
            send_elf_mail(emails[k], k, list(v), data['moderators'], server)
        # send_elf_mail('darkmidnightfury@gmail.com', 'gabe', ['jim', 'joe'], [["", ""]])
