# Casebooks Search API

The Casebooks Search API is based on [CUDL Search](https://github.com/cambridge-collection/cudl-search).

## Prerequisites

- **Docker:** Make sure Docker is installed.
- **Make:** Used for the local dev stack and for building/pushing the image. Run `make help` to list the targets.
- **AWS CLI:** Only needed to push images to ECR.
- **Environment Variables:** Set the following environment variables either in your shell or via a `.env` file:
    - `SOLR_HOST`
    - `SOLR_PORT`
    - `API_PORT`

Example `.env` file:

```env
SOLR_HOST=host.docker.internal
SOLR_PORT=8983
API_PORT=90
```

The API runs in a container, so `SOLR_HOST=localhost` would point at the API's own container rather than at Solr. Use `host.docker.internal` to reach a Solr instance published on your machine.

## Running Locally

### API and Solr together

If the `casebooks-solr` repository is checked out alongside this repository, one command builds and starts both:

```bash
make dev-up              # build and start Solr, then the API (in the background)
make dev-up ARCH=arm64   # the same, running natively on Apple Silicon
make dev-down            # stop both
```

Each project runs from its own `docker-compose.yml`. Solr reads its settings from its own repository, exactly as when you run it there. Both containers run in the background; use `docker logs -f casebooks-solr-api` or `docker logs -f casebooks-solr` to follow their output.

| Parameter  | Default             | Description |
|------------|---------------------|-------------|
| `ARCH`     | `DOCKER_DEFAULT_PLATFORM`, else your machine's architecture | `amd64` or `arm64`. Deployed images are `amd64`; `arm64` runs faster locally on Apple Silicon. |
| `API_ENV`  | `.env`              | Env file for the API, e.g. `make dev-up API_ENV=staging.env`. |
| `SOLR_DIR` | `../casebooks-solr` | Path to the casebooks-solr checkout. |

`API_ENV` is relative to this repository.

### API only

To run just the API against a Solr instance you have started separately:

```bash
docker compose --env-file .env up --build --force-recreate
```

## Accessing the API

The API will be available on the port defined in `API_PORT`. For example:

- If `API_PORT` is set to `90`, access the API at:
  [http://localhost:90/items?keyword=*](http://localhost:90/items?keyword=*)

- If `API_PORT` is set to `80`, access the API at:
  [http://localhost/items?keyword=*](http://localhost/items?keyword=*)

## Building and Pushing the Image

`make push` logs in to ECR, builds a `linux/amd64` image and pushes it with three tags:

| Tag               | Example          | Purpose |
|-------------------|------------------|---------|
| `<branch>`        | `main` | Latest image built from that branch (`/` becomes `-`). Moves with each push. Omitted on a detached `HEAD` unless you set `BRANCH`. |
| `git_<short sha>` | `git_1a2b3c4`    | The commit the image was built from. |
| `by_<user>`       | `by_an_other`      | Latest image pushed by that user, so teammates can see who pushed what. Moves with each push. |

Commit your changes before pushing: the `git_` tag records `HEAD`, not uncommitted changes in your working tree.

### Deployment settings

Each deployment has its own settings file, `<name>.env.make`, in the repository root. These files are gitignored; create one for each deployment you push to. For example, `production.env.make`:

```make
AWS_ACCOUNT_ID=<aws-account-id>
REGION=<aws-region>
IMAGE=<ecr-namespace>/<repository-name>
```

Then select it with `DEPLOY`:

```bash
make push DEPLOY=production
```

If no file exists for the name you give, `make` stops with an error rather than pushing to the wrong account. Without `DEPLOY`, `.env.make` is used if it exists.

### Commands

```bash
make push DEPLOY=production          # log in, build and push all three tags
make push DEPLOY=production FRESH=0  # the same, reusing Docker's build cache
make build DEPLOY=production         # build and tag locally without pushing
make login DEPLOY=production         # log Docker in to ECR only
```

### Parameters

Set these in a deployment file or on the command line (command-line values win).

| Parameter        | Default              | Description |
|------------------|----------------------|-------------|
| `DEPLOY`         | none                 | Name of the deployment settings file to load (`<DEPLOY>.env.make`). |
| `AWS_ACCOUNT_ID` | looked up with `aws sts get-caller-identity` | AWS account that owns the ECR repository. |
| `REGION`         | `eu-west-1`          | AWS region of the ECR repository. |
| `IMAGE`          | `casebooks/solr-api` | ECR repository namespace and name. |
| `REGISTRY`       | `<AWS_ACCOUNT_ID>.dkr.ecr.<REGION>.amazonaws.com` | Full registry host. Setting this skips the account lookup. |
| `FRESH`          | `1`                  | `1` builds with `--pull --no-cache`; `0` reuses cached layers and local base images. |
| `AWS`            | `aws`                | Command used to call the AWS CLI. `make` runs commands in a non-interactive bash shell, so shell aliases and functions are not available. If you normally reach AWS through one, set this to a command that works without them. |
| `BRANCH`, `SHA`, `WHO` | current branch, short commit, `whoami` | Command line only: override the values used in the three tags. |

## API Endpoints

### TEI Documents

- **Search TEI Items**

  **GET** `/items`

  Examples:
  - [http://localhost/items?keyword=flowers](http://localhost/items?keyword=flowers)
  - [http://localhost/items?text=york&year=1868&exclude-cancelled=Yes&f1-document-type=letter](http://localhost/items?text=york&year=1868&exclude-cancelled=Yes&f1-document-type=letter)

- **Index / Remove TEI Item**

  **PUT** and **DELETE** `/item`

## PUT and DELETE Operations

These operations are normally triggered by SNS notifications within AWS. For local testing, you can use CURL.

### PUT Requests

For TEI documents:

```bash
curl -X PUT -H "Content-Type: application/json" -d @path/to/TEI-file.json http://localhost/item
```

### DELETE Requests

To delete an item from the index, send a DELETE request with the item's ID:

```bash
curl -X DELETE http://localhost/item/idValue
```

You can find the `id` for an item by performing a search and examining the `id` property in the returned JSON.


## Customising the Solr Search API

The Solr Search API was designed to be extensible, enabling you to add new data models and endpoints or to override the existing one for ‘items’.

### File Structure Overview

The custom code for the Solr Search API is located under the `frontend/custom` directory. A typical structure looks like this:

```
Solr Search API/
├── main.py
└── frontend/
    └── custom/
        ├── __init__.py
        ├── config.py                # Centralised configuration and constants
        ├── implementation.py        # Aggregates routers from the
        |                            # models subdirectory and re-
        |                            # exports shared models/logic
        └── models/
            ├── __init__.py
            ├── site_pages.py        # Models & endpoints for
            |                        # website pages
            └── your_stuff.py        # Your models & endpoints
```

### Set Defaults in `config.py`

The following parameters must be defined in `config.py`.

`DEFAULT_ROWS` contains the number of entries retrieved per page of results

CORE_MAP maps the resource’s name to its Solr Core.

```
CORE_MAP = {
    # resource name -> solr core name
    "item": "dcp",
    "page": "site",
}
```

### How to add a New Data Model and Endpoints

This example assumes that you want to support a new resource called ‘collections’.

1. **Create a New Module**

   In the `frontend/custom/models` directory, create a new file called `collections.py`. This file should define the Pydantic V2 models and its FastAPI endpoints.

   By default, the Solr Search API makes the following presumptions about parameters:
    1. you do not redefine or attempt to use the names of the core parameters used by all models (`keyword`, `sort`, `rows`, `page`)
    2. all facet parameters will be preceded by `facet-` (*e.g.*) `facet-document-type`. These will be translated into a Solr facet query.
    2. All other parameters are treated as field names and will be translated into a Solr Query. The parameter `author` would search the `author` field defined in your Solr schema.

   For example:

   ```python
   from fastapi import APIRouter
   from pydantic import BaseModel
   import frontend.lib.utils as utils

   router = APIRouter()

   # All models should be based on CoreQueryParams. It defines the
   # parameters and functionality common to all endpoints
   class Collection(CoreQueryParams):
       id: int
       name: str
       # Add additional fields as needed.

       # You can also add custom model and field validators
       # that run before or after the core processing.
       # If the mapping of your API's parameters to Solr
       # fieldnames isn't a one to one correspondence,
       # you will need to add a get_solr_params function
       # into the model

   @router.get("/collections", response_model=list[Collection])
   def get_collections():
       # All logic concerning the parsing, validation and manipulation
       # of paramters and their values should be done in the Collection
       # model.
       # The following two commands are all that's needed to convert
       # your parameters into solr queries and retrieve the request.

       solr_params = params.get_solr_params()
       return await utils.get_request("pages", **solr_params)

   @router.put("/collections")
   def create_collection(request: Request):
       data = await request.body()
       json_dict = json.loads(data)
       if json_dict.get("facet-document-type") == "site":
           logger.info(f"Indexing {json_dict.get('fileID')}")
           status_code = await utils.put_item("page", data, {"f": ["$FQN:/**"]})
       else:
           logger.error(f"Invalid site JSON for fileID: {json_dict.get('fileID')}")
           status_code = utils.INTERNAL_ERROR_STATUS_CODE
       return status_code

   @router.delete("/page/{file_id}")
   async def delete_collection(file_id: str):
      # delete_resource takes two parameters. The first is the
      # core name (defined in your custom implementation
      # the unique id value of your resource
	    return await utils.delete_resource("page", file_id)

   ```

2. **Register the Router for your endpoints**

   Import your new router into `frontend/custom/implementation.py` and then include it in the aggregated router. It will then be automatically available to the search API.

   Example modification to `implementation.py`:

   ```python
   from fastapi import APIRouter
   from frontend.custom.models.site_pages import router as pages_router

   # Import your router
   from frontend.custom.models.collections import router as collections_router

   router = APIRouter()

   router.include_router(pages_router)

   # Register your collection endpoints
   router.include_router(collections_router)
   ```

### Default Endpoints for Items

If no custom implementation is provided for `ItemsQueryParams` and its endpoints, the Solr Search API will fall back to using the default ones defined in the main application.

The most common customisation will be providing a custom data model (`ItemsQueryParams`) for item queries, which can be done according to the instructions above. There is no need to create the actual endpoints since the default ones will use your new data model **provided you register it** using `router.include_router`.

New projects likely won't need much (if any customisation), esp. if their search field names and facet field names match the names of the fields in your solr schema.
