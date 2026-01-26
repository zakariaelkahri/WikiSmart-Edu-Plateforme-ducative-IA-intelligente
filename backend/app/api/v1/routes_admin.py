from fastapi import APIRouter, Depends

from app.schemas.stats import GlobalStatsResponse
from app.api.v1.routes_auth import get_current_admin

router = APIRouter(prefix="/admin", tags=["admin"])


@router.get("/stats", response_model=GlobalStatsResponse, summary="Get global platform statistics")
async def get_global_stats(current_admin = Depends(get_current_admin)):
    # TODO: implement stats_service to compute global metrics
    raise NotImplementedError
