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
        
        # Apply user management schema
        db = SessionLocal()
        try:
            # Add new columns to users table
            print("\n🔄 Applying User Management Schema...")
            
            # Check if columns exist before adding
            db.execute(text("""
                ALTER TABLE users ADD COLUMN IF NOT EXISTS role VARCHAR(20) DEFAULT 'farmer';
                ALTER TABLE users ADD COLUMN IF NOT EXISTS status VARCHAR(20) DEFAULT 'active';
                ALTER TABLE users ADD COLUMN IF NOT EXISTS last_login TIMESTAMP NULL;
                ALTER TABLE users ADD COLUMN IF NOT EXISTS is_email_verified BOOLEAN DEFAULT FALSE;
            """))
            
            # Create indexes
            db.execute(text("CREATE INDEX IF NOT EXISTS idx_user_role ON users(role);"))
            db.execute(text("CREATE INDEX IF NOT EXISTS idx_user_status ON users(status);"))
            db.execute(text("CREATE INDEX IF NOT EXISTS idx_user_email_verified ON users(is_email_verified);"))
            
            db.commit()
            print("✅ User Management Schema applied!")
            
            # Verify tables exist
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
