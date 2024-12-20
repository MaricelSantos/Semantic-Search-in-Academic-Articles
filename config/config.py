import os
from dotenv import load_dotenv
import cohere 

load_dotenv()  # Load .env file

cohere_api_key: str = os.getenv("COHERE_API_KEY")
cohere_client= cohere.ClientV2()



