import unittest
from fastapi.testclient import TestClient
from app.main import app

class TestAPIIntegrations(unittest.TestCase):
    def setUp(self):
        self.client = TestClient(app)

    def test_root_endpoint(self):
        response = self.client.get("/")
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json()["system"], "Voice AI Studio API")

    def test_hardware_endpoint(self):
        response = self.client.get("/api/v1/hardware")
        self.assertEqual(response.status_code, 200)
        self.assertIn("device", response.json())

    def test_tts_rest_endpoint(self):
        response = self.client.post("/api/v1/tts", json={"text": "Teste API REST TTS"})
        self.assertEqual(response.status_code, 200)
        self.assertIn("audio_path", response.json())

    def test_openai_speech_endpoint(self):
        response = self.client.post("/v1/audio/speech", json={"input": "Test OpenAI Endpoint", "voice": "alloy"})
        self.assertEqual(response.status_code, 200)

    def test_mcp_tools(self):
        response = self.client.get("/mcp/tools")
        self.assertEqual(response.status_code, 200)
        self.assertGreater(len(response.json()["tools"]), 0)

    def test_mcp_call(self):
        response = self.client.post("/mcp/call", json={"name": "generate_speech", "arguments": {"text": "MCP Speech Text"}})
        self.assertEqual(response.status_code, 200)
        self.assertIn("audio_path", response.json())

if __name__ == "__main__":
    unittest.main()
