from core.configs import settings, DBBaseModel
from core.database import engine

# Importar modelos para reconhecimento
from models.models import UsuarioModel, EspecialidadeModel, ProfissionalModel, ClienteModel, AgendamentoModel

async def criar_tabelas() -> None:
    print('Criando tabelas do HealthScheduler no banco...')
    async with engine.begin() as conn:
        await conn.run_sync(DBBaseModel.metadata.drop_all)
        await conn.run_sync(DBBaseModel.metadata.create_all)
    print('Tabelas criadas com sucesso!')

if __name__ == '__main__':
    import asyncio
    asyncio.run(criar_tabelas())
