from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker, AsyncSession
from core.config import settings


class DBConnector:
    def __init__(self, url: str, echo: bool = False):

        self.engine = create_async_engine(
            url=url,
            echo=echo,
        )
        self.session_factory = async_sessionmaker(
            bind=self.engine,
            autocommit=False,
            expire_on_commit=False,
            autoflush=False,
        )

    async def generate_session(self):
        async with self.session_factory() as session:
            yield session
            await session.close()


db = DBConnector(
    url=settings.db_url,
    echo=settings.db_echo,
)



