"""
Entry point of all MCP servers
"""

import contextlib
import logging
import os
from typing import List

import uvicorn
from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from langchain_mcp_adapters.sessions import StreamableHttpConnection
from mcp.server.fastmcp import FastMCP
from mcp.types import Tool
from pydantic import BaseModel

from tools.chembl.server import mcp as chembl_mcp
from tools.clinicaltrials.server import mcp as clinicaltrials_mcp
from tools.ensembl.server import mcp as ensembl_mcp
from tools.kegg.server import mcp as kegg_mcp
from tools.ncbi.server import mcp as ncbi_mcp
from tools.pubchem.server import mcp as pubchem_mcp
from tools.search.server import mcp as search_mcp
from tools.STRING.server import mcp as string_mcp
from tools.tcga.server import mcp as tcga_mcp
from tools.tooluniverse.server import fda_drug_mcp, monarch_mcp, opentargets_mcp
from tools.ucsc.server import mcp as ucsc_mcp
from tools.uniprot.server import mcp as uniprot_mcp
from tools.pdb.server import mcp as pdb_mcp
from tools.dbsearch.server import mcp as dbsearch_mcp

from deploy.config import conf
from deploy.traffic_monitor import SaveBodyMiddleware, log_traffic


mcps: List[FastMCP] = [
    chembl_mcp,
    kegg_mcp,
    string_mcp,
    search_mcp,
    pubchem_mcp,
    ncbi_mcp,
    uniprot_mcp,
    tcga_mcp,
    ensembl_mcp,
    ucsc_mcp,
    fda_drug_mcp,
    opentargets_mcp,
    monarch_mcp,
    clinicaltrials_mcp,
    pdb_mcp,
    dbsearch_mcp,
]


# Create a combined lifespan to manage both session managers
@contextlib.asynccontextmanager
async def lifespan(app: FastAPI):
    async with contextlib.AsyncExitStack() as stack:
        for mcp in mcps:
            await stack.enter_async_context(mcp.session_manager.run())
        yield


app = FastAPI(title="OrigeneMcps", lifespan=lifespan)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  
    allow_credentials=False, 
    allow_methods=["*"],  
    allow_headers=["*"],  
)
app.add_middleware(SaveBodyMiddleware)


# Add traffic monitor middleware
@app.middleware("http")
async def monitor_traffic(request: Request, call_next):
    response = await call_next(request)

    # Extract tool name
    path_parts = request.url.path.strip("/").split("/")
    if len(path_parts) >= 1:
        toolset = path_parts[0]
        await log_traffic(
            request,
            toolset,
            {
                "status_code": response.status_code,
            },
        )

    return response


for mcp in mcps:
    app.mount(f"/{mcp.name}/", mcp.streamable_http_app())


@app.get("/api/list_mcps")
def list_mcps():
    ans = {}
    base_url = f"{conf.mcp_index_base_url}"
    for mcp in mcps:
        ans[mcp.name] = StreamableHttpConnection(
            transport="streamable_http", url=f"{base_url}/{mcp.name}/mcp/"
        )
    return ans


class McpItem(BaseModel):
    name: str
    instructions: str
    tools: List[Tool]


class ListToolResponse(BaseModel):
    mcps: List[McpItem]


if __name__ == "__main__":
    uvicorn.run("deploy.web:app", workers=conf["workers"], port=conf["port"], reload=False)
