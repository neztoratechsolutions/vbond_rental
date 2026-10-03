from fastapi import FastAPI


app = FastAPI(
    title="Rental Platform - Property Service",
    version="1.0.0"
)


@app.get("/")
def root():
    return {
        "success": True,
        "message": "Property Service is running"
    }