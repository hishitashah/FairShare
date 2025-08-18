#!/usr/bin/env python3
"""
Simple script to test database connection
"""

from database import engine, Base
from sqlalchemy import text

def test_connection():
    try:
        # Test basic connection
        with engine.connect() as connection:
            result = connection.execute(text("SELECT version();"))
            version = result.fetchone()
            print(f"✅ Database connected successfully!")
            print(f"PostgreSQL version: {version[0]}")
            
        # Test if we can query our tables
        with engine.connect() as connection:
            result = connection.execute(text("SELECT table_name FROM information_schema.tables WHERE table_schema = 'public';"))
            tables = result.fetchall()
            print(f"\n📋 Tables in database:")
            for table in tables:
                print(f"  - {table[0]}")
                
        return True
        
    except Exception as e:
        print(f"❌ Database connection failed: {e}")
        return False

if __name__ == "__main__":
    test_connection() 