from fastapi import FastAPI
import uvicorn
app = FastAPI()
@app.get("/")
def read_root():
    return {"message": "Azure APPlication is working correctly Tests are successful!!"}
