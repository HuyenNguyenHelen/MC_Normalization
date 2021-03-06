import requests
import os
import json
import pandas as pd
import csv
import datetime
import dateutil.parser
import unicodedata
import time

bearer_token = "AAAAAAAAAAAAAAAAAAAAAPgJRAEAAAAAIc0NpzUA1KRaN%2FtSin7SfsZcYqM%3DSDbN6Dmb7NMxbxgkovOpYrmBUIYF8S2CganOgxgqrzztUrLaIy"  # os.environ.get("BEARER_TOKEN")


def create_headers(bearer_token):
    headers = {"Authorization": "Bearer {}".format(bearer_token)}
    return headers


def create_url(keyword, start_date, end_date, max_results=500):
    search_url = "https://api.twitter.com/2/tweets/search/all"  # Change to the endpoint you want to collect data from

    # change params based on the endpoint you are using
    query_params = {'query': keyword,
                    'start_time': start_date,
                    'end_time': end_date,
                    'max_results': max_results,
                    # 'expansions': 'author_id,in_reply_to_user_id,geo.place_id',
                    'tweet.fields': 'text,author_id,created_at,lang',
                    'next_token': {}}
    return (search_url, query_params)


def connect_to_endpoint(url, headers, params, next_token=None):
    params['next_token'] = next_token  # params object received from create_url function
    response = requests.request("GET", url, headers=headers, params=params)
    print("Endpoint Response Code: " + str(response.status_code))
    if response.status_code != 200:
        raise Exception(response.status_code, response.text)
    return response.json()


path = r"D:\huyen\medical CN\ss-hashtag-generated_twADR_100-500.csv"
df = pd.read_csv(path, sep=',')
df['hashtags'] = df['hashtags'].replace(' ', '')
# df["nospace"] = df["concepts"].str.replace(' ', '')
print(df.head(5))

# Inputs for tweets
# bearer_token = auth()
headers = create_headers(bearer_token)
max_results =  500
start_time = '2013-06-06T00:00:00Z'
end_time = '2021-06-26T00:00:00Z'

# Total number of tweets we collected from the loop
total_tweets = 0

# Check if flag is true
for c, j, tags in zip(df['CUI'][468:], df['Concept'][468:], df['hashtags'][468:]):
    # Inputs
    finallist = []
    count = 0  # Counting tweets per time period
    max_count =  3100  # Max tweets per concept
    flag = True
    next_token = None
    if len(str(tags)) > 3:
        for i in tags.split(','):
            # Check if max_count reached
            if count >= max_count:
                break
            print("-------------------")

            print(i)
            print("Token: ", next_token)
            url = create_url(i, start_time, end_time, max_results)
            json_response = connect_to_endpoint(url[0], headers, url[1], next_token)
            result_count = json_response['meta']['result_count']
            if 'next_token' in json_response['meta']:
                # Save the token to use for next call
                next_token = json_response['meta']['next_token']
                print("Next Token: ", next_token)
                if result_count is not None and result_count > 0 and next_token is not None:
                    print("Start Date: ", start_time)
                    sampledict = {"cui": c, "concepts": j, "tweets": json_response}
                    print('--------2222222------', sampledict)
                    finallist.append(sampledict)
                    count += result_count
                    total_tweets += result_count
                    print("Total # of Tweets added: ", total_tweets)
                    print("-------------------")
                    time.sleep(5)
                    # If no next token exists
            else:
                if result_count is not None and result_count > 0:
                    print("-------------------")
                    print("Start Date: ", start_time)
                    sampledict = {"cui": c, "concepts": j, "tweets": json_response}
                    finallist.append(sampledict)
                    print('--------1111111------', sampledict)
                    count += result_count
                    total_tweets += result_count
                    print("Total # of Tweets added: ", total_tweets)
                    print("-------------------")
                    time.sleep(5)

                # Since this is the final request, turn flag to false to move to the next time period.
                flag = False
                next_token = None
            time.sleep(5)
        with open(r"D:\huyen\medical CN\collected_data_add\byHashtag_haihua_July19_" + c + ".json", "w") as f:
            json.dump(finallist, f, indent=4)
    
    else:
        print(None)


print("Total number of results: ", total_tweets)
