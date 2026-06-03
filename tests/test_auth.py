import os
import subprocess
import time

import pytest
import requests


@pytest.fixture
def server_with_auth():
    env = os.environ.copy()
    env["OPENMEMORY_API_KEY"] = "test-key-1,test-key-2"
    env["OPENMEMORY_TRANSPORT"] = "http"
    env["OPENMEMORY_HTTP_PORT"] = "8002"
    
    process = subprocess.Popen(
        ["python", "-m", "openmemory_mcp.server"],
        env=env,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE
    )
    
    # Wait for server to start
    for _ in range(10):
        try:
            requests.get("http://127.0.0.1:8002/health", timeout=1)
            break
        except requests.exceptions.ConnectionError:
            time.sleep(0.5)
    
    yield "http://127.0.0.1:8002"
    
    process.terminate()
    process.wait()

def test_http_auth_enforcement(server_with_auth):
    base_url = server_with_auth
    
    # 1. Test health check (public)
    resp = requests.get(f"{base_url}/health")
    assert resp.status_code == 200
    
    # 2. Test root (public)
    resp = requests.get(f"{base_url}/")
    assert resp.status_code == 200
    assert resp.json()["auth_required"] is True
    
    # 3. Test MCP endpoint without auth (should be 401)
    resp = requests.get(f"{base_url}/mcp")
    assert resp.status_code == 401
    
    # 4. Test MCP endpoint with valid key 1
    headers = {"Authorization": "Bearer test-key-1"}
    resp = requests.get(f"{base_url}/mcp", headers=headers)
    assert resp.status_code == 406 # Accepted auth but wrong client headers for SSE
    
    # 5. Test MCP endpoint with valid key 2
    headers = {"Authorization": "Bearer test-key-2"}
    resp = requests.get(f"{base_url}/mcp", headers=headers)
    assert resp.status_code == 406
    
    # 6. Test MCP endpoint with invalid key
    headers = {"Authorization": "Bearer wrong-key"}
    resp = requests.get(f"{base_url}/mcp", headers=headers)
    assert resp.status_code == 401
