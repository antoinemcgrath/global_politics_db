#from popolo_data.importer import Popolo  #pip install everypolitician-popolo
import time
import pymongo
from pymongo import MongoClient
connection = c = MongoClient() #### Establish database connection
db = connection.global_politics

UNIXtime = time.time()

resource_country = "US" ## from db_update_profile_sources.py # print(resource_country) #(US)
floors = ["Senate", "House"]
#terms = ["115"]  ## 115th congress term is of interest
term = "115"  ## 115th congress term is of interest
source = "mySociety"

#### Define get of most recent US Floor JSON resource from mySociety MongoDB
def get_recent_floor_json(floor):
    mySociety_floor = db.resources.find({"url": {"$regex": floor}}).sort("created_at_UNIXtime", pymongo.DESCENDING)[0]
    #mySociety_floor['created_at_UNIXtime']
    data_source = mySociety_floor_url = mySociety_floor['url']
    #print(mySociety_Senate_url)
    mySociety_floor_data = db.mySociety.find_one({"url": mySociety_floor_url})
    jsonobject = mySociety_floor_data
    return(jsonobject)


#### From Congressional term of interest fetch a list of members ids
#for term in terms:
def get_persons_in_term(jsonobject):
    persons_in_term = []
    for membership in jsonobject['memberships']:
        if membership['legislative_period_id'] == "term/" + term:
            persons_in_term.append(membership['person_id'])
    return persons_in_term


#### From JSON of all members index ids
def get_persons_index(jsonobject):
    persons_index = []
    for person in jsonobject['persons']:
        persons_index.append(person['id'])
    return persons_index



