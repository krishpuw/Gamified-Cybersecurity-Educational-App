# agents/mitre_map.py
from __future__ import annotations
import random
from typing import Dict, List, Tuple

# Allowed tactic -> [(technique_id, technique_name), ...]
TACTIC_TECHNIQUES: Dict[str, List[Tuple[str, str]]] = {
    "Reconnaissance": [
        ("T1595", "Active Scanning"),
        ("T1595.001", "Scanning IP Blocks"),
        ("T1595.002", "Vulnerability Scanning"),
        ("T1595.003", "Wordlist Scanning"),
        ("T1590", "Gather Victim Network Information"),
    ],
    "Initial Access": [
        ("T1078", "Valid Accounts"),
        ("T1566", "Phishing"),
        ("T1190", "Exploit Public-Facing Application"),
        ("T1133", "External Remote Services"),
        ("T1189", "Drive-by Compromise"),
    ],
    "Execution": [
        ("T1204", "User Execution"),
        ("T1218", "System Binary Proxy Execution"),
        ("T1059", "Command and Scripting Interpreter"),
        ("T1047", "Windows Management Instrumentation"),
        ("T1106", "Native API"),
    ],
    "Privilege Escalation": [
        ("T1548", "Abuse Elevation Control Mechanism"),
        ("T1068", "Exploitation for Privilege Escalation"),
        ("T1546", "Event Triggered Execution"),
        ("T1055", "Process Injection"),
        ("T1134", "Access Token Manipulation"),
    ],
}

TACTICS_ALLOWED = list(TACTIC_TECHNIQUES.keys())

# simple alias/synonym handling (extend as needed)
_TACTIC_ALIASES = {
    "recon": "Reconnaissance",
    "reconnaissance": "Reconnaissance",
    "initialaccess": "Initial Access",
    "initial access": "Initial Access",
    "exec": "Execution",
    "execution": "Execution",
    "privilegeescalation": "Privilege Escalation",
    "privilege escalation": "Privilege Escalation",
}

def normalize_tactic(tactic: str | None) -> str:
    """Map user/agent input to our canonical tactic names; default Reconnaissance."""
    if not tactic:
        return "Reconnaissance"
    key = str(tactic).strip().lower().replace("-", " ")
    return _TACTIC_ALIASES.get(key, tactic if tactic in TACTICS_ALLOWED else "Reconnaissance")

def is_valid_technique_for_tactic(tactic: str, technique_id: str) -> bool:
    """True if technique_id is in the allowed list for the tactic."""
    for tid, _ in TACTIC_TECHNIQUES.get(tactic, []):
        if tid == technique_id:
            return True
    return False

def pick_technique(tactic: str) -> Tuple[str, str]:
    """Return a random (technique_id, technique_name) for a tactic."""
    pool = TACTIC_TECHNIQUES.get(tactic) or TACTIC_TECHNIQUES["Reconnaissance"]
    return random.choice(pool)




























# # services/mitre_map.py
# from __future__ import annotations
# import random
# from typing import Dict, List, Tuple, Optional

# TACTIC_TECHNIQUES: Dict[str, List[Tuple[str, str]]] = {
#     "Reconnaissance": [
#         ("T1595", "Active Scanning"),
#         ("T1595.001", "Scanning IP Blocks"),
#         ("T1595.002", "Vulnerability Scanning"),
#         ("T1595.003", "Wordlist Scanning"),
#         ("T1590", "Gathe
#r Victim Network Information"),
#     ],
#     "Initial Access": [
#         ("T1078", "Valid Accounts"),
#         ("T1566", "Phishing"),
#         ("T1190", "Exploit Public-Facing Application"),
#         ("T1133", "External Remote Services"),
#         ("T1189", "Drive-by Compromise"),
#     ],
#     "Execution": [
#         ("T1204", "User Execution"),
#         ("T1218", "System Binary Proxy Execution"),
#         ("T1059", "Command and Scripting Interpreter"),
#         ("T1047", "Windows Management Instrumentation"),
#         ("T1106", "Native API"),
#     ],
#     "Privilege Escalation": [
#         ("T1548", "Abuse Elevation Control Mechanism"),
#         ("T1068", "Exploitation for Privilege Escalation"),
#         ("T1546", "Event Triggered Execution"),
#         ("T1055", "Process Injection"),
#         ("T1134", "Access Token Manipulation"),
#     ],
# }

# TACTICS_ALLOWED = list(TACTIC_TECHNIQUES.keys())

# def pick_technique(tactic: str) -> Tuple[str, str]:
#     """Return (technique_id, technique_name) from the allowed list for a tactic."""
#     pool = TACTIC_TECHNIQUES.get(tactic) or []
#     if not pool:
#         pool = TACTIC_TECHNIQUES["Reconnaissance"]
#     return random.choice(pool)

# def is_valid_technique_for_tactic(tactic: str, technique_id: str) -> bool:
#     """Check if a technique belongs to the given tactic (using our curated map)."""
#     return any(tid == technique_id for tid, _ in TACTIC_TECHNIQUES.get(tactic, []))

# def normalize_tactic(tactic: Optional[str]) -> str:
#     """Coerce incoming strings to a supported tactic; default to Reconnaissance."""
#     if tactic in TACTIC_TECHNIQUES:
#         return tactic
#     # Optional: case-insensitive match
#     if isinstance(tactic, str):
#         for t in TACTIC_TECHNIQUES:
#             if t.lower() == tactic.lower():
#                 return t
#     return "Reconnaissance"

# def get_random_tactic() -> str:
#     """Pick a random allowed tactic."""
#     return random.choice(TACTICS_ALLOWED)

# def next_tactic_round_robin(last_tactic: Optional[str]) -> str:
#     """Cycle deterministically Recon → Initial Access → Execution → Privilege Escalation → Recon."""
#     if last_tactic not in TACTICS_ALLOWED:
#         return "Reconnaissance"
#     i = TACTICS_ALLOWED.index(last_tactic)
#     return TACTICS_ALLOWED[(i + 1) % len(TACTICS_ALLOWED)]
