# Kafka to S3 Demo Project

This project demonstrates how to build a simple data pipeline using **Apache Kafka**, **Python**, and **Amazon S3**. The pipeline consists of:

* A Kafka broker (running in Docker)
* A Kafka producer script that sends JSON messages
* A Kafka consumer script that receives messages and uploads them to an S3 bucket

⚠️ Note: Amazon S3 is a paid service. If you're using a non-new AWS account, you may be charged for object storage and requests. Please follow the cleanup instructions below to avoid extra charges.

---

## 🔧 Project Structure

```
kafka-s3-demo/
├── app/
│   ├── __init__.py
│   ├── producer.py
│   ├── consumer_to_s3.py
│   └── requirements.txt
├── docker-compose.yml
├── .env
├── .gitignore
├── LICENSE
├── README.md
```

---

## ✅ Prerequisites

* Docker & Docker Compose
* Python 3.8+
* AWS account with S3 access
* IAM user with `AmazonS3FullAccess`
* Kafka Python client: `kafka-python`

---

## 📦 Setup Instructions

### 1. Clone the repository

```
git clone <your-repo-url>
cd kafka-s3-demo
```

### 2. Set up virtual environment

```
python3 -m venv venv
source venv/bin/activate
pip install -r app/requirements.txt
```

### 3. Create a `.env` file in the root directory

```env
AWS_ACCESS_KEY_ID=your-access-key
AWS_SECRET_ACCESS_KEY=your-secret-key
AWS_REGION=your-aws-region
S3_BUCKET_NAME=your-s3-bucket-name 
```
note that bucket name is unique globally

### 4. Start Kafka & Kafka UI using Docker Compose

```
docker-compose up -d
```

This will start:

* Apache Kafka (KRaft mode)
* Kafka UI ([http://localhost:8088](http://localhost:8088))

Kafka will listen on `localhost:9094`.

### 5. Create Kafka topic (if not already created)

```
docker exec broker /opt/kafka/bin/kafka-topics.sh \
  --create \
  --topic s3-upload-test \
  --bootstrap-server localhost:9094 \
  --partitions 2 \
  --replication-factor 1
```

---

## 📨 Sending Messages

Run the producer to send JSON messages to the Kafka topic:

```bash
python app/producer.py
```

Sample logic (in producer.py):

```python
for i in range(5):
    key = str(i % 2)
    value = {"id": i, "message": f"This is message {i}"}
    producer.send("s3-upload-test", key=key, value=value)
```

---

## 📥 Consuming and Uploading to S3

Run the consumer to read messages and upload to S3:

```bash
python app/consumer_to_s3.py
```

It will consume from `s3-upload-test` and write each message to:

```
s3://<bucket-name>/kafka-demo/<key>/msg-<timestamp>.json
```

---

## 🧹 Cleanup

To stop services:

```
docker-compose down
```

To avoid extra charges:

* **Empty your S3 bucket** via the console or CLI
* Abort any unfinished multipart uploads
* Optional: delete the bucket and IAM user if no longer needed


---

## ✅ Confirmed Working

* Kafka working with external listener (`localhost:9094`)
* Producer can send JSON with keys to specific partitions
* Consumer reads, deserializes, and writes to S3
* S3 credentials managed via `.env`

---

## 🔒 Notes

* Do **not** commit `.env` to version control
* You can monitor topic data via Kafka UI ([http://localhost:8088](http://localhost:8088))
* Ensure IAM user has sufficient permissions (`PutObject`)

---

## 🔁 Next Steps (Optional Enhancements)

* Use batching to upload groups of messages
* Add Flink or dbt to process S3 data
* Dockerize the consumer script
* Add logging and monitoring

---

Enjoy building data pipelines 🚀