#### Match membership list ids to all members index and print values of interest
def get_person_data(person_in_term, persons_index, jsonobject):
    index = persons_index.index(person_in_term)
    person_json = jsonobject['persons'][index]

    #import json
    #print(json.dumps(person_json, indent=4))


    sourced_data_date = jsonobject['created_at_UNIXtime']

    #source_data
    source_imports = [str(source)+"," +str(sourced_data_date)]
    #print(source_imports)
    source_updated = UNIXtime
    #source_first: unix date
    #pushed_to_mw: unix date
    source_urls = jsonobject['meta']['sources']
    #print(resource_country, floor, term, "sourced_data_date:", sourced_data_date)


    _array = jsonobject['memberships']
    info_type_key = 'person_id'

    info_area_key = "area_id"
    info_party_key = "on_behalf_of_id"
    info_session_key = "legislative_period_id"

    def contacts_array_query(person_json):
        #[[o[info_area_key], o[info_party_key], o[info_session_key]] for o in _array if o[info_type_key] == id]
        result = [[o[info_area_key], o[info_session_key], o[info_party_key]] for o in _array if o[info_type_key] == person_json['id']]
        return result

    resp = contacts_array_query_results = contacts_array_query(person_json)
    loops_length = len(resp)
    career_us_congress_senate = []
    career_us_congress_house = []

    while 0 < loops_length:
        res = resp[loops_length - 1]
        info_area = (res[0].replace(":","/").split("/"))
        country = (info_area)[2]
        state = (info_area)[4]
        session = (res[1]).split("/")[1]
        party = (res[2]).split("/")[1]
        if len(info_area) < 6:
            district = []
            session_floor = "Senate"
            career_us_congress_senate.append([session, session_floor, country, state, district, party])
        else:
            district = (info_area)[6]
            session_floor = "House"
            career_us_congress_senate.append([session, session_floor, country, state, district, party])
        loops_length += -1

    career_us_congress_both = career_us_congress_senate + career_us_congress_house
    for one_career_session in career_us_congress_both:
        if one_career_session[0] == term:
            session = one_career_session[0]
            session_floor = one_career_session[1].capitalize()
            country = one_career_session[2].upper()
            state = one_career_session[3].upper()
            district = one_career_session[4]
            party = one_career_session[5].capitalize()


    #career_data
    career_current_country = country.upper() #ISO 3166 alpha-2
    career_current_subdivision = country + "-" + state # ("ISO 3166 alpha-2" - "ISO 3166 subdivision")
    career_current_state = state #string(ISO 3166 alpha - 2
    career_current_session = session
    career_current_floor = session_floor
    career_current_district = district
    career_current_party = party
    #career_us_executive: list(title, start_date, end_date)
    career_us_congress = career_us_congress_both

    #career_us_ca_executive: list(title, start_date, end_date)
    ####career_us_ca_senate: string
    ####career_us_ca_assembly: string
    #career_us_ca_other: list(title, start_date, end_date)
    #career_us_ca_local: list(title, start_date, end_date)
    #career_candidate_for: list(title, start_date, end_date)


    #bio_data
    bio_name = person_json['name']
    bio_given_name = person_json['given_name']  # firstname
    bio_family_name = person_json['family_name'] # lastname
    bio_gender = person_json['gender'].capitalize()
    bio_birthdate = person_json['birth_date']
    bio_image = person_json['image'].replace("original","225x275")
    bio_images = person_json['images']
    #bio_other_names = person_json['other_names']
    #bio_sort_names = person_json['sort_name']},
    print(bio_name)

    info_value_key = "value"
    info_type_key = "type" # Key to what you want
    _array = person_json['contact_details']
    print(_array)
    def contacts_array_query(query):
        many_results = []
        loop_count = 0
        #while loop_count < (len(_array)):
        result = [o[info_value_key] for o in _array if o[info_type_key] == query]
        #print(result)
        if result == []:
            #print("pass")
            pass
        else:
            #print(result)
            return result
    #contact_data
    contact_fax_gov = contacts_array_query("fax")
    contact_fax_campaign = []
    contact_email_gov = contacts_array_query("email")
    contact_email_campaign = []
    contact_phone_gov = contacts_array_query("phone")
    contact_phone_campaign = []
    contact_contact_page_gov = []
    contact_contact_page_campaign = []
    contact_twitter_gov = contacts_array_query("twitter")
    contact_twitter_campaign = []


    info_value_key = "url"
    info_type_key = "note" # Key to what you want
    _array = person_json['links']
    def links_array_query(query):
        result = [o[info_value_key] for o in _array if o[info_type_key] == query]
        return result
    #urls
    urls_twitter = links_array_query("twitter")
    urls_wiki = links_array_query("Wikipedia (en)")
    urls_instagram = links_array_query("instagram")
    urls_youtube = links_array_query("youtube")
    urls_website_gov = links_array_query("website")
    urls_website_campaign = []

    info_value_key = "identifier"
    info_type_key = "scheme" # Key to what you want
    _array = person_json['identifiers']
    def identifiers_array_query(query):
        result = [o[info_value_key] for o in _array if o[info_type_key] == query]
        return result
    #id_data
    id_everypolitician = person_json['id']
    id_ballotpedia = identifiers_array_query("ballotpedia")
    id_google_entity = identifiers_array_query("google_entity_id")
    id_wikidata = identifiers_array_query("wikidata")
    id_wikipedia = identifiers_array_query("wikipedia")
    id_wikitree = identifiers_array_query("wikitree")
    id_youtube = identifiers_array_query("youtube")
    id_cspan = identifiers_array_query("cspan")
    id_govtrack = identifiers_array_query("govtrack")
    id_maplight = identifiers_array_query("maplight")
    id_opensecrets = identifiers_array_query("opensecrets")
    id_politifact = identifiers_array_query("politifact")
    id_votesmart = identifiers_array_query("votesmart")
    #id_gov_data
    id_gov_bioguide = identifiers_array_query("bioguide")
    id_gov_fec = identifiers_array_query("fec")
    id_gov_thomas = identifiers_array_query("thomas")
    id_gov_uscongress = identifiers_array_query("uscongress")

    career_current_body = str(career_current_country.upper() + "-" + career_current_floor)


    person_update = {
        "career_data":
            {"career_current_body" : career_current_body,
             "career_current_country" : career_current_country,
             "career_current_subdivision": career_current_subdivision,
             "career_current_state": career_current_state,
             "career_current_district": career_current_district,
             "career_current_session": career_current_session,
             "career_current_floor": career_current_floor,
             "career_current_party": career_current_party,
             "career_us_congress": career_us_congress},
             #"career_us_executive": career_us_executive},
             #"career_us_ca_executive": career_us_ca_executive,
             #"career_us_ca_senate": career_us_ca_senate,
             #"career_us_ca_assembly": career_us_ca_assembly,
             #"career_us_ca_other": career_us_ca_other,
             #"career_us_ca_local": career_us_ca_local,
             #"career_candidate_for": career_candidate_for},
        "bio_data":
            {"bio_name": bio_name,
             "bio_given_name": bio_given_name,
             "bio_family_name": bio_family_name,
             "bio_gender": bio_gender,
             "bio_birthdate": bio_birthdate,
             "bio_image": bio_image,
             "bio_images": bio_images},
             #"bio_other_names": bio_other_names,
             #"bio_sort_names" :  bio_sort_names},
        "contact_data":
            {"contact_fax_gov": contact_fax_gov,
             "contact_fax_campaign": contact_fax_campaign,
             "contact_email_gov": contact_email_gov,
             "contact_email_campaign": contact_email_campaign,
             "contact_phone_gov ": contact_phone_gov,
             "contact_phone_campaign": contact_phone_campaign,
             "contact_twitter_gov" : contact_twitter_gov,
             "contact_twitter_campaign" : contact_twitter_campaign,
             "contact_contact_page_gov": contact_contact_page_gov,
             "contact_contact_page_campaign": contact_contact_page_campaign},
        "urls":
            {"urls_twitter": urls_twitter,
             "urls_wiki": urls_wiki,
             "urls_instagram": urls_instagram,
             "urls_youtube": urls_youtube,
             "urls_website_gov": urls_website_gov,
             "urls_website_campaign": urls_website_campaign},
        "id_data":
            {"id_everypolitician": id_everypolitician,
             "id_ballotpedia": id_ballotpedia,
             "id_google_entity": id_google_entity,
             "id_wikidata": id_wikidata,
             "id_wikipedia": id_wikipedia,
             "id_wikitree": id_wikitree,
             "id_youtube": id_youtube,
             "id_cspan": id_cspan,
             "id_govtrack": id_govtrack,
             "id_maplight": id_maplight,
             "id_opensecrets": id_opensecrets,
             "id_politifact": id_politifact,
             "id_votesmart": id_votesmart},
        "id_gov_data":
            {"id_gov_bioguide": id_gov_bioguide,
             "id_gov_fec": id_gov_fec,
             "id_gov_thomas": id_gov_thomas,
             "id_gov_uscongress": id_gov_uscongress},
        "source_imports" : source_imports
             }

    #person_sourced_update ={"source_imports": source_imports}

    #print(person_update)
    return(person_update, id_everypolitician)




