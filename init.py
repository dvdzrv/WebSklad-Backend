import uvicorn
import schedule
from auth import delete_expired_tokens


if __name__ == "__main__":
    from main import app
    from uvicorn import run
    import multiprocessing

    multiprocessing.freeze_support()
    uvicorn.run(app, host="0.0.0.0", port=8000, reload=False, workers=1)

    schedule.every(3).minutes.do(delete_expired_tokens)