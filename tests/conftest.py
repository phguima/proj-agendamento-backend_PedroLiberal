import asyncio
import pytest
import pytest_asyncio
from typing import AsyncGenerator
from httpx import AsyncClient, ASGITransport
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession, async_sessionmaker
from sqlalchemy.pool import StaticPool

from main import app
from core.configs import settings, DBBaseModel
from core.deps import get_session

# URL do banco de teste em memória (SQLite)
TEST_DB_URL = "sqlite+aiosqlite:///:memory:"

# Engine de teste com StaticPool para compartilhar a conexão em memória
test_engine = create_async_engine(
    TEST_DB_URL,
    connect_args={"check_same_thread": False},
    poolclass=StaticPool,
)

# Fábrica de sessões de teste
TestSessionLocal = async_sessionmaker(
    bind=test_engine,
    class_=AsyncSession,
    expire_on_commit=False,
    autocommit=False,
    autoflush=False
)

@pytest_asyncio.fixture(scope="session", autouse=True)
async def setup_db():
    """Cria as tabelas no banco de dados de teste"""
    async with test_engine.begin() as conn:
        await conn.run_sync(DBBaseModel.metadata.create_all)
    yield
    async with test_engine.begin() as conn:
        await conn.run_sync(DBBaseModel.metadata.drop_all)

async def override_get_session() -> AsyncGenerator[AsyncSession, None]:
    """Sobrescreve a dependência de sessão para usar o banco de teste"""
    async with TestSessionLocal() as session:
        yield session

# Sobrescrevendo a dependência no app FastAPI
app.dependency_overrides[get_session] = override_get_session

@pytest_asyncio.fixture
async def client() -> AsyncGenerator[AsyncClient, None]:
    """Fixture que fornece um cliente HTTP assíncrono para os testes"""
    async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as ac:
        yield ac
