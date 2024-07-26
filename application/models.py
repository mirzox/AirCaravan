from typing import Optional, Any
import logging

from fastapi import HTTPException
from sqlalchemy import (
    Column,
    Integer,
    String,
    UniqueConstraint,
    ForeignKey,
    DateTime,
    Date,
    select,
    Table
)
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.ext.hybrid import hybrid_property
from sqlalchemy.orm import declarative_base, sessionmaker, relationship, joinedload
from fastapi_pagination.ext.sqlalchemy import paginate
from sqlalchemy import case

from partner.models import Partner
from datetime import datetime
from sqlalchemy.ext.asyncio import AsyncEngine
from application import schemas
from database import Base


logger = logging.getLogger()


class RequestId(Base):
    __tablename__ = "requests"
    id = Column("id", Integer, primary_key=True, index=True)
    reuqestid = Column("reuqestid", String, unique=True, index=True)
    # status = Column("status", String, index=True)
    created_at = Column("created_at", DateTime, index=True, default=datetime.now())
    updated_at = Column("updated_at", DateTime, index=True, default=datetime.now())
    partner_id = Column("partner_id", Integer, ForeignKey("partners.id"))

    @staticmethod
    async def create_request_id(db: AsyncEngine, request_id: str, partner_id: int, status: str = 'new'):
        async_session = sessionmaker(db, class_=AsyncSession, expire_on_commit=False)
        async with async_session() as session:
            new_request = RequestId(
                reuqestid=request_id,
                partner_id=partner_id,
                # status = status
            )
            session.add(new_request)
            await session.commit()
            return new_request


application_clients = Table(
    "application_clients",
    Base.metadata,
    Column("application_id", Integer, ForeignKey("applications.id", ondelete="CASCADE")),
    Column("client_id", Integer, ForeignKey("clients.id", ondelete="CASCADE")),
    UniqueConstraint("application_id", "client_id", name="application_client")
)

_status_lookup = dict(pending_review=0, accepted=1, rejected=2)


class Client(Base):
    __tablename__ = "clients"
    id = Column("id", Integer, primary_key=True, index=True)
    firstname = Column("firstname", String, index=True)
    lastname = Column("lastname", String, index=True)
    patronymic = Column("patronymic", String, index=True)
    birthdate = Column("birthdate", Date, index=True)
    passport = Column("passport", String, index=True)
    issued_by = Column("issuedby", String, index=True)
    issued_date = Column("issueddate", Date, index=True)
    expired_date = Column("expireddate", Date, index=True)
    address = Column("address", String, index=True)
    gender = Column("gender", String, index=True)
    pinfl = Column("pinfl", String, index=True)
    created_at = Column("created_at", DateTime, index=True, default=datetime.now())
    updated_at = Column("updated_at", DateTime, index=True, default=datetime.now())
    applications = relationship("Application", secondary=application_clients, back_populates="clients",
                                cascade="all, delete", passive_deletes=True)


