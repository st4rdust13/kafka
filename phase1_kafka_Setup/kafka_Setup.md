# Kafka Setup Instructions (macOS - Homebrew Version)

## Environment
- OS: macOS (Apple Silicon)
- Java: OpenJDK 11 via Homebrew
- Kafka Version: 3.9.0 (installed via Homebrew)
- Python: 3.10
- Shell: zsh

---

## Kafka & Zookeeper Setup

### 1. Install openjdk 11 and Kafka 3.9.0 (the version that includes Zookeeper)

```
brew install openjdk@11 

brew install kafka
```

### 2. Kafka Server Start

```
zookeeper-server-start /opt/homebrew/etc/kafka/zookeeper.properties
```

### 3. Zookeeper Server Start (In a new window)

```
kafka-server-start /opt/homebrew/etc/kafka/server.properties
```

### 4. Create Kafka Topic
```
kafka-topics --create \
  --topic air_quality_data \
  --bootstrap-server localhost:9092 \
  --partitions 1 \
  --replication-factor 1
```

### 5. Verify Topic Creation
```
kafka-topics --list --bootstrap-server localhost:9092
```



## Challenges Faced While Installing Kafka

The kafka version 4.0.0 and jdk version 17 was installed first using commands - 
brew install openjdk@17 
curl -O https://downloads.apache.org/kafka/3.7.0/kafka_2.13-4.0.0.tgz
tar -xvzf kafka_2.13-4.0.0.tgz

But this led to issues in starting the kafka server -

(base) devanraj@Devans-MacBook-Air-5 kafka % zookeeper-server-start /opt/homebrew/etc/kafka/zookeeper.properties
zsh: command not found: zookeeper-server-start

This was because zookeeper was found to be not compatible with java 17 and kafka 4.0.0 versions.

This was resolved by downloading the lower versions of java 11 and kafka 3.9.0 




