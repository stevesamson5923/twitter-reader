#https://developer.twitter.com/
#
#API key:
#H5Jla4zoZcNLtDiuR125fgPhR
#
#API secret key:
#HWSbxGzQYgEhwOigJCrggYWzuGRKNcBX93CPXiyxi9RYYVrBhc
#
#You can regenerate and revoke your access token anytime
#
#Access token :
#493298328-xZkQxyCSr5QkHN8VbGwBaY2SAZNyyH3X3yFrmr6N
#
#Access token secret :
#3cPqkMk12ixa6GAfSly6W6KwuYdK0Uapw2KDZVEmP0wSI

#pipenv install tweepy --python 3.8

#https://www.tweepy.org
import tweepy
#from tweepy import OAuthHandler
import webbrowser
import time

consumer_key = 'H5Jla4zoZcNLtDiuR125fgPhR'
consumer_secret = 'HWSbxGzQYgEhwOigJCrggYWzuGRKNcBX93CPXiyxi9RYYVrBhc'

callback_uri = 'oob'

auth = tweepy.OAuthHandler(consumer_key, consumer_secret)

redirect_url = auth.get_authorization_url() 

#webbrowser.open(redirect_url)
print(redirect_url)