class Application(Base):
    __tablename__ = "applications"
    id = Column("id", Integer, primary_key=True, index=True)
    departure = Column("departure", String, index=True)
    country = Column("country", String, index=True)
    datefrom = Column("datefrom", Date, index=True)
    dateto = Column("dateto", Date, index=True)
    passengers = Column("passengers", Integer, index=True)
    hotel = Column("hotel", String, index=True)
    tour = Column("tour", String, index=True)
    operatorcode = Column('operatorcode', Integer, index=True)
    operatorname = Column('operatorname', String, index=True)
    tourid = Column("tourid", String, index=True)
    # client list column
    clients = relationship("Client", secondary=application_clients, back_populates="applications",
                           cascade="all, delete", passive_deletes=True)
    partner_id = Column("partner_id", Integer, ForeignKey("partners.id", ondelete="CASCADE"))
    status = Column("status", String, index=True, default='pending_review')
    partner = relationship("Partner", backref="applications")

    @hybrid_property
    def status_to_integer(self):
        return _status_lookup[self.status]

    @status_to_integer.expression
    def status_to_integer(cls):
        return case(_status_lookup, value=cls.status)

    @staticmethod
    async def get_all_applications(db: AsyncEngine):
        async_session = sessionmaker(db, class_=AsyncSession, expire_on_commit=False)
        async with async_session() as session:
            stmt = select(Application).options(
                joinedload(Application.partner),
                # joinedload(Application.clients)
            ).order_by(Application.status_to_integer, Application.id.desc())
            result = await paginate(session, stmt)
            return result
            # result = await session.execute(stmt)
            # return result.unique().scalars().all()

    @staticmethod
    async def get_application_by_id(db: AsyncEngine, application_id: int):
        async_session = sessionmaker(db, class_=AsyncSession, expire_on_commit=False)
        async with async_session() as session:
            stmt = select(Application).options(
                joinedload(Application.partner),
                joinedload(Application.clients)
            ).where(Application.id == application_id)
            result = await session.execute(stmt)
            application = result.scalars().first()
            if not application:
                raise HTTPException(status_code=400, detail="Application not found")
            return application

    @staticmethod
    async def get_application_by_partner_id(db: AsyncEngine, partner_id: int):
        async_session = sessionmaker(db, class_=AsyncSession, expire_on_commit=False)
        async with async_session() as session:
            # fetch parnter_id with application

            stmt = select(Application).options(
                joinedload(Application.partner, Application.clients)
            ).where(Application.partner_id == partner_id)
            result = await session.execute(stmt)
            application = result.scalars().all()
            if not application:
                raise HTTPException(status_code=400, detail="Application not found")
            return application


    @staticmethod
    async def update_application_status(db: AsyncEngine, application_id: int, status: str):
        async_session = sessionmaker(db, class_=AsyncSession, expire_on_commit=False)
        async with async_session() as session:
            stmt = select(Application).where(Application.id == application_id)
            result = await session.execute(stmt)
            application = result.scalars().first()
            if not application:
                raise HTTPException(status_code=400, detail="Application not found")
            application.status = status
            await session.commit()
            return application


    @staticmethod
    async def create_application(db: AsyncEngine, application: schemas.CreateApplication, partner_id: int):
        async_session = sessionmaker(db, class_=AsyncSession, expire_on_commit=False)
        async with async_session() as session:
            new_application = Application(
                departure=application.departure,
                country=application.country,
                datefrom=application.datefrom,
                dateto=application.dateto,
                passengers=application.passengers,
                hotel=application.hotel,
                tour=application.tour,
                operatorcode=application.operatorcode,
                operatorname=application.operatorname,
                tourid=application.tourid,
                partner_id=partner_id
            )
            # session.add(new_application)
            await session.flush()
            clients = []
            for client in application.clients:
                new_client = Client(
                    firstname=client.firstname,
                    lastname=client.lastname,
                    patronymic=client.patronymic,
                    birthdate=client.birthdate,
                    passport=client.passport,
                    issued_by=client.issued_by,
                    issued_date=client.issued_date,
                    expired_date=client.expired_date,
                    address=client.address,
                    gender=client.gender,
                    pinfl=client.pinfl,
                    applications=[new_application]
                )
                # new_client.applications.append(new_application)
                clients.append(new_client)
            session.add_all(clients)
            await session.flush()
            # print(clients[0].id)
            # for index in range(len(clients)):
            #     await clients[index].applications.append(new_application)

            # for index in range(len(clients)):
            #     new_application.clients.append(clients[index])
            await session.commit()
            return new_application

    @staticmethod
    async def delete_application(db: AsyncEngine, application_id: int):
        async_session = sessionmaker(db, class_=AsyncSession, expire_on_commit=False)
        async with async_session() as session:
            stmt = select(Application).where(Application.id == application_id)
            result = await session.execute(stmt)
            application = result.scalars().first()
            if not application:
                raise HTTPException(status_code=400, detail="Application not found")
            await session.delete(application)
            await session.commit()
            return application
