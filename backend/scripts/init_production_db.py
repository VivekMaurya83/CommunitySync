#!/usr/bin/env python3
"""
Production Database Initialization Script
Run this once after deploying to Render to set up database schema and admin user
Usage: python init_production_db.py
"""

import os
import sys
import getpass
from dotenv import load_dotenv
from sqlalchemy import create_engine, text
from sqlalchemy.orm import sessionmaker

# Load environment
load_dotenv()

# Add backend to path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'backend'))

from backend.models import Base, User, Volunteer
from backend.database import engine, get_db
from backend.config import settings

print("=" * 60)
print("🚀 CommunitySync Production Database Initialization")
print("=" * 60)

# Step 1: Verify database connection
print("\n1️⃣ Verifying database connection...")
try:
    with engine.connect() as conn:
        result = conn.execute(text("SELECT 1"))
        print("   ✅ Database connection successful")
except Exception as e:
    print(f"   ❌ Failed to connect to database: {e}")
    print("\n   Make sure DATABASE_URL is set correctly in Render environment:")
    print("   Format: postgresql://user:pwd@host/db?sslmode=require")
    sys.exit(1)

# Step 2: Create all tables
print("\n2️⃣ Creating database schema...")
try:
    Base.metadata.create_all(bind=engine)
    print("   ✅ Database schema created successfully")
except Exception as e:
    print(f"   ❌ Failed to create schema: {e}")
    sys.exit(1)

# Step 3: Create admin user
print("\n3️⃣ Creating admin user...")
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
session = SessionLocal()

try:
    # Check if admin already exists
    admin = session.query(User).filter(User.email == "admin@communitysync.com").first()
    
    if admin:
        print("   ℹ️  Admin user already exists")
    else:
        # Get credentials from user
        admin_email = input("\n   Enter admin email (default: admin@communitysync.com): ").strip()
        if not admin_email:
            admin_email = "admin@communitysync.com"
        
        admin_password = getpass.getpass("   Enter admin password (min 8 chars): ")
        if len(admin_password) < 8:
            print("   ❌ Password must be at least 8 characters")
            sys.exit(1)
        
        # Import hash function
        from backend.services.auth_service import hash_password
        
        # Create admin user
        admin = User(
            email=admin_email,
            full_name="Administrator",
            mobile_number="",
            location="",
            hashed_password=hash_password(admin_password),
            role="admin",
            account_status="approved"
        )
        
        session.add(admin)
        session.commit()
        print(f"   ✅ Admin user created: {admin_email}")
        
except Exception as e:
    session.rollback()
    print(f"   ❌ Failed to create admin user: {e}")
    sys.exit(1)
finally:
    session.close()

print("\n" + "=" * 60)
print("✅ Production database initialization complete!")
print("=" * 60)
print("\n📋 Next steps:")
print("   1. Verify admin login at frontend URL")
print("   2. Upload test crisis report")
print("   3. Check Render logs for any errors")
print("   4. Monitor API performance")
print("\n💬 Support:")
print("   - Render logs: Dashboard → Service → Logs")
print("   - Database: Neon dashboard → Database → Query Editor")
print("\n")
