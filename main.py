from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from routes.data_routes import root

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Allows all origins. Adjust this for production.
    allow_credentials=True,
    allow_methods=["*"],  # Allows all HTTP methods.
    allow_headers=["*"],  # Allows all headers.
)

app.include_router(root)

# Optionally, you can add a root endpoint for health checks
@app.get("/test")
async def read_root():
    return {"message": "Welcome to the Task Manager API"}
