import os
import tweepy
import tw_util
import tw_class

#limit = api.rate_limit_status()

def get_hist_tweet(save_path):

    '''
    1. path: 输出的路径
    '''

    api = tw_util.get_auth_api("pengyuxia")

    '''
    for possible parameters of tweepy.Cursor(api.search...), check 
    https://developer.twitter.com/en/docs/tweets/search/api-reference/get-search-tweets
    '''

    #max_id = '979625831290032128'

    until = '2018-03-30'

    tweets_cursor = tweepy.Cursor(api.search, q="trump", count=100, lang="en", tweet_mode='extended', result_type="recent", include_entities="false", until=until)
    #Two possible attribute for tweets_cursor -> items() or pages()
    #usage: items(nums_limit) -> 'nums_limits' indicates how many tweets you'd like like to get a one time
    #------ if you leave it blank, it will get all tweets.


    nums_line = 5000*500
    nums_file = 3


    writer = tw_class.MyWriter(nums_line, nums_file, "hist", save_path)
        
    while True:

        try:

            for tweet_info in tweets_cursor.items():

                """
                if a tweet object is a retweeted tweet, the text in 'full_text' attribute will be truncated, 
                -- i.e. it is incomplete and end up with "..."
                -- e.g. "It is a go..." 
                -- in this case, the full_text of the original tweet can be found in the "full_text" attribute of "retweeted_status" object.
                -- check https://twittercommunity.com/t/retrieve-full-tweet-when-truncated-non-retweet/75542
                """

                if 'retweeted_status' in dir(tweet_info): # if it is a retweeted tweet
                    tweet_text = tweet_info.retweeted_status.full_text
                else:
                    tweet_text = tweet_info.full_text

                # #tweet_text = str(tweet_text).replace("\n", "")
                #
                # tweet_text = tw_util.process_tweet_text(tweet_text)
                #
                # print(tweet_text)
                #
                # # remaining = api.rate_limit_status()['resources']['search']['/search/tweets']['remaining']
                # # print(remaining)
                #
                # f.write(tweet_text + "\n")

                tweet_text = tw_util.process_tweet_text(tweet_text)
                print(tweet_info.id)
                writer.write_data(tweet_text)


        except tweepy.TweepError as te:
            print(te)
            tw_util.handle_TweepError(api)
            continue
                




if __name__ == "__main__":

    

    path = os.getcwd()

    get_hist_tweet(path+"/data")
