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
            "name": operation_name, # integrate type of attack right here 
            "adversary_id": adversary_id,
            "group": group,
             "autonomous": 1 if autonomous else 0
             
        }

        response = requests.post(f"{self.base_url}/api/v2/operations", headers=self.headers, json=payload)

        print("=== START ATTACK RESPONSE ===")
        print("Status Code:", response.status_code)
        print("Response Body:", response.text)

        if response.status_code == 200:
            return response.json()
        else:
            return None


    # def start_attack(self, adversary_id: str, group: str = "red", autonomous: bool = True, username: str = None):
    #     operation_name = f"Attack_for_{username}" if username else "Generic_Attack"
    #     payload = {
    #         "name": operation_name,
    #         "adversary_id": adversary_id,
    #         "group": group,
    #         "autonomous": autonomous
    #  }
    #     response = requests.post(f"{self.base_url}/api/v2/operations", headers=self.headers, json=payload)
    #     return response.json() if response.status_code == 200 else None

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
        payload = {
            "name": name,
            "description": description,
            "objective": objective_id,
            "atomic_ordering": ability_ids  # flat list, no phase dict
            }

        print("[DEBUG] Adversary creation payload:", payload)
        
        response = requests.post(f"{self.base_url}/api/v2/adversaries", headers=self.headers, json=payload)
        if response.status_code != 200:
            print("[ERROR] Failed to create adversary")
            print("[ERROR] Status Code:", response.status_code)
            print("[ERROR] Response Body:", response.text)
            return None

        return response.json()

    

def get_operation_status(self, operation_id):
    try:
        response = requests.get(
            f"{self.base_url}/api/v2/operations/{operation_id}",
            headers=self.headers
        )
        if response.ok:
            return response.json()  # ✅ return the full data
    except Exception as e:
        print(f"[ERROR] Failed to get operation status: {e}")
    return None

