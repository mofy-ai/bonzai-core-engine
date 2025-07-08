"""
Production Database Setup for Bonzai Desktop
Supports both PostgreSQL (Railway) and SQLite (fallback)
"""

import os
import sqlite3
import logging
from datetime import datetime
from sqlalchemy import create_engine, text, MetaData, Table, Column, Integer, String, DateTime, JSON, Float
from sqlalchemy.exc import SQLAlchemyError

logger = logging.getLogger(__name__)

def setup_production_database():
    """
    Setup database for Railway deployment
    Supports PostgreSQL (Railway) with SQLite fallback
    """
    database_url = os.getenv('DATABASE_URL')
    
    if database_url and database_url.startswith('postgresql'):
        logger.info("🔧 Setting up PostgreSQL database for production...")
        return setup_postgresql_database(database_url)
    else:
        logger.info("🔧 Setting up SQLite database for development/fallback...")
        return setup_sqlite_database()

def setup_postgresql_database(database_url):
    """Setup PostgreSQL database on Railway"""
    try:
        # Create engine with connection pooling
        engine = create_engine(
            database_url,
            pool_size=5,
            max_overflow=10,
            pool_pre_ping=True,
            pool_recycle=300
        )
        
        with engine.connect() as conn:
            # Create conversations table
            conn.execute(text("""
                CREATE TABLE IF NOT EXISTS conversations (
                    id SERIAL PRIMARY KEY,
                    user_id VARCHAR(255) NOT NULL,
                    ai_provider VARCHAR(100) NOT NULL,
                    messages JSONB NOT NULL DEFAULT '[]',
                    emotional_context JSONB DEFAULT '{}',
                    metadata JSONB DEFAULT '{}',
                    created_at TIMESTAMP DEFAULT NOW(),
                    updated_at TIMESTAMP DEFAULT NOW()
                );
            """))
            
            # Create emotional history table
            conn.execute(text("""
                CREATE TABLE IF NOT EXISTS emotional_history (
                    id SERIAL PRIMARY KEY,
                    user_id VARCHAR(255) NOT NULL,
                    mood FLOAT DEFAULT 0.5,
                    stress FLOAT DEFAULT 0.5,
                    focus FLOAT DEFAULT 0.5,
                    energy FLOAT DEFAULT 0.5,
                    confidence FLOAT DEFAULT 0.5,
                    creativity FLOAT DEFAULT 0.5,
                    context JSONB DEFAULT '{}',
                    session_id VARCHAR(255),
                    timestamp TIMESTAMP DEFAULT NOW()
                );
            """))
            
            # Create user preferences table
            conn.execute(text("""
                CREATE TABLE IF NOT EXISTS user_preferences (
                    id SERIAL PRIMARY KEY,
                    user_id VARCHAR(255) UNIQUE NOT NULL,
                    preferences JSONB DEFAULT '{}',
                    learning_data JSONB DEFAULT '{}',
                    ai_provider_preferences JSONB DEFAULT '{}',
                    zai_personality JSONB DEFAULT '{}',
                    created_at TIMESTAMP DEFAULT NOW(),
                    updated_at TIMESTAMP DEFAULT NOW()
                );
            """))
            
            # Create system metrics table
            conn.execute(text("""
                CREATE TABLE IF NOT EXISTS system_metrics (
                    id SERIAL PRIMARY KEY,
                    metric_name VARCHAR(255) NOT NULL,
                    metric_value FLOAT NOT NULL,
                    metadata JSONB DEFAULT '{}',
                    timestamp TIMESTAMP DEFAULT NOW()
                );
            """))
            
            # Create api usage tracking
            conn.execute(text("""
                CREATE TABLE IF NOT EXISTS api_usage (
                    id SERIAL PRIMARY KEY,
                    user_id VARCHAR(255),
                    endpoint VARCHAR(255) NOT NULL,
                    ai_provider VARCHAR(100),
                    tokens_used INTEGER DEFAULT 0,
                    response_time_ms INTEGER,
                    status_code INTEGER,
                    timestamp TIMESTAMP DEFAULT NOW()
                );
            """))
            
            # Create indexes for better performance
            conn.execute(text("CREATE INDEX IF NOT EXISTS idx_conversations_user_id ON conversations(user_id);"))
            conn.execute(text("CREATE INDEX IF NOT EXISTS idx_emotional_history_user_id ON emotional_history(user_id);"))
            conn.execute(text("CREATE INDEX IF NOT EXISTS idx_emotional_history_timestamp ON emotional_history(timestamp);"))
            conn.execute(text("CREATE INDEX IF NOT EXISTS idx_api_usage_timestamp ON api_usage(timestamp);"))
            
            conn.commit()
            
        logger.info("✅ PostgreSQL database setup completed successfully!")
        return engine
        
    except SQLAlchemyError as e:
        logger.error(f"❌ PostgreSQL setup failed: {e}")
        logger.info("🔄 Falling back to SQLite...")
        return setup_sqlite_database()