#        result = db.climate_politics.update_one(
#        {id_everypolitician: "id_everypolitician"},
#        {"$addToSet":
#            {"career_us_congress":
#                {"$each": [career_us_congress]
#                }
#            }
#        },True
#    )

#    print(result.modified_count)




#### Get most recent US Floor JSON resource from mySociety MongoDB
for floor in floors:
    jsonobject = get_recent_floor_json(floor)
    #popolo = Popolo(jsonobject)

    persons_in_term = get_persons_in_term(jsonobject)
    persons_index = get_persons_index(jsonobject)
    for person_in_term in persons_in_term:
        results = get_person_data(person_in_term, persons_index, jsonobject)
        #print(person_update)
        person_update = results[0]
        id_everypolitician = results[1]
        #print(person_update)
        result = db.climate_politics.update_one(
            {"id_everypolitician": id_everypolitician},
            {'$set':
            {"id_everypolitician": id_everypolitician,
             "bio_name": person_update["bio_data"]['bio_name'],
             "career_current_subdivision": person_update["career_data"]['career_current_subdivision'],
             "career_data": person_update["career_data"],
             "bio_data": person_update["bio_data"],
             "contact_data": person_update["contact_data"],
             "urls": person_update["urls"],
             "id_data": person_update["id_data"],
             "id_CP_MW" : str(person_update["bio_data"]['bio_name'] + "_(" + person_update['career_data']['career_current_body'] + ")").replace(" ", "_"),
             "id_gov_data": person_update["id_gov_data"]}},True
        )
        print(result.modified_count)
        if (result.modified_count) == 0:  #### has recieved new contact append source import to list
            print("Updated")
            db.climate_politics.update_one({"id_everypolitician": id_everypolitician},
                                           {'$push': {"source_imports": person_update['source_imports']}})
        else: #### =0 no update was made content remains the same do not update source
            print("Not Updated")
            pass

    print(floor)
