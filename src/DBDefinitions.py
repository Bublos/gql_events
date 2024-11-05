from email.policy import default
import sqlalchemy
import datetime
import uuid

from sqlalchemy import (
    Column,
    String,
    BigInteger,
    Integer,
    DateTime,
    ForeignKey,
    Sequence,
    Table,
    Boolean,
)
from sqlalchemy.ext.hybrid import hybrid_property
# from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship
from sqlalchemy.orm import declarative_base
from .UUID import UUIDColumn, UUIDFKey
BaseModel = declarative_base()


# id = Column(UUID(as_uuid=True), primary_key=True, server_default=sqlalchemy.text("uuid_generate_v4()"),)

###########################################################################################################################
#
###########################################################################################################################


###########################################################################################################################
#
# zde definujte sve SQLAlchemy modely
# je-li treba, muzete definovat modely obsahujici jen id polozku, na ktere se budete odkazovat
#
###########################################################################################################################
class EventModel(BaseModel):
    __tablename__ = "events"

    id = UUIDColumn()
    name = Column(String, comment="Name of the event")
    name_en = Column(String, comment = "Name of the event")
    description = Column(String, comment="Description of the event")
    startdate = Column(DateTime, comment = "Start date and time of the event")
    enddate = Column(DateTime, comment = "End date and time of the event")
    
    place = Column(String, comment="Place of the event")
    place_id = UUIDFKey(nullable=True)

    @hybrid_property
    def duration(self):
        return (self.enddate - self.startdate)#.total_seconds() / 60
    
    created = Column(DateTime, server_default=sqlalchemy.sql.func.now(), comment="Date and time of creation of the event")
    lastchange = Column(DateTime, server_default=sqlalchemy.sql.func.now(), comment="Date and time of last change of the event")
    createdby = UUIDFKey(nullable=True)#Column(ForeignKey("users.id"), index=True, nullable=True)
    changedby = UUIDFKey(nullable=True)#Column(ForeignKey("users.id"), index=True, nullable=True)
    rbacobject = UUIDFKey(nullable=True, comment="id rbacobject")#Column(ForeignKey("users.id"), index=True, nullable=True)

    masterevent_id = Column(ForeignKey("events.id"), index=True, nullable=True, comment="id of the master event")
    type_id = Column(ForeignKey("eventtypes.id"), index=True, comment="id of the event type")
    # type = relationship("EventTypeModel", back_populates="events")
    type = relationship("EventTypeModel", viewonly=True)
    presences = relationship("PresenceModel", viewonly=True)
    sub_events = relationship("EventModel", viewonly=True, uselist=True)
    master_event = relationship("EventModel", viewonly=True, uselist=False)

    groups = relationship("EventGroupModel", viewonly=True, uselist=True)

class EventTypeModel(BaseModel):
    __tablename__ = "eventtypes"

    id = UUIDColumn()
    name = Column(String, comment="Name of the event type")
    name_en = Column(String, comment="Name of the event type")

    category_id = Column(ForeignKey("eventcategories.id"), index=True, comment="id of the event category")

    created = Column(DateTime, server_default=sqlalchemy.sql.func.now(), comment="Date and time of creation of the event type")
    lastchange = Column(DateTime, server_default=sqlalchemy.sql.func.now(), comment="Date and time of last change of the event type")
    createdby = UUIDFKey(nullable=True)#Column(ForeignKey("users.id"), index=True, nullable=True)
    changedby = UUIDFKey(nullable=True)#Column(ForeignKey("users.id"), index=True, nullable=True)
    rbacobject = UUIDFKey(nullable=True, comment="id rbacobject")#Column(ForeignKey("users.id"), index=True, nullable=True)

    events = relationship("EventModel", back_populates="type")  

class EventCategoryModel(BaseModel):
    __tablename__ = "eventcategories"

    id = UUIDColumn()
    name = Column(String, comment="Name of the event category")
    name_en = Column(String, comment="Name of the event category")

    created = Column(DateTime, server_default=sqlalchemy.sql.func.now(), comment="Date and time of creation of the event category")
    lastchange = Column(DateTime, server_default=sqlalchemy.sql.func.now(), comment="Date and time of last change of the event category")
    createdby = UUIDFKey(nullable=True)#Column(ForeignKey("users.id"), index=True, nullable=True)
    changedby = UUIDFKey(nullable=True)#Column(ForeignKey("users.id"), index=True, nullable=True)
    rbacobject = UUIDFKey(nullable=True, comment="id rbacobject")#Column(ForeignKey("users.id"), index=True, nullable=True)

    eventtypes = relationship("EventTypeModel", viewonly=True)

class EventGroupModel(BaseModel):
    __tablename__ = "events_groups"
    id = UUIDColumn()
    event_id = Column(ForeignKey("events.id"), index=True, comment="id of the event")
    group_id = UUIDFKey()#Column(ForeignKey("groups.id"), index=True)

    created = Column(DateTime, server_default=sqlalchemy.sql.func.now(), comment="Date and time of creation of the event group")
    lastchange = Column(DateTime, server_default=sqlalchemy.sql.func.now(), comment="Date and time of last change of the event group")
    createdby = UUIDFKey(nullable=True)#Column(ForeignKey("users.id"), index=True, nullable=True)
    changedby = UUIDFKey(nullable=True)#Column(ForeignKey("users.id"), index=True, nullable=True)
    rbacobject = UUIDFKey(nullable=True, comment="id rbacobject")#Column(ForeignKey("users.id"), index=True, nullable=True)

    event = relationship("EventModel")
    #group = relationship("GroupModel")

