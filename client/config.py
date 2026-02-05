from fastmcp import Client
import os
from dotenv import load_dotenv

load_dotenv()

mcp_client = Client("server/main.py")

api_key=os.getenv("GEMINI_API_KEY")

ia_model = os.getenv("MODEL")
