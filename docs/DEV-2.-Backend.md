# Backend Deployment for Development

The recommended way to run FMTM is with Docker. You can also develop on your local machine outside of Docker, see below.

> NOTE: If you haven't yet downloaded the Repository and setup your environment variables, please check the [Getting Started](https://github.com/hotosm/fmtm/blob/main/docs/DEV-1.-Getting-Started.md) wiki page.

Now let's get started :thumbsup:

## 1. Start the API with Docker

The easiest way to get up and running is by using the FMTM Docker deployment. Docker creates a virtual environment, isolated from your computer's environment, installs all necessary dependencies, and creates a container for each the database, the api, and the frontend. These containers talk to each other via the URLs defined in the docker-compose file and your env file.

### 1A: Starting the Containers

1. You will need to [Install Docker](https://docs.docker.com/engine/install/) and ensure that it is running on your local machine.
2. From the command line: navigate to the top level directory of the FMTM project.
3. From the command line run: `docker-compose pull`.
   This will pull the latest container builds from **main** branch.
4. Make sure you have a `.env` file with all required variables, see [Getting Started](https://github.com/hotosm/fmtm/blob/main/docs/DEV-1.-Getting-Started.md).
5. Once everything is pulled, from the command line run: `docker compose up -d api`
6. If everything goes well you should now be able to **navigate to the project in your browser:** `http://127.0.0.1:8000/docs`

> Note: If that link doesn't work, check the logs with `docker log fmtm_api`.

> Note: the database host `fmtm-db` is automatically resolved by docker compose to the database container IP.

- FMTM uses ODK Central to store ODK data.
- To facilitate faster development, the Docker setup includes a Central server.
- The credentials are provided via the `.env` file.

> Note: Alternatively, you may use an external Central server and user in the `.env`.

### 1B: Import Test Data

Some test data is available to get started quickly.

1. Navigate to the `import-test-data` endpoint in the API docs page:
   <http://127.0.0.1:8000/docs#/debug/import_test_data_debug_import_test_data_get>
2. Click `Try it out`, then `execute`.

## 2. Start the API without Docker

To run FMTM without Docker, you will need to start the database, then the API.

### 2A: Starting the Database

#### Option 1: Run the Database (only) in Docker

Running the database in Docker means postgres does not need to be installed on your local machine.

1. You will need to [Install Docker](https://docs.docker.com/engine/install/) and ensure that it is running on your local machine.
2. Start an instance of Postgres (with Postgis):

```bash
docker run -d --name fmtm_db -e POSTGRES_PASSWORD=xxxx -p 5432:5432 postgis/postgis:15-3.3
```

The database should be accessible at localhost:5432.

> Note: if port 5432 is already taken, then change the `-p ANY_PORT:5432` declaration.

#### Option 2: Run the database locally

For advanced users, it is also possible to run a postgresql/postgis database locally, however you will need to set it up yourself and make it accessible on a port.

### 2B. Starting the API

After starting the database, from the command line:

1. Navigate to the top level directory of the FMTM project.
2. Install PDM with: `pip install pdm`
3. Install backend dependencies with PDM: `pdm install`
4. Run the Fast API backend with: `pdm run uvicorn app.main:api --host 0.0.0.0 --port 8000`

The API should now be accessible at: <http://127.0.0.1:8000/docs>

## 3. Hybrid Docker/Local

- It is not recommended to run FMTM in a container while using a local database on your machine.
- It is possible, but complicates the docker networking slightly.
- The FMTM container cannot see the local machine's `localhost`, so we need a workaround.
- **Option 1**: add `network_mode: "host"` under the `api:` service in the **docker-compose.yml** file.
- **Option 2**: use the direct container IP address for the database for **FMTM_DB_HOST**, found via `docker inspect fmtm_db`.

## Backend Tips

### Implement authorization on an endpoints

To add authentication to an endpoint, import `login_required` from `auth` module, you can use it as a decorator or use fastapi `Depends(login_required)` on endpoints.

## Backend Debugging

- The `docker-compose.yml` builds FMTM using the `debug-with-odk` target in the Dockerfile.
- The debug image contains `debugpy` to assist debugging in the container.

To use it:

1. Re-build the docker image `docker compose build api`
2. Start the docker container `docker compose up -d api`
3. Connect to the debugger on port **5678**.

You can configure your IDE to do this with the build in debugger.

Example launch.json config for vscode:

```
{
  "configurations": [
    {
      "name": "Remote - Server Debug",
      "type": "python",
      "request": "attach",
      "host": "localhost",
      "port": 5678,
      "pathMappings": [
        {
          "localRoot": "${workspaceFolder}/src/backend/app",
          "remoteRoot": "/opt/app"
        }
      ],
      "justMyCode": false
    }
  ]
}
```

> Note: either port 5678 needs to be bound to your localhost (default), or the `host` parameter can be set to the container IP address.

## Conclusion

Running the FMTM project is easy with Docker. You can also run the
project locally outside of Docker, but it requires more setup. The
frontend is built with React and Typescript, and the backend is built
with FastAPI. Use the tips provided to customize and extend the
functionality of the project.
