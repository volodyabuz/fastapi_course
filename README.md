
# 📘 Справочная информация для разработки

## 🗄️ Работа с Alembic (миграции)

### Создание новой миграции
```bash
alembic revision --autogenerate -m "MESSAGE"
```

Где MESSAGE — описание изменений в миграции.

## ⚙️ Настройка Alembic
1. Файл alembic.ini
Добавьте директорию src в конфигурацию:

```bash
script_location = %(here)s/src/migrations
prepend_sys_path = . src
```
Раскомментируйте строки для формата имени миграции и офорлмению по pep8:
```bash
file_template = %%(year)d_%%(month).2d_%%(day).2d_%%(hour).2d%%(minute).2d-%%(rev)s_%%(slug)s
hooks = black
black.type = console_scripts
black.entrypoint = black
black.options = -l 88 REVISION_SCRIPT_FILENAME
```
Установите пакет black
```bash
pip install black
```
2. Файл env.py (в папке migrations)
Добавьте область видимости:
```bash
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[2]))
```
Подключите базовый класс и модели:
```bash
from src.database import Base
from src.models.hotels import TableOrm
```
Переопределите URL подключения к БД:
```bash
from src.config import settings

config.set_main_option("sqlalchemy.url", f"{settings.DB_URL}?async_fallback=True")
```
💡 Примечание: ?async_fallback=True необходим для работы асинхронного драйвера.

Настройте метаданные для SQLAlchemy:
```bash
target_metadata = Base.metadata
```
🗄️ Настройка базы данных и SQLAlchemy
Файл config.py
```bash
from pydantic_settings import BaseSettings, SettingsConfigDict

class Settings(BaseSettings):
    DB_HOST: str
    DB_PORT: int
    DB_USER: str
    DB_PASS: str
    DB_NAME: str

    @property
    def DB_URL(self):
        return f"postgresql+asyncpg://{self.DB_USER}:{self.DB_PASS}@{self.DB_HOST}:{self.DB_PORT}/{self.DB_NAME}"

    model_config = SettingsConfigDict(env_file=".env")

settings = Settings()
```
Файл database.py
```bash
from sqlalchemy.ext.asyncio import async_sessionmaker, create_async_engine
from sqlalchemy.orm import DeclarativeBase

from src.config import settings
```

# Создание асинхронного движка
```bash
engine = create_async_engine(settings.DB_URL)
```

# Создание фабрики сессий
```bash
async_session_maker = async_sessionmaker(bind=engine, expire_on_commit=False)
```
# Базовый класс для моделей
```bash
class Base(DeclarativeBase):
    pass
```
🚀 Добавление пути приложения в main.py
Для корректного импорта модулей добавьте путь к родительской директории:

```bash
import sys
from pathlib import Path

sys.path.append(str(Path(__file__).parent.parent))
```

🔧 Быстрые команды

| Команда | Описание |
|:-|:-|
| alembic revision --autogenerate -m "message" |	Создать миграцию|
| alembic upgrade head |	Применить все миграции|
| alembic downgrade -1 |	Откатить последнюю миграцию|
| alembic history |	Показать историю миграций|

⚠️ Важные моменты

Асинхронность: Используется драйвер asyncpg, поэтому все операции с БД должны быть асинхронными.

Переменные окружения: Все настройки хранятся в файле .env, который не должен попадать в репозиторий.

Пути импорта: Убедитесь, что пути к модулям настроены корректно для избежания ошибок импорта.

Команды ORM

Работа с сессией:
```bash
async with async_session_maker() as session:
    <your code> (query or stmt)
    await session.execute(query) # выполнить запрос в БД
    result.scalars().all() # scalars - вытащить объект из кортежа
    result.first() # первое значение
    result.one_or_none() # вернуть одно значение или ничего. А если значений больше - ошибка
    await session.commit() # закоммитить сессию (при select не нужно)
```

Выборка данных
```bash
query = select(HotelsOrm) # получить данные из модели
# добавить фильтры:
query = query.filter_by(title=title) # добавление ОПЦИОНАЛЬНОГО параметра
query = query.where(HotelsOrm.title.like(f"%{title}%"))
query = query.filter(func.lower(HotelsOrm.title).like(f"%{title.strip().lower()}%"))
query = query.filter(func.lower(HotelsOrm.title).contains(title.strip().lower())) # конструкция like %<text>%
query = (
             query
             .limit(limit)
             .offset(offset)
         )
```

Добавление данных
```bash
add_hotel_stmt = insert(HotelsOrm).values(**hotel_data.model_dump()) # вместо **args можно именованные параметры
```