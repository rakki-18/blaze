import tweepy
import csv
import os
from wallet_address import get_wallet_address_from_user

# file_name should be present in the folder
def write_csv(data, file_name):
    with open(file_name, 'a') as outfile:
        writer = csv.writer(outfile)
        writer.writerow(data)


bearer_token = os.environ.get('bearer_token')
client = tweepy.Client(bearer_token=bearer_token, wait_on_rate_limit = True)


# Gets all the followers of the user 'screen_name'
# Stores the data in file_name
# Eg: 
# screen_name = 'elonmusk', file_name = 'elonmusk_followers.csv'
def get_followers(screen_name, file_name):
    user_id = client.get_user(username = screen_name).data.id

    all_user_fields = ['id', 'name', 'username', 'location', 'created_at', 'description', 'entities', 'pinned_tweet_id', 'profile_image_url', 'protected', 'public_metrics', 'url', 'verified', 'withheld']
    # Header
    write_csv(all_user_fields, file_name)



    response = client.get_users_followers(id=user_id, user_fields=all_user_fields, max_results = 1000)

    # Handle when user has 0 followers
    if not response.data:
        return
    
    for user in response.data:
        user_field_response = []
        for field in all_user_fields:
            user_field_response.append(getattr(user,field))

        wallet_address = get_wallet_address_from_user(user_field_response)
        # TODO: add wallet_address also to the csv
        write_csv(user_field_response)
    
    

    while 'next_token' in response.meta:
        next_token = response.meta['next_token']
        response = client.get_users_followers(id=user_id, user_fields=all_user_fields, max_results = 1000, pagination_token=next_token)
        for user in response.data:
            user_field_response = []
            for field in all_user_fields:
                user_field_response.append(getattr(user,field))
            write_csv(user_field_response)

screen_name = 'elonmusk'
file_name = 'followers.csv'



