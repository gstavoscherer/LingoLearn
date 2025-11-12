from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.core.security import get_current_user_id
from app.database.connection import get_db
from app.services.dashboard import dashboard
from app.schemas.dashboard import DashboardResponse

router = APIRouter(prefix="/dashboard", tags=["Dashboard"])

@router.get("", status_code=200, response_model=DashboardResponse)
async def get_dashboard_data(db: Session = Depends(get_db), user_id = Depends(get_current_user_id)):
   return await dashboard(db=db, user_id=user_id)