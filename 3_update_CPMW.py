import time
import pymongo
from pymongo import MongoClient
connection = c = MongoClient() #### Establish database connection
db = connection.global_politics

UNIXtime = time.time()

resource_country = "US" ## from db_update_profile_sources.py # print(resource_country) #(US)
#terms = ["115"]  ## 115th congress term is of interest
term = "115"  ## 115th congress term is of interest

import mwclient
import re
from sunlight import openstates
import os

#### Access your MW with bot/admin approved permissions
with open(os.path.expanduser('~') + "/.invisible/mw.csv", 'r') as f:
    e = f.read()
    keys = e.split(',')
    #print(keys)
    login_user = keys[0]  #consumer_key
    login_password = keys[1]  #consumer_secret

gov = "US" #Example US or US_CA
branches = ['House', "Senate"]
Upper_District_Var ="['career_data']['career_current_state']"
Lower = "House"
Lower_District_Var ="['career_data']['career_current_district']"

ua = 'CPMWTool run by User:1A' #UserAgent bot note
site = mwclient.Site(('http', 'www.climatepolitics.info'), path='/w/',)
site.login(login_user, login_password)

save_note = "Bot creating US Congressional profiles"
default = "" #Create a result for dictionary response when key does not occure
count = 0

cats = []
for branch in branches:
    cats.append(gov + "-" + branch)

#print(cats)


states = {
        'AK': 'Alaska',
        'AL': 'Alabama',
        'AR': 'Arkansas',
        'AS': 'American Samoa',
        'AZ': 'Arizona',
        'CA': 'California',
        'CO': 'Colorado',
        'CT': 'Connecticut',
        'DC': 'District of Columbia',
        'DE': 'Delaware',
        'FL': 'Florida',
        'GA': 'Georgia',
        'GU': 'Guam',
        'HI': 'Hawaii',
        'IA': 'Iowa',
        'ID': 'Idaho',
        'IL': 'Illinois',
        'IN': 'Indiana',
        'KS': 'Kansas',
        'KY': 'Kentucky',
        'LA': 'Louisiana',
        'MA': 'Massachusetts',
        'MD': 'Maryland',
        'ME': 'Maine',
        'MI': 'Michigan',
        'MN': 'Minnesota',
        'MO': 'Missouri',
        'MP': 'Northern Mariana Islands',
        'MS': 'Mississippi',
        'MT': 'Montana',
        'NA': 'National',
        'NC': 'North Carolina',
        'ND': 'North Dakota',
        'NE': 'Nebraska',
        'NH': 'New Hampshire',
        'NJ': 'New Jersey',
        'NM': 'New Mexico',
        'NV': 'Nevada',
        'NY': 'New York',
        'OH': 'Ohio',
        'OK': 'Oklahoma',
        'OR': 'Oregon',
        'PA': 'Pennsylvania',
        'PR': 'Puerto Rico',
        'RI': 'Rhode Island',
        'SC': 'South Carolina',
        'SD': 'South Dakota',
        'TN': 'Tennessee',
        'TX': 'Texas',
        'UT': 'Utah',
        'VA': 'Virginia',
        'VI': 'Virgin Islands',
        'VT': 'Vermont',
        'WA': 'Washington',
        'WI': 'Wisconsin',
        'WV': 'West Virginia',
        'WY': 'Wyoming'
}


