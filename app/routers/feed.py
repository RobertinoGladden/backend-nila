"""Feed management router"""
from fastapi import APIRouter, Depends, HTTPException, Header
from sqlalchemy.orm import Session
from typing import Optional, List
from app.database import get_db
from app.services.auth_service import get_current_user
from app.services.feed_service import (
    get_user_feed_stocks, get_farming_cycle_feed_stock, record_feed_transaction,
    get_feed_history, get_feed_statistics,
    create_feeding_schedule, get_farming_cycle_schedules, record_feeding,
    get_feeding_history, get_feeding_statistics
)
from app.schemas import (
    FeedStockResponse, FeedTransactionCreate, FeedTransactionResponse,
    FeedingScheduleCreate, FeedingScheduleResponse,
    FeedingHistoryCreate, FeedingHistoryResponse
)

router = APIRouter(prefix="/feed", tags=["Feed Management"])


def get_user_from_token(authorization: Optional[str] = Header(None), db: Session = Depends(get_db)):
    """Dependency to get user from token"""
    if not authorization:
        raise HTTPException(status_code=401, detail="Missing authorization token")
    
    token = authorization.replace("Bearer ", "")
    user = get_current_user(db, token)
    
    if not user:
        raise HTTPException(status_code=401, detail="Invalid or expired token")
    
    return user


# ── FEED STOCK MANAGEMENT ──────────────────────────────────────

@router.get("/stocks", response_model=List[FeedStockResponse])
def list_feed_stocks(
    user = Depends(get_user_from_token),
    db: Session = Depends(get_db)
):
    """
    Get all feed stocks for the current user
    """
    stocks = get_user_feed_stocks(db, user.id)
    return stocks


@router.get("/stocks/{farming_cycle_id}", response_model=Optional[FeedStockResponse])
def get_stock_for_cycle(
    farming_cycle_id: int,
    user = Depends(get_user_from_token),
    db: Session = Depends(get_db)
):
    """
    Get feed stock for a specific farming cycle
    """
    stock = get_farming_cycle_feed_stock(db, farming_cycle_id)
    if not stock:
        raise HTTPException(status_code=404, detail="Feed stock not found")
    
    if stock.user_id != user.id:
        raise HTTPException(status_code=403, detail="Access denied")
    
    return stock


# ── FEED TRANSACTIONS ──────────────────────────────────────────

@router.post("/stocks/{stock_id}/transaction", response_model=FeedTransactionResponse)
def record_transaction(
    stock_id: int,
    transaction: FeedTransactionCreate,
    user = Depends(get_user_from_token),
    db: Session = Depends(get_db)
):
    """
    Record a feed transaction (input or usage)
    """
    from app.services.feed_service import get_feed_stock
    stock = get_feed_stock(db, stock_id)
    
    if not stock:
        raise HTTPException(status_code=404, detail="Feed stock not found")
    
    if stock.user_id != user.id:
        raise HTTPException(status_code=403, detail="Access denied")
    
    try:
        tx = record_feed_transaction(db, stock_id, transaction)
        return tx
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Transaction failed: {str(e)}")


@router.get("/stocks/{stock_id}/history", response_model=List[FeedTransactionResponse])
def get_stock_history(
    stock_id: int,
    limit: int = 100,
    user = Depends(get_user_from_token),
    db: Session = Depends(get_db)
):
    """
    Get feed transaction history for a stock
    """
    from app.services.feed_service import get_feed_stock
    stock = get_feed_stock(db, stock_id)
    
    if not stock:
        raise HTTPException(status_code=404, detail="Feed stock not found")
    
    if stock.user_id != user.id:
        raise HTTPException(status_code=403, detail="Access denied")
    
    history = get_feed_history(db, stock_id, limit)
    return history


@router.get("/stocks/{stock_id}/stats", response_model=dict)
def get_stock_stats(
    stock_id: int,
    user = Depends(get_user_from_token),
    db: Session = Depends(get_db)
):
    """
    Get statistics for a feed stock
    """
    from app.services.feed_service import get_feed_stock
    stock = get_feed_stock(db, stock_id)
    
    if not stock:
        raise HTTPException(status_code=404, detail="Feed stock not found")
    
    if stock.user_id != user.id:
        raise HTTPException(status_code=403, detail="Access denied")
    
    stats = get_feed_statistics(db, stock_id)
    return stats


