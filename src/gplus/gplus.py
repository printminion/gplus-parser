'''
Created on Nov 16, 2012

@author: cr
'''
import urllib2
import urllib
import json
from time import sleep

from gparser import gparser

FOLDER_CACHE = './cache/'
GPLUS_COOKIE = ''

def searchPlace(local, name):

    #https://plus.google.com/local/Munich/s/35%20Millimeter

    cacheFile =  '%splacesearch_%s_%s.json' % (FOLDER_CACHE, local, name)
        
    #AF_initDataCallback
    if ifCached(cacheFile):
        #get cached version
        myFile = open(cacheFile, 'r')
        gjson = myFile.read()
        myFile.close()
        
        obj = json.loads(gjson)
        
        return obj

    headers = {
               "accept": "*/*"
    #,"accept-charset":"ISO-8859-1,utf-8;q=0.7,*;q=0.3"
    #,"accept-encoding":"gzip,deflate,sdch"
    #,"accept-language":"de,ru;q=0.8,en-US;q=0.6,en;q=0.4"
    ,"cookie": GPLUS_COOKIE
    #,"referer":"https://plus.google.com/_/apps-static/_/js/home/b,lcs/rt=h/ver=xNU4cE53wdQ.en./sv=1/am=!RJB-ZogI5Z2JBe3iEb3PwHwe4usp6Q4EaICEaDKPAvqDLP3Ur3R3cqb9/d=1/rs=AItRSTP1hM9j_veN38zpYcW_h8yB6SDGiw"
    ,"user-agent":"Mozilla/5.0 (X11; Linuxheaders x86_64) AppleWebKit/537.11 (KHTML, like Gecko) Chrome/23.0.1271.64 Safari/537.11"
    #,"x-chrome-uma-enabled": "1"
    #,"x-chrome-variations":"CLC1yQEIk7bJAQihtskBCKK2yQEIp7bJAQiptskBCLe2yQEIwYPKAQ=="
    #,"x-same-domain":"1"
    }
    

#    if location == '':
#        location = '*'
    
    url = 'https://plus.google.com/local/%s/s/%s' % (local, name)
    
#    request = urllib2.Request(url)
    request = urllib2.Request(url, headers=headers)

    f = urllib2.build_opener().open(request)
    response = f.read()
    #print response
    
    filter = "({key: '58', isError:  false , data: "
    response = response[response.find(filter) + len(filter):]
    
#    response = "({key: '5', isError:  false , data: %s" % response
    response = response[:response.find('});</script>')]
    
#    gjson = response
    
    gjson = gparser.toJSON(response)
    
    #print gjson
    
    myFile = open(cacheFile, 'w')
    myFile.write(gjson)
    myFile.close()
    
    obj = json.loads(gjson)
    return obj


def searchPlaces(location):
    #https://plus.google.com/local/M%C3%BCnchen%2C%20Germany
    
    cacheFile =  '%ssearchPlaces_%s.json' % (FOLDER_CACHE, location)
        
    if ifCached(cacheFile):
        #get cached version
        myFile = open(cacheFile, 'r')
        gjson = myFile.read()
        myFile.close()
        
        obj = json.loads(gjson)
        
        return obj
    
    url = 'https://plus.google.com/_/local/' + location + '/s/by:experts%20restaurants?hl=en&ozv=es_oz_20121114.12_p2&avw=lc%3A2&_reqid=840204&rt=j'
    
    headers = {
               "accept": "*/*"
    #,"accept-charset":"ISO-8859-1,utf-8;q=0.7,*;q=0.3"
    #,"accept-encoding":"gzip,deflate,sdch"
    #,"accept-language":"de,ru;q=0.8,en-US;q=0.6,en;q=0.4"
    ,"cookie": GPLUS_COOKIE
    #,"referer":"https://plus.google.com/_/apps-static/_/js/home/b,lcs/rt=h/ver=xNU4cE53wdQ.en./sv=1/am=!RJB-ZogI5Z2JBe3iEb3PwHwe4usp6Q4EaICEaDKPAvqDLP3Ur3R3cqb9/d=1/rs=AItRSTP1hM9j_veN38zpYcW_h8yB6SDGiw"
    #,"user-agent":"Mozilla/5.0 (X11; Linuxheaders x86_64) AppleWebKit/537.11 (KHTML, like Gecko) Chrome/23.0.1271.64 Safari/537.11"
    #,"x-chrome-uma-enabled": "1"
    #,"x-chrome-variations":"CLC1yQEIk7bJAQihtskBCKK2yQEIp7bJAQiptskBCLe2yQEIwYPKAQ=="
    #,"x-same-domain":"1"
    }
    
    request = urllib2.Request(url, headers=headers)
    f = urllib2.build_opener().open(request)
    response = f.read()
    gjson = gparser.toJSON(response)
    
    myFile = open(cacheFile, 'w')
    myFile.write(gjson)
    myFile.close()
    
    search = json.loads(gjson)
    
    return search


