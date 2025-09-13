# Chat Model Documents: https://python.langchain.com/v0.2/docs/integrations/chat/
import os
from dotenv import load_dotenv
from langchain_google_genai import ChatGoogleGenerativeAI

# Load environment variables from .env
load_dotenv()
google_api_key = os.getenv("GOOGLE_API_KEY")

# Invoke the model
llm = ChatGoogleGenerativeAI(model='gemini-1.5-flash', temperature=0.7)
response = llm.invoke("Which is the world's largest passenger aircraft")
print(response.content)