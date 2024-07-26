from typing import Optional, Any
import logging

from sqlalchemy import (
    Column,
    Integer,
    String,
    UniqueConstraint,
    ForeignKey,
    DateTime,
    select,
    delete,
    update
)
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import declarative_base, sessionmaker
from sqlalchemy.ext.asyncio import AsyncEngine
from sqlalchemy.sql import case
from fastapi_pagination.ext.sqlalchemy import paginate

from partner.schemas import ListPartner
from partner import schemas
from database import Base
import subprocess


logger = logging.getLogger()


async def generate_api_key():
    # Run the openssl command to generate a 64-character API key
    result = subprocess.run(['openssl', 'rand', '-base64', '48'], capture_output=True, text=True)
    api_key = result.stdout[:64]
    return api_key


class Partner(Base):
    __tablename__ = "partners"
    id = Column("id", Integer, primary_key=True, index=True)
    name = Column("name", String(256), nullable=False)
    phone = Column("phone", String(256), nullable=False)
    is_active = Column("is_active", Integer, nullable=False, default=1)
    api_callback_url = Column("api_callback_url", String(256), nullable=True)

    def to_json(self):
        return dict(id=self.id, name=self.name, phone=self.phone, api_callback_url=self.api_callback_url)

    # @staticmethod
    # async def get_partner_by_api_key(db: AsyncEngine, api_key: str):
    #     async with db.connect() as session:
    #         result = await session.execute(
    #             select(Partner).where(Partner.api_key == api_key)
    #         )
    #         partner = result.scalars().first()
    #         return partner

    @staticmethod
    async def get_partner_by_id(db: AsyncEngine, partner_id: int):
        async with db.connect() as session:
            result = await session.execute(
                select(Partner).where(Partner.id == partner_id)
            )
            partner = result.first()
            return partner

    @staticmethod
    async def get_all_partners(db: AsyncEngine):
        async_session = sessionmaker(db, class_=AsyncSession, expire_on_commit=False)
        async with async_session() as session:
            # result = await session.execute(
            #     select(Partner)
            # )
            query = select(Partner).order_by(Partner.id.desc())
            # partners = result.all()
            partners = await paginate(session, query)
            return partners

    @staticmethod
    async def create_partner(db: AsyncEngine, partner: schemas.PartnerCreate):
        async_session = sessionmaker(db, class_=AsyncSession, expire_on_commit=False)
        async with async_session() as session:
            partner = Partner(
                name=partner.name,
                phone=partner.phone,
                api_callback_url=partner.api_callback_url,
                # api_key=str(uuid4())
            )
            session.add(partner)
            await session.flush()
            api_key = ApiKey(
                api_key=str(await generate_api_key()),
                partner_id=partner.id
            )
            session.add(api_key)
            await session.commit()
            return partner

    @staticmethod
    async def update_partner(db: AsyncEngine, partner_id: int, partner: schemas.PartnerUpdate):
        async_session: sessionmaker = sessionmaker(db, class_=AsyncSession, expire_on_commit=False)
        async with async_session() as session:
            result = await session.execute(
                select(Partner).filter(Partner.id == partner_id)
            )
            db_partner = result.scalars().one()
            for key, value in partner.model_dump(exclude_unset=True).items():
                setattr(db_partner, key, value)
            session.add(db_partner)
            await session.commit()
            return db_partner

    @staticmethod
    async def delete_partner(db: AsyncEngine, partner_id: int):
        async_session: sessionmaker = sessionmaker(db, class_=AsyncSession, expire_on_commit=False)
        async with async_session() as session:
            # await session.execute(
            #     delete(ApiKey).where(ApiKey.partner_id == partner_id)
            # )
            await session.execute(
                delete(Partner).where(Partner.id == partner_id)
            )
            await session.commit()


    @staticmethod
    async def deactivate_partner(db: AsyncEngine, partner_id: int):
        async with db.connect() as session:
            result = await session.execute(
                update(Partner).where(Partner.id == partner_id).values(is_active=0).returning(Partner)
            )
            partner = result.first()
            api_key = await session.execute(
                update(ApiKey).where(ApiKey.partner_id == partner_id).values(is_active=0).returning(ApiKey)
            )
            await session.commit()
            return partner


    @staticmethod
    async def activate_partner(db: AsyncEngine, partner_id: int):
        async with db.connect() as session:
            result = await session.execute(
                update(Partner).where(Partner.id == partner_id).values(is_active=1).returning(Partner)
            )
            partner = result.first()
            api_key = await session.execute(
                update(ApiKey).where(ApiKey.partner_id == partner_id).values(is_active=1).returning(ApiKey)
            )
            await session.commit()
            return partner