def getUserProfile(profileId, reparse = False, sleepBeforeRequest = 0):
    
    #AF_initDataCallback
    cacheFile =  '%sprofile_%s.json' % (FOLDER_CACHE, profileId)
    response = None
    
    sourceFile = cacheFile.replace('.json', '.html')
    
    if reparse:
        if ifCached(sourceFile):
#            print 'get source html'
            myFile = open(sourceFile, 'r')
            response = myFile.read()
            myFile.close()
    elif ifCached(cacheFile):
        #get cached version
        myFile = open(cacheFile, 'r')
        gjson = myFile.read()
        myFile.close()
        
        obj = json.loads(gjson)

        myFile = open(cacheFile.replace('.json', '.data.json'), 'r')
        data = myFile.read()
        data = json.loads(data)
        myFile.close()
                                
#        return (reviews, locationName, obj)
        return (data, obj)

    url = 'https://plus.google.com/%s/about?gl=EN&hl=en-EN' % profileId
    data = {}
    data['id'] = profileId
    data['status'] = 'parsing'
    
        
    if reparse and response is not None:
        #do no request
        pass
    else:
        try:
            if sleepBeforeRequest > 0:
                sleep(sleepBeforeRequest)
            
            request = urllib2.Request(url)
            f = urllib2.build_opener().open(request)
            response = f.read()
            #print response
        except:
            data['status'] = 'parse error'
            return (data, None)
        
        
        #save html
        myFile = open(cacheFile.replace('.json', '.html'), 'w')
        myFile.write(response)
        myFile.close()
    

    
    data['id'] = profileId
    filter = '<span class="qja">'
    reviews = '0'
    data['reviews'] = 0
    if response.find(filter) > 0:
        reviews = response[response.find(filter) + len(filter):]
        reviews = reviews[:reviews.find('</span>')]
        reviews = reviews.replace(' reviews', '')
        reviews = reviews.replace(' review', '')
        data['reviews'] = reviews
    
#    print 'reviews:%s' % reviews
    
#    myFile = open(cacheFile.replace('.json', '.count'), 'w')
#    myFile.write(reviews)
#    myFile.close()
    
    #<span class="FJ9Y4">Munich Frauenkirche</span>
    
    data['name'] = None
    
    filter = '<span class="FJ9Y4">'  
    locationName = response[response.find(filter) + len(filter):]
    locationName = locationName[:locationName.find('</span>')]
#    myFile = open(cacheFile.replace('.json', '.locationName'), 'w')
#    myFile.write(locationName)
#    myFile.close()
    data['name'] = locationName
#    print 'name:%s' % locationName
    #tagline
      
    data['tagline'] = []
    #<div class="Ca a-f-e">Software Engineer, Munich, Germany</div>
    filter = '<div class="Ca a-f-e">'
    taglinestring = response
    if taglinestring.find('Tagline') > 0:
    
        while taglinestring.find(filter) > 0:
            taglinestring = taglinestring[taglinestring.find(filter) + len(filter):]
            tagline = taglinestring[:taglinestring.find('</div>')]
            taglinestring = taglinestring[len(tagline):]
            data['tagline'].append(tagline)
            
#            print 'tagline:%s' % tagline
    
    data['location'] = []
    #<span class="Yta Zta">Google, Munich</span>
    filter = '<span class="Yta Zta">'
    locationstring = response
    while locationstring.find(filter) > 0:
        locationstring = locationstring[locationstring.find(filter) + len(filter):]
        location = locationstring[:locationstring.find('</span>')]
        locationstring = locationstring[len(location):]
        data['location'].append(location)

#    print data
    
    filter = "({key: '5', isError:  false , data: "
    response = response[response.find(filter) + len(filter):]
    response = response[:response.find('});</script>')]
    gjson = gparser.toJSON(response)
    obj = None
    try:
        data['followers'] = 'failed to parse'
        data['following'] = 'failed to parse'
    
        obj = json.loads(gjson)
        #print gjson
        
        #extend parsed data
        data = parseProfileData(data, obj)
    except:
        pass
    myFile = open(cacheFile.replace('.json', '.data.json'), 'w')
    myFile.write(json.dumps(data))
    myFile.close()
    
    
    myFile = open(cacheFile, 'w')
    myFile.write(json.dumps(obj))
    myFile.close()
    
    
    return (data, obj)

