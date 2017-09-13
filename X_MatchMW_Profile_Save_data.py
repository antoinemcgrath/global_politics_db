import mwclient
import re
import os

#### Access your MW with bot/admin approved permissions
with open(os.path.expanduser('~') + "/.invisible/mw.csv", 'r') as f:
    e = f.read()
    keys = e.split(',')
    #print(keys)
    login_user = keys[0]  #consumer_key
    login_password = keys[1]  #consumer_secret


ua = 'CPMWTool run by User:1A' #UserAgent bot note
site = mwclient.Site(('http', 'www.climatepolitics.info'), path='/w/',)
site.login(login_user, login_password)

#for one in site.Categories:
#    print(one)

Cand_list = []
for page in site.Categories['Candidates']:
    Cand_list.append(page.name)