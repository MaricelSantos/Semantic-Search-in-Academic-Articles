from fastapi import APIRouter, HTTPException
from app.services.embedding_handler import prompt_query
from app.services.data_store import data_store_instance
from app.models.searchresponse import SearchResponse
from typing import List

router = APIRouter()

@router.post("/", response_model=List[SearchResponse])
async def search_embeddings_endpoint(query: str):
    """Returns the 3 most similar documents based on the query.

    Parameters
    ----------
    query : str


    Returns
    -------
    List
        Dict of the 3 most similar documents.
        Content dict: ID, title, author, doi, abstract, similarity_score
                

    Raises
    ------
    HTTPException
        404: Raised when no documents are found matching the query.
        500: Raised when an internal server error occurs while processing the request.
    """
    try:          
        # Genera embeddings para el query específico
        results = prompt_query(query)
        results_list =[]
        for i in range(3):
            result_dict = {
                "ID": results["metadatas"][0][i]["ID"],
                "title": results["metadatas"][0][i]["title"][1:-1],
                "author": results["metadatas"][0][i]["author"],
                "doi": results["metadatas"][0][i]['doi'],
                "abstract": results["documents"][0][i],
                "similarity_score": round(1 - float(results["distances"][0][i]),4)
            }
            results_list.append((SearchResponse(**result_dict)))


        return results_list
    
    except HTTPException as http_err:
        raise http_err 
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error interno: {str(e)}")