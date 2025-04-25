import pytest
import pytest_asyncio
from httpx import AsyncClient
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import sessionmaker
from app.backend.db import Base
from app.main import app
from app.backend.db_depends import get_db


TEST_DATABASE_URL = "sqlite+aiosqlite:///:memory:"


engine = create_async_engine(TEST_DATABASE_URL, echo=False)
TestingSessionLocal = sessionmaker(
    autocommit=False,
    autoflush=False,
    bind=engine,
    class_=AsyncSession
)

@pytest_asyncio.fixture(scope="function")
async def db_session():

    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    session = TestingSessionLocal()
    try:
        yield session
    finally:
        await session.close()
        # Очистка схем
        async with engine.begin() as conn:
            await conn.run_sync(Base.metadata.drop_all)

@pytest_asyncio.fixture(scope="function")
async def test_client(db_session):

    async def override_get_db():
        try:
            yield db_session
        finally:
            pass

    app.dependency_overrides[get_db] = override_get_db

    async with AsyncClient(app=app, base_url="http://test") as client:
        yield client

    app.dependency_overrides.clear()

@pytest.mark.asyncio
async def test_create_and_get_product(test_client):

    response = await test_client.post("/products/", json={"name": "Laptop"})
    assert response.status_code == 201
    body = response.json()
    assert body.get("status_code") == 201
    assert body.get("transaction") == "Successful"


    response = await test_client.get("/products/")
    assert response.status_code == 200
    products = response.json()
    assert isinstance(products, list)
    assert len(products) == 1
    assert products[0]["name"] == "Laptop"
    assert products[0]["categories"] == []

@pytest.mark.asyncio
async def test_create_and_get_category(test_client):

    response = await test_client.post("/categories/", json={"name": "Electronics"})
    assert response.status_code == 201
    body = response.json()
    assert body.get("status_code") == 201
    assert body.get("transaction") == "Successful"


    response = await test_client.get("/categories/")
    assert response.status_code == 200
    categories = response.json()
    assert isinstance(categories, list)
    assert len(categories) == 1
    assert categories[0]["name"] == "Electronics"
    assert categories[0]["products"] == []

@pytest.mark.asyncio
async def test_create_and_get_pairs(test_client):

    await test_client.post("/products/", json={"name": "Phone"})
    await test_client.post("/categories/", json={"name": "Mobile"})

    # Создание связи
    response = await test_client.post("/pairs/", json={"product_id": 1, "category_id": 1})
    assert response.status_code == 201
    assert response.json().get("message") == "Pair created successfully"

    # Проверка списка пар
    response = await test_client.get("/pairs/")
    assert response.status_code == 200
    data = response.json()
    assert isinstance(data, list)
    assert len(data) == 1
    assert data[0]["product"] == "Phone"
    assert data[0]["category"] == "Mobile"

@pytest.mark.asyncio
async def test_empty_relations(test_client):

    await test_client.post("/products/", json={"name": "Book"})

    await test_client.post("/categories/", json={"name": "Furniture"})


    response = await test_client.get("/pairs/")
    assert response.status_code == 200
    data = response.json()

    assert any(p["product"] == "Book" and p["category"] is None for p in data)
    assert any(p["category"] == "Furniture" and p["product"] is None for p in data)