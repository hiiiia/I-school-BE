from fastapi.testclient import TestClient
from main import app

from database import get_db, engine, SessionLocal
import pytest


@pytest.fixture(scope="function")
def db_session():
    connection = engine.connect()
    transaction = connection.begin()
    session = SessionLocal(bind=connection)

    yield session

    session.close()
    transaction.rollback()
    connection.close()


@pytest.fixture(scope="function")
def client(db_session):
    def override_get_db():
        try:
            yield db_session
        finally:
            db_session.close()

    app.dependency_overrides[get_db] = override_get_db
    return TestClient(app)

################################################

def test_correct_post(client):
    timetable_id = 1
    course_code = "CS101"
    response = client.post(
        url=f'/api/v1/timetables/{timetable_id}',
        json={"courseCode": course_code})
    assert response.json() == {"success" : True, "data" : None, "error" : None}
    

def test_correct_timetable_incorrect_coursecode_post(client):
    timetable_id = 1
    course_code = "Bad Course Code"
    response = client.post(
        url=f'/api/v1/timetables/{timetable_id}',
        json={"courseCode": course_code})
    assert response.json() == {'success': False, 'data': None, 'error': '강의가 존재하지 않습니다.'}


def test_incorrect_timetable_correct_coursecode_post(client):
    timetable_id = 4
    course_code = "CS101"
    response = client.post(
        url=f'/api/v1/timetables/{timetable_id}',
        json={"courseCode": course_code})
    assert response.json() == {'success': False, 'data': None, 'error': "시간표가 존재하지 않습니다."}

def test_incorrect_timetable_incorrect_coursecode_post(client):
    timetable_id = 4
    course_code = "Bad Course Code"
    response = client.post(
        url=f'/api/v1/timetables/{timetable_id}',
        json={"courseCode": course_code})
    assert response.json() == {'success': False, 'data': None, 'error': "시간표가 존재하지 않습니다."}

def test_try_exist_course_post(client):
    timetable_id = 1
    course_code = "CS101"
    response = client.post(
        url=f'/api/v1/timetables/{timetable_id}',
        json={"courseCode": course_code})
    response = client.post(
        url=f'/api/v1/timetables/{timetable_id}',
        json={"courseCode": course_code})
    assert response.json() == {'success': False, 'data': None, 'error': "이미 존재하는 강의입니다."}

###############################################


def test_correct_del(client):
    timetable_id = 1
    course_code = "CS101"
    response = client.post(
        url=f'/api/v1/timetables/{timetable_id}',
        json={"courseCode": course_code})
    response = client.request(
        method="DELETE",
        url=f'/api/v1/timetables/{timetable_id}',
        json={"courseCode": course_code})
    assert response.json() == {"success": True, "data": None, "error": None}

def test_correct_timetable_incorrect_coursecode_del(client):
    timetable_id = 1
    course_code = "Bad Course Code"
    response = client.post(
        url=f'/api/v1/timetables/{timetable_id}',
        json={"courseCode": course_code})
    response = client.request(
        method="DELETE",
        url=f'/api/v1/timetables/{timetable_id}',
        json={"courseCode": course_code})
    assert response.json() == {'success': False, 'data': None, 'error': '강의가 존재하지 않습니다.'}


def test_incorrect_timetable_correct_coursecode_del(client):
    timetable_id = 4
    course_code = "CS101"
    response = client.post(
        url=f'/api/v1/timetables/{timetable_id}',
        json={"courseCode": course_code})
    response = client.request(
        method="DELETE",
        url=f'/api/v1/timetables/{timetable_id}',
        json={"courseCode": course_code})
    assert response.json() == {'success': False, 'data': None, 'error': "시간표가 존재하지 않습니다."}

def test_incorrect_timetable_incorrect_coursecode_del(client):
    timetable_id = 4
    course_code = "Bad Course Code"
    response = client.post(
        url=f'/api/v1/timetables/{timetable_id}',
        json={"courseCode": course_code})
    
    response = client.request(
        method="DELETE",
        url=f'/api/v1/timetables/{timetable_id}',
        json={"courseCode": course_code})
    assert response.json() == {'success': False, 'data': None, 'error': "시간표가 존재하지 않습니다."}

