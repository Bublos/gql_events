from typing import Optional, List, Union, Annotated, ForwardRef
import strawberry
from dataclasses import dataclass

###########################################################################################################################
#
# zde definujte sve GQL modely
# - nove, kde mate zodpovednost
# - rozsirene, ktere existuji nekde jinde a vy jim pridavate dalsi atributy
#
###########################################################################################################################
import json
import datetime
from enum import Enum
import typing

import strawberry.types
from uoishelpers.resolvers import getLoadersFromInfo, getUserFromInfo
# from src.GraphResolvers import resolveEventsForUser
from src.GraphResolvers import create_statement_for_event_presences
from .GraphPermissions import (
    
    OnlyForAdmins,    
    # RBACPermission
)
from uoishelpers.gqlpermissions import (
    OnlyForAuthentized,
    RoleBasedPermissionForRUDOps
)

from .GraphResolvers import (
    # getLoadersFromInfo,
    
    IDType,

    resolve_reference,
    resolve_id,
    resolve_name,
    resolve_name_en,
    resolve_lastchange,
    resolve_created,
    resolve_createdby,
    resolve_changedby,

    # asPage,
    
    # encapsulateInsert,
    # encapsulateUpdate,
    # encapsulateDelete
    )


from uoishelpers.resolvers import (
    encapsulateInsert,
    encapsulateUpdate,
    encapsulateDelete
)

from uoishelpers.resolvers import (
    getLoadersFromInfo, 
    createInputs,

    InsertError, 
    Insert, 
    UpdateError, 
    Update, 
    DeleteError, 
    Delete
)

from uoishelpers.gqlpermissions import (
    RBACObjectGQLModel
)

# from src.DBResolvers import DBResolvers
from src.DBResolvers import (
    EventModelResolvers,
    EventTypeModelResolvers,
    EventCategoryModelResolvers,
    EventGroupModelResolvers,

    PresenceModelResolvers,
    PresenceTypeModelResolvers,

    InvitationTypeModelResolvers
)

from uoishelpers.resolvers import getLoadersFromInfo

GroupGQLModel = Annotated["GroupGQLModel", strawberry.lazy(".GraphTypeDefinitionsExt")]
UserGQLModel = Annotated["UserGQLModel", strawberry.lazy(".GraphTypeDefinitionsExt")]
# RBACObjectGQLModel = Annotated["RBACObjectGQLModel", strawberry.lazy(".GraphTypeDefinitionsExt")]
PresenceTypeGQLModel = Annotated["PresenceTypeGQLModel", strawberry.lazy(".GraphTypeDefinitions")]

EventInputFilter_ = Annotated["EventInputFilter", strawberry.lazy(".GraphTypeDefinitions")]
EventGQLModel_ = Annotated["EventGQLModel", strawberry.lazy(".GraphTypeDefinitions")]

# region Presence Model
@strawberry.federation.type(keys=["id"], description="""Describes a relation of an user to the event by invitation (like invited) and participation (like absent)""")
class PresenceGQLModel:
    @classmethod
    def getLoader(cls, info: strawberry.types.Info):
        # return getLoadersFromInfo(info).events_users
        return getLoadersFromInfo(info).PresenceModel

    resolve_reference = resolve_reference

    id = resolve_id
    lastchange = resolve_lastchange
    created = resolve_created
    createdby = resolve_createdby
    changedby = resolve_changedby

    @strawberry.field(
        description="""Present, Vacation etc.""",
        permission_classes=[
            OnlyForAuthentized,
            # OnlyForAuthentized
        ]
    )
    async def presence_type(self, info: strawberry.types.Info) -> Optional['PresenceTypeGQLModel']:
        result = await PresenceTypeGQLModel.resolve_reference(info, self.presencetype_id)
        return result
    
    # presence_type2 = strawberry.field(
    #     description="""Present, Vacation etc.""",
    #     permission_classes=[
    #         OnlyForAuthentized,
    #         # OnlyForAdmins
    #     ],
    #     resolver=DBResolvers.PresenceModel.presence_type(PresenceTypeGQLModel)
    # )

    @strawberry.field(description="""Invited, Accepted, etc.""",
        permission_classes=[
            OnlyForAuthentized,
            # OnlyForAdmins
        ])
    async def invitation_type(self, info: strawberry.types.Info) -> Optional['InvitationTypeGQLModel']:
        result = await InvitationTypeGQLModel.resolve_reference(info, self.invitationtype_id)
        return result

    @strawberry.field(description="""The user / participant""",
        permission_classes=[
            OnlyForAuthentized,
            # OnlyForAdmins
        ])
    async def user(self, info: strawberry.types.Info) -> Optional["UserGQLModel"]:
        from .GraphTypeDefinitionsExt import UserGQLModel
        result = await UserGQLModel.resolve_reference(info, id=self.user_id)
        return result

    @strawberry.field(description="""The event""",
        permission_classes=[
            OnlyForAuthentized,
            # OnlyForAdmins
        ])
    async def event(self, info: strawberry.types.Info) -> Optional['EventGQLModel']:
        result = await EventGQLModel.resolve_reference(info, id=self.event_id)
        return result
# endregion

# region EventType Model

@strawberry.federation.type(keys=["id"], description="""Represents an event type""")
class EventTypeGQLModel:

    @classmethod
    def getLoader(cls, info: strawberry.types.Info):
        # return getLoadersFromInfo(info).eventtypes
        return getLoadersFromInfo(info).EventTypeModel

    resolve_reference = resolve_reference

    id = resolve_id
    name = resolve_name
    name_en = resolve_name_en

    lastchange = resolve_lastchange
    created = resolve_created
    createdby = resolve_createdby
    changedby = resolve_changedby

    # @strawberry.field(
    #     description="""Related events""",
    #     permission_classes=[
    #         OnlyForAuthentized,
    #         # OnlyForAdmins
    #     ])
    # async def events(self, info: strawberry.types.Info) -> List['EventGQLModel']:
    #     loader = EventGQLModel.getLoader(info)
    #     result = await loader.filter_by(type_id=self.id)
    #     return result
# endregion

# region PresenceType Model
@strawberry.federation.type(keys=["id"], description="""Represents a type of presence (like Present)""")
class PresenceTypeGQLModel:

    @classmethod
    def getLoader(cls, info: strawberry.types.Info):
        return getLoadersFromInfo(info).eventpresencetypes

    resolve_reference = resolve_reference

    id = resolve_id
    name = resolve_name
    name_en = resolve_name_en

    lastchange = resolve_lastchange
    created = resolve_created
    createdby = resolve_createdby
    changedby = resolve_changedby

