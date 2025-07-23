# test_integration.py
import boto3
import pandas as pd
import json

print("🚀 Integration Test Started!")

# AWS S3 Test
try:
    s3 = boto3.client('s3')
    buckets = s3.list_buckets()
    print(f"✅ AWS S3 Connected! Found {len(buckets['Buckets'])} buckets")
    for bucket in buckets['Buckets']:
        print(f"   - {bucket['Name']}")
except Exception as e:
    print(f"❌ AWS S3 Error: {e}")

# Pandas Test
try:
    df = pd.DataFrame({
        'name': ['AWS', 'Git', 'Python', 'VS Code'],
        'status': ['✅', '✅', '✅', '✅']
    })
    print("\n✅ Pandas Working!")
    print(df)
except Exception as e:
    print(f"❌ Pandas Error: {e}")

# AWS Identity Test
try:
    sts = boto3.client('sts')
    identity = sts.get_caller_identity()
    print(f"\n✅ AWS Identity: {identity['Arn']}")
except Exception as e:
    print(f"❌ AWS Identity Error: {e}")

print("\n🎉 Integration Test Complete!")