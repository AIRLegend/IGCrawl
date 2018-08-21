![](https://upload.wikimedia.org/wikipedia/commons/thumb/e/e7/Instagram_logo_2016.svg/132px-Instagram_logo_2016.svg.png)
# IGCrawl
### Open socurce Instagram scraper

This code is part of a personal project focused in social media analytics. I am releasing this part of my software for anyone who wants to get data from Instagram. Currently it's possible to mine:

* **User info:** User id, username, followers, followings, posts, whether is a company profile or private.
* **Posts info:** Post url (photo), text and number of likes.

##Install
Clone this repo and run this command:
> python3 setup.py install

##Uninstall
Run this command
> pip3 remove IGCrawl

##Explanation

The module consists of three classes: 

* **IGCrawl:** The class which gets the data. It returns objects of the other classes.
	* It needs an username/password of a existing Instagram account. I recommend using a dummy one.

* **IGCUser:** This class represents an Instagram user.

* **IGPost:** This class represents a post in Instagram.

There are more comments in the code.

