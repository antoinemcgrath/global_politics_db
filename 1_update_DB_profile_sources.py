#/Library/Frameworks/Python.framework/Versions/3.5/Resources/Python.app

import time
import requests
import pycountry
from everypolitician import EveryPolitician as ep#### mySociety package
from pymongo import MongoClient
connection = c = MongoClient() #### Establish database connection
db = connection.global_politics



resource_interests = ['US', 'US-CA'] # Country & subdivision codes to gather resources for

#### Get clean seperate lists of the resource interests
def resource_interests_seperation():
    def_resource_countries = []
    def_resource_countries_names = []
    def_resource_subdivisions = []
    for resource_interest in resource_interests:
        #print(resource_interest)
        try:
            name = (pycountry.countries.get(alpha_2=resource_interest).name)
            def_resource_countries.append(resource_interest)
            def_resource_countries_names.append(name)
        except KeyError:
            def_resource_subdivisions.append(resource_interest)
            print(resource_interest, "line 28", "KeyError")
    return(def_resource_countries, def_resource_countries_names, def_resource_subdivisions)


response = resource_interests_seperation()
resource_countries = response[0]
resource_countries_names = response[1]
resource_subdivisions = response[2]
#print(resource_countries, resource_countries_names, resource_subdivisions)
#### Clean resource lists obtained



#### Define the database check to see if db.resources is up to date
def db_check(source_value, key, key_value):
    if db.resources.find({"source": source_value, key: key_value}).count() > 0:
        print("Item already exists")
        pass
    else:
        print("Updating", key, key_value)
        UNIXtime = time.time()
        if key == "url": #### key url import method
            jsonobject = requests.get(key_value).json() # Fetch url json file
            jsonobject['url'] = key_value
            jsonobject['source'] = source_value
            jsonobject['created_at_UNIXtime'] = UNIXtime
            db.mySociety.insert(jsonobject)
            #db.mySociety.save(jsonobject)
            db.resources.insert({'source': source_value, key: key_value, 'created_at_UNIXtime': UNIXtime})
            return(key_value)
        else:
            print("Key value type", key, "does not have an import method")


#### Acquire global_politics resources
## mySociety (Countries Legislatures)

## mySociety is an attempt at globaly listing politicians
## Their current focus is on heads of state and uploading wikidata
## Their docs http://docs.everypolitician.org/repo_structure.html
## The welcome data source identifications and web scrapers (they recomend morph scraping https://morph.io/documentation)
## everypolitician python package https://github.com/everypolitician/everypolitician-python

def get_mySociety_lists():
    def_mySociety_country_code = []    # code
    def_mySociety_country_aliases = []         # [0]slug [1]name [2]code
    for country in ep().countries():
        resp = (country.slug, country.name, country.code)
        def_mySociety_country_aliases.append(resp)    # [0]slug [1]name [2]code
        def_mySociety_country_code.append(country.code)
    return(def_mySociety_country_aliases, def_mySociety_country_code)



response = get_mySociety_lists()
mySociety_country_aliases = response[0]
mySociety_country_code = response[1]
#print (mySociety_country_aliases)
#print (mySociety_country_code)


def get_mySociety_slug(resource_country):
    index = mySociety_country_code.index(resource_country)
    return(mySociety_country_aliases[index][0])


def get_mySociety_current_urls():
    def_mySociety_current_urls = []
    for resource_country in resource_countries:
        mySociety_slug = get_mySociety_slug(resource_country)
        for leg in ep().country(mySociety_slug).legislatures():
            def_mySociety_current_urls.append(leg.popolo_url)
            print(mySociety_slug) # United-States-of-America
    return(def_mySociety_current_urls)


mySociety_db_key_values = get_mySociety_current_urls()

####
keys_to_update = []
for mySociety_db_key_value in mySociety_db_key_values:
    print(mySociety_db_key_value)
    status = db_check("mySociety", "url", mySociety_db_key_value)
    #print(status)
