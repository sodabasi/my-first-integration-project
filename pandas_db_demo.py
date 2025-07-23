# pandas_db_demo.py - Complete Version
import pandas as pd
from sqlalchemy import create_engine, text
import numpy as np

print("🚀 Pandas + PostgreSQL Integration Demo")

# Database connection
RDS_ENDPOINT = "my-dev-database.cqx0ougy8gof.us-east-1.rds.amazonaws.com"
conn_str = f"postgresql://postgres:DataScience123!@{RDS_ENDPOINT}:5432/postgres?sslmode=require"

try:
    engine = create_engine(conn_str)
    print("✅ Database engine created")
except Exception as e:
    print(f"❌ Engine creation failed: {e}")
    exit()

def create_sample_data():
    print("\n1. Generating sample data...")
    np.random.seed(42)
    
    data = []
    for i in range(50):  # 50 records for testing
        record = {
            'order_id': f'ORD-{1000+i}',
            'customer_id': f'CUST-{np.random.randint(1, 20)}',
            'product': np.random.choice(['Laptop', 'Mouse', 'Keyboard', 'Monitor']),
            'quantity': np.random.randint(1, 5),
            'price': round(np.random.uniform(50.0, 500.0), 2),
            'region': np.random.choice(['North', 'South', 'East', 'West'])
        }
        record['total_amount'] = round(record['quantity'] * record['price'], 2)
        data.append(record)
    
    df = pd.DataFrame(data)
    print(f"   ✅ Created {len(df)} records")
    return df

def upload_to_database(df):
    print("\n2. Uploading to database...")
    try:
        df.to_sql('sales_data', engine, if_exists='replace', index=False)
        print(f"   ✅ Uploaded {len(df)} records")
        
        with engine.connect() as conn:
            result = conn.execute(text("SELECT COUNT(*) FROM sales_data"))
            count = result.fetchone()[0]
            print(f"   ✅ Verified: {count} records")
        return True
    except Exception as e:
        print(f"   ❌ Upload failed: {e}")
        return False

def analyze_data():
    print("\n3. Analyzing data...")
    try:
        df = pd.read_sql("SELECT * FROM sales_data", engine)
        
        print(f"\n📊 Analysis:")
        print(f"   Total Records: {len(df)}")
        print(f"   Total Revenue: ${df['total_amount'].sum():,.2f}")
        print(f"   Average Order: ${df['total_amount'].mean():.2f}")
        
        top_products = df.groupby('product')['total_amount'].sum().sort_values(ascending=False)
        print(f"\n🏆 Top Products:")
        for product, revenue in top_products.items():
            print(f"   {product}: ${revenue:,.2f}")
            
        return True
    except Exception as e:
        print(f"   ❌ Analysis failed: {e}")
        return False

# Main execution
if __name__ == "__main__":
    try:
        df = create_sample_data()
        if upload_to_database(df):
            if analyze_data():
                print(f"\n🎉 Integration Complete!")
            else:
                print(f"\n⚠️ Analysis failed")
        else:
            print(f"\n❌ Upload failed")
    except Exception as e:
        print(f"\n❌ Demo failed: {e}")