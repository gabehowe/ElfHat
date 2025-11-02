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
load_dotenv()

from randler import generate, generate_image

type email = str

class Template(str):
    """Very basic HTML Template generator."""
    def template(self: str, varname, var):
        return Template(self.replace(f'{{%{varname}%}}', var))

template = Template(open('tem.html').read())
data = json.load(open('santa.json'))



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
    barr = io.BytesIO()
    img.save(barr, format='PNG')
    part = MIMEBase("application", "octet-stream")
    part.set_payload(barr.getvalue())
    filename = os.path.basename(path)
    encoders.encode_base64(part)
    part.add_header('Content-Disposition', f'inline; filename={filename}')
    cid = ''.join(random.choices(string.ascii_letters + string.digits, k=10))
    part.add_header('Content-Id', f'<{cid}>')
    return part, cid

def create_message(assignments: List[str], amount: str, target: str):
    """ Create a message to place on the image. """
    return f"""\
    You're in charge of {assignments[0]} and {assignments[1]} for secret santa.
    You have {amount} between both of them.
    If you're not {target}, ignore this email entirely.

    Mystery Man
    """



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
    message = MIMEMultipart("alternative")
    message['To'] = target_email
    message["Subject"] = "Your secret santa card is ready..."
    message["From"] = f'Mystery Man <{os.environ["EMAIL"]}>'
    cc = f'{moderators[0][0]} <{moderators[0][1]}>'
    for i in moderators[1:]:
        cc += f', {i[0]} <{i[1]}>'
    message['CC'] = cc
    text_part = MIMEText(text)

    html = copy(template).template('cid', cid)
    html_part = MIMEText(html, "html")

    message.attach(text_part)
    message.attach(html_part)
    message.attach(image_part)
    to = [target_email] + [i[1] for i in moderators]
    server.sendmail(message['From'], to, message.as_string())


if __name__ == '__main__':
    context = ssl.create_default_context()

    with smtplib.SMTP_SSL(os.environ['SMTP_URL'], int(os.environ['SSL_PORT']), context=context) as server:
        server.login(os.environ['EMAIL'], os.environ['PASSWORD'])
        print('Logged in?')
        values = generate(data)
        emails = {i[0]: i[1] for i in data['participants']}
        for k, v in values.items():
            send_elf_mail(emails[k], k, list(v), data['moderators'], server)
        # send_elf_mail('darkmidnightfury@gmail.com', 'gabe', ['jim', 'joe'], [["", ""]])