# endregion

# region InvitationType Model
@strawberry.federation.type(keys=["id"], description="""Represents if an user has been invited to the event ot whatever""")
class InvitationTypeGQLModel:

    @classmethod
    def getLoader(cls, info: strawberry.types.Info):
        return getLoadersFromInfo(info).eventinvitationtypes

    resolve_reference = resolve_reference

    id = resolve_id
    name = resolve_name
    name_en = resolve_name_en

    lastchange = resolve_lastchange
    created = resolve_created
    createdby = resolve_createdby
    changedby = resolve_changedby


# from src.GraphResolvers import resolveEventsForGroup


import datetime
# from src.GraphResolvers import (
#     resolveEventById,
#     resolveGroupsForEvent,
#     resolvePresencesForEvent
# )

# endregion

# region Event Model

@strawberry.enum(description=" TimeUnit")
class TimeUnit(Enum):
    SECONDS = "seconds"
    MINUTES = "minutes"
    HOURS = "hours"
    DAYS = "days"
    WEEKS = "weeks"

PresenceInputFilter_ = Annotated["PresenceInputFilter", strawberry.lazy(".GraphTypeDefinitions")]
@strawberry.federation.type(keys=["id"], description="""Entity representing an event (calendar item)""")
class EventGQLModel:

    @classmethod
    def getLoader(cls, info: strawberry.types.Info):
        return getLoadersFromInfo(info).events

    resolve_reference = resolve_reference

    id = resolve_id
    name = resolve_name
    name_en = resolve_name_en

    lastchange = resolve_lastchange
    created = resolve_created
    createdby = resolve_createdby
    changedby = resolve_changedby

    @strawberry.field(
        description="""Event duration, implicitly in minutes""",
        permission_classes=[
            OnlyForAuthentized,
            # OnlyForAdmins
        ])
    def duration(self, unit: TimeUnit=TimeUnit.MINUTES) -> Optional[float]:
        result = self.duration.total_seconds()
        if unit == TimeUnit.SECONDS:
            return result
        if unit == TimeUnit.MINUTES:
            return result / 60
        if unit == TimeUnit.HOURS:
            return result / 60 / 60
        if unit == TimeUnit.DAYS:
            return result / 60 / 60 / 24
        if unit == TimeUnit.WEEKS:
            return result / 60 / 60 / 24 / 7
        # raise Exception("Unknown unit for duration")
        
    @strawberry.field(
        description="""
        If teaching hour, rbacobject is group where (first) teacher belongs to
        If personal event, rbacobject is user who created event
        """,
        permission_classes=[
            OnlyForAuthentized,
            # OnlyForAdmins
        ])
    async def rbac(self, info: strawberry.types.Info) -> Optional[RBACObjectGQLModel]:
        from .GraphTypeDefinitionsExt import RBACObjectGQLModel
        return await RBACObjectGQLModel.resolve_reference(info=info, id=self.rbacobject)

    @strawberry.field(
        description="""Event description""",
        permission_classes=[
            OnlyForAuthentized,
            # OnlyForAdmins
        ])
    def description(self) -> Optional[str]:
        return self.description

    @strawberry.field(
        description="""Place""",
        permission_classes=[
            OnlyForAuthentized,
            # OnlyForAdmins
        ])
    def place(self) -> Optional[str]:
        return self.place

    @strawberry.field(
        description="""Place id""",
        permission_classes=[
            OnlyForAuthentized,
            # OnlyForAdmins
        ])
    def place_id(self) -> Optional[IDType]:
        return self.place_id

    @strawberry.field(
        description="""Date&time of event begin""",
        permission_classes=[
            OnlyForAuthentized,
            # OnlyForAdmins
        ])
    def startdate(self) -> Optional[datetime.datetime]:
        return self.startdate

    @strawberry.field(
        description="""Date&time of event end""",
        permission_classes=[
            OnlyForAuthentized,
            # OnlyForAdmins
        ])
    def enddate(self) -> Optional[datetime.datetime]:
        return self.enddate

    @strawberry.field(
        description="""Groups of users linked to the event""",
        permission_classes=[
            OnlyForAuthentized,
            # OnlyForAdmins
        ])
    async def groups(self, info: strawberry.types.Info) -> List["GroupGQLModel"]:
        from .GraphTypeDefinitionsExt import GroupGQLModel
        loader = getLoadersFromInfo(info).events_groups
        rows = await loader.filter_by(event_id=self.id)
        return map(lambda row: GroupGQLModel(id=row.group_id), rows)           

    
    @strawberry.field(
        description="""Users linked to the event""",
        permission_classes=[
            OnlyForAuthentized,
            # OnlyForAdmins
        ])
    async def users(self, info: strawberry.types.Info, where: Optional[PresenceInputFilter_]=None) -> List["UserGQLModel"]:
        wheredict = None if where is None else strawberry.asdict(where)
        from .GraphTypeDefinitionsExt import UserGQLModel
        loader = getLoadersFromInfo(info).events_users
        statement = create_statement_for_event_presences(id=self.id, where=wheredict)
        rows = await loader.execute_select(statement)
        return map(lambda row: UserGQLModel(id=row.user_id), rows)           
        pass
    # @strawberry.field(
    #     description="""Participants of the event and if they were absent or so...""",
    #     permission_classes=[
    #         OnlyForAuthentized,
    #         # OnlyForAdmins
    #     ])
    # async def presences(self, info: strawberry.types.Info) -> List["PresenceGQLModel"]:
    #     # loader = getLoadersFromInfo(info).presences
    #     loader = PresenceGQLModel.getLoader(info)
    #     result = await loader.filter_by(event_id=self.id)
    #     return result
    
    presences = strawberry.field(
        description="""Participants of the event and if they were absent or so...""",
        resolver=EventModelResolvers.Vector(
            "presences", 
            GQLModel=PresenceGQLModel,
            WhereFilterModel=PresenceInputFilter_
            ),
        permission_classes=[
            OnlyForAuthentized,
            # OnlyForAdmins
        ]        
    )

    @strawberry.field(
        description="""Type of the event""",
        permission_classes=[
            OnlyForAuthentized,
            # OnlyForAdmins
        ])
    async def event_type(self, info: strawberry.types.Info) -> Optional["EventTypeGQLModel"]:
        result = await EventTypeGQLModel.resolve_reference(info=info, id=self.type_id)
        return result

    @strawberry.field(
        description="""event which contains this event (aka semester of this lesson)""",
        permission_classes=[
            OnlyForAuthentized,
            # OnlyForAdmins
        ])
    async def master_event(self, info: strawberry.types.Info) -> Optional["EventGQLModel"]:
        result = None
        if (self.masterevent_id is not None):
            result = await EventGQLModel.resolve_reference(info=info, id=self.masterevent_id)
        return result

    # @strawberry.field(
    #     description="""""",
    #     permission_classes=[
    #         OnlyForAuthentized,
    #         # OnlyForAdmins
    #     ])
    # async def rbactest(self, info: strawberry.types.Info) -> Optional[strawberry.scalars.JSON]:
    #     # RBACPermission.getActiveRoles()
    #     result = await RBACPermission().getActiveRoles(self.rbacobject, info=info) if self.rbacobject else {}
    #     # resultstr = json.dumps(result, ensure_ascii=False, default=str)
    #     # result = json.loads(resultstr)
    #     # print(result, flush=True)
    #     return result


    # @strawberry.field(
    #     description="""events which are contained by this event (aka all lessons for the semester)""",
    #     permission_classes=[
    #         OnlyForAuthentized,
    #         # OnlyForAdmins
    #     ])
    # async def sub_events(self, info: strawberry.types.Info) -> List["EventGQLModel"]:
    #     # loader = getLoadersFromInfo(info).events
    #     loader = EventGQLModel.getLoader(info)
    #     result = await loader.filter_by(masterevent_id=self.id)
    #     return result
    
    sub_events = strawberry.field(
        description="""events which are contained by this event (aka all lessons for the semester)""",
        resolver=EventModelResolvers.Vector(
            "sub_events",
            GQLModel=EventGQLModel_,
            WhereFilterModel=EventInputFilter_
            ),
        permission_classes=[
            OnlyForAuthentized,
            # OnlyForAdmins
        ])
    