class ApiKey(Base):
    __tablename__ = "api_keys"
    id = Column("id", Integer, primary_key=True, index=True)
    api_key = Column("api_key", String(256), nullable=False)
    partner_id = Column("partner_id", Integer, ForeignKey("partners.id", ondelete="CASCADE"), nullable=False)
    is_active = Column("is_active", Integer, nullable=False, default=1)
    is_shown = Column("is_shown", Integer, nullable=False, default=0)

    def to_json(self):
        return dict(id=self.id, api_key=self.api_key, partner=self.partner_id, is_active=self.is_active,
                    is_shown=self.is_shown)

    @staticmethod
    async def check_api_key(db: AsyncEngine, api_key: str):
        '''
        :param db: AsyncEngine - connection to database
        :param api_key: partner api key to check in database
        :return: ApiKey object
        '''
        async with db.connect() as session:
            result = await session.execute(
                select(ApiKey).where(ApiKey.api_key == api_key, ApiKey.is_active == 1)
            )
            api_key = result.first()
            return api_key

    @staticmethod
    async def check_api_key_by_partner_id(db: AsyncEngine, api_key: str, partner_id: int):
        '''
        :param db: AsyncEngine - connection to database
        :param api_key: partner api key to check in database
        :param partner_id:  partner id to check in database
        :return: ApiKey object
        '''
        async with db.connect() as session:
            result = await session.execute(
                select(ApiKey).where(ApiKey.api_key == api_key, ApiKey.partner_id == partner_id, ApiKey.is_active)
            )
            api_key = result.first()
            return api_key

    @staticmethod
    async def get_partner_by_api_key(db: AsyncEngine, api_key: str):
        '''
        :param api_key:
        :param db: AsyncEngine - connection to database
        :return: ApiKey object
        '''
        async with db.connect() as session:
            result = await session.execute(
                select(ApiKey.partner_id).where(ApiKey.api_key == api_key)
            )
            partner_id = result.scalar()
            return partner_id

    @staticmethod
    async def create_api_key(db: AsyncEngine, partner_id: int):
        '''
        :param db: AsyncEngine - connection to database
        :param partner_id: partner id to create api key
        :return: ApiKey object
        '''
        async_session = sessionmaker(db, class_=AsyncSession, expire_on_commit=False)
        async with async_session() as session:
            async with session.begin():
                # Check if an ApiKey with the given partner_id exists
                result = await session.execute(
                    select(ApiKey).where(ApiKey.partner_id == partner_id)
                )
                existing_api_key = result.scalars().first()

                if existing_api_key:
                    # Update the existing ApiKey
                    await session.execute(
                        update(ApiKey)
                        .where(ApiKey.id == existing_api_key.id)
                        .values(api_key=str(await generate_api_key()), is_shown=1)
                    )
                    await session.commit()
                    return existing_api_key
                else:
                    # Create a new ApiKey
                    new_api_key = ApiKey(
                        api_key=str(await generate_api_key()),
                        partner_id=partner_id
                    )
                    session.add(new_api_key)
                    await session.commit()
                    return new_api_key

    @staticmethod
    async def deactivate_api_key(db: AsyncEngine, api_key: str):
        '''
        :param db: AsyncEngine - connection to database
        :param api_key: partner
        :return: ApiKey object
        '''
        async with db.connect() as session:
            result = await session.execute(
                update(ApiKey).where(ApiKey.api_key == api_key).values(is_active=0).returning(ApiKey)
            )
            api_key = result.first()
            await session.commit()
            return api_key
