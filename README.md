# ElfHat
a secret santa organizer 

Randomly generates assignments and emails them to participants.

Usage: 

Create a `.env` file with the following

- `SSL_PORT`: The port to use for ssl.
- `SMTP_URL`: The mail server to attempt to log in at.
- `EMAIL`: The email to send the email out with.
- `PASSWORD`: The password to log in with.
- `TEST_DESTINATION_EMAIL`: The email to use for tests

Install requirements from requirements.txt

```bash
$ pip install -r requirements.txt
```

Then modify `santa.json` with the following information:

- `"participants"`: A list of list pairs (`[["Jakob", "Jakob@example.com"]]`) to create assignments for.
- `"moderators"`: A list of list pairs to send modertor information to.
- `"amount"`: The amount given to each participant for participation in the event.

Then run 

```bash
$ py smtp.py
```
