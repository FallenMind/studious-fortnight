import uvicorn
from app import app
if __name__ == '__main__':
    uvicorn.run(app, port=8000, access_log=True, host="0.0.0.0")
