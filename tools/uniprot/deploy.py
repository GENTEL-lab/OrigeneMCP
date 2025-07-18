from tools.uniprot.server import mcp

if __name__ == "__main__":
    mcp.settings.port = 8791
    mcp.run(transport="streamable-http")
