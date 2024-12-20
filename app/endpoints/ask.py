from fastapi import APIRouter, HTTPException
from app.services.RAG_answer import RAG_answer
from app.models.askresponse import AskResponse


router = APIRouter()

@router.post("/", response_model = AskResponse )
async def RAG_answer_endpoint(query: str):
    """Connect with LLM and generate response.
    The groundedness metric is reported.

    Parameters
    ----------
    query : str
        User query

    Returns
    -------
    query: str
        User query
    response: str
        Model response
    groundedness: float
        Groundedness value
        

    Raises
    ------
    HTTPException
        404: Raised when no documents are found matching the query.
        500: Raised when an internal server error occurs while processing the request.
    
    """
    try:          
    
        response = RAG_answer(query)

   
        return AskResponse(query=query, response=response[0], groundedness= response[1])    
    except HTTPException as http_err:
        raise http_err  
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error interno: {str(e)}")