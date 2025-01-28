import pytest
import logging
import uuid
import sqlalchemy
import json
import datetime


myquery = """
{
  me {
    id
    fullname
    email
    roles {
      valid
      group { id name }
      roletype { id name }
    }
  }
}"""

@pytest.mark.asyncio
async def test_result_test(NoRole_UG_Server):
    # response = {}
    response = await NoRole_UG_Server(query=myquery, variables={})
    
    print("response", response, flush=True)
    logging.info(f"response {response}")
    pass

from .gt_utils import (
    getQuery,

    createByIdTest2, 
    createUpdateTest2, 
    createTest2, 
    createDeleteTest2
)

test_event_by_id = createByIdTest2(tableName="events")
test_event_coverage = createByIdTest2(tableName="events", queryName="coverage")
test_event_update = createUpdateTest2(tableName="events", variables={"name": "newname"})
test_event_create = createTest2(
    tableName="events", 
    queryName="create", 
    variables={
        "name": "newname",
        "type_id": "a517c2fd-8dc7-4a2e-a107-cbdb88ba2aa5",
    })
test_event_delete = createDeleteTest2(
    tableName="events", 
    variables={
        "id": "18375c23-767c-4c1e-adb6-9b2beb463534", 
        "name": "newname",
        "type_id": "a517c2fd-8dc7-4a2e-a107-cbdb88ba2aa5",
        }
    )

test_event_type_by_id = createByIdTest2(tableName="eventtypes")
# test_event_type_page = createTest2(tableName="eventtypes", queryName="readp")
test_event_type_create = createTest2(tableName="eventtypes", queryName="create", variables={"name": "newname"})
test_event_type_update = createUpdateTest2(tableName="eventtypes", variables={"name": "newname"})
test_event_type_delete = createDeleteTest2(tableName="eventtypes", variables={"name": "newname"})
test_event_user_update = createUpdateTest2(
    tableName="events_users", 
    variables={
        "id": "63145c51-7772-4621-8073-cffd33f8c6bc", 
        "invitationtype_id": "e8713b6e-a79c-11ed-b76e-0242ac110002"
    }
)






""" test_reservation = createByIdTest2(tableName="facilities_events", variables={"id": "7dcf3d10-3a41-4c36-9700-99d885a1e474"})
test_reservation_create = createTest2(
    tableName="facilities_events", 
    queryName="create",
    variables={
        "id": "bab05e55-3f92-40b5-9272-4b66a368138f", 
        "facility_id": "7dcf3d10-3a41-4c36-9700-99d885a1e474",
        "event_id": "a64871f8-2308-48ff-adb2-33fb0b0741f1",
        "state_id": "1639d8f7-f949-4a23-b93c-9bb96128b54f"
        }
    ) """

""" @pytest.mark.asyncio
async def test_reservation_update(SchemaExecutorDemo):
    tableName="facilities_events"
    variables={
        "id": "e622232d-e34d-4efc-8094-74ace62c7989",
        "facility_id": "7dcf3d10-3a41-4c36-9700-99d885a1e474",
        "state_id": "83e7e264-464d-47ce-8ccd-a5b962fdeed4"
    }
    queryRead = getQuery(tableName=tableName, queryName="read")
    queryUpdate = getQuery(tableName=tableName, queryName="update")
    _variables = variables

    variable_values = {**variables}
    variable_values["id"] = variables["facility_id"]
    responseJson = await SchemaExecutorDemo(query=queryRead, variable_values=variable_values)
    responseData = responseJson.get("data")
    assert responseData is not None, f"got no data while asking for lastchange atribute {responseJson}"
    
    [responseEntity, *_] = responseData.values()
    assert responseEntity is not None, f"got no entity while asking for lastchange atribute {responseJson}"
    reservations = responseEntity["reservations"]
    reservation = next(filter(lambda r: r["id"] == variables["id"], reservations), None)
    assert reservation is not None, f"reservation not found {reservations}"
    lastchange = reservation.get("lastchange", None)
    assert lastchange is not None, f"query read for table {tableName} is not asking for lastchange which is needed"
    _variables["lastchange"] = lastchange
    responseJson = await SchemaExecutorDemo(query=queryUpdate, variable_values=_variables)
    assert "errors" not in responseJson, f"update failed {responseJson}"
    logging.info(f"query for {queryUpdate} with {_variables}, no tested response")

    pass

@pytest.mark.asyncio
async def test_reservation_delete(SchemaExecutorDemo):
    tableName="facilities_events"
    variables={
        "id": "e622232d-e34d-4efc-8094-74ace62c7989",
        "facility_id": "7dcf3d10-3a41-4c36-9700-99d885a1e474",
        "state_id": "83e7e264-464d-47ce-8ccd-a5b962fdeed4"
    }
    queryRead = getQuery(tableName=tableName, queryName="read")
    queryDelete = getQuery(tableName=tableName, queryName="delete")
    _variables = variables

    variable_values = {**variables}
    variable_values["id"] = variables["facility_id"]
    responseJson = await SchemaExecutorDemo(query=queryRead, variable_values=variable_values)
    responseData = responseJson.get("data")
    assert responseData is not None, f"got no data while asking for lastchange atribute {responseJson}"
    
    [responseEntity, *_] = responseData.values()
    assert responseEntity is not None, f"got no entity while asking for lastchange atribute {responseJson}"
    reservations = responseEntity["reservations"]
    reservation = next(filter(lambda r: r["id"] == variables["id"], reservations), None)
    assert reservation is not None, f"reservation not found {reservations}"
    lastchange = reservation.get("lastchange", None)
    assert lastchange is not None, f"query read for table {tableName} is not asking for lastchange which is needed"
    _variables["lastchange"] = lastchange
    responseJson = await SchemaExecutorDemo(query=queryDelete, variable_values=_variables)
    assert "errors" not in responseJson, f"update failed {responseJson}"
    logging.info(f"query for {queryDelete} with {_variables}, no tested response")

    pass """

text_event_resolve_reference = createTest2(
    tableName="events",
    queryName="resolve_reference",
    variables={
        "id": "a64871f8-2308-48ff-adb2-33fb0b0741f1"
    }
)