# endregion



###########################################################################################################################
#
# zde definujte resolvers pro Query model
#
###########################################################################################################################

from uoishelpers.resolvers import createInputs

# region EventType Model
@createInputs
@dataclass
class EventTypeInputFilter:
    name: str
    name_en: str

# @strawberry.field(
#     description="""Finds all types of events paged""",
#     permission_classes=[
#         OnlyForAuthentized,
#         # OnlyForAdmins
#     ]
#     )
# @asPage
# async def event_type_page(self, info: strawberry.types.Info, skip: Optional[int] = 0, limit: Optional[int] = 10, where: Optional[EventTypeInputFilter] = None) -> List["EventTypeGQLModel"]:
#     return EventTypeGQLModel.getLoader(info)

event_type_page = strawberry.field(
    description="""Finds all types of events paged""",
    resolver=EventTypeModelResolvers.Page(
        GQLModel=EventTypeGQLModel,
        WhereFilterModel=EventTypeInputFilter
    ),
    permission_classes=[
        OnlyForAuthentized,
        # OnlyForAdmins
    ]
    )

@strawberry.field(
    description="""Gets type of event by id""",
    permission_classes=[
        OnlyForAuthentized,
        # OnlyForAdmins
    ]
    )
async def event_type_by_id(self, info: strawberry.types.Info, id: IDType) -> Optional["EventTypeGQLModel"]:
    return await EventTypeGQLModel.resolve_reference(info=info, id=id)
# endregion

# region PresenceType Model
@createInputs
@dataclass
class PresenceTypeInputFilter:
    id: IDType
    name: str
    name_en: str

# @strawberry.field(
#     description="""Finds all types of presences paged""",
#     permission_classes=[
#         OnlyForAuthentized,
#         # OnlyForAdmins
#     ]
#     )
# @asPage
# async def presence_type_page(self, info: strawberry.types.Info, skip: Optional[int] = 0, limit: Optional[int] = 10, where: Optional[PresenceTypeInputFilter] = None) -> List["PresenceTypeGQLModel"]:
#     return PresenceTypeGQLModel.getLoader(info)

presence_type_page = strawberry.field(
    description="""Finds all types of presences paged""",
    resolver = PresenceTypeModelResolvers.Page(
        GQLModel=PresenceTypeGQLModel,
        WhereFilterModel=PresenceTypeInputFilter
    ),
    permission_classes=[
        OnlyForAuthentized,
        # OnlyForAdmins
    ]
    )

@strawberry.field(
    description="""Gets type of presence by id""",
    permission_classes=[
        OnlyForAuthentized,
        # OnlyForAdmins
    ]
    )
async def presence_type_by_id(self, info: strawberry.types.Info, id: IDType) -> Optional["PresenceTypeGQLModel"]:
    return await PresenceTypeGQLModel.resolve_reference(info=info, id=id)

# endregion

# region InvitationType Model
@createInputs
@dataclass
class InvitationTypeInputFilter:
    id: IDType
    name: str
    name_en: str

# @strawberry.field(
#     description="""Finds all types of invitation paged""",
#     permission_classes=[
#         OnlyForAuthentized,
#         # OnlyForAdmins
#     ]
#     )
# @asPage
# async def invitation_type_page(self, info: strawberry.types.Info, skip: Optional[int] = 0, limit: Optional[int] = 10, where: Optional[InvitationTypeInputFilter] = None) -> List["InvitationTypeGQLModel"]:
#     return InvitationTypeGQLModel.getLoader(info)

invitation_type_page = strawberry.field(
    description="""Finds all types of invitation paged""",
    resolver=InvitationTypeModelResolvers.Page(
        GQLModel=InvitationTypeGQLModel,
        WhereFilterModel=InvitationTypeInputFilter
    ),
    permission_classes=[
        OnlyForAuthentized,
        # OnlyForAdmins
    ]
    )

@strawberry.field(
    description="""Gets type of invitation by id""",
    permission_classes=[
        OnlyForAuthentized,
        # OnlyForAdmins
    ])
async def invitation_type_by_id(self, info: strawberry.types.Info, id: IDType) -> Optional["InvitationTypeGQLModel"]:
    return await InvitationTypeGQLModel.resolve_reference(info=info, id=id)
# endregion

# region Presence Model

@createInputs
@dataclass
class PresenceInputFilter:
    name: str
    name_en: str
    user_id: IDType
    presence_type: PresenceTypeInputFilter
    invitation_type: InvitationTypeInputFilter
    event: EventInputFilter_


