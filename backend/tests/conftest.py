#test version of database.py

import os

import pytest
from dotenv import load_dotenv
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

import db_models
from database import Base, get_db

from main import app


load_dotenv()

TEST_DATABASE_URL = os.getenv("TEST_DATABASE_URL")

if TEST_DATABASE_URL is None:
    raise RuntimeError("TEST_DATABASE_URL is not set")


test_engine = create_engine(TEST_DATABASE_URL) #Foundation USED TO CREATE DB connections ; SQL Alchemy's connection manager for TEST_DB

TestingSessionLocal = sessionmaker( #rules for creating sessions, not the session itself -- Whenever a test need a DB Dession, create one thriugh test_engine
    autocommit=False, #you must explicitly commit using db.commit
    autoflush=False, #Will not push before every query, you must control when flushign or committing happens 
    bind=test_engine #Every SESSION CREATED belongs to viridian_test
) # db = TestingSessionLocal() callas a real session

@pytest.fixture(scope="session", autouse=True)
def prepare_test_database():
    Base.metadata.drop_all(bind=test_engine)
    Base.metadata.create_all(bind=test_engine)

    yield

    Base.metadata.drop_all(bind=test_engine)

def override_get_db(): 
    db = TestingSessionLocal() #creates a session for test_engine -> viridian_test

    try:
        yield db #yeild/wait session to the FASTAPI engpoint 
    finally: #executes whether the request succeeds or raises an exception.
        db.close() #dependency resumes, close the session once the request completes or crashes


app.dependency_overrides[get_db] = override_get_db  #substitute Depends(get_db) for TestingSessionLocal()

@pytest.fixture(scope="session", autouse=True) #run this fixture once for teh entire pytest command -- Not once per test, automatically
def prepare_test_database(): #creates the schema once ; tables exist
    Base.metadata.drop_all(bind=test_engine)  #deletes the table before testing to prevent conflict.
    Base.metadata.create_all(bind=test_engine) #recreates the tables based on SQL Alchemy models for testing

    yield #wait for PYTEST SESSION TO CONCLUDE

    Base.metadata.drop_all(bind=test_engine) #deletes all tables after testing 

@pytest.fixture(autouse=True)
def clean_database(): #deletes test rows before every test ; data is empty
    db = TestingSessionLocal()

    try:
        for table in reversed(db_models.Base.metadata.sorted_tables): #deletes child tables first, then parent tables.
            db.execute(table.delete())

        db.commit()
        yield
    finally:
        db.close()

@pytest.fixture # better controlled setup and cleanup to start test client, reusability, easy customatization, and less shared state between tests.
def client():
    with TestClient(app) as test_client: #TestClient(app) - Lets Python send simulated HTTP requests into the FASTAPI application
        yield test_client #returns a response object containing the status code, json, and headers without opening swagger, starting a browser, or making real network requests...

@pytest.fixture
def auth_header(client):
    register_response = client.post(
        "/auth/register",
        json={
            "email": "fixture@example.com",
            "username": "fixtureuser",
            "password": "password123"
        }
    )

    assert register_response.status_code == 201

    login_response = client.post(
        "/auth/login",
        json={
            "email": "fixture@example.com",
            "password": "password123"
        }
    )

    assert login_response.status_code == 200

    access_token = login_response.json()["access_token"]

    return {
        "Authorization": f"Bearer {access_token}"
    }