from sqlalchemy import select, and_, Result

from src.db import connector
from src.core.config import settings
from src.models.users import User, RoleEnum

from src.api.auth.utils import hash_password


async def create_superuser():
    async with connector.session_factory() as session:  # Используем контекстный менеджер
        stmt = select(User).where(
            and_(
                User.email == settings.admin.email,
                User.role == RoleEnum.admin
            )
        )

        result = await session.execute(stmt)
        user = result.scalars().first()

        password_hash=hash_password(settings.admin.password).decode('utf-8')
        if not user:
            try:
                user = User(
                    email=settings.admin.email,
                    password_hash=password_hash,
                    role=RoleEnum.admin
                )
                session.add(user)
                await session.commit()
            except Exception as e:
                pass

    print("Created superuser")
    return user