# @strawberry.field(
#     description="""Finds all events paged""",
#     permission_classes=[
#         OnlyForAuthentized,
#         # OnlyForAdmins
#     ]
#     )
# @asPage
# async def presence_page(self, info: strawberry.types.Info, skip: Optional[int] = 0, limit: Optional[int] = 10, where: Optional[PresenceInputFilter] = None) -> List["PresenceGQLModel"]:
#     return PresenceGQLModel.getLoader(info)


presence_page = strawberry.field(
    description="""Finds all presences paged""",
    permission_classes=[
        OnlyForAuthentized,
        # OnlyForAdmins
    ],
    resolver=PresenceModelResolvers.Page(
        GQLModel=PresenceGQLModel, 
        WhereFilterModel=PresenceInputFilter)
    )

@strawberry.field(
    description="""Finds presence by id""",
    permission_classes=[
        OnlyForAuthentized,
        # OnlyForAdmins
    ]
    )
async def presence_by_id(self, info: strawberry.types.Info, id: IDType) -> Optional["PresenceGQLModel"]:
    return await PresenceGQLModel.resolve_reference(info=info, id=id)

# endregion

# region Event Model
@createInputs
@dataclass
class EventGroupInputFilter:
    group_id: IDType
   

@createInputs
@dataclass
class EventInputFilter:
    type_id: IDType
    masterevent_id: IDType
    name: str
    name_en: str
    # duration: float # SELECT Problem :(
    duration: datetime.timedelta
    startdate: datetime.datetime
    enddate: datetime.datetime
    type: EventTypeInputFilter
    presences: PresenceInputFilter
    groups: EventGroupInputFilter
    place_id: IDType
    

# @strawberry.field(
#     description="""Finds all events paged""",
#     permission_classes=[
#         OnlyForAuthentized,
#         # OnlyForAdmins
#     ]
#     )
# @asPage
# async def event_page(self, info: strawberry.types.Info, skip: Optional[int] = 0, limit: Optional[int] = 10, where: Optional[EventInputFilter] = None) -> List["EventGQLModel"]:
#     return EventGQLModel.getLoader(info)

event_page = strawberry.field(
    description="""Finds all events paged""",
    resolver=EventModelResolvers.Page(
        GQLModel=EventGQLModel,
        WhereFilterModel=EventInputFilter
    ),
    permission_classes=[
        OnlyForAuthentized,
        # OnlyForAdmins
    ]
    )

@strawberry.field(
    description="""Gets event by id""",
    permission_classes=[
        OnlyForAuthentized,
        # OnlyForAdmins
    ]
    )
async def event_by_id(self, info: strawberry.types.Info, id: IDType) -> Optional["EventGQLModel"]:
    return await EventGQLModel.resolve_reference(info=info, id=id)
# endregion
###########################################################################################################################
#
# zde definujte svuj Query model
#
###########################################################################################################################


# region Query
@strawberry.type(description="""Type for query root""")
class Query:
    event_by_id = event_by_id
    event_page = event_page

    event_presence_page = presence_page
    event_presence_by_id = presence_by_id

    event_type_by_id = event_type_by_id
    event_type_page = event_type_page

    event_presence_type_by_id = presence_type_by_id
    event_presence_type_page = presence_type_page


    event_invitation_type_by_id = invitation_type_by_id
    event_invitation_type_page = invitation_type_page


# endregion

###########################################################################################################################
#
# zde definujte resolvers pro Mutation model
#
###########################################################################################################################

from typing import Optional
# region Event
@strawberry.input(description="Datastructure for event insert")
class EventInsertGQLModel:
    name: str = strawberry.field(description="Name of the event")
    type_id: IDType = strawberry.field(description="Type ID of the event")
    id: typing.Optional[IDType] = strawberry.field(description="Primary key (UUID) of the event, can be client-generated", default=None)
    
    masterevent_id: typing.Optional[IDType] = strawberry.field(description="ID of the master event", default=None)
    place: typing.Optional[str] = strawberry.field(description="Location name of the event", default="")
    place_id: typing.Optional[IDType] = strawberry.field(description="ID of the event location", default=None)
    
    startdate: typing.Optional[datetime.datetime] = strawberry.field(
        description="Start date of the event",
        default_factory=lambda: datetime.datetime.now()
    )
    enddate: typing.Optional[datetime.datetime] = strawberry.field(
        description="End date of the event",
        default_factory=lambda: (datetime.datetime.now() + datetime.timedelta(minutes=30))
    )
    
    rbacobject_id: typing.Optional[IDType] = strawberry.field(
        description="Group ID or user ID defining access rights",
        default=None
    )
    createdby_id: strawberry.Private[IDType] = None



@strawberry.input(description="Datastructure for event update")
class EventUpdateGQLModel:
    id: IDType = strawberry.field(description="Primary key (UUID) of the event")
    lastchange: datetime.datetime = strawberry.field(description="Last change timestamp")
    
    name: typing.Optional[str] = strawberry.field(description="Name of the event", default=None)
    masterevent_id: typing.Optional[IDType] = strawberry.field(description="ID of the master event", default=None)
    type_id: typing.Optional[IDType] = strawberry.field(description="Type of the event", default=None)
    place: typing.Optional[str] = strawberry.field(description="Location name of the event", default=None)
    place_id: typing.Optional[IDType] = strawberry.field(description="ID of the event location", default=None)
    startdate: typing.Optional[datetime.datetime] = strawberry.field(description="Event start date", default=None)
    enddate: typing.Optional[datetime.datetime] = strawberry.field(description="Event end date", default=None)
    
    changedby_id: strawberry.Private[IDType] = None
    rbacobject_id: strawberry.Private[IDType] = None


@strawberry.input(description="Attributes needed for event delete")
class EventDeleteGQLModel:
    lastchange: datetime.datetime = strawberry.field(description="Timestamp of the last change")
    id: IDType = strawberry.field(description="Primary key (UUID) of the event")


    
@strawberry.type(description="""Result of event operation""")
class EventResultGQLModel:
    id: IDType = None
    msg: str = None

    @strawberry.field(description="""Result of event operation""")
    async def event(self, info: strawberry.types.Info) -> Optional[EventGQLModel]:
        result = await EventGQLModel.resolve_reference(info, self.id)
        return result


@strawberry.mutation(
    description="C operation",
    permission_classes=[
        OnlyForAuthentized,
        # OnlyForAdmins
    ]
    )

