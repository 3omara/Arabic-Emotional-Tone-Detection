import pandas as pd
import tweepy as tw

for i in range(10):

    print("Iteration No.: " + str(i) + "\n")
    tweets_df = pd.DataFrame(columns=['user_name','user_location','user_description','user_verified','date','text','source'])

    try:
        tweets_df = pd.read_csv('tweets.csv')
    except:
        pass

    regions_df = pd.read_csv('regions.csv')
    regions_df.drop(regions_df.columns[[0]], axis=1,inplace=True)
    print(regions_df.columns)
    my_api_key = ""
    my_api_secret = ""

    auth = tw.OAuthHandler(my_api_key, my_api_secret)
    api = tw.API(auth, wait_on_rate_limit=True)


    search_query = "Vodafone OR Orange OR Etisalat OR WE OR فودافون OR موبينيل OR اتصالات -filter:retweets"

    if 'maxid' not in regions_df.columns:
        regions_df['maxid'] = 1563619242158788615

    tweet_num = 100
    time_step = 1000000000000000

    latitude_ind = regions_df.columns.get_loc("latitude")
    longitude_ind = regions_df.columns.get_loc("longitude")
    radius_ind = regions_df.columns.get_loc("radius")
    maxid_ind = regions_df.columns.get_loc("maxid")

    for ind, region in enumerate(regions_df['name'].unique()):
        
        print(region + ":")

        if regions_df.iloc[abs(ind), maxid_ind] < 1477066353093877760:
            print("limit reached for this region")
            continue

        latitude = regions_df.iloc[ind, latitude_ind]
        longitude = regions_df.iloc[ind, longitude_ind]
        radius = regions_df.iloc[ind, radius_ind]
        region_maxid = regions_df.iloc[ind, maxid_ind]-1

        geocode = str(latitude)+","+str(longitude)+","+str(radius)+"km"

        tweets = tw.Cursor(api.search_tweets, q=search_query, lang="ar", max_id = region_maxid, geocode=geocode).items(tweet_num)
        tweets_copy = []

        for tweet in tweets:
            tweets_copy.append(tweet)

        tweet_no = len(tweets_copy)
        
        if tweet_no==0:
            regions_df.at[regions_df[regions_df['name']==region].index[0], 'maxid'] = min(regions_df.iloc[abs(ind-1), maxid_ind], regions_df.iloc[abs(ind), maxid_ind] - time_step)
            regions_df.to_csv('regions.csv')
            continue

        regions_df.at[regions_df[regions_df['name']==region].index[0], 'maxid'] = tweets_copy[-1].id

        print("Total Tweets fetched:", tweet_no)


        i = 0
        for tweet in tweets_copy:
            full_text = tweet.text
            try:
                status = api.get_status(tweet.id, tweet_mode = "extended")
                full_text = status.full_text
            except:
                print("failed to retrieve full text of tweet id: " + tweet.id)
                pass
            row = {
                'user_name': tweet.user.name, 
                'user_location': region,
                'user_description': tweet.user.description,
                'user_verified': tweet.user.verified,
                'date': tweet.created_at,
                'text': full_text,
                'source': tweet.source
            }
            row2df = pd.DataFrame.from_records([row])
            tweets_df = pd.concat([tweets_df, row2df], axis=0)

            i+=1

        tweets_df.to_csv('tweets.csv')
        regions_df.to_csv('regions.csv')
        print(str(tweet_no)+" tweets from " + region + " have been retrieved successfully\n")