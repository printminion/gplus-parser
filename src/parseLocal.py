#https://plus.google.com/local/M%C3%BCnchen%2C%20Germany/s/by%3Aexperts
import urllib2
from gplus import gplus
import sys
import imp
import json
from time import sleep
import gparser

settings = imp.load_source('module.name', './settings.py')

gplus.FOLDER_CACHE = settings.PATH_CACHE
gplus.GPLUS_COOKIE = settings.GPLUS_COOKIE

def printt(str, file = gplus.FOLDER_CACHE + '_profile_run.log'):
    print str
    myFile = open(file, 'aw')
    myFile.write('%s\n' % str)
    myFile.close()
    
    
def searchPlacesByGivenNames(city, places):
    ''' 
    search places by given name
    ''' 
    for place in places:
        #location = urllib2.quote("4 Seasons Restaurant")
    
        search = gplus.searchPlace(city, urllib2.quote(place))#'35%20Millimeter')
    
        try:
            printt('%s\t%s' % (place, search[5][1][0][33][29][7]))
        except:
            printt('%s\t%s' % (place, 'none'))
            
    
    #for place in search[5][1][0][33][29]:
    #    print place[7] #place[0][10]
        
        #print placegplus[10] #place[0][10]reviewer
        
        
        #116313710465364883329
#sys.exit()
#
#search = gplus.searchPlaces('M%C3%BCnchen,%20Germany')
#print search


def parsePlaceReviewers(placeToFetch, sleep = 0):
    
    
    (reviews, name, search) = gplus.getPlaceInfo(placeToFetch, sleep)
    
    printt('%s\t%s\t%s' % (placeToFetch, reviews, name))
    
    if search == None:
        return
    
    
#    print
    #print 'place:%s' % placeToFetch
    #print 'place:%s' % search
    #print 'reviews for place:%s' % search[2][59][7][18][0][1]
    #print 'reviews for place:%s' % search[2][59][7][18][1][1]
    #https://plus.google.com/local/Munich%2C%20Germany/cacheFile =  '%ssearchresultsonly_%s.json' % (FOLDER_CACHE, userId)s/by%3A108939854631801299820
    location = 'Munich%2C%20Germany'
    #location = ''
    #print ''
    #print "reviews for\n%s\t%s" % (placeToFetch, location)
    reviewers = []
    
    
    try:
        reviewers = search[2][59][7][11][0]
    except:
        pass
    
    
    for reviewer in reviewers:
        userName = reviewer[0][0][1]
        #print userName    for place in places:
        if len(reviewer[0][0]) > 2:
            userId = reviewer[0][3]
            #print '    %s' % userId
            #print reviewer
    
            (reviews, userPlaces) = gplus.userPlaces(userId, location) # Aygul
    #        print '    reviewsData:%s' % userPlaces
            #print '    reviewsCount:%s for %s' % (reviews, urllib2.unquote(location))
            
            printt('\t%s\t%s\t%s' % (userId, reviews, userName))
    #        print 'reviews:%s' % userPlaces[5][1][1][33][18][0][1]
            #print 'reviews:%s' % userPlaces[5][1][1][33][18][1]
            #print 'reviews:%s' % userPlaces[5][1][
    #print "------------"
#1][33][18][1][1]
        

    


#get place info
#https://plus.googlparsePlaceReviewerse.com/105673568444741904826/about?gl=DE&hl=en-DE

#parse users

#get user places
#https://plus.google.com/local/*/s/by%3A100637659921903226572
#userPlaces = gplus.userPlaces('101697775213251991950') # Aygul
#print 'reviews:%s' % userPlaces[5][1][1][33][18][reviewer0][1]
#print 'reviews:%s' % userPlareviewsces[5][1][1][33][18][1][1]
#https://plus.google.com/105673568444741904826/about?gl=DE&hl=en-DE
#user = gplus.searchResultsOnly('100637659921903226572') #Manfred Mueller
#print 'reviews:%s' % len(user[0][1][1])
#
#user = gplus.searchgplusResultsOnly('101697775213251991950') # Aygul
#print 'reviews:%s' % len(user[0][1][1])




#print userPlaces



#places = [line.strip() for line in open('places.txt')]
#searchPlacesByGivenNames('Munich', places)

#https://plus.google.printcom/118423825197084813171/about?gl=DE&hl=en-DE

#parsePlaceReviewers('118423825197084813171')#Munich Frauenkirche
#parsePlaceReviewers('102231670071959591188')#Augustiner-Keller

#parsePlaceReviewers('115023799404113624496')#Augustiner-Keller


#myFile = open('/home/cr/develop/python/zagat/cache/place_115023799404113624496.json', 'r')
#gjson = myFile.read()
#myFile.close()
#
#gjson = gparser.gparser.toJSON(gjson)
#obj = json.loads(gjson)

#sys.exit()


#places = [line.strip() for line in open('local_ids.txt')]
#for place in places:
#    parsePlaceReviewers(place, 1)

users = ['113750533748883690330', '105062617611748079921', '110793623474522801689']
users = ['104512463398531242371']
#users = [line.strip() for line in open('profile_ids.txt')]

for user in users:
#    print user
    profile_id = name = None
    following = followers = 'hidden'

    try:
        (reviews, name, profile) = gplus.getUserProfile(user)
    except:
        printt('%s\t%s\t%s\t%s\tPARSE ERROR' % (user, name, followers, following))
        print "Unexpected error:", sys.exc_info()
        continue
    
    #print profile
    try:
        following = profile[3][0][0]
    except:
        pass


    try:
        followers = profile[3][2][0]
    except:
        pass
    
    
    try:
        profile_id = profile[0]
        printt('%s\t%s\t%s\t%s' % (profile_id, name, followers, following))
    except:
        printt('%s\t%s\t%s\t%s\tPARSE ERROR' % (profile_id, name, followers, following))
        pass    
    #print 'name:%s' % name
    #print 'id:%s' % profile_id
    #print 'followers:%s' % followers
    #print 'following:%s' % following
    





sys.exit()



