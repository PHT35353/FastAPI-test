import logging
import uvicorn
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import Dict

# Create a FastAPI app
app = FastAPI()

# Set up logging
logging.basicConfig(level=logging.INFO)

# Add CORS Middleware to allow requests from different origins
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Update this to specific allowed origins for more security
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Define the data model for receiving distance
class DistanceModel(BaseModel):
    line_id: str
    distance: float

# A dictionary to hold the distance values for each line
distances: Dict[str, float] = {}

# Define a root endpoint to test server status
@app.get("/")
async def root():
    return {"message": "FastAPI server is running."}

# Define a route to receive the distance value
@app.post("/send-distance/")
async def send_distance(data: DistanceModel):
    global distances
    distances[data.line_id] = data.distance
    logging.info(f"Received distance for line {data.line_id}: {data.distance}")
    return {"status": "success"}

# Define a route to get all distance values
@app.get("/get-distances/")
async def get_distances():
    if distances:
        logging.info(f"Returning distances: {distances}")
        return {"distances": distances}
    else:
        logging.warning("No distances set yet.")
        return {"distances": {}}

# Define a route to delete a distance value
@app.delete("/delete-distance/{line_id}")
async def delete_distance(line_id: str):
    global distances
    if line_id in distances:
        del distances[line_id]
        logging.info(f"Deleted distance for line: {line_id}")
        return {"status": "deleted"}
    else:
        logging.warning(f"Line ID {line_id} not found.")
        return {"status": "not found"}

# Run the FastAPI app on port 8000
if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0", port=8000)
