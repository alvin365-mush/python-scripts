import requests
import pymongo
import datetime
import logging

# Set up logging
logging.basicConfig(filename='job_update.log', level=logging.INFO)

# Connect to MongoDB
uri = 'mongodb server uri'
client = pymongo.MongoClient(uri)
db = crafter_jobs

# Fetch data from RapidAPI
url = "https://jsearch.p.rapidapi.com/search"

querystring = {"query":"all in kenya","page":"1","num_pages":"1"}

headers = {
	"X-RapidAPI-Key": "key",
	"X-RapidAPI-Host": "jsearch.p.rapidapi.com"
}

response = requests.request("GET", url, headers=headers, params=querystring)
data = response.json()

# Insert new jobs into MongoDB
for job in data:
    job_id = job['job_id']
    if db.jobs.count_documents({'job_id': job_id}) == 0:
        job['created_at'] = datetime.datetime.utcnow()
        db.jobs.insert_one(job)
        logging.info(f'Inserted job with ID {job_id}')

# Remove expired jobs from MongoDB
current_time = datetime.datetime.utcnow()
expired_jobs = db.jobs.find({'job_offer_expiration_timestamp': {'$lt': current_time}})
for job in expired_jobs:
    job_id = job['job_id']
    db.jobs.delete_one({'job_id': job_id})
    logging.info(f'Deleted job with ID {job_id}')

