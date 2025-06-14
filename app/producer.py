from kafka import KafkaProducer
import json

producer = KafkaProducer(
    bootstrap_servers='localhost:9094',
    value_serializer=lambda v: json.dumps(v).encode('utf-8'),
    key_serializer=lambda k: str(k).encode('utf-8')
)

for i in range(5):
    key = i%2
    value= {"id": i, "message": f"This is message {i}"}
    producer.send("s3-upload-test", key=key, value=value)

producer.flush()
print("✅ Messages sent.")