`# FastAPI + PostgreSQL with Docker Compose

This project runs a **FastAPI** application with **PostgreSQL 17** using **Docker Compose**.

## 🚀 Quick Start

1. **Clone the repository**:
   ```sh
   https://github.com/ChoriyevJamshid/fastapi_test_app.git
   cd fastapi_test_app
   ```

2. **Create a `.env` file** (optional, if environment variables are needed):
   ```sh
   touch .env
   ```

3. **Run the application**:
   ```sh
   docker-compose up --build
   ```

4. **Access the API**:
    - FastAPI Docs: [http://localhost:8001/docs](http://localhost:8001/docs)
    - OpenAPI JSON: [http://localhost:8001/openapi.json](http://localhost:8001/openapi.json)

---

## 🛠 Environment Variables

Configure environment variables in `.env` file:

```env
SECRET_KEY=

DB_NAME=
DB_USER=
DB_PASSWORD=
DB_HOST=postgres
DB_PORT=

DB_URL=postgresql+asyncpg://username:password@postgres:port/db_name
```

---

## 📌 Notes

- Ensure Docker and Docker Compose are installed on your system.
- You can stop the containers with:
  ```sh
  docker-compose down
  ```
- To run in **detached mode** (background):
  ```sh
  docker-compose up -d
  ```
- Admin:
  ```
  Email: admin@admin.com
  Password: admin
  ```
