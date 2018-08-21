"""
This file is part of Foobar.

Foobar is free software: you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation, either version 3 of the License, or
(at your option) any later version.
    
Foobar is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU General Public License for more details.

You should have received a copy of the GNU General Public License
along with Foobar.  If not, see <https://www.gnu.org/licenses/>.
"""

from InstagramAPI import InstagramAPI
import re
import requests as req
import time

class IGCrawl:
    def __init__(self, username, password):
        self.username = username
        self.password = password
        self.API = None
        
    def __login_api(self):
        self.API = InstagramAPI(self.username, self.password)
        self.API.login()

    def __getUserId(self, txt):
        return int(re.search('"id":"(\d*)"', txt)[1])

    def __getNumberFollowers(self, txt):
        return int(re.search('edge_followed_by":{"count":(\d*)', txt)[1])

    def __getNumberFollowing(self, txt):
        return int(re.search('edge_follow":{"count":(\d*)', txt)[1])

    def __getNumberPosts(self, txt):
        return int(re.search('edge_owner_to_timeline_media":{"count":(\d*)', txt)[1])

    def __getIsPrivate(self, txt):
        return bool(re.search('is_private":(\w*),', txt)[1])

    def __getIsCompany(self, txt):
        return bool(re.search('is_verified":(\w*),', txt)[1])

    def __getIsVerified(self, txt):
        return bool(re.search('is_verified":(\w*),', txt)[1])

    # Get the list of users who follow the user.
    def getUserFollowersList(self, userid):
        if self.API is None:
            self. __login_api()
        self.API.getUserFollowers(userid)
        users = self.API.LastJson
        listFo = []
        for user in users['users']: 
            listFo.append(IGUser(user['pk'], user['username'], user['is_private']))
        return listFo

    # Get the list of users which the user follows.
    def getUserFollowingList(self, userid):
        if self.API is None:
            self. __login_api()
        self.API.getUserFollowings(userid)
        users = API.LastJson
        listFo = []
        for user in users['users']: 
            listFo.append(IGUser(user['pk'], user['username'], user['is_private']))
        return listFo


    # Return an user given the username. expand means whether its followers and followings
    # should be loaded or not. It is slower.
    def getUserInfo(self, username, expand = False):
        txt = req.get('https://www.instagram.com/{}/?__a=1/'.format(username)).text   
        user = IGUser()
        if txt is not None:
            user.userid = self.__getUserId(txt)
            user.username = username
            user.num_followers = self.__getNumberFollowers(txt)
            user.num_following = self.__getNumberFollowing(txt)
            user.posts = self.__getNumberPosts(txt)
            user.is_verified = self.__getIsVerified(txt)
            user.is_company = self.__getIsCompany(txt)
            user.is_private = self.__getIsPrivate(txt)
            
            if user.is_private is False:  
                # This will only work if the profile is public
                list_following = self.getUserFollowingList(user.userid)
                list_followers = self.getUserFollowersList(user.userid)
                #Expand following list (get basic info of all users)

                if expand is True:
                    #Get basic info of all childs, but no their childs
                    pool = ThreadPool(4) 
                    pool.map(getUserInfo, list_following, False)
                    pool.map(getUserInfo, list_followers, False) 
        
        return user

    # Get the posts info of an user.
    def getPosts(self, user):
        posts = []
        if user is not None and user.userid > -1:
            if self.API is None:
                self. __login_api()
            self.API.getUserFeed(str(user.userid))
            res = self.API.LastJson
            for item in res['items']:
                try:
                    posts.append(IGPost(item['image_versions2']['candidates'][0], 
                        item['caption']['text'], item['like_count']))
                except:
                    None

        return posts


class IGUser:
    def __init__(self, userid=-1, username='', is_private=False, num_followers = -1, 
            num_following=-1, posts=-1, is_verified = False, is_company = False, 
            list_followers=[], list_following=[]):
        self.userid = userid
        self.username = username
        self.is_private = is_private
        self.num_followers = num_followers
        self.num_following = num_following
        self.posts = posts
        self.is_verified = is_verified
        self.is_company = is_company
        self.list_followers = list_followers
        self.list_following = list_following

    def __str__(self):
        return "{} - {} ---- FOLLOWERS: {}".format(self.userid, self.username, self.num_followers)
    def __repr__(self):
        return str(self)
    def __lt__(self, other):
        return self.num_followers<other.num_followers

class IGPost:
    def __init__(self, url=None, text=None, likes=0):
        self.url = url
        self.text = text
        self.likes = likes

    

    

