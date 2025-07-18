from tools.search.server import mcp

if __name__ == "__main__":
    mcp.settings.port = 8792
    mcp.run(transport="streamable-http")
