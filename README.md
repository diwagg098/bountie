## V2 Backend for Bountie Mobile Apps & Web

### Tech Stack
- FastAPI (0.70.0)
- Alembic (1.7.4)


### To create a new table or update table
``` alembic revision -m "name of revision"
``` alembic upgrade head
OR
``` alembic downgrade -1


### Running the Project
``` docker-compose up --build -d
