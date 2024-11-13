import logging
import uvicorn
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import json
from pydantic import BaseModel
from typing import List, Dict

# Define the PipeModel class to represent an individual pipe
class PipeModel(BaseModel):
    name: str
    distance: float
    coordinates: List[List[float]]
    
# Define the PipesModel class to represent a list of pipes
class PipesModel(BaseModel):
    pipes: List[PipeModel]  # List of pipes with names and distances

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

# Global variables to hold the distance values and saved maps
distanceValues = []
saved_maps = {}

# Define the data model for receiving distances
class DistancesModel(BaseModel):
    distances: list[float]  # List of distances in meters

# Define a data model to hold map data
class MapDataModel(BaseModel):
    user_id: str  # You can use this to store map data for specific users
    map_data: dict  # JSON structure for the map's drawn features

# Define a root endpoint to test server status
@app.get("/")
async def root():
    return {"message": "FastAPI server is running."}

# Clear distanceValues on initialization or when no distances are sent
@app.post("/send-pipes/")
async def send_pipes(data: PipesModel):
    global distanceValues
    if len(data.pipes) == 0:
        distanceValues = []
        logging.warning("Received empty pipes list. Ignoring and clearing previous distances.")
        return {"status": "error", "message": "No pipes selected"}

    distanceValues = [{"name": pipe.name, "distance": pipe.distance, "coordinates": pipe.coordinates} for pipe in data.pipes]
    logging.info(f"Received pipes: {distanceValues}")

    return {"status": "success", "pipes": distanceValues}



# Route to get distances, will return empty if no distances are available
@app.get("/get-distances/")
async def get_distances():
    if distanceValues:
        logging.info(f"Returning pipes: {distanceValues}")
        total_distance = sum(pipe["distance"] for pipe in distanceValues)
        return {"individual_pipes": distanceValues, "total_distance": total_distance}
    else:
        logging.warning("No pipes have been set yet.")
        return {"individual_pipes": [], "total_distance": 0}

@app.post("/save-map/")
async def save_map(data: MapDataModel):
    # Save the map data in an in-memory dictionary keyed by user_id
    saved_maps[data.user_id] = data.map_data
    logging.info(f"Map data saved for user_id: {data.user_id}")
    return {"status": "success", "message": "Map data saved successfully"}

@app.get("/load-map/{user_id}")
async def load_map(user_id: str):
    # Retrieve the map data for the given user_id
    if user_id in saved_maps:
        logging.info(f"Map data retrieved for user_id: {user_id}")
        return {"status": "success", "map_data": saved_maps[user_id]}
    else:
        logging.warning(f"No saved map found for user_id: {user_id}")
        return {"status": "error", "message": "No saved map found for this user"}

# Run the FastAPI app on port 8000
if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0", port=8000)
