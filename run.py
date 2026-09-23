import uvicorn


if __name__ == "__main__":
    # Change 5000 to your desired port number
    uvicorn.run("app.main:app", host="127.0.0.1", port=8000, reload=True)