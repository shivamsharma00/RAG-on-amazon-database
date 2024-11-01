# src/database.py

from pymongo import MongoClient, ASCENDING
import os
from typing import List, Dict
from pymongo.collection import Collection
import logging
from pymongo.errors import BulkWriteError

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

def get_mongo_client(uri: str = None) -> MongoClient:
    """
    Create a MongoDB client.
    
    Args:
        uri (str): The MongoDB URI.
        
    Returns:
        MongoClient: A MongoDB client instance.
    """
    if uri is None:
        uri = os.getenv("MONGODB_URI", "mongodb://localhost:27017/")
    client = MongoClient(uri)
    logger.info("MongoDB client created successfully.")
    return client

def insert_records(collection, records: List[Dict]) -> None:
    """
    Insert multiple records into a MongoDB collection.

    Args:
        collection (str): The name of the collection to insert records into.
        records (List[Dict]): The list of records to insert.
    """
    try:
        logger.info(f"Inserting {len(records)} records into {collection} collection...")
        collection.insert_many(records)
        logger.info(f"Records inserted successfully.")
    except BulkWriteError as e:
        logger.error(f"BulkWriteError occurred: {e.details}")
    except Exception as e:
        logger.error(f"Error inserting records into {collection} collection: {e}")
        raise e

def create_vector_index(collection) -> None:
    """
    Create a vector index on a collection field.

    Args:
        collection (Collection): The collection to create the vector index on.
        
    """
    logger.info(f"Creating vector index on field {collection.name}....")
    try:
        collection.create_index([('title', ASCENDING)], name='title_index')
        collection.create_index([('text', ASCENDING)], name='text_index')
        collection.create_index([('embedding', 'cosine')], name='embedding_index')

        logger.info(f"Vector index created successfully.")
    except Exception as e:
        logger.error(f"Error creating vector index on field {collection.name}: {e}")
        raise e

def create_collection(db, collection_name: str) -> Collection:
    """
    Create a collection in the database.

    Args:
        db (Database): The database to create the collection in.
        collection_name (str): The name of the collection to create.

    Returns:
        Collection: The created collection.
    """
    logger.info(f"Creating collection {collection_name} in database {db.name}...")
    return db[collection_name]