async def event_insert(
    self, info: strawberry.types.Info, event: EventInsertGQLModel) -> typing.Union[EventGQLModel, InsertError[EventGQLModel]]:
    return await Insert[EventGQLModel].DoItSafeWay(info=info, entity=event)

@strawberry.mutation(
    description="updates the event",
    permission_classes=[
        OnlyForAuthentized,
        # OnlyForAdmins
        # RoleBasedPermissionForRUDOps(roles="administrátor", GQLModel=EventGQLModel)
    ])
async def event_update(
    self, info: strawberry.types.Info, event: EventUpdateGQLModel) -> typing.Union[EventGQLModel, UpdateError[EventGQLModel]]:
    return await Update[EventGQLModel].DoItSafeWay(info=info, entity=event)

@strawberry.mutation(
    description="deletes the event",
    permission_classes=[
        OnlyForAuthentized,
        # OnlyForAdmins
    ])
async def event_delete(
    self, info: strawberry.types.Info, event: EventDeleteGQLModel) -> typing.Union[None, DeleteError[EventGQLModel]]:
    return await Delete[EventGQLModel].DoItSafeWay(info=info, entity=event)

# endregion

# region PresenceType
@strawberry.input(description="Datastructure for insert")
class PresenceInsertGQLModel:
    user_id: IDType
    event_id: IDType
    invitationtype_id: IDType
    presencetype_id: Optional[IDType] = None
    id: Optional[IDType] = None
    createdby: strawberry.Private[IDType] = None
    rbacobject: strawberry.Private[IDType] = None


@strawberry.input(description="Datastructure for update")
class PresenceUpdateGQLModel:
    id: IDType
    lastchange: datetime.datetime
    invitationtype_id: Optional[IDType] = None
    presencetype_id: Optional[IDType] = None
    changedby: strawberry.Private[IDType] = None
    rbacobject: strawberry.Private[IDType] = None

@strawberry.input(description="Datastructure for delete")
class PresenceDeleteGQLModel:
    id: IDType
    lastchange: datetime.datetime
    
@strawberry.type(description="""Result of user operation""")
class PresenceResultGQLModel:
    id: IDType = None
    msg: str = None

    @strawberry.field(description="""Result of presence operation""")
    async def presence(self, info: strawberry.types.Info) -> Union[PresenceGQLModel, None]:
        result = await PresenceGQLModel.resolve_reference(info, self.id)
        return result

@strawberry.mutation(
    description="creates new presence",
    permission_classes=[
        OnlyForAuthentized,
        # OnlyForAdmins
    ])
async def presence_insert(
    self, info: strawberry.types.Info, presence: PresenceInsertGQLModel
) -> typing.Union[PresenceGQLModel, InsertError[PresenceGQLModel]]:
    return await Insert[PresenceGQLModel].DoItSafeWay(info=info, entity=presence)


@strawberry.mutation(
    description="updates the presence",
    permission_classes=[
        OnlyForAuthentized,
        # OnlyForAdmins
    ])
async def presence_update(
    self, info: strawberry.types.Info, presence: PresenceUpdateGQLModel
) -> typing.Union[PresenceGQLModel, UpdateError[PresenceGQLModel]]:
    return await Update[PresenceGQLModel].DoItSafeWay(info=info, entity=presence)


@strawberry.mutation(
    description="deletes the presence",
    permission_classes=[
        OnlyForAuthentized,
        # OnlyForAdmins
    ])
# async def presence_delete(self, info: strawberry.types.Info, id: IDType) -> PresenceResultGQLModel:
#     return await encapsulateDelete(info, PresenceGQLModel.getLoader(info), id, PresenceResultGQLModel(id=None, msg="ok"))

async def presence_delete(
    self, info: strawberry.types.Info, presence: PresenceDeleteGQLModel
) -> typing.Optional[DeleteError[PresenceGQLModel]]:
    return await Delete[PresenceGQLModel].DoItSafeWay(info=info, entity=presence)


# endregion

# region EventType
@strawberry.input(description="First datastructure for event type creation")
class EventTypeInsertGQLModel:
    name: str = strawberry.field(description="Name of the event type")
    name_en: typing.Optional[str] = strawberry.field(description="English name of the event type", default=None)
    id: typing.Optional[IDType] = strawberry.field(description="Primary key (UUID) of the event type, can be client-generated", default=None)
    createdby_id: strawberry.Private[IDType] = None
    rbacobject_id: typing.Optional[IDType] = strawberry.field(
        description="Group ID or user ID defining access rights",
        default=None
    )



@strawberry.input(description="Datastructure for updating an event type")
class EventTypeUpdateGQLModel:
    id: IDType = strawberry.field(description="Primary key (UUID) of the event type")
    lastchange: datetime.datetime = strawberry.field(description="Timestamp of the last modification")
    name: typing.Optional[str] = strawberry.field(description="Name of the event type", default=None)
    name_en: typing.Optional[str] = strawberry.field(description="English name of the event type", default=None)
    changedby_id: strawberry.Private[IDType] = None
    rbacobject_id: strawberry.Private[IDType] = None


@strawberry.type(description="""Result of event type operation""")
class EventTypeResultGQLModel:
    id: IDType = None
    msg: str = None

    @strawberry.field(description="""Event type""")
    async def event_type(self, info: strawberry.types.Info) -> Optional[EventTypeGQLModel]:
        result = await EventTypeGQLModel.resolve_reference(info, self.id)
        return result
    
@strawberry.mutation(
    description="creates new event type",
    permission_classes=[
        OnlyForAuthentized,
        # OnlyForAdmins
    ])

async def event_type_insert(
    self, info: strawberry.types.Info, event_type: EventTypeInsertGQLModel
) -> typing.Union[EventTypeGQLModel, InsertError[EventTypeGQLModel]]:
    return await Insert[EventTypeGQLModel].DoItSafeWay(info=info, entity=event_type)


@strawberry.mutation(
    description="updates the event type",
    permission_classes=[
        OnlyForAuthentized,
        # OnlyForAdmins
    ])
async def event_type_update(
    self, info: strawberry.types.Info, event_type: EventTypeUpdateGQLModel
) -> typing.Union[EventTypeGQLModel, UpdateError[EventTypeGQLModel]]:
    return await Update[EventTypeGQLModel].DoItSafeWay(info=info, entity=event_type)


@strawberry.mutation(
    description="deletes the event type",
    permission_classes=[
        OnlyForAuthentized,
        # OnlyForAdmins
    ])

