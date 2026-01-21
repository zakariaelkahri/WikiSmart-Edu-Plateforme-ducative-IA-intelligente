from fastapi import APIRouter

from app.schemas.stats import GlobalStatsResponse

router = APIRouter(prefix="/admin", tags=["admin"])


@router.get("/stats", response_model=GlobalStatsResponse, summary="Get global platform statistics")
async def get_global_stats():
    # TODO: implement stats_service to compute global metrics
    raise NotImplementedError
