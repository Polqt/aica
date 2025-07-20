<!-- 

Start docker
docker-compose up -d

Rerun the database:
docker-compose exec api python -c "from aica_backend.db.init_db import init_db; init_db()" 

Checkings
cd c:/Users/poyhi/aica-thesis && docker-compose logs -f --tail=20 api 

-->

