from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from .models import User

class UserRepository:
    def __init__(self, session: AsyncSession):
        self.session = session

    async def get_by_telegram_id(self, telegram_id: int) -> User | None:
        result = await self.session.execute(
            select(User).where(User.telegram_id == telegram_id)
        )
        return result.scalar_one_or_none()

    async def create(self, telegram_id: int) -> User:
        user = User(telegram_id=telegram_id)
        self.session.add(user)
        await self.session.commit()
        return user
    

    async def set_topic_id(self, telegram_id: int, topic_id: int) -> User:
    
        stmt = select(User).where(User.telegram_id == telegram_id)
        result = await self.session.execute(stmt)
        user = result.scalar_one_or_none()
        
        if not user:
            raise ValueError(f"User with telegram_id {telegram_id} not found")
        
        # Устанавливаем topic_id
        user.topic_id = topic_id
        
        # Сохраняем изменения
        await self.session.commit()
        
        return user