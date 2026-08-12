from aiokafka import AIOKafkaProducer, AIOKafkaConsumer
import json

from fastapi import HTTPException
from pydantic import BaseModel

import routers
import schemas

BOOTSTRAP_SERVER = 'localhost:9092'


topics_dict = {
    'checkreg': routers.check_registration,
    'getuser': routers.get_user_data,
    'getgames': routers.get_games,
    'buygame': routers.buy_one_game,
    'pupbalance': routers.pup_balance,
}

schemas_dict = {
    'checkreg': schemas.SCheckUser,
    'getuser': schemas.SCheckUser,
    'getgames': None,
    'buygame': schemas.SPaymentAdd,
    'pupbalance': schemas.SPaymentAdd,
}

topics = ['checkreg', 'getuser', 'buygame', 'getgames', 'pupbalance']

async def consuming():
    producer = AIOKafkaProducer(
        bootstrap_servers=BOOTSTRAP_SERVER,
        value_serializer=lambda v: json.dumps(v).encode('utf-8')
    )

    consumer = AIOKafkaConsumer(
        *topics,
        bootstrap_servers=BOOTSTRAP_SERVER,
        value_deserializer=lambda m: json.loads(m.decode('utf-8')),
        group_id='test_group',
        auto_offset_reset='earliest',
        enable_auto_commit=True
    )

    await producer.start()
    await consumer.start()

    try:
        async for msg in consumer:
            temp_topic = msg.topic
            try:
                if schemas_dict[temp_topic] is None:
                    result = await topics_dict[temp_topic]()
                else:
                    schema = schemas_dict[temp_topic](**msg.value)
                    result = await topics_dict[temp_topic](schema)


                result = serializable(result)
                #print(result)

                await producer.send(temp_topic + '_res', value=result)
            except HTTPException as e:
                #print(e)
                await producer.send(temp_topic + '_res', value={'ok':False, 'detail':e.detail})
    finally:
        await consumer.stop()
        await producer.stop()


def serializable(obj):
    if isinstance(obj, BaseModel):
        return obj.model_dump()
    elif isinstance(obj, list):
        return [serializable(item) for item in obj]
    elif isinstance(obj, dict):
        return {serializable(key): serializable(value) for key, value in obj.items()}
    else:
        return obj