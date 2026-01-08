# xray_sdk.py
import requests
import threading
import uuid

class XRay:
    def __init__(self, endpoint="http://127.0.0.1:8000/api", pipeline_name="default"):
        self.endpoint = endpoint
        self.pipeline_name = pipeline_name
        self.run_id = None
        self.session = requests.Session()

    def start(self):
        """Initializes a new run on the server."""
        try:
            response = self.session.post(f"{self.endpoint}/runs/", json={
                "pipeline_name": self.pipeline_name
            })
            if response.status_code == 201:
                self.run_id = response.json()['id']
                print(f"[X-Ray] Started Run: {self.run_id}")
            else:
                print(f"[X-Ray] Failed to start run: {response.text}")
        except Exception as e:
            print(f"[X-Ray] Connection Error: {e}")

    def log(self, step_name, step_type, inputs, outputs, reasoning=None):
        """
        Logs a step. Uses threading to avoid blocking the main app.
        """
        if not self.run_id:
            print("[X-Ray] Warning: Log attempted without starting a run.")
            return

        # Sanitize data (Handle the '5000 items' requirement)
        safe_inputs = self._sanitize(inputs)
        safe_outputs = self._sanitize(outputs)
        
        payload = {
            "step_name": step_name,
            "step_type": step_type,
            "inputs": safe_inputs,
            "outputs": safe_outputs,
            "metadata": {"reasoning": reasoning} if reasoning else {}
        }

        # Send in background thread
        thread = threading.Thread(target=self._send_payload, args=(payload,))
        thread.start()

    def _send_payload(self, payload):
        url = f"{self.endpoint}/runs/{self.run_id}/log_step/"
        try:
            self.session.post(url, json=payload)
        except Exception as e:
            print(f"[X-Ray] Upload Failed: {e}")

    def _sanitize(self, data, limit=10):
        """
        If a list is too long, truncate it. 
        Addresses the 'Performance & Scale' requirement.
        """
        if isinstance(data, list) and len(data) > limit:
            return {
                "sample": data[:limit],
                "total_count": len(data),
                "note": "Truncated for performance"
            }
        return data