async def event_type_delete(
    self, info: strawberry.types.Info, event_type: EventDeleteGQLModel
) -> typing.Union[None, DeleteError[EventTypeGQLModel]]:
    return await Delete[EventTypeGQLModel].DoItSafeWay(info=info, entity=event_type)


# endregion

# region PresenceType
@strawberry.input(description="First datastructure for event type creation")
class PresenceTypeInsertGQLModel:
    name: str
    name_en: str
    id: Optional[IDType] = None
    createdby: strawberry.Private[IDType] = None
    rbacobject: strawberry.Private[IDType] = None

@strawberry.input(description="Datastructure for event type update")
class PresenceTypeUpdateGQLModel:
    id: IDType
    lastchange: datetime.datetime
    name: Optional[str] = None
    name_en: Optional[str] = None
    changedby: strawberry.Private[IDType] = None
    rbacobject: strawberry.Private[IDType] = None

@strawberry.input(description="Datastructure for event type delete")
class PresenceTypeDeleteGQLModel:
    id: IDType
    lastchange: datetime.datetime

@strawberry.type(description="""Result of event type operation""")
class PresenceTypeResultGQLModel:
    id: IDType = None
    msg: str = None

    @strawberry.field(description="""Presence type""")
    async def presence_type(self, info: strawberry.types.Info) -> Optional[PresenceTypeGQLModel]:
        result = await PresenceTypeGQLModel.resolve_reference(info, self.id)
        return result
    
@strawberry.mutation(
    description="creates new presence type",
    permission_classes=[
        OnlyForAuthentized,
        OnlyForAdmins
    ])
async def presence_type_insert(
    self, info: strawberry.types.Info, presence_type: PresenceTypeInsertGQLModel
) -> typing.Union[PresenceTypeGQLModel, InsertError[PresenceTypeGQLModel]]:
    return await Insert[PresenceTypeGQLModel].DoItSafeWay(info=info, entity=presence_type)


@strawberry.mutation(
    description="updates the presence type",
    permission_classes=[
        OnlyForAuthentized,
        OnlyForAdmins
    ])
async def presence_type_update(
    self, info: strawberry.types.Info, presence_type: PresenceTypeUpdateGQLModel
) -> typing.Union[PresenceTypeGQLModel, UpdateError[PresenceTypeGQLModel]]:
    return await Update[PresenceTypeGQLModel].DoItSafeWay(info=info, entity=presence_type)


@strawberry.mutation(
    description="deletes the presence type",
    permission_classes=[
        OnlyForAuthentized,
        OnlyForAdmins
    ])
async def presence_type_delete(
    self, info: strawberry.types.Info, presence_type: PresenceTypeDeleteGQLModel
) -> typing.Union[None, DeleteError[PresenceTypeGQLModel]]:
    return await Delete[PresenceTypeGQLModel].DoItSafeWay(info=info, entity=presence_type)


# endregion

# region InvitationType
@strawberry.input(description="First datastructure for invitation type creation")
class InvitationTypeInsertGQLModel:
    name: str
    name_en: Optional[str] = None
    id: Optional[IDType] = None
    createdby: strawberry.Private[IDType] = None
    rbacobject: Optional[IDType] = \
        strawberry.field(description="group_id or user_id defines access rights", default=None)


@strawberry.input(description="Datastructure for invitation type update")
class InvitationTypeUpdateGQLModel:
    id: IDType
    lastchange: datetime.datetime
    name: Optional[str] = None
    name_en: Optional[str] = None
    changedby: strawberry.Private[IDType] = None
    rbacobject: strawberry.Private[IDType] = None

@strawberry.input(description="Datastructure for invitation type delete")
class InvitationTypeDeleteGQLModel:
    id: IDType
    lastchange: datetime.datetime

@strawberry.type(description="""Result of event type operation""")
class InvitationTypeResultGQLModel:
    id: IDType = None
    msg: str = None

    @strawberry.field(description="""Presence type""")
    async def invitation_type(self, info: strawberry.types.Info) -> Optional[InvitationTypeGQLModel]:
        result = await InvitationTypeGQLModel.resolve_reference(info, self.id)
        return result
    
@strawberry.mutation(
    description="creates new invitation type",
    permission_classes=[
        OnlyForAuthentized,
        OnlyForAdmins
    ])
async def invitation_type_insert(
    self, info: strawberry.types.Info, invitation_type: InvitationTypeInsertGQLModel
) -> typing.Union[InvitationTypeGQLModel, InsertError[InvitationTypeGQLModel]]:
    return await Insert[InvitationTypeGQLModel].DoItSafeWay(info=info, entity=invitation_type)


@strawberry.mutation(
    description="updates the invitation type",
    permission_classes=[
        OnlyForAuthentized,
        OnlyForAdmins
    ])
async def invitation_type_update(
    self, info: strawberry.types.Info, invitation_type: InvitationTypeUpdateGQLModel
) -> typing.Union[InvitationTypeGQLModel, UpdateError[InvitationTypeGQLModel]]:
    return await Update[InvitationTypeGQLModel].DoItSafeWay(info=info, entity=invitation_type)


@strawberry.mutation(
    description="deletes the invitation type",
    permission_classes=[
        OnlyForAuthentized,
        OnlyForAdmins
    ])
async def invitation_type_delete(
    self, info: strawberry.types.Info, invitation_type: InvitationTypeDeleteGQLModel
) -> typing.Union[None, DeleteError[InvitationTypeGQLModel]]:
    return await Delete[InvitationTypeGQLModel].DoItSafeWay(info=info, entity=invitation_type)


# endregion

# region Event User

@strawberry.input(description="First datastructure for invitation type creation")
class EventUserInsertGQLModel:
    event_id: IDType
    user_id: IDType
    invitationtype_id: IDType
    id: Optional[IDType] = None
    presencetype_id: Optional[IDType] = None
    createdby: strawberry.Private[IDType] = None
    rbacobject: strawberry.Private[IDType] = None

@strawberry.input(description="Datastructure for invitation type update")
class EventUserUpdateGQLModel:
    id: IDType
    lastchange: datetime.datetime
    invitationtype_id: Optional[IDType] = None
    presencetype_id: Optional[IDType] = None
    changedby: strawberry.Private[IDType] = None
    rbacobject: strawberry.Private[IDType] = None


@strawberry.input(description="Datastructure for invitation type update")
class EventUserDeleteGQLModel:
    event_id: IDType
    user_id: IDType
    lastchange: datetime.datetime

