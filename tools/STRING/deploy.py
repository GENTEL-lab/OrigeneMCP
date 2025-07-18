from tools.STRING.server import mcp

if __name__ == "__main__":
    mcp.settings.port = 8790
    mcp.run(transport="streamable-http")
