import crypt
import paramiko
import os


class SSH:
    def __init__(self, host, username, password=None, ssh_key_path=None):
        self.host = host
        self.username = username
        self.ssh = paramiko.SSHClient()
        self.is_connected = False
        self.ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        self.password = password
        self.ssh_key = ssh_key_path
        if password is None and ssh_key_path is None:
            self.ssh_key = f"{os.getenv('HOME')}/.ssh/id_rsa"

    @staticmethod
    def make_hash(password, method='SHA512'):
        if method == 'SHA512':
            method = crypt.METHOD_SHA512
        elif method == 'SHA256':
            method = crypt.METHOD_SHA256
        elif method == 'MD5':
            method = crypt.METHOD_MD5
        return crypt.crypt(password, crypt.mksalt(method))

    def connect(self):
        if self.password is not None:
            self.ssh.connect(self.host, username=self.username, password=self.password)
        else:
            self.ssh.connect(self.host, username=self.username, key_filename=self.ssh_key)
        self.is_connected = True

    def close(self):
        self.ssh.close()
        self.is_connected = False

    def change_password(self, password_hash, user=None):
        if user is None:
            user = self.username
        if not self.is_connected:
            self.connect()
        self.ssh.exec_command(f'echo -n \'{user}:{password_hash}\' | chpasswd -e')
        self.close()