def setup_sqlite_database():
    """Setup SQLite database for development/fallback"""
    try:
        db_path = os.getenv('SQLITE_DB_PATH', '/app/bonzai_production.db')
        
        # Ensure directory exists
        os.makedirs(os.path.dirname(db_path), exist_ok=True)
        
        conn = sqlite3.connect(db_path)
        cursor = conn.cursor()
        
        # Create conversations table
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS conversations (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                user_id TEXT NOT NULL,
                ai_provider TEXT NOT NULL,
                messages TEXT NOT NULL DEFAULT '[]',
                emotional_context TEXT DEFAULT '{}',
                metadata TEXT DEFAULT '{}',
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            );
        """)
        
        # Create emotional history table
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS emotional_history (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                user_id TEXT NOT NULL,
                mood REAL DEFAULT 0.5,
                stress REAL DEFAULT 0.5,
                focus REAL DEFAULT 0.5,
                energy REAL DEFAULT 0.5,
                confidence REAL DEFAULT 0.5,
                creativity REAL DEFAULT 0.5,
                context TEXT DEFAULT '{}',
                session_id TEXT,
                timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            );
        """)
        
        # Create user preferences table
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS user_preferences (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                user_id TEXT UNIQUE NOT NULL,
                preferences TEXT DEFAULT '{}',
                learning_data TEXT DEFAULT '{}',
                ai_provider_preferences TEXT DEFAULT '{}',
                zai_personality TEXT DEFAULT '{}',
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            );
        """)
        
        # Create system metrics table
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS system_metrics (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                metric_name TEXT NOT NULL,
                metric_value REAL NOT NULL,
                metadata TEXT DEFAULT '{}',
                timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            );
        """)
        
        # Create api usage tracking
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS api_usage (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                user_id TEXT,
                endpoint TEXT NOT NULL,
                ai_provider TEXT,
                tokens_used INTEGER DEFAULT 0,
                response_time_ms INTEGER,
                status_code INTEGER,
                timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            );
        """)
        
        # Create indexes
        cursor.execute("CREATE INDEX IF NOT EXISTS idx_conversations_user_id ON conversations(user_id);")
        cursor.execute("CREATE INDEX IF NOT EXISTS idx_emotional_history_user_id ON emotional_history(user_id);")
        cursor.execute("CREATE INDEX IF NOT EXISTS idx_emotional_history_timestamp ON emotional_history(timestamp);")
        cursor.execute("CREATE INDEX IF NOT EXISTS idx_api_usage_timestamp ON api_usage(timestamp);")
        
        conn.commit()
        conn.close()
        
        logger.info("✅ SQLite database setup completed successfully!")
        return f"sqlite:///{db_path}"
        
    except Exception as e:
        logger.error(f"❌ SQLite setup failed: {e}")
        raise

def get_database_connection():
    """Get database connection for the app"""
    database_url = os.getenv('DATABASE_URL')
    
    if database_url and database_url.startswith('postgresql'):
        engine = create_engine(database_url, pool_pre_ping=True)
        return engine
    else:
        db_path = os.getenv('SQLITE_DB_PATH', '/app/bonzai_production.db')
        return create_engine(f"sqlite:///{db_path}")

def health_check_database():
    """Health check for database connectivity"""
    try:
        engine = get_database_connection()
        with engine.connect() as conn:
            conn.execute(text("SELECT 1"))
        return {"status": "healthy", "database": "connected"}
    except Exception as e:
        return {"status": "unhealthy", "database": f"error: {str(e)}"}

if __name__ == "__main__":
    # Initialize database on startup
    setup_production_database()
    
    # Test connection
    health = health_check_database()
    if health["status"] == "healthy":
        logger.info("🎉 Database is ready for production!")
    else:
        logger.error(f"❌ Database health check failed: {health}")
