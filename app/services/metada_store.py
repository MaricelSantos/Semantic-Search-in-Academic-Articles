class MetadataStore:
    _instance = None

    def __new__(cls, *args, **kwargs):
        if cls._instance is None:
            cls._instance = super(MetadataStore, cls).__new__(cls)
        return cls._instance

    def __init__(self):
        if not hasattr(self, "metadata_store"):
            self.metadata_store = {}

    def update_metadata(self, document_id, metadata):
        self.metadata_store[document_id] = metadata

    def get_metadata(self, document_id):
        return self.metadata_store.get(document_id)

    def get_all_metadata(self):
        return self.metadata_store
    
    def get_bibdoc_metadata(self, bib_doc_id):
        resultado= {}
        for id, subdiccionario in self.metadata_store.items():
            if subdiccionario.get('bib_doc_id') == bib_doc_id:
                resultado[id] = subdiccionario
        return resultado
