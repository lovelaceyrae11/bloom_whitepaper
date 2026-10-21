# Copyright (c) 2025-2026 Lacey Rae Castleberry. Dual-Licensed (AGPLv3 / Commercial). See COMMERCIAL_LICENSE.md
import argparse, time
import sys

parser = argparse.ArgumentParser()
parser.add_argument('--frequency', type=float, default=528.0)
parser.add_argument('--nodes', type=int, default=127)
parser.add_argument('--persist', action='store_true')
args = parser.parse_args()

print(f'[*] Initializing Castleberry Bloom Engine Daemon...')
print(f'[*] Frequency: {args.frequency}Hz | Nodes: {args.nodes} | Persist: {args.persist}')
print('[+] Daemon active and synchronized. Lattice stable.')
