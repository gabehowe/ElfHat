import io
import json
import os.path
import random
import smtplib, ssl
import string
from copy import copy
from email import encoders
from email.mime.base import MIMEBase
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

from randler import generate, generate_image


class Template(str):
    def template(self: str, varname, var):
        return Template(self.replace(f'{{%{varname}%}}', var))


ssl_port = 465

password = input("Type password: ")
context = ssl.create_default_context()
template = Template(open('tem.html').read())
data = json.load(open('santa.json'))


def load_image(path, title, subtitle, note):
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


def send_elf_mail(target_email, target, target_santees, moderators: list):
    text = f"""\
    You're in charge of {target_santees[0]} and {target_santees[1]} for secret santa.
    You have {data['amount']} between both of them.
    If you're not {target}, ignore this email entirely.

    Mystery Man
    """

    image_part, cid = load_image('sscard.png', target, f'Your people are {target_santees[0]} and {target_santees[1]}.',
                                 f'You have {data["amount"]} for gifts for both of your people that must arrive by christmas day.')
    message = MIMEMultipart("alternative")
    message['To'] = target_email
    message["Subject"] = "Your secret santa card is ready..."
    message["From"] = 'Mystery Man <santa@gabe.how>'
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
    with smtplib.SMTP_SSL("smtppro.zoho.com", ssl_port, context=context) as server:
        server.login('santa@gabe.how', password)
        print('Logged in?')
        values = generate(data)
        emails = {i[0]: i[1] for i in data['participants']}
        for k, v in values.items():
            send_elf_mail(emails[k], k, list(v), data['moderators'])
        # send_elf_mail('darkmidnightfury@gmail.com', 'gabe', ['jim', 'joe'], '')
