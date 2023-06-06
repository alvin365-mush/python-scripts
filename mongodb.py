import pymongo
import requests
import datetime

# connect to MongoDB
client = pymongo.MongoClient('mongo client')
db = client['mydatabase']
collection = db['jobs']

# fetch data from Rapid API endpoint
url = 'https://rapidapi.com/api/data-jobs/'
headers = {
    'x-rapidapi-key': 'your_api_key',
    'x-rapidapi-host': 'data-jobs.p.rapidapi.com'
}
response = requests.get(url, headers=headers)

# parse data and update MongoDB collection
if response.status_code == 200:
    jobs = response.json()
    for job in jobs:
        # remove existing document with the same job_id
        collection.delete_one({'job_id': job['job_id']})
        # insert new document
        collection.insert_one(job)

    # delete documents with job_offer_expiration_timestamp in the past
    current_timestamp = datetime.datetime.now().timestamp()
    collection.delete_many({'job_offer_expiration_timestamp': {'$lt': current_timestamp}})

