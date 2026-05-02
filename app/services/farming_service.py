"""Farming cycle management service"""
from datetime import datetime, date, timedelta
from sqlalchemy.orm import Session
from app.models import FarmingCycle, FeedStock, FeedingHistory, FeedingSchedule
from app.schemas import FarmingCycleCreate, FarmingCycleUpdate, FarmingCycleResponse


def create_farming_cycle(db: Session, user_id: int, cycle_data: FarmingCycleCreate) -> FarmingCycle:
    """Create a new farming cycle"""
    # Generate cycle name if not provided
    cycle_name = cycle_data.cycle_name or f"Cycle {datetime.now().strftime('%Y-%m-%d')}"
    
    farming_cycle = FarmingCycle(
        user_id=user_id,
        cycle_name=cycle_name,
        seeding_date=cycle_data.seeding_date,
        status="active"
    )
    db.add(farming_cycle)
    db.flush()
    
    # Create associated feed stock for this cycle
    feed_stock = FeedStock(
        user_id=user_id,
        farming_cycle_id=farming_cycle.id,
        current_quantity=0,
        unit="kg"
    )
    db.add(feed_stock)
    db.commit()
    db.refresh(farming_cycle)
    
    return farming_cycle


def get_farming_cycle(db: Session, cycle_id: int) -> FarmingCycle:
    """Get farming cycle by ID"""
    return db.query(FarmingCycle).filter(FarmingCycle.id == cycle_id).first()


def get_user_farming_cycles(db: Session, user_id: int) -> list:
    """Get all farming cycles for a user"""
    return db.query(FarmingCycle).filter(FarmingCycle.user_id == user_id).all()


def get_active_farming_cycle(db: Session, user_id: int) -> FarmingCycle:
    """Get the active farming cycle for a user"""
    return db.query(FarmingCycle).filter(
        FarmingCycle.user_id == user_id,
        FarmingCycle.status == "active"
    ).first()


def calculate_farming_days(seeding_date: date) -> int:
    """Calculate number of days since seeding"""
    return (date.today() - seeding_date).days


def update_farming_cycle(db: Session, cycle_id: int, update_data: FarmingCycleUpdate) -> FarmingCycle:
    """Update farming cycle"""
    cycle = get_farming_cycle(db, cycle_id)
    if not cycle:
        return None
    
    if update_data.cycle_name:
        cycle.cycle_name = update_data.cycle_name
    if update_data.status:
        cycle.status = update_data.status
    if update_data.actual_harvest_date:
        cycle.actual_harvest_date = update_data.actual_harvest_date
        if cycle.status != "completed":
            cycle.status = "completed"
    
    cycle.updated_at = datetime.now()
    db.commit()
    db.refresh(cycle)
    
    return cycle


def get_farming_cycle_stats(db: Session, cycle_id: int) -> dict:
    """Get statistics for a farming cycle"""
    cycle = get_farming_cycle(db, cycle_id)
    if not cycle:
        return None
    
    farming_days = calculate_farming_days(cycle.seeding_date)
    
    # Get total feed given
    total_feed = db.query(FeedingHistory).filter(
        FeedingHistory.farming_cycle_id == cycle_id
    ).count()
    
    # Get total feed quantity given
    from sqlalchemy import func
    total_feed_quantity = db.query(func.sum(FeedingHistory.quantity_given)).filter(
        FeedingHistory.farming_cycle_id == cycle_id
    ).scalar() or 0
    
    # Get feeding schedule count
    schedule_count = db.query(FeedingSchedule).filter(
        FeedingSchedule.farming_cycle_id == cycle_id
    ).count()
    
    return {
        "cycle_id": cycle_id,
        "farming_days": farming_days,
        "total_feeding_events": total_feed,
        "total_feed_quantity": total_feed_quantity,
        "feeding_schedules": schedule_count,
        "seeding_date": cycle.seeding_date,
        "status": cycle.status
    }