@strawberry.mutation(
    description="creates new event user",
    permission_classes=[
        OnlyForAuthentized,
        # OnlyForAdmins
    ])
async def event_user_insert(
    self, info: strawberry.types.Info, event_user: EventUserInsertGQLModel
) -> typing.Union[PresenceGQLModel, InsertError[PresenceGQLModel]]:
    return await Insert[PresenceGQLModel].DoItSafeWay(info=info, entity=event_user)


@strawberry.mutation(
    description="updates event user",
    permission_classes=[
        OnlyForAuthentized,
        # OnlyForAdmins
    ])
async def event_user_update(
    self, info: strawberry.types.Info, event_user: EventUserUpdateGQLModel
) -> typing.Union[PresenceGQLModel, UpdateError[PresenceGQLModel]]:
    return await Update[PresenceGQLModel].DoItSafeWay(info=info, entity=event_user)


# @strawberry.mutation(
#     description="deletes presence",
#     permission_classes=[
#         OnlyForAuthentized,
#         # OnlyForAdmins
#     ])
# async def event_user_delete(self, info: strawberry.types.Info, event_user: EventUserDeleteGQLModel) -> EventResultGQLModel:
#     loader = PresenceGQLModel.getLoader(info)
#     rows = await loader.filter_by(event_id=event_user.event_id, user_id=event_user.user_id)
#     row = next(rows, None)
#     result = EventResultGQLModel(id=event_user.event_id, msg="ok")
#     result.msg = "ok" if row is not None else "fail"
#     if row is not None:
#         await loader.delete(row.id)
#     return result

@strawberry.mutation(
    description="deletes event user",
    permission_classes=[
        OnlyForAuthentized,
        # OnlyForAdmins
    ])
async def event_user_delete(
    self, info: strawberry.types.Info, event_user: EventUserDeleteGQLModel
) -> typing.Optional[DeleteError[PresenceGQLModel]]:
    return await Delete[PresenceGQLModel].DoItSafeWay(info=info, entity=event_user)

# async def event_user_delete(
#     self, info: strawberry.types.Info, event_user: EventUserDeleteGQLModel
# ) -> typing.Union[None, DeleteError[PresenceGQLModel]]:
#     loader = PresenceGQLModel.getLoader(info)
#     rows = await loader.filter_by(event_id=event_user.event_id, user_id=event_user.user_id)
#     row = next(rows, None)

#     if row is None:
#         return None  # Or return DeleteError[PresenceGQLModel]("Entity not found")

#     return await Delete[PresenceGQLModel].DoItSafeWay(info=info, entity=row)




# endregion

# region Event Group

@strawberry.input(description="First datastructure for invitation type creation")
class EventGroupInputGQLModel:
    id: Optional[IDType] = None
    event_id: IDType
    group_id: IDType
    createdby: strawberry.Private[IDType] = None
    rbacobject: strawberry.Private[IDType] = None


@strawberry.input(description="Datastructure for invitation type update")
class EventGroupDeleteGQLModel:
    # id: IDType
    event_id: IDType
    group_id: IDType
    createdby: strawberry.Private[IDType] = None
    rbacobject: strawberry.Private[IDType] = None

# @strawberry.mutation(
#     description="creates new presence type",
#     permission_classes=[
#         OnlyForAuthentized,
#         # OnlyForAdmins
#     ])
# async def event_group_insert(self, info: strawberry.types.Info, event_group: EventGroupInputGQLModel) -> EventResultGQLModel:
#     loader = getLoadersFromInfo(info).events_groups
#     rows = await loader.filter_by(event_id=event_group.event_id, group_id=event_group.group_id)
#     row = next(rows, None)
#     result = EventResultGQLModel(id=event_group.event_id, msg="ok")
#     result.msg = "ok" if row is None else "fail"
#     if row is None:
#         await loader.insert(event_group)
#     return result

@strawberry.mutation(
    description="inserts event group to event",
    permission_classes=[
        OnlyForAuthentized,
        # OnlyForAdmins
    ])
async def event_group_insert(
    self, info: strawberry.types.Info, event_group: EventGroupInputGQLModel
) -> typing.Union[EventGQLModel, UpdateError[EventGQLModel]]:
    loader = getLoadersFromInfo(info).events_groups
    rows = await loader.filter_by(event_id=event_group.event_id, group_id=event_group.group_id)
    row = next(rows, None)
    event_entity = await EventGQLModel.resolve_reference(info, event_group.event_id)
    if row is not None:
        return UpdateError[EventGQLModel](msg="fail", _entity=event_entity, _input=event_group)  # Prevent duplicate entries

    return event_entity


# @strawberry.mutation(
#     description="creates new presence type",
#     permission_classes=[
#         OnlyForAuthentized,
#         # OnlyForAdmins
#     ])
# async def event_group_delete(self, info: strawberry.types.Info, event_group: EventGroupInputGQLModel) -> EventResultGQLModel:
#     loader = getLoadersFromInfo(info).events_groups
#     rows = await loader.filter_by(event_id=event_group.event_id, group_id=event_group.group_id)
#     row = next(rows, None)
#     result = EventResultGQLModel(id=event_group.event_id, msg="ok")
#     result.msg = "ok" if row is not None else "fail"
#     if row is not None:
#         await loader.delete(row.id)
#     return result

@strawberry.mutation(
    description="deleetes event group from event",
    permission_classes=[
        OnlyForAuthentized,
        # OnlyForAdmins
    ])
async def event_group_delete(self, info: strawberry.types.Info, event_group: EventGroupInputGQLModel) -> typing.Union[EventGQLModel, UpdateError[EventGQLModel]]:
    loader = getLoadersFromInfo(info).events_groups
    rows = await loader.filter_by(event_id=event_group.event_id, group_id=event_group.group_id)
    row = next(rows, None)
    event_entity = await EventGQLModel.resolve_reference(info, event_group.event_id)
    if row is None:
        return UpdateError[EventGQLModel](msg="fail", _entity=event_entity, _input=event_group)
    await loader.delete(row.id)
    return event_entity


# endregion
###########################################################################################################################
#
# zde definujte Mutation model
#
###########################################################################################################################

