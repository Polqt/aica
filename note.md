<!-- 

docker-compose up --build

Start docker
docker-compose up -d

Rerun the database:
docker-compose exec api python -c "from aica_backend.db.init_db import init_db; init_db()" 

Checkings
cd c:/Users/poyhi/aica-thesis && docker-compose logs -f --tail=20 api 

docker system df

# From the root directory
cd c:/Users/poyhi/aica-thesis
C:/Python313/python.exe -c "from src.aica_backend.database.init_db import init_db; init_db()"

# Option 1: Navigate to src directory and run with uvicorn (recommended)
cd c:/Users/poyhi/aica-thesis/src
C:/Python313/python.exe -m uvicorn aica_backend.api.main:app --host 0.0.0.0 --port 8000 --reload


python -m uvicorn api.main:app --reload
-->

