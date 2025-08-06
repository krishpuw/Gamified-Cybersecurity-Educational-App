import time
import requests

class AttackAgent:
    def __init__(self, caldera_url: str, api_key: str):
        self.base_url = caldera_url
        self.headers = {
            "KEY": api_key ,
            "Content-Type": "application/json"
        }

    def start_attack(self, adversary_id: str, group: str = "red", autonomous: bool = True, username: str = None):
        operation_name = f"Attack_for_{username}" if username else "Generic_Attack"
        payload = {
            "name": operation_name,
            "adversary_id": adversary_id,
            "group": group,
            "autonomous": autonomous
     }
        response = requests.post(f"{self.base_url}/api/v2/operations", headers=self.headers, json=payload)
        return response.json() if response.status_code == 200 else None

    def get_operation_status(self, operation_id: str):
        response = requests.get(f"{self.base_url}/api/v2/operations/{operation_id}", headers=self.headers)
        return response.json() if response.status_code == 200 else None

    def cancel_attack(self, operation_id: str):
        response = requests.delete(f"{self.base_url}/api/v2/operations/{operation_id}", headers=self.headers)
        return response.status_code == 204

    def wait_for_attack_start(self, operation_id: str, timeout: int = 10):
        start_time = time.time()
        while time.time() - start_time < timeout:
            status = self.get_operation_status(operation_id)
            if status and status.get("state") == "running":
                return True
            time.sleep(1)
        return False

    
    def get_all_objectives(self):
        response = requests.get(f"{self.base_url}/api/v2/objectives", headers=self.headers)
        if response.status_code == 200:
            return response.json()
        return []

    def get_all_abilities(self):
        response = requests.get(f"{self.base_url}/api/v2/abilities", headers=self.headers)
        if response.status_code == 200:
            return response.json()
        return []
    
    def create_adversary(self, name: str, description: str, objective_id: str, ability_ids: list):
        attack_phases = {
            "1": ability_ids  # All abilities go into phase 1; you can split across multiple phases if you want
        }

        payload = {
          "name": name,
            "description": description,
            "objective": objective_id,
            "atomic_ordering": attack_phases
        }

        response = requests.post(f"{self.base_url}/api/v2/adversaries", headers=self.headers, json=payload)
        return response.json() if response.status_code == 200 else None
    

    def get_operation_status(self, operation_id):
        try:
            response = requests.get(
                f"{self.base_url}/api/v2/operations/{operation_id}",
                headers=self.headers
            )
            if response.ok:
                data = response.json()
                return data.get("state", "unknown")
        except Exception as e:
            print(f"[ERROR] Failed to get operation status: {e}")
        return None



    
