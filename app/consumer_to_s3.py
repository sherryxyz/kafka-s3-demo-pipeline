from dotenv import load_dotenv
import os
from kafka import KafkaConsumer
import json
import boto3
import time
from datetime import datetime


load_dotenv()

aws_access_key = os.getenv("AWS_ACCESS_KEY_ID")
aws_secret_key = os.getenv("AWS_SECRET_ACCESS_KEY")
region = os.getenv("AWS_REGION")
bucket = os.getenv("S3_BUCKET_NAME")

print("S3 config loaded.")

# init boto3 S3 client
s3_client = boto3.client(
    "s3",
    aws_access_key_id=aws_access_key,
    aws_secret_access_key=aws_secret_key,
    region_name=region
)

def safe_json_deserializer(v):
    try:
        if not v:
            return None
        return json.loads(v.decode("utf-8"))
    except Exception as e:
        print(f"❌ Failed to decode value: {v} - {e}")
        return None

def safe_key_deserializer(k):
    try:
        return k.decode("utf-8") if k else None
    except Exception:
        return None

# setup Kafka consumer
consumer = KafkaConsumer(
    "s3-upload-test",
    bootstrap_servers="localhost:9094",
    auto_offset_reset="latest",
    value_deserializer=safe_json_deserializer,
    key_deserializer=safe_key_deserializer,
    group_id="kafka-s3-group"
)

print("✅ Consumer started. Listening for messages...")


for msg in consumer:
    print(f"📥 Key: {msg.key}, Value: {msg.value}, Partition: {msg.partition}")

    # prepare upload content
    content = json.dumps(msg.value)
    timestamp = datetime.utcnow().strftime("%Y%m%d-%H%M%S")
    key = msg.key or "no-key"

    # define S3 object key
    s3_key = f"kafka-demo/{key}/msg-{timestamp}.json"

    # upload to s3
    try:
        s3_client.put_object(
            Bucket=bucket,
            Key=s3_key,
            Body=content,
            ContentType='application/json'
        )
        print(f"✅ Uploaded to s3://{bucket}/{s3_key}")
    except Exception as e:
        print(f"❌ Failed to upload to S3: {e}")