from fastapi import FastAPI
from routes import predict, health

app = FastAPI(
    title="NSRI Model API",
    description="API for accessing trained NSRI models",
    version="1.0.0"
)

app.include_router(health.router, prefix="/api/v1")
app.include_router(predict.router, prefix="/api/v1/predict")

@app.get("/")
def read_root():
    return {"message": "NSRI Backend API is running"}