# ── FEEDING SCHEDULE MANAGEMENT ────────────────────────────────

@router.post("/schedule/{farming_cycle_id}", response_model=FeedingScheduleResponse)
def create_schedule(
    farming_cycle_id: int,
    schedule_data: FeedingScheduleCreate,
    user = Depends(get_user_from_token),
    db: Session = Depends(get_db)
):
    """
    Create a feeding schedule for a farming cycle
    """
    from app.services.farming_service import get_farming_cycle
    cycle = get_farming_cycle(db, farming_cycle_id)
    
    if not cycle:
        raise HTTPException(status_code=404, detail="Farming cycle not found")
    
    if cycle.user_id != user.id:
        raise HTTPException(status_code=403, detail="Access denied")
    
    try:
        schedule = create_feeding_schedule(db, farming_cycle_id, schedule_data)
        return schedule
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to create schedule: {str(e)}")


@router.get("/schedule/{farming_cycle_id}", response_model=List[FeedingScheduleResponse])
def list_schedules(
    farming_cycle_id: int,
    user = Depends(get_user_from_token),
    db: Session = Depends(get_db)
):
    """
    Get all feeding schedules for a farming cycle
    """
    from app.services.farming_service import get_farming_cycle
    cycle = get_farming_cycle(db, farming_cycle_id)
    
    if not cycle:
        raise HTTPException(status_code=404, detail="Farming cycle not found")
    
    if cycle.user_id != user.id:
        raise HTTPException(status_code=403, detail="Access denied")
    
    schedules = get_farming_cycle_schedules(db, farming_cycle_id)
    return schedules


# ── FEEDING HISTORY ────────────────────────────────────────────

@router.post("/history/{farming_cycle_id}", response_model=FeedingHistoryResponse)
def record_feeding_event(
    farming_cycle_id: int,
    feeding_data: FeedingHistoryCreate,
    user = Depends(get_user_from_token),
    db: Session = Depends(get_db)
):
    """
    Record a feeding event
    """
    from app.services.farming_service import get_farming_cycle
    cycle = get_farming_cycle(db, farming_cycle_id)
    
    if not cycle:
        raise HTTPException(status_code=404, detail="Farming cycle not found")
    
    if cycle.user_id != user.id:
        raise HTTPException(status_code=403, detail="Access denied")
    
    try:
        feeding = record_feeding(db, farming_cycle_id, feeding_data)
        return feeding
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to record feeding: {str(e)}")


@router.get("/history/{farming_cycle_id}", response_model=List[FeedingHistoryResponse])
def list_feeding_history(
    farming_cycle_id: int,
    limit: int = 100,
    user = Depends(get_user_from_token),
    db: Session = Depends(get_db)
):
    """
    Get feeding history for a farming cycle
    """
    from app.services.farming_service import get_farming_cycle
    cycle = get_farming_cycle(db, farming_cycle_id)
    
    if not cycle:
        raise HTTPException(status_code=404, detail="Farming cycle not found")
    
    if cycle.user_id != user.id:
        raise HTTPException(status_code=403, detail="Access denied")
    
    history = get_feeding_history(db, farming_cycle_id, limit)
    return history


@router.get("/history/{farming_cycle_id}/stats", response_model=dict)
def get_history_stats(
    farming_cycle_id: int,
    user = Depends(get_user_from_token),
    db: Session = Depends(get_db)
):
    """
    Get feeding statistics for a farming cycle
    """
    from app.services.farming_service import get_farming_cycle
    cycle = get_farming_cycle(db, farming_cycle_id)
    
    if not cycle:
        raise HTTPException(status_code=404, detail="Farming cycle not found")
    
    if cycle.user_id != user.id:
        raise HTTPException(status_code=403, detail="Access denied")
    
    stats = get_feeding_statistics(db, farming_cycle_id)
    return stats