def format_page(cat, x_id, count):
    new_page = a_page = insert = fn = a = b = c = d = e = f = g = h = i = j = k = l = m = n = o = p = q = r = ""
    a = '{{' + x_id['career_data']['career_current_body'] +'\n'
    #fn = str(x_id['bio_data']['bio_given_name'], default)) #BC first_name includes unwanted middle initials
    #fn = str(re.sub(' .*', '', fn))  #BC first_name includes unwanted middle initials
    b = '|Firstname=' + x_id['bio_data']['bio_given_name'] +'\n'
    c = '|Lastname=' + x_id['bio_data']['bio_family_name'] +'\n'
    d = '|Fullname=' + x_id['bio_name'] +'\n'
    #e = '|Nickname=' + str(x.get("Nickname", default)) +'\n'
    f = '|Gender=' + x_id['bio_data']['bio_gender'] +'\n'
    g = '|Office=' + x_id['career_data']['career_current_body'] + '\n'
    h = '|State='+ states[(str(x_id['career_data']['career_current_state']))] +'\n'
    i = '|Wing=' + x_id['career_data']['career_current_floor'] +'\n'
    j = '|Level=' + x_id['career_data']['career_current_body']  +'\n'
    if x_id['career_data']['career_current_body'] == 'US-House':
        k = '|District=' + x_id['career_data']['career_current_state'] + "-" + x_id['career_data']['career_current_district'] + '\n'
    else:
        k = '|District=' + x_id['career_data']['career_current_state']  +'\n'
    l = '|Party=' + x_id['career_data']['career_current_party']  +'\n'
    ll = '|Session=' + x_id['career_data']['career_current_session']  +'\n'
    m = '|OfficialGovSite=' + str(x_id['urls']['urls_website_gov']).replace("['","").replace("']","").replace("[]","") +'\n'
    n = '|AdditionalSite=' + str(x_id['urls']['urls_website_campaign']).replace("['","").replace("']","").replace("[]","") +'\n'
    o = '|Photo=' + x_id['bio_data']['bio_image'] +'\n'
    p = '|id_everypolitician=' + x_id['id_data']['id_everypolitician'] +'\n'
    q = '|id_CP_MW=' +  x_id['id_CP_MW'] +'\n'
    q1 = '|Q1=' +  x_id['crowdsourced']['Q1'] +'\n'
    q2 = '|Q2=' +  x_id['crowdsourced']['Q2'] +'\n'
    q3 = '|Q3=' +  x_id['crowdsourced']['Q3'] +'\n'

    #print(x_id['career_data']['climate_caucus_member'].get(keys,""))


    try:
        if '2015' in x_id['career_data']['climate_caucus_member']:
            print("Q2 in caucus")
            q2preface = str("|Q2=" + x_id['bio_data']['bio_given_name'] + " is a member of the House Climate Solutions Caucus, a bipartisan group of Representatives with a stated goal of working together to achieve action addressing the risks from climate change."+'\n')
            q2 = q2.replace("|Q2=", q2preface)
            print("Q2 in caucus")
            print(q2)

            import sys
            sys.exit()
        else:
            pass
    #except:
     #   print("error")

    print(q2)



    tweeturls = ""
    loop = 0
    for one in (x_id['urls']['urls_twitter']):
        if one == []:
            pass
        else:
            loop += 1
            one = one.replace("['","").replace("']","")
            one = str("|TW"+str(loop) +"=" + one +"\n") # + " " + one[20:] + "]" +"\n")
            tweeturls += one
    qq = tweeturls
    #print (qq)
    #qw = '|TW2=' + str(x_id['urls']['urls_twitter'][1]).replace("['","").replace("']","").replace("[]","") +'\n'
    #qe = '|TW3=' + str(x_id['urls']['urls_twitter'][2]).replace("['","").replace("']","").replace("[]","") +'\n'
    r = '}}'
    insert = (a + b + c + d + f + g + h + i + j + k + l + ll + m + n + o + q + q1 + q2 + q3 + qq + r)

    new_page = x_id['id_CP_MW']
    print(new_page)

    a_page = site.Pages[new_page]
    if a_page.exists == False:
        a_page.save(insert, save_note)
        count = count + 1
        #print (count)
    else:
        a_page.save(insert, save_note)
        #print("Page already exists, will overwrite")
    print(k)
    time.sleep(5)

for cat in cats:
    id_list = []
    ids = db.climate_politics.find({ "career_data.career_current_body" : cat, "career_data.career_current_session" : term})#,{"_id":1})
    #print(ids)
    for id in ids:
    #    id_list.append(id['_id'])
    #print(len(id_list))
    #print(len(id_list))
        #print(id['id_CP_MW'])
        #print(cat)
        #print(id)
        format_page(cat, id, count)