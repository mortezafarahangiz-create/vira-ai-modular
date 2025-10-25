import os
import json
import requests
from dotenv import load_dotenv
from fastapi import FastAPI
from pydantic import BaseModel
import uvicorn

# Load environment variables
load_dotenv()

HF_API_TOKEN = os.getenv("HF_API_TOKEN")

# Use the DistilGPT2 model for text generation (assuming the 404 issue is resolved or will be temporary)
MODEL_ENDPOINT = "https://api-inference.huggingface.co/models/distilgpt2" 

app = FastAPI()

class Query(BaseModel):
    # For text generation, we just need the question (input prompt)
    question: str

@app.get("/")
def read_root():
    return {"message": "Server is running. Send a POST request to /answer."}

@app.post("/answer")
async def get_answer(query: Query):
    headers = {
        "Authorization": f"Bearer {HF_API_TOKEN}",
        "Content-Type": "application/json"
    }

    # Simplified payload for text generation models (like GPT2/DistilGPT2)
    json_payload = {
        "inputs": query.question,
        "parameters": {
            "max_new_tokens": 64,
            "temperature": 0.8,
            "return_full_text": False 
        }
    }

    try:
        response = requests.post(MODEL_ENDPOINT, headers=headers, json=json_payload, timeout=30)
        response.raise_for_status()
        
        data = response.json()
        
        # Hugging Face API usually returns a list containing 'generated_text'
        if data and isinstance(data, list) and data[0] and 'generated_text' in data[0]:
            answer = data[0]['generated_text'].strip()
            
            return {"answer": answer}
        
        else:
            # If the AI model returns a JSON that is not the expected list structure (e.g., an error message)
            if data and isinstance(data, dict) and 'error' in data:
                 raise Exception(f"AI Model Execution Error: {data.get('error')}")

            raise Exception("Unexpected response format or empty response from AI model.")
            
    except requests.exceptions.HTTPError as e:
        status_code = e.response.status_code
        response_text = e.response.text if e.response.text else 'Service Unavailable'

        # If we get a specific error message from HF, extract it.
        try:
            error_data = e.response.json()
            error_message = error_data.get("error", response_text)
        except:
            error_message = response_text

        if status_code == 401:
            detail = "401: Authentication Failed. Check HF_API_TOKEN validity."
        elif status_code == 404:
            detail = "404: Model Not Found. (Likely a temporary HF issue)."
        elif status_code == 400:
            detail = f"400: Bad Request. Check JSON payload. HF Error: {error_message}"
        else:
            detail = f"{status_code}: {error_message}"

        raise Exception(f"API Error: {detail}")
        
    except Exception as e:
        raise Exception(f"Internal Server Error: {e}")
