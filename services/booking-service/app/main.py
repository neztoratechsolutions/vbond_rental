from fastapi import FastAPI


app = FastAPI(
    title="Rental Platform - Booking Service",
    version="1.0.0"
)


@app.get("/")
def root():
    return {
        "success": True,
        "message": "Booking Service is running"
    }