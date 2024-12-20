from fastapi import FastAPI
from app.endpoints import upload, embeddings, query, ask

app = FastAPI()

# Registrar los routers
# Post upload
app.include_router(upload.router, prefix="/upload", tags=["Upload"])
# Post generate-embedding
app.include_router(embeddings.router, prefix="/embeddings", tags=["embeddings"])
# Post search
app.include_router(query.router, prefix="/search", tags=["search"])
# Post ask
app.include_router(ask.router, prefix="/ask", tags=["ask"])
