from fastapi import FastAPI
from pydantic import BaseModel

# Create a FastAPI app
app = FastAPI()

# Define the data model for receiving distance
class DistanceModel(BaseModel):
    distance: float

# Define a route to receive the distance value
@app.post("/send-distance/")
async def send_distance(data: DistanceModel):
    # Note: Streamlit session state is no longer accessible here.
    # You'll need to store the distance in a backend database or in-memory dictionary if necessary.
    print(f"Received distance: {data.distance}")
    return {"status": "success"}