def parseProfileData(data, profile_gjson):
    following = followers = 'hidden'
    #print profile
    data['followers'] = 'hidden'
    data['following'] = 'hidden'
        
    try:
        following = profile_gjson[3][0][0]
    except:
        pass


    try:
        followers = profile_gjson[3][2][0]
    except:
        pass
    
    
    try:
        profile_id = profile_gjson[0]

        data['followers'] = followers
        data['following'] = following
        data['status'] = 'success'
        
    except:
#        printt('%s\t%s\t%s\t%s\tPARSE ERROR' % (profile_id, name, followers, following))
        data['status'] = 'parse error'
        pass            
    
    
    return data


def getPlaceInfo(placeId, sleepBeforeRequest = 0):
    
    #AF_initDataCallback
    cacheFile =  '%splace_%s.json' % (FOLDER_CACHE, placeId)
        
    if ifCached(cacheFile):
        #get cached version
        myFile = open(cacheFile, 'r')
        gjson = myFile.read()
        myFile.close()
        
        obj = json.loads(gjson)

        myFile = open(cacheFile.replace('.json', '.count'), 'r')
        reviews = myFile.read()
        myFile.close()
        
        myFile = open(cacheFile.replace('.json', '.locationName'), 'r')
        locationName = myFile.read()
        myFile.close()
                        
        return (reviews, locationName, obj)

    url = 'https://plus.google.com/%s/about?gl=EN&hl=en-EN' % placeId
    
    
    try:
        if sleepBeforeRequest > 0:
            sleep(sleepBeforeRequest)
        
        request = urllib2.Request(url)
        f = urllib2.build_opener().open(request)
        response = f.read()
        #print response
    except:
        return (0, 'REMOVE THIS ID', None)
    
    
    #save html
    myFile = open(cacheFile.replace('.json', '.html'), 'w')
    myFile.write(response)
    myFile.close()
    
    
    filter = '<span class="qja">'
    reviews = '0'
    if response.find(filter) > 0:
        reviews = response[response.find(filter) + len(filter):]
        reviews = reviews[:reviews.find('</span>')]
        reviews = reviews.replace(' reviews', '')
        reviews = reviews.replace(' review', '')
    
    myFile = open(cacheFile.replace('.json', '.count'), 'w')
    myFile.write(reviews)
    myFile.close()
    
    #<span class="FJ9Y4">Munich Frauenkirche</span>
    
    filter = '<span class="FJ9Y4">'  
    locationName = response[response.find(filter) + len(filter):]
    locationName = locationName[:locationName.find('</span>')]
    myFile = open(cacheFile.replace('.json', '.locationName'), 'w')
    myFile.write(locationName)
    myFile.close()
      
    
    filter = "({key: '5', isError:  false , data: "
    response = response[response.find(filter) + len(filter):]
    
#    response = "({key: '5', isError:  false , data: %s" % response
    response = response[:response.find('});</script>')]
    
    
    gjson = gparser.toJSON(response)
#    gjson = gparser.toJSON(gjson)
    
    
    #print gjson
    
    myFile = open(cacheFile, 'w')
    myFile.write(gjson)
    myFile.close()
    
    obj = json.loads(gjson)
    return (reviews, locationName, obj)

#    return gjson


def userPlaces(placeId, location = ''):
    
    cacheFile =  '%suser_places_%s_%s.json' % (FOLDER_CACHE, placeId, location)
        
    #AF_initDataCallback
    if ifCached(cacheFile):
        #get cached version
        myFile = open(cacheFile, 'r')
        gjson = myFile.read()
        myFile.close()
        
        obj = json.loads(gjson)
        
        myFile = open(cacheFile.replace('.json', '.count'), 'r')
        reviews = myFile.read()
        myFile.close()
        
        
        return (reviews, obj)

    headers = {
               "accept": "*/*"
    #,"accept-charset":"ISO-8859-1,utf-8;q=0.7,*;q=0.3"
    #,"accept-encoding":"gzip,deflate,sdch"
    #,"accept-language":"de,ru;q=0.8,en-US;q=0.6,en;q=0.4"
    ,"cookie": GPLUS_COOKIE
    #,"referer":"https://plus.google.com/_/apps-static/_/js/home/b,lcs/rt=h/ver=xNU4cE53wdQ.en./sv=1/am=!RJB-ZogI5Z2JBe3iEb3PwHwe4usp6Q4EaICEaDKPAvqDLP3Ur3R3cqb9/d=1/rs=AItRSTP1hM9j_veN38zpYcW_h8yB6SDGiw"
    ,"user-agent":"Mozilla/5.0 (X11; Linuxheaders x86_64) AppleWebKit/537.11 (KHTML, like Gecko) Chrome/23.0.1271.64 Safari/537.11"
    #,"x-chrome-uma-enabled": "1"
    #,"x-chrome-variations":"CLC1yQEIk7bJAQihtskBCKK2yQEIp7bJAQiptskBCLe2yQEIwYPKAQ=="
    #,"x-same-domain":"1"
    }
    

    if location == '':
        location = '*'
    
    url = 'https://plus.google.com/local/%s/s/by%%3A%s' % (location, placeId)
    
    
