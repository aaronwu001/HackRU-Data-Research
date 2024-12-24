import os
import pandas as pd
from pymongo import MongoClient
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# MongoDB connection string from environment variable
MONGO_URI = os.getenv("MONGO_URI")
if not MONGO_URI:
    raise ValueError("Environment variable MONGO_URI not found!")

def export_collection_to_csv(database_name, collection_name, output_file):
    """
    Exports all documents from a specified MongoDB collection to a CSV file.

    Args:
        database_name (str): Name of the database.
        collection_name (str): Name of the collection.
        output_file (str): Path to the output CSV file.
    """
    # Function to flatten nested dictionaries
    def flatten_document(doc):
        flat_doc = {}
        for key, value in doc.items():
            if isinstance(value, dict):  # Handle nested dictionaries
                for sub_key, sub_value in value.items():
                    flat_doc[f"{key}_{sub_key}"] = sub_value
            else:
                flat_doc[key] = value
        return flat_doc

    # Connect to MongoDB
    client = MongoClient(MONGO_URI)
    db = client[database_name]
    collection = db[collection_name]

    # Retrieve all documents from the collection
    documents = list(collection.find())

    # Flatten all documents
    flattened_documents = [flatten_document(doc) for doc in documents]

    # Convert to Pandas DataFrame
    df = pd.DataFrame(flattened_documents)

    # Ensure all ObjectId fields are strings for CSV compatibility
    if "_id" in df.columns:
        df["_id"] = df["_id"].astype(str)

    # Ensure the output directory exists
    os.makedirs(os.path.dirname(output_file), exist_ok=True)

    # Save DataFrame to CSV
    df.to_csv(output_file, index=False, encoding="utf-8")

    print(f"All documents from the '{collection_name}' collection in the '{database_name}' database have been exported to '{output_file}'.")


if __name__ == "__main__":
    while True:
        print("\n--- Export MongoDB Collection to CSV ---")
        
        # Get database name, collection name, and output file name from the user
        database_name = input("Enter the database name (default: 'prod'): ") or "prod"
        collection_name = input("Enter the collection name (default: 'users'): ") or "users"
        output_file = input("Enter the output file path (default: '../data/collection_csv/users_collection.csv'): ") or "../data/collection_csv/users_collection.csv"

        # Call the function to export the collection to a CSV file
        try:
            export_collection_to_csv(database_name, collection_name, output_file)
        except Exception as e:
            print(f"An error occurred: {e}")

        # Ask the user if they want to export another collection
        continue_choice = input("Do you want to export another collection? (yes/no): ").strip().lower()
        if continue_choice != "yes":
            print("Exiting program.")
            break
