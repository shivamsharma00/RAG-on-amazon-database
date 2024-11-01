# setup.py

from src.data_ingestion import load_data
from src.preprocessing import preprocess_dataframe
from src.vectorization import generate_embeddings
from src.database import insert_records, get_mongo_client, create_collection, create_vector_index
import logging
import numpy as np

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

def main():

    file_paths = [
        "data/raw/Amazon_Fashion.jsonl", 
        "data/raw/Appliances.csv",
        "data/raw/UnstructuredReviews.txt"
    ]

    # Load data
    df = load_data(file_paths)
    logger.info("data loaded successfully")

    # Preprocess data
    df_clean = preprocess_dataframe(df)
    logger.info("data preprocessed successfully")

    # Generate embeddings
    embeddings = generate_embeddings(df_clean['text'].tolist())
    logger.info("embeddings generated successfully")

    # Prepare data for mongodb
    df_clean['embedding'] = embeddings.tolist()
    records = df_clean.to_dict(orient='records')
    logger.info("data prepared for mongodb successfully")

    # Insert data into mongodb
    client = get_mongo_client()
    db = client['AmazonDataset']
    collection = db['reviews']
    insert_records(collection, records)
    logger.info("data inserted into mongodb successfully")

    # Create indexes
    create_vector_index(collection)
    logger.info("vector index created successfully")

if __name__ == "__main__":
    main()


