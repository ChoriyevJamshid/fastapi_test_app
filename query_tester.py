import asyncio
from typing import List

from sqlalchemy import select, String
from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker, AsyncSession
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column


class Base(DeclarativeBase):
    __abstract__ = True
    id: Mapped[int] = mapped_column(primary_key=True)


class User(Base):
    __tablename__ = "users"

    username: Mapped[str] = mapped_column(String(32), unique=True)
    first_name: Mapped[str] = mapped_column(String(32), nullable=True)
    last_name: Mapped[str] = mapped_column(String(32), nullable=True)
    email: Mapped[str] = mapped_column(String(100))
    password_hash: Mapped[str]
    active: Mapped[bool] = mapped_column(default=True, server_default="true")

    def __str__(self) -> str:
        return self.username


class Product(Base):
    __tablename__ = "products"
    title: Mapped[str]
    summary: Mapped[str | None]



class QueryTester:
    def __init__(self):
        self.engine = create_async_engine(
            url="sqlite+aiosqlite:///test_db.sqlite3",
            echo=True
        )
        self.session_factory = async_sessionmaker(
            bind=self.engine,
            expire_on_commit=False,
            autocommit=False,
            autoflush=False
        )


    async def generate_session(self):
        async with self.session_factory() as session:
            yield session
            await session.close()

    async def create_tables(self):
        async with self.engine.begin() as conn:
            await conn.run_sync(Base.metadata.create_all)

    async def drop_tables(self):
        async with self.engine.begin() as conn:
            await conn.run_sync(Base.metadata.drop_all)


async def add_user(session: AsyncSession, user: dict) -> User:
    user: User = User(**user)
    session.add(user)
    await session.commit()
    return user


async def get_users(session: AsyncSession) -> List[User]:
    stmt = select(User)
    result = await session.execute(stmt)
    return list(result.scalars())


async def get_user_by_email(session: AsyncSession, email: str) -> User:
    stmt = select(User).where(User.email == email)
    result = await session.execute(stmt)
    return result.scalar_one_or_none()


async def create_product(session: AsyncSession, product: dict) -> Product:
    product = Product(**product)
    session.add(product)
    await session.commit()


async def get_product(session: AsyncSession, title: str):
    stmt = select(Product).where(Product.title == title).order_by(Product.id)
    result = await session.execute(stmt)
    return result.scalars()


async def main():
    tester: QueryTester = QueryTester()
    # await tester.create_tables()
    session = tester.session_factory()

    # await create_product(session, {
    #     "title": "Product 1",
    #     "summary": "Product 3 summary",
    # })
    #
    # await create_product(session, {
    #     "title": "Product 2",
    #     "summary": "Product 2 summary",
    # })
    # queries
    # user = await get_user_by_email(session, email="j1amshid@mail.ru")
    # print(user)
    # print(user.id, user.username)
    # end queries
    products = await get_product(session, "Product 1")
    for product in products:
        print(f"title = {product.title}, summary = {product.summary}")
    # print(f"\n{product.title}, {product.summary}\n")

    await session.close()

if __name__ == "__main__":
    asyncio.run(main())
