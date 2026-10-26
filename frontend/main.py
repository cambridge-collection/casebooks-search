#!/usr/bin/env python3
import json
from pathlib import Path
from typing import Optional, Annotated

from fastapi import FastAPI, HTTPException, Query, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import FileResponse

from frontend.lib.utils import *

origins = [
    "https://casebooks-production.casebooks.lib.cam.ac.uk",
    "https://casebooks.lib.cam.ac.uk",
]

app = FastAPI()
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(implementation.router)


@app.get("/robots.txt", include_in_schema=False)
async def robots():
    return FileResponse(Path(__file__).parent / "robots.txt")


@app.get("/items")
async def get_items(params: Annotated[implementation.ItemsQueryParams, Query()]):
    solr_params = params.get_solr_params()
    return await get_request("items", **solr_params)


@app.put("/item")
async def update_item(request: Request):
    data = await request.body()
    json_dict = json.loads(data)
    if json_dict.get("facet-document-type"):
        logger.info(f"Indexing {json_dict.get('id')}")
        status_code = await put_item("item", data, {"f": ["$FQN:/**", "/*"]})
    else:
        detail = f"Invalid item JSON for id: {json_dict.get('id')}"
        logger.error(detail)
        raise HTTPException(status_code=400, detail=detail)
    return status_code


@app.delete("/item/{file_id}")
async def delete_item(file_id: str):
    return await delete_resource("item", file_id)
