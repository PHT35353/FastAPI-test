import logging
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel

# Create a FastAPI app
app = FastAPI()

# Set up logging
logging.basicConfig(level=logging.INFO)

# Add CORS Middleware to allow requests from different origins
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Update this to specific allowed origins if you want more security
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Define the data model for receiving distance
class DistanceModel(BaseModel):
    distance: float

# A global variable to hold the distance value
distanceValue = None

# Define a route to receive the distance value
@app.post("/send-distance/")
async def send_distance(data: DistanceModel):
    global distanceValue
    distanceValue = data.distance
    logging.info(f"Received distance: {data.distance}")
    return {"status": "success"}

# Define a route to get the distance value
@app.get("/get-distance/")
async def get_distance():
    if distanceValue is not None:
        logging.info(f"Returning distance: {distanceValue}")
        return {"distance": distanceValue}
    else:
        logging.warning("Distance value is not set yet.")
        return {"distance": None}
