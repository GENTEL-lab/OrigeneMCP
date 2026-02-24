from tools.depmap.server import mcp

if __name__ == "__main__":
    mcp.settings.port = 8792  # DepMap service port
    mcp.run(transport="streamable-http")
