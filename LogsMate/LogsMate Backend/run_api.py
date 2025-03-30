import uvicorn

if __name__ == "__main__":
    print("Starting LogsMate API server...")
    print("API will be available at http://localhost:8000")
    print("Documentation will be available at http://localhost:8000/docs")
    uvicorn.run("src.api:app", host="0.0.0.0", port=8000, reload=True) 