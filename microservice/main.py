from fastapi import FastAPI
from consumer import consume
from router import router


class App(FastAPI):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)


app = App()
app.include_router(router)


@app.on_event('startup')
async def startup():
    await consume()
