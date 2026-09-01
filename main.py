from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from routes import predict, health, nsri, auth

app = FastAPI(
    title="NSRI Model API",
    description="API for accessing trained NSRI models",
    version="1.0.0"
)

# CORS configuration
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(health.router, prefix="/api/v1")
app.include_router(auth.router, prefix="/api/v1/auth", tags=["auth"])
app.include_router(predict.router, prefix="/api/v1/predict")
app.include_router(nsri.router, prefix="/api/v1/nsri")

@app.get("/")
def read_root():
    return {"message": "NSRI Backend API is running"}
