import os
import json
from pymongo import MongoClient
from datetime import datetime
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# MongoDB connection string from environment variable
MONGO_URI = os.getenv("MONGO_URI")
if not MONGO_URI:
    raise ValueError("Environment variable MONGO_URI is not set correctly!")

def json_serializable(data):
    """
    Handles serialization of non-JSON serializable data types.

    Args:
        data: The data to be serialized.

    Returns:
        Serialized data (e.g., bytes converted to strings or datetime to ISO 8601 format).
    """
    if isinstance(data, bytes):
        return data.decode("utf-8")  # Convert bytes to string
    if isinstance(data, datetime):
        return data.isoformat()  # Convert datetime to ISO 8601 format
    raise TypeError(f"Object of type {type(data)} is not JSON serializable")

def download_all_collections_to_json(database_name, collections, output_dir):
    """
    Downloads all collections from a specified MongoDB database and saves them as JSON files.

    Args:
        database_name (str): The name of the database.
        collections (list): A list of collection names to export.
        output_dir (str): Directory to save the output JSON files.
    """
    # Connect to MongoDB
    client = MongoClient(MONGO_URI)
    db = client[database_name]

    # Ensure the output directory exists
    os.makedirs(output_dir, exist_ok=True)

    # Iterate over each collection
    for collection_name in collections:
        collection = db[collection_name]
        
        # Retrieve all documents from the collection
        documents = list(collection.find())
        
        # Process special data types in documents
        for doc in documents:
            for key, value in doc.items():
                if isinstance(value, bytes):  # Handle bytes
                    doc[key] = value.decode("utf-8")
                elif isinstance(value, datetime):  # Handle datetime
                    doc[key] = value.isoformat()
                elif isinstance(value, dict):  # Handle nested dictionaries
                    doc[key] = json.loads(json.dumps(value, default=json_serializable))
                elif isinstance(value, list):  # Handle lists
                    doc[key] = [
                        json_serializable(item) if isinstance(item, (bytes, datetime)) else item
                        for item in value
                    ]
            # Convert ObjectId to string
            doc["_id"] = str(doc["_id"])
        
        # Save the documents to a JSON file
        output_file = os.path.join(output_dir, f"{collection_name}.json")
        with open(output_file, "w", encoding="utf-8") as file:
            json.dump(documents, file, indent=4, ensure_ascii=False)
        
        print(f"Collection '{collection_name}' exported to '{output_file}'.")

    print("All collections have been exported successfully.")

if __name__ == "__main__":
    # Database and collection configuration
    DATABASE_NAME = "prod"
    COLLECTIONS = [
        "f24-points-syst",
        "forgot-password",
        "houses",
        "magicLinks",
        "slackMessages",
        "teams",
        "users"
    ]
    # Update OUTPUT_DIR to point to ../data
    OUTPUT_DIR = os.path.join("..", "data/collections_json")

    # Call the function to download all collections to JSON
    download_all_collections_to_json(DATABASE_NAME, COLLECTIONS, OUTPUT_DIR)
