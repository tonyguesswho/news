
import fastapi


router = fastapi.APIRouter()


@router.get('/', include_in_schema=False)
def index():
    return {
        "message": "News API aggregator"
    }
