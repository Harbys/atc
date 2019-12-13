import pykeepass
import os
from pykeepass.exceptions import CredentialsIntegrityError
import getpass4
import uuid
import GitHub
import FaceBook
import Reddit
import SSH


class KeepassManager:
    def __init__(self, password=getpass4.getpass("Database Password:"), dbpath=f'{os.getenv("HOME")}/Passwords.kdbx'):
        try:
            self.database = pykeepass.PyKeePass(dbpath, password=password)
            self.defaultgroup = self.database.root_group
            self.git = None
            self.fb = None
            self.reddit = None
            self.ssh = None
        except CredentialsIntegrityError:
            print("Wrong Password")
            exit()
        except FileNotFoundError:
            print(f'No such File: {os.getenv("HOME")}/Passwords.kdbx')
            exit()

    def find(self, query):
        return self.database.find_entries(title=query, first=True)

    def edit(self, query, password):
        self.database.find_entries(title=query, first=True).password = password
        self.database.save()

    def addentry(self, title, username, password, url="",  group='', notes=""):
        if group != "":
            grouptochange = self.database.find_groups(name=group, first=True)
            if grouptochange is not None:
                group = grouptochange
            else:
                group = self.defaultgroup
        else:
            group = self.defaultgroup

        self.database.add_entry(group, title=title, username=username, password=password, url=url, notes=notes)
        self.database.save()

    @staticmethod
    def createpassword(security=1):
        pastoret = ""
        for x in range(security):
            pastoret += uuid.uuid4().hex
        return pastoret

    def initgh(self):
        gitcreds = self.database.find_entries(title='github', first=True)
        topt = self.database.find_entries(title='github-topt', first=True)
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

    def initfb(self):
        fbcreds = self.database.find_entries(title='fb', first=True)
        self.fb = FaceBook.FaceBook(fbcreds.login, fbcreds.password)
        del fbcreds

    def initreddit(self):
        redditcreds = self.database.find_entries(title='reddit', first=True)
        reddittopt = self.database.find_entries(title='reddit-topt', first=True)
        if reddittopt is not None:
            self.reddit = Reddit.Reddit(redditcreds.username, redditcreds.password, reddittopt.password)
        else:
            self.reddit = Reddit.Reddit(redditcreds.username, redditcreds.password)
        del reddittopt, redditcreds

    def changeredditpassword(self):
        if self.reddit is None:
            self.initreddit()
        newpassword = self.createpassword(2)
        if self.reddit.changepassword(newpassword):
            self.edit('reddit', newpassword)
            return True
        else:
            return False

    def initssh(self):
        sshcreds = self.database.find_entries(title='ssh', first=True)
        if sshcreds is not None:
            self.ssh = SSH.SSH(sshcreds.url, sshcreds.username, sshcreds.password, sshcreds.notes)
        del sshcreds

    def changesshpassword(self, method='SHA512', user=None):
        if self.ssh is None:
            self.initssh()
        newpassword = self.createpassword(2)
        self.ssh.changepassword(self.ssh.mkhash(newpassword, method), user)
        self.edit('ssh', newpassword)
