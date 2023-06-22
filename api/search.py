from fastapi import APIRouter
from fastapi.params import Depends

from api.es_connection import get_searcher, Searcher

router = APIRouter()


@router.get("/")
def search_by_email(
    email: str,
    searcher: Searcher = Depends(get_searcher)
):
    result = searcher.search_by_field("email", email)

    return result
