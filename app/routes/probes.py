from fastapi import APIRouter
from schemas.status import StatusResponse

router = APIRouter()


@router.get("/liveness", response_model=StatusResponse)
async def health_check() -> StatusResponse:
    return StatusResponse(status="ok")


@router.get("/startup", response_model=StatusResponse)
async def health_startup() -> StatusResponse:
    return StatusResponse(status="healthy")


@router.get("/ready", response_model=StatusResponse)
async def health_ready() -> StatusResponse:
    return StatusResponse(status="ready")
