from tools.clinicaltrials.server import mcp as mcp_server

if __name__ == "__main__":
    mcp_server.settings.port = 8792
    mcp_server.run(transport="streamable-http")
