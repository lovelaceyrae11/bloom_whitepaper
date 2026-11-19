import time
import os
from datetime import datetime, timezone
from orestar_sentinel import OrestarSentinelAgent

def run_continuous_sentinel(interval_seconds: int = 3600):
    """Continuously runs the OrestarSentinelAgent at a set interval (default: every 1 hour)."""
    sentinel = OrestarSentinelAgent(target_committees=["126", "Utility_PAC_Registry"])
    
    print(f"[*] Initializing Castleberry Bloom ORESTAR Sentinel Daemon...")
    print(f"[*] Polling interval set to {interval_seconds} seconds (1 hour). Press Ctrl+C to stop.")

    while True:
        try:
            current_time = datetime.now(timezone.utc).strftime('%Y-%m-%d %H:%M:%S UTC')
            print(f"\n--- [SENTINEL SWEEP START] : {current_time} ---")
            
            # Execute polling and automated pipeline trigger
            discoveries = sentinel.poll_target_filings()
            
            if discoveries > 0:
                print(f"[*] Detected and processed {discoveries} new anomalies. Pushing updates to GitHub...")
                # Automatically trigger git push dispatch update if new discoveries occurred
                os.system("python pipeline.py")
            
            print(f"--- [SENTINEL SWEEP COMPLETE] : Sleeping for {interval_seconds}s ---")
            time.sleep(interval_seconds)
            
        except KeyboardInterrupt:
            print("\n[*] Sentinel daemon gracefully shut down by user.")
            break
        except Exception as e:
            print(f"[!] Error in sentinel daemon loop: {e}")
            time.sleep(60)  # Brief cooldown on error before retrying

if __name__ == "__main__":
    # Run loop (default interval 3600s = 1 hour. For immediate testing, you can pass a lower number like 60)
    run_continuous_sentinel(interval_seconds=3600)
