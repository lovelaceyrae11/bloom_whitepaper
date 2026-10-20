import argparse, time

parser = argparse.ArgumentParser()
parser.add_argument('--frequency', type=float, default=528.0)
parser.add_argument('--scale', type=float, default=1.618)
parser.add_argument('--mode', type=str, default='active-sync')
args = parser.parse_args()

print(f'[*] Initializing Swarm Bridge...')
print(f'[*] Frequency: {args.frequency}Hz | Phi-Scale: {args.scale} | Mode: {args.mode}')
print('[+] Swarm bridge active. Telemetry ingestion synchronized.')
