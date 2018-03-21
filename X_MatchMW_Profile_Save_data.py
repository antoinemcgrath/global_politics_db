import mwclient
import re
import os
from fuzzywuzzy import fuzz  #Import Matching
from fuzzywuzzy import process  #Import Matching
from pymongo import MongoClient

connection = c = MongoClient()  #Setup MongoDB
def connect_mongoDB():
    db = connection.global_politics #db.tweets.ensure_index("id", unique=True, dropDups=True)
    print("Mongo global_politics DB Connected")
    # The MongoDB connection info. Database name is global_politics and your collection name is climate_politics.
    #db.climate_politics.create_index( "id", unique=True, dropDups=True )
    collection = db.climate_politics
    print("Collection climate_politics connected")
    return(collection)


collection = connect_mongoDB()
#End MongoDB Setup



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



states = {
        'Alaska': 'AK',
        'Alabama': 'AL',
        'Arkansas': 'AR',
        'American Samoa': 'AS',
        'Arizona': 'AZ',
        'California': 'CA',
        'Colorado': 'CO',
        'Connecticut': 'CT',
        'District of Columbia': 'DC',
        'Delaware': 'DE',
        'Florida': 'FL',
        'Georgia': 'GA',
        'Guam': 'GU',
        'Hawaii': 'HI',
        'Iowa': 'IA',
        'Idaho': 'ID',
        'Illinois': 'IL',
        'Indiana': 'IN',
        'Kansas': 'KS',
        'Kentucky': 'KY',
        'Louisiana': 'LA',
        'Massachusetts': 'MA',
        'Maryland': 'MD',
        'Maine': 'ME',
        'Michigan': 'MI',
        'Minnesota': 'MN',
        'Missouri': 'MO',
        'Northern Mariana Islands': 'MP',
        'Mississippi': 'MS',
        'Montana': 'MT',
        'National': 'NA',
        'North Carolina': 'NC',
        'North Dakota': 'ND',
        'Nebraska': 'NE',
        'New Hampshire': 'NH',
        'New Jersey': 'NJ',
        'New Mexico': 'NM',
        'Nevada': 'NV',
        'New York': 'NY',
        'Ohio': 'OH',
        'Oklahoma': 'OK',
        'Oregon': 'OR',
        'Pennsylvania': 'PA',
        'Puerto Rico': 'PR',
        'Rhode Island': 'RI',
        'South Carolina': 'SC',
        'South Dakota': 'SD',
        'Tennessee': 'TN',
        'Texas': 'TX',
        'Utah': 'UT',
        'Virginia': 'VA',
        'Virgin Islands': 'VI',
        'Vermont': 'VT',
        'Washington': 'WA',
        'Wisconsin': 'WI',
        'West Virginia': 'WV',
        'Wyoming': 'WY',
        '': ''
}









cat_list = ['Candidates']

page_list = []
for cat in cat_list:
  for a_page in site.Categories[cat]:
      listpage = site.Pages[a_page]
      page_list += [listpage.name]

def DB_add_Q_values(db_match, Q1_text, Q2_text, Q3_text):
    collection.update_one({
        '_id': db_match['_id']
    }, {
        '$set': {
            'crowdsourced.Q1': Q1_text,
            'crowdsourced.Q2': Q2_text,
            'crowdsourced.Q3': Q3_text
        }
    }, upsert=False)
    print("updated: ", db_match['_id'], db_match['bio_name'])



##Capture crowdsourced_values
mw_handles_list =[]
for page in page_list:
    one_page = site.Pages[page]
    page_text = one_page.text()

    State_start = page_text.find("|State=")+7
    if State_start != 6:
        State_end = page_text[State_start:].find("|") + State_start
        State_text = (page_text[State_start:State_end]).replace('\n','')
        #State_code = next(filter(lambda x: State_text in states[x], states))
        State_code = states[State_text]
    else:
        print("NO STATE??")
        State_code = ""

    Q1_start = page_text.find("|Q1=")+4
    if Q1_start != 3:
        Q1_end = page_text[Q1_start:].find("|") + Q1_start
        Q1_text = page_text[Q1_start:Q1_end]
    else:
        #print("no Q1")
        Q1_text = ""


    Q2_start = page_text.find("|Q2=")+4
    if Q2_start != 3:
        Q2_end = page_text[Q2_start:].find("|") + Q2_start
        Q2_text = page_text[Q2_start:Q2_end]
    else:
        Q2_text = ""

    Q3_start = page_text.find("|Q3=")+4
    if Q3_start != 3:
        Q3_end = page_text[Q3_start:].find("|") + Q3_start
        Q3_text = page_text[Q3_start:Q3_end]
    else:
        Q3_text = ""

    #print ("WM page name is: ", one_page.name)
    #print(Q1_start, Q2_start, Q3_start)
    #print ("Q1: ", Q1_text)
    #print ("Q2: ", Q2_text)
    #print ("Q3: ", Q3_text)




    #Q1 = "|Q1="
    #Q2 = "|Q2="
    #Q3 = "|Q3="
    matches = collection.find({"career_data.career_current_state": State_code})
    for db_match in matches:


        #print("DB state matches include: ", State_code)
        #print(match['bio_name'])

        confidence = eval = fuzz.ratio(db_match['bio_name'], one_page.name)

        #### 4.  Approve or reject matches
        if confidence >= 85:  # More than 80, High confidence match
            print("Match!  MW profile name =  One in DB")
            print(str(confidence) + ": " + db_match['bio_name'] + " = " + str(one_page.name) + "   High confidence, more than 85")
            DB_add_Q_values(db_match, Q1_text, Q2_text, Q3_text)
            pass
        if confidence < 60:  # Less than 70, unlikely that there is a match
            #print(str(confidence) + ": " + match['bio_name'] + " = " + str(one_page.name) + "   Low confidence, less than 50")
            pass
        elif confidence in range(60, 85):  # Match is in the 70-80 range you decide!
            print(str(confidence) + ": " + db_match['bio_name'] + " = " + str(one_page.name) + "   Med confidence, between 85 and 60")

            print("Uncertain 60-85 range. Visit users page. Is it a match y/n?")
            usertext = input("\n")
            if usertext == "y":
                print("Match, adding handle to profile")
                DB_add_Q_values(db_match, Q1_text, Q2_text, Q3_text)
            else:
                print("Not a match")



    one_page = page_text = None
    State_start = State_end = State_text = State_code = None
    Q1_start = Q1_end = Q1_text = None
    Q2_start = Q2_end = Q2_text = None
    Q3_start = Q3_end = Q3_text = None