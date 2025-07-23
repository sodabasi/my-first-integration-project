# advanced_data_generator.py - Enhanced E-commerce Dataset
import pandas as pd
import numpy as np
from datetime import datetime, timedelta
from sqlalchemy import create_engine, text
import warnings
warnings.filterwarnings('ignore')

print("🚀 Advanced Data Analysis - Dataset Generation")

# Database connection
RDS_ENDPOINT = "my-dev-database.cqx0ougy8gof.us-east-1.rds.amazonaws.com"
conn_str = f"postgresql://postgres:DataScience123!@{RDS_ENDPOINT}:5432/postgres?sslmode=require"
engine = create_engine(conn_str)

def generate_comprehensive_dataset():
    """Generate realistic e-commerce dataset with advanced features"""
    np.random.seed(42)
    
    print("\n📊 Generating comprehensive dataset...")
    
    # Date range for 2 years of data
    start_date = datetime(2023, 1, 1)
    end_date = datetime(2024, 12, 31)
    date_range = pd.date_range(start_date, end_date, freq='D')
    
    # Product catalog with realistic pricing
    products_catalog = {
        'Electronics': {
            'Laptop': {'base_price': 800, 'margin': 400, 'seasonality': 1.2},
            'Monitor': {'base_price': 300, 'margin': 200, 'seasonality': 1.0},
            'Keyboard': {'base_price': 80, 'margin': 40, 'seasonality': 0.9},
            'Mouse': {'base_price': 40, 'margin': 30, 'seasonality': 0.8},
            'Headphones': {'base_price': 150, 'margin': 100, 'seasonality': 1.1}
        },
        'Office': {
            'Chair': {'base_price': 250, 'margin': 150, 'seasonality': 0.7},
            'Desk': {'base_price': 400, 'margin': 200, 'seasonality': 0.8},
            'Lamp': {'base_price': 60, 'margin': 40, 'seasonality': 0.6}
        }
    }
    
    # Customer segments with different behaviors
    customer_segments = {
        'Premium': {'spend_multiplier': 1.5, 'frequency': 0.3, 'avg_items': 2.5},
        'Regular': {'spend_multiplier': 1.0, 'frequency': 0.5, 'avg_items': 1.8},
        'Budget': {'spend_multiplier': 0.7, 'frequency': 0.6, 'avg_items': 1.2},
        'Bulk': {'spend_multiplier': 1.3, 'frequency': 0.1, 'avg_items': 4.0}
    }
    
    # Regional characteristics
    regions_data = {
        'North': {'population_weight': 0.3, 'income_modifier': 1.2, 'tech_affinity': 1.3},
        'South': {'population_weight': 0.25, 'income_modifier': 0.9, 'tech_affinity': 0.8},
        'East': {'population_weight': 0.3, 'income_modifier': 1.1, 'tech_affinity': 1.2},
        'West': {'population_weight': 0.15, 'income_modifier': 1.0, 'tech_affinity': 1.0}
    }
    
    records = []
    customer_history = {}  # Track customer behavior over time
    
	# Generate 2000+ records with realistic patterns
    for i in range(2000):
        # Select date with seasonal patterns - FIXED VERSION
        if i < 500:  # Q1 - Lower sales
            days_idx = np.random.randint(0, 90)
            date = start_date + timedelta(days=days_idx)
            seasonal_factor = 0.8
        elif i < 1000:  # Q2 - Spring boost
            days_idx = np.random.randint(90, 180)
            date = start_date + timedelta(days=days_idx)
            seasonal_factor = 1.1
        elif i < 1500:  # Q3 - Summer steady
            days_idx = np.random.randint(180, 270)
            date = start_date + timedelta(days=days_idx)
            seasonal_factor = 1.0
        else:  # Q4 - Holiday season
            days_idx = np.random.randint(270, 730)  # 2 years = ~730 days
            date = start_date + timedelta(days=days_idx)
            seasonal_factor = 1.4
        
        # Select region based on population weights
        region = np.random.choice(
            list(regions_data.keys()),
            p=[regions_data[r]['population_weight'] for r in regions_data.keys()]
        )
        region_info = regions_data[region]
        
        # Generate or reuse customer
        if np.random.random() < 0.3 and customer_history:  # 30% repeat customers
            customer_id = np.random.choice(list(customer_history.keys()))
            segment = customer_history[customer_id]['segment']
        else:  # New customer
            customer_id = f'CUST-{10000 + len(customer_history)}'
            segment = np.random.choice(list(customer_segments.keys()))
            customer_history[customer_id] = {
                'segment': segment,
                'region': region,
                'lifetime_orders': 0,
                'total_spent': 0
            }
        
        segment_info = customer_segments[segment]
        
        # Select category and product
        category = np.random.choice(list(products_catalog.keys()))
        product = np.random.choice(list(products_catalog[category].keys()))
        product_info = products_catalog[category][product]
        
        # Calculate realistic pricing with multiple factors
        base_price = product_info['base_price']
        price_variation = np.random.uniform(0.9, 1.1)  # ±10% variation
        seasonal_effect = seasonal_factor * product_info['seasonality']
        regional_effect = region_info['income_modifier']
        segment_effect = segment_info['spend_multiplier']
        
        unit_price = round(base_price * price_variation * seasonal_effect * regional_effect, 2)
        
        # Quantity based on customer segment and product type
        if category == 'Office' and segment == 'Bulk':
            quantity = np.random.randint(2, 8)
        else:
            max_qty = int(segment_info['avg_items'] * np.random.uniform(0.5, 2.0))
            quantity = max(1, max_qty)
        
        # Calculate totals
        subtotal = round(unit_price * quantity, 2)
        
        # Add discount logic
        discount_rate = 0
        if customer_history[customer_id]['lifetime_orders'] > 5:  # Loyalty discount
            discount_rate = 0.05
        elif subtotal > 1000:  # Bulk discount
            discount_rate = 0.10
        elif date.month in [11, 12]:  # Holiday discount
            discount_rate = 0.15
        
        discount_amount = round(subtotal * discount_rate, 2) if np.random.random() < 0.3 else 0
        total_amount = subtotal - discount_amount
        
        # Shipping and handling
        shipping_cost = 0 if total_amount > 100 else round(np.random.uniform(5, 15), 2)
        final_total = total_amount + shipping_cost
        
        # Customer satisfaction (influenced by multiple factors)
        satisfaction_base = 4.0
        if segment == 'Premium':
            satisfaction_base = 4.5
        elif segment == 'Budget':
            satisfaction_base = 3.8
        
        satisfaction = round(min(5.0, max(1.0, 
            satisfaction_base + np.random.normal(0, 0.5))), 1)
        
        # Create record
        record = {
            'order_id': f'ORD-{100000 + i}',
            'customer_id': customer_id,
            'order_date': date.strftime('%Y-%m-%d'),
            'category': category,
            'product': product,
            'quantity': quantity,
            'unit_price': unit_price,
            'subtotal': subtotal,
            'discount_rate': discount_rate,
            'discount_amount': discount_amount,
            'shipping_cost': shipping_cost,
            'total_amount': final_total,
            'region': region,
            'customer_segment': segment,
            'satisfaction_rating': satisfaction,
            'day_of_week': date.strftime('%A'),
            'month': date.month,
            'quarter': f'Q{(date.month-1)//3 + 1}',
            'is_weekend': 1 if date.weekday() >= 5 else 0,
            'is_holiday_season': 1 if date.month in [11, 12] else 0
        }
        
        records.append(record)
        
        # Update customer history
        customer_history[customer_id]['lifetime_orders'] += 1
        customer_history[customer_id]['total_spent'] += final_total
    
    df = pd.DataFrame(records)
    
    print(f"✅ Generated {len(df)} records with advanced features:")
    print(f"   • Date range: {df['order_date'].min()} to {df['order_date'].max()}")
    print(f"   • Categories: {df['category'].nunique()}")
    print(f"   • Products: {df['product'].nunique()}")
    print(f"   • Customers: {df['customer_id'].nunique()}")
    print(f"   • Total revenue: ${df['total_amount'].sum():,.2f}")
    
    return df

