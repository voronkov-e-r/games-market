from aiokafka import AIOKafkaProducer, AIOKafkaConsumer
import json
import asyncio

BOOTSTRAP_SERVER = 'localhost:9092'

async def say_to_kafka(topic:str, value=None):
    producer = AIOKafkaProducer(
        bootstrap_servers=BOOTSTRAP_SERVER,
        value_serializer=lambda v: json.dumps(v).encode('utf-8')
    )

    cons_topic = topic + '_res'
    consumer = AIOKafkaConsumer(
        cons_topic,
        bootstrap_servers=BOOTSTRAP_SERVER,
        value_deserializer=lambda m: json.loads(m.decode('utf-8')),
        group_id='test_group',
        auto_offset_reset='earliest',
        enable_auto_commit=False
    )

    await producer.start()
    await consumer.start()

    try:
        partitions = consumer.assignment()
        for partition in partitions:
            end_offset = await consumer.end_offsets([partition])
            consumer.seek(partition, end_offset[partition])

        await producer.send(topic, value)

        async for msg in consumer:
            await consumer.commit()
            return msg.value

    except Exception as e:
        return {'ok':False, 'detail':e}
    finally:
        await producer.stop()
        await consumer.stop()

    return {'ok':False}


def kafka_feedback(topic:str, value=None):
    result = asyncio.run(say_to_kafka(topic, value))
    return result