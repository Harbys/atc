# atc
Python app that changes passwords for you

**KeepassManager methods**

**KeepassManager(password, dbpath)**  
password - password to decrypt kdbx database : defaults to asking for password  
dbpath - path to databse : defaults to ~/Passwords.kdbx  


**find(query)**  
returns first found entry with provided query  


**edit(query, password)**  
query - title of entry to edit  
password - new password to set in entry  


**add_entry(self, title, username, password, url,  group, notes)**  
title - title of entry  
username - username to set in entry  
password - password to set in entry  
url - urld to set in entry : defaults to empty  
group - entry group : defaults to Root  
notes - entry notes : defaults to empty  


**change_gh_password()**  
changes GitHub password and updates database  
(for GH to work tfa is required)  


**change_reddit_password()**  
changes reddit password and updates database  


**change_fb_password()**  
changes FaceBook password  

**change_password_over_ssh(method, user)**  
changes password over ssh  
methods: SHA512, SHA256, MD5 : defaults to SHA512  
user: username whos password will be changed : defaults to username from database  



## KeePassXC Setup
**for github**  
title github  
username [username]  
password [password]  

title github-topt  
password [topt_secret]  


**for reddit**  
title reddit  
username [username]  
password [password]  

_optional (use when using reddit tfa)_  
title reddit-topt  
password [topt_secret]  


**for FaceBook**
title fb
username [email]
password [password]


**for password change over ssh**
title ssh
username [user_with_root_privileges]
password [password] _optional if using rsa key_
url [host]
notes [path to rsa key] _optional if using password_