import uvicorn
from admin_db import init_db

if __name__ == "__main__":
    init_db()
    from main import app
    from uvicorn import run
    import multiprocessing

    multiprocessing.freeze_support()
    uvicorn.run(app, host="0.0.0.0", port=8000, reload=False, workers=1)