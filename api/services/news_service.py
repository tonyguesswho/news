import httpx
import sys
from typing import List, Dict, Optional
from datetime import timedelta
import json
from api.redis import client as redisClient
from api.utils.search import get_search


class Source(object):
    def __init__(self, url: str, name: Optional[str] = None):
        self.url = url
        self.res = None
        self.headers = dict()
        self.mapping = None
        self.name = name
        self.data = None
        self.auth = None
        self.method = "get"

    async def send(self):
        try:
            async with httpx.AsyncClient() as client:
                if self.method == 'post':
                    response = await client.post(self.url, headers=self.headers, data=self.data, auth=self.auth)
                else:
                    response = await client.get(self.url, headers=self.headers, auth=self.auth)
                response.raise_for_status()
                self.res = response
                return self.res.json()
        except httpx.RequestError as exc:
            print(f"An error occured while requesting {exc.request.url!r}.")
        except httpx.HTTPStatusError as exc:
            print(
                f"Error response {exc.response.status_code} while requesting {exc.request.url!r}.")

    def map_fields(self, res: List[Dict]):
        if self.mapping:
            d = [{
                "headline": news[self.mapping['headline']],
                "link": news[self.mapping['link']],
                "source": self.name
            } for news in res]
            return d
        else:
            return res


class NewsApi(Source):
    def __init__(self):
        super(NewsApi, self).__init__(
            url="https://newsapi.org/v2/top-headlines?country=us&apiKey=7b5668ee107c43148ae27505380de5da", name="News Api")

        self.mapping = {
            "headline": "title",
            "link": "url",
        }

    async def get(self):
        try:
            response = await super(NewsApi, self).send()
            return self.map_fields(response['articles'])
        except Exception:
            pass


class RedditApi(Source):
    def __init__(self):
        super(RedditApi, self).__init__(
            url="https://oauth.reddit.com/r/news", name="Reddit")

        self.mapping = {
            "headline": "title",
            "link": "url",
        }

    async def get(self):
        try:
            redisToken = redisClient.get('redisToken')
            if redisToken is None:
                token = await RedisToken().get()
                auth = {
                    "authToken": token,
                    "client": "reddit"
                }
                redisClient.setex("redisToken", timedelta(
                    seconds=3500), value=json.dumps(auth),)
            else:
                res = json.loads(redisToken)
                token = res["authToken"]
            headers = {'User-Agent': 'News/0.0.1'}
            headers = {
                **headers, **{'Authorization': f"bearer {token}"}}
            self.headers = headers
            response = await super(RedditApi, self).send()
            res = response['data']['children']
            raw_res = [news["data"] for news in res]
            return self.map_fields(raw_res)
        except Exception as e:
            print(e)


class RedisToken(Source):
    def __init__(self):
        super(RedisToken, self).__init__(
            url="https://www.reddit.com/api/v1/access_token")

    async def get(self):
        try:
            print("here")
            headers = {'User-Agent': 'News/0.0.1'}
            auth = ("wOxuBhRWgfTf-A", "gfOnTkiLM2xCqQ217cSC8G9ZEC09nA")

            data = {'grant_type': 'password',
                    'username': 'tonymadinga',
                    'password': 'Guesswho1.'}
            self.data = data
            self.headers = headers
            self.method = 'post'
            self.auth = auth
            response = await super(RedisToken, self).send()
            return response['access_token']
        except Exception:
            pass


async def get_news(search: Optional[str] = None, sources=[RedditApi, NewsApi]):
    news = redisClient.get('news')
    if news:
        data = []
        for source in sources:
            result = await source().get()
            if result and isinstance(result, list):
                data = [*data, *result]
        redisClient.setex("news", timedelta(
            seconds=3600), value=json.dumps(data),)
        if search is not None:
            return get_search(data, search)
        return data
    else:
        res = json.loads(news)
        if search is not None:
            return get_search(data, search)
        return res
