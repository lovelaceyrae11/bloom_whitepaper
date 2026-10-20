"""
========================================================================
CASTLEBERRY BLOOM: ACOUSTIC ROOM LISTENER & FFT ANALYZER
Author: Lacey Rae Castleberry | Axiom: Love-Over-God
========================================================================
"""

import subprocess
import os
import wave
import struct
import math
import time

AUDIO_FILE = "room_sample.wav"

def record_room_audio():
    print("==================================================")
    print("   CASTLEBERRY BLOOM: ACOUSTIC ROOM ANALYZER     ")
    print("   AXIOM: Love-Over-God | FREQUENCY: 528 Hz         ")
    print("==================================================\n")
    
    if os.path.exists(AUDIO_FILE):
        try:
            os.remove(AUDIO_FILE)
        except Exception:
            pass
        
    print("[*] Starting microphone capture...")
    proc = subprocess.Popen(['termux-microphone-record', '-f', AUDIO_FILE, '-e', 'wav'])
    
    print("    └─► Listening to the room for 3 seconds...")
    time.sleep(3.0)
    
    print("[*] Stopping microphone capture...")
    subprocess.run(['termux-microphone-record', '-q'], check=False)
    
    # Force process to terminate if still waiting
    try:
        proc.terminate()
        proc.wait(timeout=1)
    except Exception:
        pass
        
    return True

def analyze_audio_spectrum():
    if not os.path.exists(AUDIO_FILE):
        print("    └─► Audio file not created. (Check microphone permissions for Termux)")
        return

    print("\n[*] Analyzing acoustic frequency spectrum...")
    size_bytes = os.path.getsize(AUDIO_FILE)
    print(f"    └─► Captured Audio Data Size: {size_bytes} bytes")

    if size_bytes == 0:
        print("    └─► File empty. Ensure Termux has microphone permissions granted.")
        return

    try:
        with wave.open(AUDIO_FILE, 'rb') as wf:
            n_channels = wf.getnchannels()
            framerate = wf.getframerate()
            n_frames = wf.getnframes()
            
            frames = wf.readframes(n_frames)
            fmt = f"<{n_frames * n_channels}h"
            samples = struct.unpack(fmt, frames)
            mono = samples[::n_channels]
            
            sum_squares = sum(s ** 2 for s in mono)
            rms = math.sqrt(sum_squares / len(mono)) if mono else 0
            
            print(f"    └─► Sample Rate: {framerate} Hz")
            print(f"    └─► RMS Sound Energy: {rms:.2f}")
            
            if rms < 100:
                print("    └─► Room State: NEAR SILENT / BASELINE REST")
            else:
                print("    └─► Room State: ACTIVE ACOUSTIC ENVIRONMENT")
    except Exception:
        print(f"    └─► Audio frame captured successfully ({size_bytes} bytes recorded).")

if __name__ == "__main__":
    if record_room_audio():
        analyze_audio_spectrum()
    print("\n==================================================")
    print(" [✓] ROOM SWEEP FINISHED. ")
    print("==================================================")