##########################################################
#
# Zmena
#
##########################################################
class PresenceModel(BaseModel):
    __tablename__ = "events_users"
    id = UUIDColumn()

    event_id = Column(ForeignKey("events.id"), index=True, comment="id of the event")
    user_id = UUIDFKey()#Column(ForeignKey("users.id"), index=True)
    
    invitationtype_id = Column(ForeignKey("eventinvitationtypes.id"), index=True, comment= "id of the invitation type")
    presencetype_id = Column(ForeignKey("eventpresencetypes.id"), index=True, nullable=True, comment="id of the presence type")

    created = Column(DateTime, server_default=sqlalchemy.sql.func.now(), comment="Date and time of creation of the presence")
    lastchange = Column(DateTime, server_default=sqlalchemy.sql.func.now(), comment="Date and time of last change of the presence")
    createdby = UUIDFKey(nullable=True)#Column(ForeignKey("users.id"), index=True, nullable=True)
    changedby = UUIDFKey(nullable=True)#Column(ForeignKey("users.id"), index=True, nullable=True)
    rbacobject = UUIDFKey(nullable=True, comment="id rbacobject")#Column(ForeignKey("users.id"), index=True, nullable=True)

    presence_type = relationship("PresenceTypeModel", viewonly=True)
    invitation_type = relationship("InvitationTypeModel", viewonly=True)
    event = relationship("EventModel", viewonly=True)

class PresenceTypeModel(BaseModel):
    __tablename__ = "eventpresencetypes"
    id = UUIDColumn()

    name = Column(String, comment="Name of the presence type")
    name_en = Column(String, comment="Name of the presence type")
    # present, vacantion, ...

    created = Column(DateTime, server_default=sqlalchemy.sql.func.now(), comment="Date and time of creation of the presence type")
    lastchange = Column(DateTime, server_default=sqlalchemy.sql.func.now(), comment="Date and time of last change of the presence type")
    createdby = UUIDFKey(nullable=True)#Column(ForeignKey("users.id"), index=True, nullable=True)
    changedby = UUIDFKey(nullable=True)#Column(ForeignKey("users.id"), index=True, nullable=True)
    rbacobject = UUIDFKey(nullable=True, comment="id rbacobject")#Column(ForeignKey("users.id"), index=True, nullable=True)

class InvitationTypeModel(BaseModel):
    __tablename__ = "eventinvitationtypes"
    id = UUIDColumn()

    name = Column(String, comment="Name of the invitation type")
    name_en = Column(String, comment="Name of the invitation type")
    # initiator, invited mandatory, invited voluntary, accepted, tentatively accepted, rejected,

    created = Column(DateTime, server_default=sqlalchemy.sql.func.now(), comment="Date and time of creation of the invitation type")
    lastchange = Column(DateTime, server_default=sqlalchemy.sql.func.now(), comment="Date and time of last change of the invitation type")
    createdby = UUIDFKey(nullable=True)#Column(ForeignKey("users.id"), index=True, nullable=True)
    changedby = UUIDFKey(nullable=True)#Column(ForeignKey("users.id"), index=True, nullable=True)
    rbacobject = UUIDFKey(nullable=True, comment="id rbacobject")#Column(ForeignKey("users.id"), index=True, nullable=True)

##########################################################
#
# Zmena konec
#
##########################################################

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.ext.asyncio import create_async_engine


async def startEngine(connectionstring, makeDrop=False, makeUp=True):
    """Provede nezbytne ukony a vrati asynchronni SessionMaker"""
    asyncEngine = create_async_engine(connectionstring)

    async with asyncEngine.begin() as conn:
        if makeDrop:
            await conn.run_sync(BaseModel.metadata.drop_all)
            print("BaseModel.metadata.drop_all finished")
        if makeUp:
            try:
                await conn.run_sync(BaseModel.metadata.create_all)
                print("BaseModel.metadata.create_all finished")
            except sqlalchemy.exc.NoReferencedTableError as e:
                print(e)
                print("Unable automaticaly create tables")
                return None

    async_sessionMaker = sessionmaker(
        asyncEngine, expire_on_commit=False, class_=AsyncSession
    )
    return async_sessionMaker


import os


def ComposeConnectionString():
    """Odvozuje connectionString z promennych prostredi (nebo z Docker Envs, coz je fakticky totez).
    Lze predelat na napr. konfiguracni file.
    """
    user = os.environ.get("POSTGRES_USER", "postgres")
    password = os.environ.get("POSTGRES_PASSWORD", "example")
    database = os.environ.get("POSTGRES_DB", "data")
    hostWithPort = os.environ.get("POSTGRES_HOST", "host.docker.internal:5432")

    driver = "postgresql+asyncpg"  # "postgresql+psycopg2"
    connectionstring = f"{driver}://{user}:{password}@{hostWithPort}/{database}"
    connectionstring = os.environ.get("CONNECTION_STRING", connectionstring)

    return connectionstring
