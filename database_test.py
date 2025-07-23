# database_test.py
import psycopg2
from sqlalchemy import create_engine, text
import pandas as pd
from datetime import datetime

print("🗄️ Database Integration Test")
print(f"Time: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")

# RDS connection info (şimdilik placeholder)
RDS_ENDPOINT = "my-dev-database.cqx0ougy8gof.us-east-1.rds.amazonaws.com"
RDS_PORT = "5432"
RDS_DATABASE = "postgres"
RDS_USERNAME = "postgres"
RDS_PASSWORD = "DataScience123!"

def test_connection(endpoint):
    """Test database connection"""
    try:
        # Connection string
        conn_str = f"postgresql://{RDS_USERNAME}:{RDS_PASSWORD}@{RDS_ENDPOINT}:{RDS_PORT}/{RDS_DATABASE}?sslmode=require"
        
        print(f"🔌 Connecting to: {endpoint}")
        
        # Create engine
        engine = create_engine(conn_str)
        
        # Test query
        with engine.connect() as conn:
            result = conn.execute(text("SELECT version()"))
            version = result.fetchone()[0]
            print(f"✅ Database Connected!")
            print(f"   PostgreSQL Version: {version.split(',')[0]}")
            
            # Test basic operations
            conn.execute(text("CREATE TABLE IF NOT EXISTS test_table (id SERIAL PRIMARY KEY, name VARCHAR(50), created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP)"))
            conn.execute(text("INSERT INTO test_table (name) VALUES ('Integration Test')"))
            result = conn.execute(text("SELECT COUNT(*) FROM test_table"))
            count = result.fetchone()[0]
            print(f"   Test table records: {count}")
            
            conn.commit()
            
        return True
        
    except Exception as e:
        print(f"❌ Connection failed: {e}")
        print("💡 Make sure:")
        print("   1. RDS database is 'Available'")
        print("   2. Security group allows port 5432")
        print("   3. Public access is enabled")
        return False

def test_pandas_integration():
    """Test pandas with database"""
    print("\n📊 Testing Pandas Integration...")
    
    sample_data = {
        'product': ['Laptop', 'Mouse', 'Keyboard', 'Monitor'],
        'price': [999.99, 29.99, 89.99, 299.99],
        'stock': [50, 200, 75, 30]
    }
    
    df = pd.DataFrame(sample_data)
    print("✅ Sample DataFrame created:")
    print(df)
    print(f"   Shape: {df.shape}")
    
    return df

if __name__ == "__main__":
    if "YOUR_RDS_ENDPOINT_HERE" in RDS_ENDPOINT:
        print("⏳ Waiting for RDS endpoint...")
        print("\n📋 Next steps:")
        print("1. Go to AWS Console → RDS")
        print("2. Wait for database status: 'Available'")
        print("3. Copy the endpoint address")
        print("4. Update RDS_ENDPOINT in this file")
    else:
        success = test_connection(RDS_ENDPOINT)
        if success:
            test_pandas_integration()