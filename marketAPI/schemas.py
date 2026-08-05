from pydantic import BaseModel, ConfigDict, EmailStr

class SUserAdd(BaseModel):
    name: str
    mail: EmailStr
    password: str

class SCheckUser(BaseModel):
    mail: EmailStr
    password: str



class SGameAdd(BaseModel):
    name: str
    price: float

class SGame(SGameAdd):
    id: int

    model_config = ConfigDict(from_attributes=True)



class SPaymentAdd(BaseModel):
    user_id: int
    value: float
    payment_id: str
    idempotence_key: str