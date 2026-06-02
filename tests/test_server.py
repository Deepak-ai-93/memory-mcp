from openmemory_mcp.server import create_mcp


def test_create_mcp_server():
    mcp = create_mcp()
    assert mcp.name == "OpenMemory MCP"
