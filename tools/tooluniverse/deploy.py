from tools.tooluniverse.server import opentargets_mcp as app

if __name__ == "__main__":
    app.settings.port = 8793
    app.run("streamable-http")
