"""Feed stock and feeding management service"""
from datetime import datetime
from sqlalchemy.orm import Session
from sqlalchemy import func
from app.models import FeedStock, FeedTransaction, FeedingSchedule, FeedingHistory
from app.schemas import FeedTransactionCreate, FeedingScheduleCreate, FeedingHistoryCreate


def get_feed_stock(db: Session, stock_id: int) -> FeedStock:
    """Get feed stock by ID"""
    return db.query(FeedStock).filter(FeedStock.id == stock_id).first()


def get_user_feed_stocks(db: Session, user_id: int) -> list:
    """Get all feed stocks for a user"""
    return db.query(FeedStock).filter(FeedStock.user_id == user_id).all()


def get_farming_cycle_feed_stock(db: Session, farming_cycle_id: int) -> FeedStock:
    """Get feed stock for a farming cycle"""
    return db.query(FeedStock).filter(
        FeedStock.farming_cycle_id == farming_cycle_id
    ).first()


def record_feed_transaction(db: Session, stock_id: int, transaction: FeedTransactionCreate) -> FeedTransaction:
    """Record a feed transaction (input or usage)"""
    feed_stock = get_feed_stock(db, stock_id)
    if not feed_stock:
        raise ValueError("Feed stock not found")
    
    previous_quantity = feed_stock.current_quantity
    
    # Update quantity based on transaction type
    if transaction.transaction_type == "input":
        new_quantity = previous_quantity + transaction.quantity
    elif transaction.transaction_type == "usage":
        if transaction.quantity > previous_quantity:
            raise ValueError(f"Insufficient feed stock. Available: {previous_quantity}, Requested: {transaction.quantity}")
        new_quantity = previous_quantity - transaction.quantity
    else:
        raise ValueError("Invalid transaction type")
    
    # Create transaction record
    feed_tx = FeedTransaction(
        feed_stock_id=stock_id,
        transaction_type=transaction.transaction_type,
        quantity=transaction.quantity,
        notes=transaction.notes,
        previous_quantity=previous_quantity,
        new_quantity=new_quantity
    )
    db.add(feed_tx)
    
    # Update feed stock
    feed_stock.current_quantity = new_quantity
    feed_stock.updated_at = datetime.now()
    
    db.commit()
    db.refresh(feed_tx)
    
    return feed_tx


def get_feed_history(db: Session, stock_id: int, limit: int = 100) -> list:
    """Get feed transaction history for a stock"""
    return db.query(FeedTransaction).filter(
        FeedTransaction.feed_stock_id == stock_id
    ).order_by(FeedTransaction.created_at.desc()).limit(limit).all()


def get_feed_statistics(db: Session, stock_id: int) -> dict:
    """Get feed statistics for a stock"""
    feed_stock = get_feed_stock(db, stock_id)
    if not feed_stock:
        return None
    
    # Total input
    total_input = db.query(func.sum(FeedTransaction.quantity)).filter(
        FeedTransaction.feed_stock_id == stock_id,
        FeedTransaction.transaction_type == "input"
    ).scalar() or 0
    
    # Total usage
    total_usage = db.query(func.sum(FeedTransaction.quantity)).filter(
        FeedTransaction.feed_stock_id == stock_id,
        FeedTransaction.transaction_type == "usage"
    ).scalar() or 0
    
    # Transaction count
    tx_count = db.query(FeedTransaction).filter(
        FeedTransaction.feed_stock_id == stock_id
    ).count()
    
    return {
        "stock_id": stock_id,
        "current_quantity": feed_stock.current_quantity,
        "unit": feed_stock.unit,
        "total_input": total_input,
        "total_usage": total_usage,
        "transaction_count": tx_count,
        "min_threshold": feed_stock.min_threshold,
        "below_threshold": feed_stock.current_quantity < feed_stock.min_threshold if feed_stock.min_threshold else False
    }


# ── FEEDING SCHEDULE MANAGEMENT ────────────────────────────────

def create_feeding_schedule(db: Session, farming_cycle_id: int, schedule_data: FeedingScheduleCreate) -> FeedingSchedule:
    """Create a feeding schedule"""
    schedule = FeedingSchedule(
        farming_cycle_id=farming_cycle_id,
        scheduled_time=schedule_data.scheduled_time,
        expected_quantity=schedule_data.expected_quantity,
        frequency=schedule_data.frequency,
        status="active"
    )
    db.add(schedule)
    db.commit()
    db.refresh(schedule)
    
    return schedule


def get_feeding_schedule(db: Session, schedule_id: int) -> FeedingSchedule:
    """Get feeding schedule by ID"""
    return db.query(FeedingSchedule).filter(FeedingSchedule.id == schedule_id).first()


def get_farming_cycle_schedules(db: Session, farming_cycle_id: int) -> list:
    """Get all feeding schedules for a farming cycle"""
    return db.query(FeedingSchedule).filter(
        FeedingSchedule.farming_cycle_id == farming_cycle_id
    ).all()


def record_feeding(db: Session, farming_cycle_id: int, feeding_data: FeedingHistoryCreate) -> FeedingHistory:
    """Record a feeding event"""
    feeding = FeedingHistory(
        feeding_schedule_id=feeding_data.feeding_schedule_id,
        farming_cycle_id=farming_cycle_id,
        actual_time=datetime.now(),
        quantity_given=feeding_data.quantity_given,
        administered_by=feeding_data.administered_by,
        notes=feeding_data.notes
    )
    db.add(feeding)
    db.commit()
    db.refresh(feeding)
    
    return feeding


def get_feeding_history(db: Session, farming_cycle_id: int, limit: int = 100) -> list:
    """Get feeding history for a farming cycle"""
    return db.query(FeedingHistory).filter(
        FeedingHistory.farming_cycle_id == farming_cycle_id
    ).order_by(FeedingHistory.created_at.desc()).limit(limit).all()


def get_feeding_statistics(db: Session, farming_cycle_id: int) -> dict:
    """Get feeding statistics for a farming cycle"""
    # Total feeding events
    total_events = db.query(FeedingHistory).filter(
        FeedingHistory.farming_cycle_id == farming_cycle_id
    ).count()
    
    # Total feed given
    total_quantity = db.query(func.sum(FeedingHistory.quantity_given)).filter(
        FeedingHistory.farming_cycle_id == farming_cycle_id
    ).scalar() or 0
    
    # Average per feeding
    avg_quantity = db.query(func.avg(FeedingHistory.quantity_given)).filter(
        FeedingHistory.farming_cycle_id == farming_cycle_id
    ).scalar() or 0
    
    # Active schedules
    active_schedules = db.query(FeedingSchedule).filter(
        FeedingSchedule.farming_cycle_id == farming_cycle_id,
        FeedingSchedule.status == "active"
    ).count()
    
    return {
        "farming_cycle_id": farming_cycle_id,
        "total_feeding_events": total_events,
        "total_feed_quantity": total_quantity,
        "average_per_feeding": round(avg_quantity, 2),
        "active_schedules": active_schedules
    }
