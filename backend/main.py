import os
import sys
import uvicorn
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from contextlib import asynccontextmanager

# Add the parent directory (backend) to the Python path 
# This allows importing modules inside the backend directory (e.g., backend.core)
sys.path.append(os.path.dirname(os.path.abspath(__file__))) 
sys.path.append(os.path.join(os.path.dirname(os.path.abspath(__file__)), '..'))

# -----------------
# 1. LIFESPAN CONTEXT MANAGER
# This context manager handles startup and shutdown logic for the application.
# Currently, it only logs the application state, but can be extended for DB connection, etc.
# -----------------

@asynccontextmanager
async def lifespan(app: FastAPI):
    """
    Handles startup and shutdown events for the application.
    """
    # Startup Events
    print("Application Startup: Vira-AI Modular Backend starting up...")
    
    # The application runs here (yield)
    yield
    
    # Shutdown Events
    print("Application Shutdown: Vira-AI Modular Backend shutting down...")

# -----------------
# 2. APPLICATION INITIALIZATION
# Initialize the FastAPI application with metadata and the defined lifespan.
# -----------------

app = FastAPI(
    title="Vira-AI Modular Backend API",
    description="Core services for ViraAI applications, supporting various AI modules.",
    version="1.0.0",
    docs_url="/docs",
    redoc_url="/redoc",
    lifespan=lifespan
)

# -----------------
# 3. CORS MIDDLEWARE
# Configure Cross-Origin Resource Sharing (CORS) to allow frontend access.
# Allow all origins, credentials, methods, and headers for development simplicity.
# IMPORTANT: In production, restrict 'origins' to your actual frontend domain(s).
# -----------------

origins = ["*"]  # Allow all origins for development ease

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# -----------------
# 4. PRIMARY ROUTES
# Define basic health and root routes. 
# More complex routes (API endpoints) will be added from other modules later.
# -----------------

@app.get("/", tags=["Health"])
async def root():
    """
    Root endpoint to confirm the API is running.
    """
    return {"message": "Vira-AI Modular Backend is Online!"}

@app.get("/health", tags=["Health"])
async def health_check():
    """
    Standard health check endpoint.
    """
    return {"status": "ok", "service": "vira-ai-modular"}

# -----------------
# 5. SERVER RUNNER
# Standard entry point to run the application using Uvicorn directly if executed as a script.
# This part is typically used for local development, as deployment environments 
# (like Cloud Run or Hugging Face Spaces) run the server command directly (e.g., uvicorn main:app).
# -----------------

if __name__ == "__main__":
    # Get port from environment variable, default to 8000
    port = int(os.environ.get("PORT", 8000))
    # Run the Uvicorn server
    uvicorn.run(app, host="0.0.0.0", port=port)
