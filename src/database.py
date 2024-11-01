# src/database.py

from pymongo import MongoClient
import os
from typing import List, Dict
import logging

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
        uri = os.getenv("MONGODB_URI")
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
    except Exception as e:
        logger.error(f"Error inserting records into {collection} collection: {e}")
        raise e

def create_vector_index(collection, field_name: str = 'embedding', index_name: str = 'embedding_index') -> None:
    """
    Create a vector index on a collection field.

    Args:
        collection (str): The name of the collection to create the vector index on.
        field_name (str): The name of the field to create the vector index on.
        index_name (str): The name of the vector index.
    """
    logger.info(f"Creating vector index on field {field_name}....")
    try:
        collection.create_index([(field_name, 'cosine')], name=index_name)
        logger.info(f"Vector index created successfully.")
    except Exception as e:
        logger.error(f"Error creating vector index on field {field_name}: {e}")
        raise e
