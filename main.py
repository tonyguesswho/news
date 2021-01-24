import fastapi
import uvicorn
from api import news_api, home




api = fastapi.FastAPI()


def confiqure():
    api.include_router(news_api.router)
    api.include_router(home.router)


confiqure()


if __name__ == "__main__":
    uvicorn.run(api)
