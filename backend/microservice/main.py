from fastapi import FastAPI
import uvicorn

from consumer import consume
from router import router

app = FastAPI()
app.include_router(router)


@app.on_event('startup')
async def startup():
    await consume()


if __name__ == '__main__':
    uvicorn.run(app, host='0.0.0.0', port=8000, reload=True)
