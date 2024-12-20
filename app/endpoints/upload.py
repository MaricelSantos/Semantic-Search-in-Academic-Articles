from fastapi import APIRouter, HTTPException, File, UploadFile
from app.services.data_store import data_store_instance , MetadataStore
from typing import Annotated
import bibtexparser

router = APIRouter()


@router.post("/")
async def upload_files(file: Annotated[UploadFile, "Archivo .bib"]):
    """Uploading .bib documents.

    Parameters
    ----------
    data : UploadData
        .bib file with consulted bibliography

    Returns
    -------
    message:
        Result of the process.
    bib_doc_id:
        id of bib. file


    Raises
    ------
        HTTPException
        400: ValueError
    
    """
    try:
        # Verifica la extensión del archivo
        if not file.filename.endswith(".bib"):
            raise HTTPException(status_code=400, detail="El archivo debe tener la extensión .bib")
        
        bib_data = await file.read()

        # Parsea el archivo .bib
        bib_database = bibtexparser.loads(bib_data)

        # Convierte los entries del archivo .bib a una lista de diccionarios
        bib_dict = bib_database.entries
        
        bibdoc_id = data_store_instance.id_bibdoc_counter
        data_store_instance.save_data(bib_dict)
        
        return {"message": "Bibliografía guardada correctamente", "bib_doc_id" : bibdoc_id}
    
    except HTTPException as e:
        # Relanza el error si es un HTTPException ya definido
        raise e
    except ValueError as e:
        raise HTTPException(status_code=400, detail="Error al procesar el archivo .bib: " + str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail="Error interno del servidor: " + str(e))


@router.get("/documents/")
async def get_documents():
    """All saved bibliography.

    Returns
    -------
    Dict
        Each key is the ID of the document
        Each value is the complete dictionary of that document
    
    Raises
    ------
    HTTPException
        404: Raised when no documents are found matching the query.
        500: Raised when an internal server error occurs while processing the request.
    """
    try:
        documents = data_store_instance.get_all_documents()

        if not documents:
            # Devuelve un resultado vacío en lugar de lanzar una excepción
            return {"message": "No hay documentos disponibles", "documents": []}

        # Devuelve los documentos como una lista de objetos con IDs y datos
        return [{"id": doc_id, **doc_data} for doc_id, doc_data in documents.items()]
    
    except HTTPException as http_err:
        raise http_err 
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error interno: {str(e)}")
    
@router.get("/document/{document_id}")
async def get_document(document_id : str):
    """Returns saved data from the requested bibliography.

    Parameters
    ----------
    document_id : str
        "Article name in AuthorYear format"

    Returns
    -------
    Dict
        Information about the requested article

    Raises
    ------
    HTTPException
        404: Document not found
    """
    document = data_store_instance.get_all_data(document_id)
    if not document:
        raise HTTPException(status_code=404, detail="Documento no encontrado")
    return document



@router.get("/documents/articles")
async def get_documents():
    """All saved articles.
    Articles are documents whit abstract.

    Returns
    -------
    Dict
        Each key is the ID of the document
        Each value is the complete dictionary of that document
    
    Raises
    ------
    HTTPException
        404: Raised when no documents are found matching the query.
        500: Raised when an internal server error occurs while processing the request.
    """
    try:
        metadata_store = MetadataStore() 
        articles = metadata_store.get_all_metadata()

        if not articles:
            # Devuelve un resultado vacío en lugar de lanzar una excepción
            return {"message": "No hay articulos disponibles", "documents": []}

        # Devuelve los documentos como una lista de objetos con IDs y datos
        return [{"id": doc_id, **doc_data} for doc_id, doc_data in articles.items()]
    
    except HTTPException as http_err:
        raise http_err 
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error interno: {str(e)}")