from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from endpoints.delete_endpoint.file_remover import delete_file_router
from endpoints.post_endpoint.cleaner_route import cleaner_router
from endpoints.get_endpoints.live_update import live_update_router


app = FastAPI(
    title="Data Cleaner",
    version="1.0"
)

# CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:5500",
        "http://127.0.0.1:5500",
        "http://localhost:3000"
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"]
)

# Root
@app.get("/")
def root():
    return {
        "message": "Welcome to Quant Calc!",
        "description": "Backend server for Quant Calc.",
        "health_check": "/health",
        "available_endpoints": {
            "DELETE": [
                ["/delete/filename(this is the name of what ever file you uploaded)"]
            ],
            "POST": [
                ["/cleaner/upload"]
            ]
        }
    }

# Health
@app.get("/health")
def health_check():
    return {
        "status": "healthy",
        "message": "CSV/Excel cleaner is running"
    }

app.include_router(delete_file_router)
app.include_router(cleaner_router)
app.include_router(live_update_router)