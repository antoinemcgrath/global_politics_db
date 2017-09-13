## ClimatePolitics.info is embracing a global focus by utilizing International Organization for Standardization codes.
## Mediawiki categories with the following schema will be created as needed:
## -ISO 3166-1 alpha-2 Country codes (also used by Internet's country code top-level domains.)
## -ISO 3166-2 Country subdivision codes
### US-CA is the United States of America with subdivision of California
### https://en.wikipedia.org/wiki/ISO_3166-2:US




#for country in ep.countries():
#    print(country.code, country.slug, 'has', len(country.legislatures()), 'legislatures')

us = ep.country('United-States-of-America')

for country in ep.countries():
    for leg in country.legislatures():
        leg.popolo_url


for country in ep.countries():
     for leg in country.legislatures():
         print()
         #country = country.code
         branch = leg.slug
         branchfullname = leg.name
         url = leg.popolo_url
         print (country.name, branch, url)
         for one in leg.legislative_periods():
             legsess = one.slug
             legname = one.name
             print (legsess, legname)

if dburl == url:
    pass


import pycountry
## We'll use python package pycountry
##  -For ISO country, subdivision, language, currency and script definitions and their translations
##  -Maintained generoursly by Christian Theune (ctheune) of http://flyingcircus.io/
##  -Site: https://pypi.python.org/pypi/pycountry/17.5.14
pycountry.countries.get(alpha_2='US')
pycountry.countries.get(alpha_2='US').name
