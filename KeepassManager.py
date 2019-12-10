import pykeepass
import os
from pykeepass.exceptions import CredentialsIntegrityError
import getpass4
import uuid
import GitHub


class KeepassManager:
    def __init__(self, password=getpass4.getpass("Database Password:"), dbpath=f'{os.getenv("HOME")}/Passwords.kdbx'):
        try:
            self.Database = pykeepass.PyKeePass(dbpath, password=password)
            self.defaultgroup = self.Database.root_group
            self.git = None
        except CredentialsIntegrityError:
            print("Wrong Password")
            exit()
        except FileNotFoundError:
            print(f'No such File: {os.getenv("HOME")}/Passwords.kdbx')
            exit()

    def find(self, query):
        return self.Database.find_entries(title=query, first=True)

    def edit(self, query, password):
        self.Database.find_entries(title=query, first=True).password = password
        self.Database.save()

    def addentry(self, title, username, password, url="",  group='', notes=""):
        if group != "":
            grouptochange = self.Database.find_groups(name=group, first=True)
            if grouptochange is not None:
                group = grouptochange
            else:
                group = self.defaultgroup
        else:
            group = self.defaultgroup

        self.Database.add_entry(group, title=title, username=username, password=password, url=url, notes=notes)
        self.Database.save()

    @staticmethod
    def createpassword(security=1):
        pastoret = ""
        for x in range(security):
            pastoret += uuid.uuid4().hex
        return pastoret

    def initgh(self):
        gitcreds = self.Database.find_entries(title='github', first=True)
        topt = self.Database.find_entries(title='github-topt', first=True)
        self.git = GitHub.GitHub(gitcreds.username, gitcreds.password, topt.password)
        del gitcreds, topt

    def changeghpassword(self):
        if self.git is None:
            self.initgh()
        newpassword = self.createpassword(2)
        if self.git.changepassword(newpassword):
            self.edit('github', newpassword)
            return True
        else:
            return False
