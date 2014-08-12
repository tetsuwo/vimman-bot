import twitter
import secret

api = twitter.Api(
    consumer_key = secret.dict['consumer_key'],
    consumer_secret = secret.dict['consumer_secret'],
    access_token_key = secret.dict['access_token_key'],
    access_token_secret = secret.dict['access_token_secret']
)

api = twitter.Api(consumer_key,consumer_secret,access_token,access_secret)

