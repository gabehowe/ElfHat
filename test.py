""" 
Simple Unit tests to avoid sending erroneous emails.
Requires manual checking of test email.

usage: source .env && py test.py
"""
import unittest
import os
import randler
import smtp
import ssl
import smtplib
from dotenv import load_dotenv

class TestEmails(unittest.TestCase):
    
    def setUp(self):
        load_dotenv()
        context = ssl.create_default_context();
        self.server = smtplib.SMTP_SSL(os.environ['SMTP_URL'], int(os.environ['SSL_PORT']), context=context)
        self.server.login(os.environ['EMAIL'], os.environ['PASSWORD'])


    def tearDown(self) -> None:
        self.server.close()
        return super().tearDown()


    def test_email(self):
        smtp.send_elf_mail(os.environ['TEST_DESTINATION_EMAIL'], 'gabe', ['jim', 'joe'], [( "", "" )], self.server)
    

    def test_graph(self):
        load_dotenv()
        names = {'Jakob', 'Jason', 'Edward', 'Gottfried', 'Johannes'}
        assignments = randler.generate_all_assignments(names);
        smtp.send_graph_rep(assignments, [('gabriel', os.environ['TEST_DESTINATION_EMAIL'])], self.server)

    
    def test_deployment(self):
        names = {'Jakob', 'Jason', 'Edward', 'Gottfried', 'Johannes'}
        assignments = randler.generate_all_assignments(names);
        emails = {i:os.environ['TEST_DESTINATION_EMAIL'] for i in names}
        smtp.send_assignments(assignments, emails, [('moderator', os.environ['TEST_DESTINATION_EMAIL'])], self.server)


class Others(unittest.TestCase):
    def test_names(self):
        names = {'Jakob', 'Jason', 'Edward', 'Gottfried', 'Johannes'}
        assignments = randler.generate_all_assignments(names);
        appearances = {i: 0 for i in names}
        print(appearances)
        for _ ,(u,v) in assignments:
            appearances[u] += 1
            appearances[v] += 1
        self.assertTrue(all([i == 2 for i in appearances.values()]), str(appearances))



if __name__ == '__main__':
    load_dotenv()
    unittest.main()
