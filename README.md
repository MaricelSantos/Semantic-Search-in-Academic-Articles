# Semantic Search in Academic Articles: A First Aproximation
Initial proof of concept

This project is part of The Final Challenge of Get Talent AI, organized by Pi Data Strategy & Consulting (https://piconsulting.com.ar/)

## Actual Version

The API provided will allow you to extract from .bib files the necessary information to create summaries, paragraphs and sentences, using reliable data and providing the corresponding citation. In order to incorporate these fragments into written productions.
This API uses a RAG method where the consulted documents are the abstracts present in the .bib files. The metadata of these files provides the rest of the context to the LLM.
The implemented LLM model is provided by Cohere (https://cohere.com/).
The vector database is provided by Chroma (https://docs.trychroma.com/docs/overview/introduction).
The API was designed and documented using FastAPI (https://fastapi.tiangolo.com/), incorporating Pydantic for data validation. 
It features a scalable and modular architecture, leveraging FastAPI routers for improved maintainability and flexibility.

### Endpoints
-Upload: Allows you to upload .bib files.
Then you can see all the documents uploaded, the documents that have an abstract and filter by ID: AuthorYear.
-Embedding: Performs the vectorization process of the documents and the saving of the data in the Chroma collection. 
This version saves the data locally by default for all the documents available at the time of its execution.
If you later want to upload new .bib files to add them to the database, you can do so using the .bib file id
-Query: Performs a search for documents that are most similar to the query. Returns the first three with data on author, title, doi, abstract and similarity score.
-Ask: Ask the LLM. The response will be provided in Spanish in this version, accompanied by a groundedness metric to help the user assess the reliability of the answer.


### Instructions for Running the Project

Clone the repository
Create your virtual environment
Make sure you have Python and pip installed
Create a cohere key and put it in confg folder

Install dependencies

```python
pip install -r requirements.txt
```

Run the API

```python
uvicorn app.main:app --reload
```

Database
The repository contains .bib files used for testing and a chroma collection for testing.
