from config.config import cohere_client
import chromadb 
from chromadb import Documents, EmbeddingFunction, Embeddings


#chroma_client = chromadb.Client()

# Define el directorio donde deseas almacenar la colección
#persist_directory = "../db/collections"

chroma_client = chromadb.PersistentClient(path="db/collections")


# Define la función para obtener embeddings de Cohere
def get_embeddings(text):
    """
    Funcion para generar embeddings.
    """
    response = cohere_client.embed(
        texts=text,
        model="embed-multilingual-v3.0", #Este modelo es el de mayor dimension entre los multilingüe y el de mayor numero de tokens
        input_type="search_document",
        embedding_types=["float"],
    )
    return response.embeddings.float_  # Cohere devuelve embeddings como una lista de listas


# Crea la clase personalizada de EmbeddingFunction para ChromaDB
class MyEmbeddingFunction(EmbeddingFunction):
    def __call__(self, input: Documents) -> Embeddings:
        # Llama a la función de Cohere para obtener las embeddings
        return get_embeddings(input)  # input es una lista de textos

# Creo la coleccion
# Crea una colección usando la función de embeddings personalizada
collection = chroma_client.get_or_create_collection(name="abstracts",
                                        embedding_function=MyEmbeddingFunction(),
                                        metadata = {"hnsw:space": "cosine"}
                                     )


def generate_embeddings(documents: dict):
    """
    Función para almacenar embeddings.


    El texto con el que se genera embeddings son los abstracts de
    articulos. El resto de las llaves se usan como metadata.
    Parameters
    ----------
    documents : Metadatastore instance        

    """
    ids = []   
    metadata_list = []
    abstracts = []

    for clave, valor in documents.items():
        ids.append(clave)
        abstracts.append((valor['abstract']))
        # Crear una copia del diccionario sin el campo 'abstract'
        metadata = {k: v for k, v in valor.items() if k != 'abstract'}
        
        # Agregar la metadata (sin el abstract) a la lista de metadata
        metadata_list.append(metadata)

        
    # Obtén los embeddings para los fragmentos de texto
    collection.add(
        documents= abstracts,
        metadatas= metadata_list,
        ids= ids
    )
    
def prompt_query(prompt):
    results = collection.query(
        query_texts= prompt,  # Pasamos el prompt
        n_results=3  # Número de resultados a retornar
    )
    return results

def generated_query(sentence_generated):
    results = collection.query(
        query_texts= sentence_generated,  # Pasamos el prompt
        n_results=1  # Número de resultados a retornar
    )
    return results





