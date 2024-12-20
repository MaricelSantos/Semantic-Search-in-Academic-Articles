from typing import List
from app.services.metada_store import MetadataStore
# Clase estructura Singleton
class DataStore:
    _instance = None  # Variable de clase para almacenar la instancia única

    def __new__(cls, *args, **kwargs):
        # Si no existe una instancia, se crea una y se guarda en _instance
        if cls._instance is None:
            cls._instance = super(DataStore, cls).__new__(cls)
        return cls._instance

    def __init__(self):
        # Inicializa la clase solo una vez
        if not hasattr(self, "data_store"):
            self.data_store = {}  # Diccionario para almacenar los datos
            self.metadata_store = MetadataStore()  # Asocia el singleton de metadata
            self.id_bibdoc_counter = 1   # Contador global para los IDs del file

            
            
    def articles_metadata(self, document: dict):
        
        claves_metadata= ['ID', 'title', 'year', 'doi', 'author', 'abstract', 
                          'keywords', 'ENTRYTYPE', 'bib_doc_id']
               
        # Verifica que sea un articulo
        if 'abstract' in document and document['abstract']:
            doc_id = document['ID']
            metadata = {key: value for key, value in document.items() if key in claves_metadata}
            self.metadata_store.update_metadata(doc_id, metadata)
            
    def save_data(self, documents: List[dict]):
        
        for document in documents:
        # Verifica si el articulo ya existe
            if any(d["ID"] == document['ID'] for d in self.data_store.values()):
                raise ValueError("Ya existe bibliografia con el mismo ID.")
            document_id = document['ID']
            self.data_store[document_id]= document
            bibdoc_id = self.id_bibdoc_counter
            document['bib_doc_id'] = bibdoc_id
            self.articles_metadata(document) 
        
        self.id_bibdoc_counter += 1

    def get_all_data(self, document_id):
        # Obtiene un documento específico
        return self.data_store.get(document_id)
        

    def get_all_documents(self):
        # Retorna todos los documentos
        return self.data_store

    def delete_data(self, document_id):
        # Elimina un documento por su ID
        if document_id in self.data_store:
            del self.data_store[document_id]
        else:
            raise ValueError("El documento no existe.")


# Instancia Singleton de DataStore
data_store_instance = DataStore()


