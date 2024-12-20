from fastapi import APIRouter, HTTPException
from app.services.embedding_handler import generate_embeddings
from app.services.metada_store import MetadataStore
from typing import Optional


router = APIRouter()

@router.post("/generate-embeddings")
async def generate_embeddings_endpoint(bib_doc_id: Optional[int] = None):
    """
    Genera embeddings de abstracts
    para un archivo .bib específico o para todos los documentos.

    Parameters
    ----------
    bibdocument_id : Optional - int
        
    """
    try:
        metadata_store = MetadataStore() 
        # Si `bibdocument_id` es proporcionado, verifica que el archivo exista en la base de datos. 
        if bib_doc_id:
            bibdoc = metadata_store.get_bibdoc_metadata(bib_doc_id)
            if not bibdoc:
                raise HTTPException(status_code=404, detail="Archivo .bib no encontrado.")
            
            # Genera embeddings para el documento específico
            generate_embeddings(bibdoc)

            return {"message": "Embeddings generados y guardados exitosamente.", "bib_document_id": bib_doc_id}
        
        # Si no se proporciona `bibdocument_id`, genera embeddings para todos los documentos

        else:
            store = metadata_store.get_all_metadata()
            all_documents = [{"id": doc_id, **doc_data} for doc_id, doc_data in store.items()]
            if not all_documents:
                 raise HTTPException(status_code=404, detail="No hay documentos para procesar.")

            # Genera y guarda embeddings para todos los documentos
             
            generate_embeddings(store)


            return {"message": "Embeddings generados y guardados exitosamente para todos los documentos."}

    except HTTPException as http_err:
        raise http_err  # Relanza el error HTTP definido previamente
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error interno: {str(e)}")