import requests
import pymongo

# Define app_id
app_id = "6513d6527214df061df75888"

# Define the API URL to fetch user data
user_api_url = "https://dummyapi.io/data/v1/user"

# Set up MongoDB connection
client = pymongo.MongoClient("mongodb://localhost:27017/")
db = client["database_name"]  # Replace 'your_database_name' with your actual database name
users_collection = db["users"]

# Define headers with app_id
headers = {"app-id": app_id}

# Fetch user data from the API
response = requests.get(user_api_url, headers=headers)
user_data = response.json()

# Store user data in the database
users_collection.insert_many(user_data["data"])

# Define the API URL template to fetch user posts
post_api_url_template = "https://dummyapi.io/data/v1/user/{}/post"

# Fetch the list of users from the database
users_list = list(users_collection.find({}, {"id": 1}))

# Set up a collection to store posts data
posts_collection = db["posts"]

# Iterate over each user and fetch their posts
for user in users_list:
    user_id = user["id"]
    post_api_url = post_api_url_template.format(user_id)
    
    # Fetch posts data from the API
    response = requests.get(post_api_url, headers=headers)
    posts_data = response.json()
    
    # Store the posts data in the database
    posts_collection.insert_many(posts_data["data"])
