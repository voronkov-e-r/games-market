from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column


engine = create_async_engine(
    'sqlite+aiosqlite:///tasks.db'
)
new_session = async_sessionmaker(engine, expire_on_commit=False)


class Model(DeclarativeBase):
    pass


class UsersORM(Model):
    __tablename__ = 'users'

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str]
    mail: Mapped[str] = mapped_column(unique=True)
    password: Mapped[str]
    balance: Mapped[float] = mapped_column(nullable=False, default=0.0)


class GamesORM(Model):
    __tablename__ = 'games'

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(unique=True)
    price: Mapped[float]


class PaymentORM(Model):
    __tablename__ = 'payment'

    id: Mapped[int] = mapped_column(primary_key=True)
    user_id: Mapped[int]
    value: Mapped[float]
    payment_id: Mapped[str]
    idempotence_key: Mapped[str]
    status: Mapped[str] = mapped_column(default='processing')



async def create_tables():
    async with engine.begin() as conn:
        await conn.run_sync(Model.metadata.create_all)

async def delete_tables():
    async with engine.begin() as conn:
        await conn.run_sync(Model.metadata.drop_all)