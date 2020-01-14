import KeepassManager


"""
this is just a demonstation of how to change gh password and update keepass database
in order for this demo to work y need to have github and github-topt (topt secret as password)  entry in your database
"""

man = KeepassManager.KeepassManager()
man.change_gh_password()
