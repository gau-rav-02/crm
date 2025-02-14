import pymongo
from pymongo.server_api import ServerApi
from bson.objectid import ObjectId
from config import MONGO_CONNECTION_STRING

class DatabaseConnection:
    def __init__(self):
        try:
            # Connect using the connection string
            self.client = pymongo.MongoClient(MONGO_CONNECTION_STRING, server_api=ServerApi('1'))
            
            # Verify connection
            self.client.admin.command('ping')
            
            # Select database
            self.db = self.client['nptech_crm']
            
            # Create collections
            self.users_collection = self.db['users']
            self.education_collection = self.db['education']
            self.internships_collection = self.db['internships']
            self.login_collection = self.db['login']
            
            print("Successfully connected to MongoDB Atlas")
        
        except Exception as e:
            print(f"Connection error: {e}")
            self.client = None
            self.db = None

    def authenticate_user(self, username, password):
        user = self.login_collection.find_one({
            'username': username, 
            'password': password
        })
        return user is not None

    def register_user(self, username, password):
        # Check if username already exists
        existing_user = self.login_collection.find_one({'username': username})
        if existing_user:
            return False
        
        # Insert new user
        self.login_collection.insert_one({
            'username': username,
            'password': password
        })
        return True

    def insert_user(self, user_data):
        return self.users_collection.insert_one(user_data).inserted_id

    def insert_education(self, education_data):
        return self.education_collection.insert_one(education_data).inserted_id

    def insert_internship(self, internship_data):
        return self.internships_collection.insert_one(internship_data).inserted_id

    def close(self):
        if self.client:
            self.client.close()