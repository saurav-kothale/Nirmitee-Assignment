from fastapi import FastAPI
from src.file_upload.router import file_router
from src.transform.route import convertor_router
import uvicorn

app = FastAPI()

@app.get("/")
def demo():
    return{
        "message" : "Working correctly"
    }

app.include_router(file_router, tags=["File Upload APIS"])
app.include_router(convertor_router, tags=["Convert to Excel"])

if __name__ == "__main__":
    uvicorn.run("main:app", port=8000, reload=True)