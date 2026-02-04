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
    
    async def get_telegram_id_by_topic_id(self, topic_id: int) :
        """Получить telegram_id по topic_id"""
        stmt = select(User.telegram_id).where(User.topic_id == topic_id)
        result = await self.session.execute(stmt)
        
        telegram_id = result.scalar_one_or_none()
        return telegram_id
    

    async def get_topic_id_by_telegram_id(self, telegram_id: int) -> Optional[int]:
        """Получить topic_id по telegram_id"""
        stmt = select(User.topic_id).where(User.telegram_id == telegram_id)
        result = await self.session.execute(stmt)
        
        topic_id = result.scalar_one_or_none()
        return topic_id