# Amazon Reviews Data Pipeline

## Table of Contents
- [Introduction](#introduction)
- [Project Architecture](#project-architecture)
- [Dataset](#dataset)
- [Setup and Installation](#setup-and-installation)
- [Usage](#usage)
- [API Endpoints](#api-endpoints)
- [Design Choices and Trade-offs](#design-choices-and-trade-offs)
- [Scalability and Optimization](#scalability-and-optimization)
- [Future Work](#future-work)
- [Contributing](#contributing)
- [License](#license)

## Introduction

This project implements a data pipeline for ingesting, preprocessing, vectorizing, and querying Amazon product reviews. It also provides an API for searching reviews and generating answers using Retriever-Augmented Generation (RAG).

## Project Architecture

![Architecture Diagram](path_to_architecture_diagram.png)

The pipeline consists of the following components:

1. **Data Ingestion**: Loading data from various file formats into a unified DataFrame.
2. **Data Preprocessing**: Cleaning and transforming the data for efficient storage and retrieval.
3. **Vectorization**: Generating embeddings for unstructured text using a pre-trained language model.
4. **Database Storage**: Inserting records and embeddings into MongoDB, and creating indexes for optimization.
5. **API Layer**: Providing endpoints for searching and generating answers based on user queries.

## Dataset

The project uses the Amazon Reviews dataset, which contains both structured and unstructured data, including product titles, review texts, ratings, and timestamps.

## Setup and Installation

### Prerequisites

- Python 3.8 or higher
- MongoDB 4.4 or higher with vector search capabilities
- CUDA-compatible GPU (for GPU acceleration)
- [SentenceTransformers](https://www.sbert.net/)
- [Transformers](https://huggingface.co/transformers/)
- FastAPI

### Installation

1. **Clone the repository**

   ```bash
   git clone https://github.com/yourusername/amazon-reviews-pipeline.git
   cd amazon-reviews-pipeline

2. **Create a virtual environment and install dependencies**

   ```bash
   python -m venv venv
   source venv/bin/activate
   pip install -r requirements.txt
   ```

3. **Set up environment variables**

   ```bash
   export MONGODB_URI="mongodb://localhost:27017/"
   ```

## Usage

Running the data pipeline:

```bash
python setup.py
```
This script will:

- Load and preprocess the data.
- Generate embeddings using a pre-trained model.
- Insert data into MongoDB and create necessary indexes.

### Starting the API server:

```bash
uvicorn src.api:app --host 0.0.0.0 --port 8000
```

### API endpoints:

- `POST /search`: Search for reviews based on a query.

#### Request body:
```json
{
    "text": "query",
    "top_k": 5
}

#### Response body:
```json
{
  "results": [
    {
      "_id": "5f8f8c44b5e1e2a9c3b0d7a1",
      "title": "Great running shoes",
      "text": "These shoes are incredibly comfortable...",
      "score": 1.2345
    },
    ...
  ]
}
```
- `POST /generate`: Generate an answer based on a query.

#### Request body:
```json
{
    "text": "query",
    "top_k": 5
}
```

#### Response body:
```json
{
    "answer": "answer"
}
```