#    request = urllib2.Request(url)
    request = urllib2.Request(url, headers=headers)
    f = urllib2.build_opener().open(request)
    response = f.read()
    #print response
    
    #save html
    myFile = open(cacheFile.replace('.json', '.html'), 'w')
    myFile.write(response)
    myFile.close()
    
    filter = '<div role="button" class="a-f-e c-b c-b-T m3i2xf" tabindex="0">'
    reviews = '0'
    if response.find(filter) > 0:
        reviews = response[response.find(filter) + len(filter):]
        reviews = reviews[:reviews.find('</div>')]
        reviews = reviews.replace(' reviews', '')
        reviews = reviews.replace(' review', '')
            
    #save html
    myFile = open(cacheFile.replace('.json', '.count'), 'w')
    myFile.write(reviews)
    myFile.close()
    
        
    filter = "({key: '58', isError:  false , data: "
    response = response[response.find(filter) + len(filter):]
    
#    response = "({key: '5', isError:  false , data: %s" % response
    response = response[:response.find('});</script>')]
    
#    gjson = response
    
    gjson = gparser.toJSON(response)
    
    #print gjson
    
    myFile = open(cacheFile, 'w')
    myFile.write(gjson)
    myFile.close()
    
    
    obj = json.loads(gjson)
    
    return (reviews, obj)

#    return gjson


def ifCached(file):
    try:
        with open(file) as f: pass
        return True
    except IOError as e:
        return False
   
def searchResultsOnly(userId):
    
    cacheFile =  '%ssearchresultsonly_%s.json' % (FOLDER_CACHE, userId)

    if ifCached(cacheFile):
        #get cached version
        myFile = open(cacheFile, 'r')
        gjson = myFile.read()
        myFile.close()
      
        obj = json.loads(gjson)
        
        return obj
    
    url = "https://plus.google.com/_/local/searchresultsonly?hl=en&ozv=es_oz_20121114.12_p2&avw=lc%3A2&_reqid=49500&rt=j"
    
    
    headers = {
    #:host:plus.google.com
    #:method:POST
    #:path:/_/local/searchresultsonly?hl=en&ozv=es_oz_20121114.12_p2&avw=lc%3A2&_reqid=49500&rt=j
    #:scheme:https
    #:version:HTTP/1.1
    
    "accept":"*/*"
#    ,"accept-charset":"ISO-8859-1,utf-8;q=0.7,*;q=0.3"
#    ,"accept-encoding":"gzip,deflate,sdch"
#    ,"accept-language":"de,ru;q=0.8,en-US;q=0.6,en;q=0.4"
#    ,"content-length":"291"
#    ,"content-type":"application/x-www-form-urlencoded;charset=UTF-8"
    ,"cookie": GPLUS_COOKIE
#    ,"origin":"https://plus.google.com"
#    ,"referer":"https://plus.google.com/_/apps-static/_/js/home/b,lcs/rt=h/ver=xNU4cE53wdQ.en./sv=1/am=!RJB-ZogI5Z2JBe3iEb3PwHwe4usp6Q4EaICEaDKPAvqDLP3Ur3R3cqb9/d=1/rs=AItRSTP1hM9j_veN38zpYcW_h8yB6SDGiw"
#    ,"user-agent":"Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.11 (KHTML, like Gecko) Chrome/23.0.1271.64 Safari/537.11"
#    ,"x-chrome-uma-enabled":"1"
#    ,"x-chrome-variations":"CLC1yQEIk7bJAQihtskBCKK2yQEIp7bJAQiptskBCLe2yQEIwYPKAQ=="
#    ,"x-same-domain":"1"
    }
    
    data = {     
    "f.req": '[[[[4,"Manfred Mueller","by:%s","en",1,[]]],[],null,"*",[],["Munich",[49.057213,11.185937,11.531896,8.457714]]],[10]]' % userId
    ,"at": "AObGSAgm6O26TYJI5-qezaC3vSiROAQNnQ:1353069899379"
    }
    
    data = urllib.urlencode(data)

    request = urllib2.Request(url, data=data, headers=headers)
    f = urllib2.build_opener().open(request)
    response = f.read()
#    print response
    
    gjson = gparser.toJSON(response)
    
    myFile = open(cacheFile, 'w')
    myFile.write(gjson)
    myFile.close()
    
    obj = json.loads(gjson)
    
    return obj
    
        