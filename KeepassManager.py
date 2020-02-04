import pykeepass
import os
from pykeepass.exceptions import CredentialsIntegrityError
import getpass4
import secrets
import GitHub
import FaceBook
import Reddit
import SSH


class KeepassManager:
    def __init__(self, password, dbpath):
        try:
            if password is None:
                password = getpass4.getpass('Database password:')
            if dbpath is None:
                dbpath = f"{os.getenv('HOME')}/Passwords.kdbx"
            self.database = pykeepass.PyKeePass(dbpath, password=password)
            self.default_group = self.database.root_group
            self.git = None
            self.fb = None
            self.reddit = None
            self.ssh = None
        except CredentialsIntegrityError:
            print("Wrong Password")
            exit()
        except FileNotFoundError:
            print(f'No such File: {dbpath}')
            exit()

    def find(self, query):
        return self.database.find_entries(title=query, first=True)

    def edit(self, query, password):
        self.database.find_entries(title=query, first=True).password = password
        self.database.save()

    def add_entry(self, title, username, password, url="",  group='', notes=""):
        if group != "":
            grouptochange = self.database.find_groups(name=group, first=True)
            if grouptochange is not None:
                group = grouptochange
            else:
                group = self.default_group
        else:
            group = self.default_group

        self.database.add_entry(group, title=title, username=username, password=password, url=url, notes=notes)
        self.database.save()

    @staticmethod
    def create_password(security=1):
        return secrets.token_urlsafe(security*32)

    def init_gh(self):
        gitcreds = self.database.find_entries(title='github', first=True)
        topt = self.database.find_entries(title='github-topt', first=True)
        self.git = GitHub.GitHub(gitcreds.username, gitcreds.password, topt.password)
        del gitcreds, topt

    def change_gh_password(self):
        if self.git is None:
            self.init_gh()
        new_password = self.create_password(2)
        if self.git.changepassword(new_password):
            self.edit('github', new_password)
            return True
        else:
            return False

    def init_fb(self):
        fb_credentials = self.database.find_entries(title='fb', first=True)
        self.fb = FaceBook.FaceBook(fb_credentials.username, fb_credentials.password)
        del fb_credentials

    def change_fb_password(self):
        if self.fb is None:
            self.init_fb()
        new_password = self.create_password(2)
        if self.fb.change_password(new_password):
            self.edit('fb', new_password)
            del new_password
            return True
        else:
            return False

    def init_reddit(self):
        reddit_credentials = self.database.find_entries(title='reddit', first=True)
        reddit_otp = self.database.find_entries(title='reddit-topt', first=True)
        if reddit_otp is not None:
            self.reddit = Reddit.Reddit(reddit_credentials.username, reddit_credentials.password, reddit_otp.password)
        else:
            self.reddit = Reddit.Reddit(reddit_credentials.username, reddit_credentials.password)
        del reddit_otp, reddit_credentials

    def change_reddit_password(self):
        if self.reddit is None:
            self.init_reddit()
        new_password = self.create_password(2)
        if self.reddit.changepassword(new_password):
            self.edit('reddit', new_password)
            del new_password
            return True
        else:
            return False

    def init_ssh(self):
        ssh_credentials = self.database.find_entries(title='ssh', first=True)
        if ssh_credentials is not None:
            self.ssh = SSH.SSH(ssh_credentials.url, ssh_credentials.username, ssh_credentials.password,
                               ssh_credentials.notes)
        del ssh_credentials

    def change_password_over_ssh(self, method='SHA512', user=None):
        if self.ssh is None:
            self.init_ssh()
        new_password = self.create_password(2)
        self.ssh.change_password(self.ssh.make_hash(new_password, method), user)
        self.edit('ssh', new_password)
