import fastapi
from typing import Optional, List
from api.models.news import News
from api.services import news_service


router = fastapi.APIRouter()


@router.get('/news')
async def get_news(search: Optional[str] = None, responsee_model=List[News]):
    data = await news_service.get_news(search)
    return data