def upload_advanced_dataset(df):
    """Upload enhanced dataset to database"""
    print("\n📤 Uploading to database...")
    
    try:
        # Create advanced table with all features
        df.to_sql('advanced_sales_data', engine, if_exists='replace', index=False, method='multi')
        print(f"   ✅ Uploaded {len(df)} records to 'advanced_sales_data' table")
        
        # Verify upload
        with engine.connect() as conn:
            result = conn.execute(text("SELECT COUNT(*) FROM advanced_sales_data"))
            count = result.fetchone()[0]
            print(f"   ✅ Verified: {count} records in database")
            
            # Show table structure
            result = conn.execute(text("""
                SELECT column_name, data_type 
                FROM information_schema.columns 
                WHERE table_name = 'advanced_sales_data' 
                ORDER BY ordinal_position
            """))
            
            columns = result.fetchall()
            print(f"   ✅ Table structure: {len(columns)} columns")
            
        return True
        
    except Exception as e:
        print(f"   ❌ Upload failed: {e}")
        return False

def main():
    try:
        # Generate comprehensive dataset
        df = generate_comprehensive_dataset()
        
        # Upload to database
        if upload_advanced_dataset(df):
            print(f"\n🎉 Advanced Dataset Ready!")
            print("=" * 50)
            print("✅ 2000+ realistic e-commerce records")
            print("✅ Multi-dimensional analysis features")
            print("✅ Customer segmentation data")
            print("✅ Seasonal and regional patterns")
            print("✅ Advanced pricing and discount logic")
            print("✅ Customer satisfaction metrics")
            print("\n🚀 Ready for Advanced Analytics!")
        else:
            print(f"\n❌ Dataset generation failed")
    
    except Exception as e:
        print(f"\n❌ Error: {e}")

if __name__ == "__main__":
    main()