# region Mutation
@strawberry.federation.type(extend=True)
class Mutation:
    event_insert = event_insert
    event_update = event_update
    event_delete = event_delete

    event_presence_insert = presence_insert
    event_presence_update = presence_update
    event_presence_delete = presence_delete

    event_type_insert = event_type_insert
    event_type_update = event_type_update
    event_type_delete = event_type_delete

    event_presence_type_insert = presence_type_insert
    event_presence_type_update = presence_type_update
    event_presence_type_delete = presence_type_delete

    event_invitation_type_insert = invitation_type_insert
    event_invitation_type_update = invitation_type_update
    event_invitation_type_delete = invitation_type_delete

    event_user_insert = event_user_insert
    # event_user_delete = event_user_delete
    event_user_update = event_user_update

    event_group_insert = event_group_insert
    event_group_delete = event_group_delete
    # pass

# endregion    

###########################################################################################################################
# 
# Custom scalar
# https://strawberry.rocks/docs/types/scalars#custom-scalars
# 
###########################################################################################################################

timedelta = strawberry.scalar(
    # NewType("TimeDelta", float),
    datetime.timedelta,
    name="timedelta",
    serialize=lambda v: v.total_seconds() / 60,
    parse_value=lambda v: datetime.timedelta(minutes=v),
)

###########################################################################################################################
#
# Schema je pouzito v main.py, vsimnete si parametru types, obsahuje vyjmenovane modely. Bez explicitniho vyjmenovani
# se ve schema objevi jen ty struktury, ktere si strawberry dokaze odvodit z Query. Protoze v teto konkretni implementaci
# nektere modely nejsou s Query propojene je potreba je explicitne vyjmenovat. Jinak ve federativnim schematu nebude
# dostupne rozsireni, ktere tento prvek federace implementuje.
#
###########################################################################################################################


from strawberry.extensions import SchemaExtension
from starlette.requests import Request
# import inspect
import aiohttp
import os
import asyncio

myquery = """
{
  me {
    id
    fullname
    email
    roles {
      group { id name }
      roletype { id name }
    }
  }
}"""

apolloQuery = "query __ApolloGetServiceDefinition__ { _service { sdl } }"
graphiQLQuery = "\n    query IntrospectionQuery {\n      __schema {\n        \n        queryType { name }\n        mutationType { name }\n        subscriptionType { name }\n        types {\n          ...FullType\n        }\n        directives {\n          name\n          description\n          \n          locations\n          args(includeDeprecated: true) {\n            ...InputValue\n          }\n        }\n      }\n    }\n\n    fragment FullType on __Type {\n      kind\n      name\n      description\n      \n      fields(includeDeprecated: true) {\n        name\n        description\n        args(includeDeprecated: true) {\n          ...InputValue\n        }\n        type {\n          ...TypeRef\n        }\n        isDeprecated\n        deprecationReason\n      }\n      inputFields(includeDeprecated: true) {\n        ...InputValue\n      }\n      interfaces {\n        ...TypeRef\n      }\n      enumValues(includeDeprecated: true) {\n        name\n        description\n        isDeprecated\n        deprecationReason\n      }\n      possibleTypes {\n        ...TypeRef\n      }\n    }\n\n    fragment InputValue on __InputValue {\n      name\n      description\n      type { ...TypeRef }\n      defaultValue\n      isDeprecated\n      deprecationReason\n    }\n\n    fragment TypeRef on __Type {\n      kind\n      name\n      ofType {\n        kind\n        name\n        ofType {\n          kind\n          name\n          ofType {\n            kind\n            name\n            ofType {\n              kind\n              name\n              ofType {\n                kind\n                name\n                ofType {\n                  kind\n                  name\n                  ofType {\n                    kind\n                    name\n                  }\n                }\n              }\n            }\n          }\n        }\n      }\n    }\n  "

class WhoAmIExtension(SchemaExtension):

    def getJWT(self):
        request: Request = self.execution_context.context["request"]
        cookies = request.cookies
        headers = request.headers
        jwtsource = cookies.get("authorization", None)
        if jwtsource is None:
            jwtsource = headers.get("Authorization", None)
            if jwtsource is not None:
                [_, jwtsource] = jwtsource.split("Bearer ")
            else:
                #unathorized
                pass
        return jwtsource
    
    async def ug_query(self, query, variables={}):
        ug_end_point = getattr(type(self), "GQLUG_ENDPOINT_URL", None)
        if ug_end_point is None:
            ug_end_point = os.environ.get("GQLUG_ENDPOINT_URL", None)
            setattr(type(self), "GQLUG_ENDPOINT_URL", ug_end_point)
            assert ug_end_point is not None, "missing explicit configuration, 'GQLUG_ENDPOINT_URL'"

        token = self.getJWT()
        cookies = {'authorization': token}        
        print(f"cookies {cookies}", flush=True)
        payload = {"query": query, "variables": variables}
        async with aiohttp.ClientSession(cookies=cookies) as session:
            async with session.post(ug_end_point, json=payload) as resp:
                responsetxt = await resp.text()
                assert resp.status == 200, f"{ug_end_point} bad status during query {query} \n{resp} / {responsetxt}"
                response = await resp.json()
                return response

    async def on_execute(self):
        query = self.execution_context.query
        if query not in [apolloQuery, graphiQLQuery]:
            whoami = await self.ug_query(query=myquery)
            whoami = whoami["data"]["me"]
            self.execution_context.context["user"] = whoami
        else:
            whoami = {}

        print("->on_execute", self.execution_context.query, flush=True)
        yield
        print("on_execute->", whoami, flush=True)

    async def resolve(self, _next, root, info: strawberry.Info, *args, **kwargs):
        # print(f"MEx {info.field_name}({', '.join(key+'='+str(value) for key, value in kwargs.items())})", flush=True)
        # print(f"MEx {info.root_value}, {info}")
        if root is not None:
            # print(f"MEx {self}, {type(root._data).__name__}(id={root._data.id}).{info.field_name}")
            # print(f"MEx {getUserFromInfo(info)}")
            print(f"IN {info.field_name}")
            await asyncio.sleep(0)
            pass
        else:
            # print(f"Mex {self}, {root}.{info.field_name}")
            pass
        result = _next(root, info, *args, **kwargs)
        if info.is_awaitable(result):
            result = await result
        # print(f"Mex {info} -> {result}")
        print(f"OUT {info.field_name}")
        return result



from .GraphTypeDefinitionsExt import UserGQLModel, GroupGQLModel
schema = strawberry.federation.Schema(
    Query, 
    types=(UserGQLModel, GroupGQLModel), 
    mutation=Mutation,
    scalar_overrides={datetime.timedelta: timedelta._scalar_definition},
    extensions=[]
    )

schema.extensions.append(WhoAmIExtension)

#schema = strawberry.federation.Schema(Query, types=(UserGQLModel,))
