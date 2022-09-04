import pytest
from fastapi.testclient import TestClient
from sqlmodel import Session, SQLModel, create_engine
from sqlmodel.pool import StaticPool

from api.database import get_session
from api.main import app
from api.models import ShortUrl


@pytest.fixture(name="session")
def session_fixture():
    engine = create_engine(
        "sqlite://", connect_args={"check_same_thread": False}, poolclass=StaticPool
    )
    SQLModel.metadata.create_all(engine)
    with Session(engine) as session:
        yield session


@pytest.fixture(name="client")
def client_fixture(session: Session):
    def get_session_override():
        return session

    app.dependency_overrides[get_session] = get_session_override
    client = TestClient(app)
    yield client
    app.dependency_overrides.clear()


def test_short_url(client: TestClient):
    url = "https://docs.python.org/3/"

    response = client.post(f"/shorten/", params={"url": url})
    data = response.json()

    created_shorturl = data["short"]
    print(f"Shorturl created: {created_shorturl}")

    response2 = client.get(f"/{created_shorturl}", allow_redirects=False)
    print(response2.__dict__)

    assert response2.status_code == 307
    assert response2.headers["location"] == url


def test_visit_count(client: TestClient):
    url = "https://docs.python.org/2/"

    response = client.post(f"/shorten/", params={"url": url})
    data = response.json()

    shorturl = data["short"]

    response = client.get(f"/info/{shorturl}")
    data = response.json()

    assert data["visits"] == 0

    client.get(f"/{shorturl}", allow_redirects=False)

    response = client.get(f"/info/{shorturl}")
    data = response.json()

    assert data["visits"] == 1
