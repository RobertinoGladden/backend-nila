"""Database initialization script - Run this once to set up the database"""
from sqlalchemy import text
from app.database import engine, SessionLocal
from app.models import Base

def init_db():
    """Initialize database with all tables"""
    print("🔄 Creating all database tables...")
    
    try:
        # Create all tables from ORM models
        Base.metadata.create_all(bind=engine)
        print("✅ Database tables created successfully!")
        
        # Verify tables exist
        db = SessionLocal()
        try:
            result = db.execute(text("""
                SELECT table_name 
                FROM information_schema.tables 
                WHERE table_schema = 'public'
                ORDER BY table_name
            """))
            
            tables = [row[0] for row in result]
            print(f"\n📋 Created tables ({len(tables)} total):")
            for table in tables:
                print(f"   - {table}")
            
        finally:
            db.close()
            
    except Exception as e:
        print(f"❌ Error creating tables: {e}")
        raise

if __name__ == "__main__":
    init_db()
    print("\n✨ Database initialization complete!")
