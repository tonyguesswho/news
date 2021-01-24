import fastapi
from typing import Optional, List
from api.models.news import News
from api.services import news_service


router = fastapi.APIRouter()


@router.get('/news', response_model=List[News])
async def get_news(search: Optional[str] = None):
    data = await news_service.get_news(search)
    return data
