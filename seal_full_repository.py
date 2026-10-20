import subprocess
import os

print("[*] Staging all untracked CML blueprints, ledgers, and engine modules...")

# Add all files to git tracking
subprocess.run(["git", "add", "."], check=True)
subprocess.run(["git", "commit", "-m", "chore: seal complete Castleberry Bloom repository state and phi-hexagonal engine modules"], check=True)

print("[+] Full repository successfully locked and committed to local git history.")
