import logging
import uvicorn
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
    allow_origins=["*"],  # Allow requests from all origins for simplicity
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Define the data model for receiving distances
class DistancesModel(BaseModel):
    distances: list[float]  # List of distances in meters

# Global variables to hold the distance values
distanceValues = []

# Define a root endpoint to test server status
@app.get("/")
async def root():
    return {"message": "FastAPI server is running."}


# Clear distanceValues on initialization or when no distances are sent
@app.post("/send-distances/")
async def send_distances(data: DistancesModel):
    global distanceValues
    if len(data.distances) == 0:
        # Clear saved distances if no distances are sent
        distanceValues = []
        logging.warning("Received empty distances. Ignoring and clearing previous distances.")
        return {"status": "error", "message": "No distances selected"}
    
    # Update with new distances
    distanceValues = data.distances
    logging.info(f"Received distances: {distanceValues}")
    
    return {"status": "success", "distances": distanceValues}

# Route to get distances, will return empty if no distances are available
@app.get("/get-distances/")
async def get_distances():
    if distanceValues:
        logging.info(f"Returning distances: {distanceValues}")
        return {"individual_distances": distanceValues, "total_distance": sum(distanceValues)}
    else:
        logging.warning("No distances have been set yet.")
        return {"individual_distances": [], "total_distance": 0}



# Run the FastAPI app on port 8000
if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0", port=8000)
