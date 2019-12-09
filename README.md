# atc
Python app that changes passwords for you

#KeepassManager methods

#KeepassManager(password, dbpath)
password - password to decrypt kdbx database : defaults to asking for password
dbpath - path to databse : defaults to ~/Passwords.kdbx


#find(query)
returns first found entry with provided query


#edit(query, password)
query - title of entry to edit
password - new password to set in entry


#addentry(self, title, username, password, url,  group, notes)
title - title of entry
username - username to set in entry
password - password to set in entry
url - urld to set in entry : defaults to empty
group - entry group : defaults to Root
notes - entry notes : defaults to empty


#initgh()
logs in to GitHub


#changeghpassword()
changes GitHub password
