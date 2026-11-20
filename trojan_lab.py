#!/usr/bin/env python3
# ============================================================
# TROJAN LIFECYCLE LAB — EDUCATIONAL, SAFE, NON-FUNCTIONAL
# ------------------------------------------------------------
# Contains:
#   1. Lifecycle simulation (prints what a RAT *would* do)
#   2. Fixed-interval beacon  (localhost only, port 4444)
#   3. Jittered beacon        (localhost only, port 4445)
#
# SAFETY:
#   - Binds to 127.0.0.1 ONLY
#   - No persistence, no execution, no file access, no exfil
#   - Fixed low-entropy payload, for detection practice only
#
# Usage:
#   python trojan_lab.py simulate
#   python trojan_lab.py beacon-fixed
#   python trojan_lab.py beacon-jitter
# ============================================================

import socket
import subprocess  # imported only to show what we deliberately DON'T do
import sys
import threading
import time
import random

HOST = "127.0.0.1"
FIXED_PORT = 4444
JITTER_PORT = 4445
BASE_INTERVAL = 5.0
JITTER = 2.0
PAYLOAD = b"BEACON"


# ------------------------------------------------------------
# 1) LIFECYCLE SIMULATION
# ------------------------------------------------------------
def banner():
    print("=" * 60)
    print("  EDUCATIONAL TROJAN LIFECYCLE SIMULATION (SAFE)")
    print("  No harmful actions are performed.")
    print("=" * 60)
    time.sleep(1)


def stage_deception():
    print("\n[STAGE 1] DECEPTION / DISGUISE")
    print("  A real Trojan would:")
    print("   - Masquerade as a legitimate file (setup.exe, game_patch.exe)")
    print("   - Use a fake icon and believable filename")
    print("   - Possibly bundle with real software (trojanized installer)")
    print("  ATT&CK: T1036 (Masquerading), T1204 (User Execution)")
    print("  -> THIS SIMULATION DOES NONE OF THIS.")


def stage_execution():
    print("\n[STAGE 2] EXECUTION")
    print("  A real Trojan would:")
    print("   - Start a hidden background process")
    print("   - Optionally spawn a child process to evade detection")
    print("   - Suppress visible windows / console")
    print("  ATT&CK: T1059 (Command & Scripting), T1106 (Native API)")
    print("  -> THIS SIMULATION ONLY PRINTS TEXT.")


def stage_persistence():
    print("\n[STAGE 3] PERSISTENCE")
    print("  A real Trojan would attempt:")
    print("   - Registry Run key:")
    print("       HKCU\\Software\\Microsoft\\Windows\\CurrentVersion\\Run")
    print("   - Startup folder copy:")
    print("       %APPDATA%\\Microsoft\\Windows\\Start Menu\\Programs\\Startup")
    print("   - Scheduled Task creation (schtasks)")
    print("   - Service installation (requires admin)")
    print("  ATT&CK: T1547.001, T1053.005")
    print("  -> THIS SIMULATION MODIFIES NOTHING.")


def stage_c2():
    print("\n[STAGE 4] COMMAND & CONTROL (C2)")
    print("  A real Trojan would:")
    print("   - Open a TCP/UDP socket to an attacker-controlled server")
    print("   - Send periodic heartbeat / beacon packets")
    print("   - Receive commands (shell, download, screenshot)")
    print("   - Possibly use DNS or HTTPS to blend with normal traffic")
    print("  ATT&CK: T1071, T1571")
    print("  -> THIS SIMULATION OPENS NO EXTERNAL SOCKETS.")


def stage_capabilities():
    print("\n[STAGE 5] CAPABILITIES (what the attacker gains)")
    caps = [
        "Remote shell / command execution",
        "File upload and download",
        "Screenshot capture",
        "Keystroke logging",
        "Webcam / microphone access",
        "Credential harvesting",
        "Lateral movement",
    ]
    for c in caps:
        print(f"   - {c}")
    print("  ATT&CK: T1059, T1105, T1113")
    print("  -> THIS SIMULATION IMPLEMENTS NONE OF THESE.")


def stage_evasion():
    print("\n[STAGE 6] EVASION / CLEANUP")
    print("  A real Trojan might:")
    print("   - Delete its dropper after installation")
    print("   - Clear event logs")
    print("   - Detect VMs/sandboxes and stay dormant")
    print("  ATT&CK: T1070, T1497")
    print("  -> THIS SIMULATION DOES NOTHING.")


def run_simulation():
    banner()
    for fn in (stage_deception, stage_execution, stage_persistence,
               stage_c2, stage_capabilities, stage_evasion):
        fn()
        time.sleep(1.2)
    print("\n" + "=" * 60)
    print("  SIMULATION COMPLETE — no harmful action was taken.")
    print("=" * 60)


# ------------------------------------------------------------
# 2) BEACON LAB (shared listener logic)
# ------------------------------------------------------------
def _listener(port, label):
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    s.bind((HOST, port))
    s.listen(1)
    print(f"[Listener:{label}] Listening on {HOST}:{port}")
    conn, addr = s.accept()
    print(f"[Listener:{label}] Client connected: {addr}")
    try:
        while True:
            data = conn.recv(1024)
            if not data:
                break
            print(f"[Listener:{label}] {time.strftime('%H:%M:%S')} "
                  f"received {len(data)} bytes: {data!r}")
    finally:
        conn.close()
        s.close()


def beacon_fixed():
    threading.Thread(target=_listener, args=(FIXED_PORT, "fixed"),
                     daemon=True).start()
    time.sleep(1)
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.connect((HOST, FIXED_PORT))
    print(f"[Client:fixed] Beaconing every {BASE_INTERVAL}s "
          f"(Ctrl+C to stop)")
    try:
        while True:
            s.sendall(PAYLOAD)
            print(f"[Client:fixed] {time.strftime('%H:%M:%S')} "
                  f"sent {len(PAYLOAD)} bytes")
            time.sleep(BASE_INTERVAL)
    except KeyboardInterrupt:
        print("\n[Client:fixed] Stopped.")
    finally:
        s.close()


def beacon_jitter():
    threading.Thread(target=_listener, args=(JITTER_PORT, "jitter"),
                     daemon=True).start()
    time.sleep(1)
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.connect((HOST, JITTER_PORT))
    print(f"[Client:jitter] Beacon: {BASE_INTERVAL}s ± {JITTER}s "
          f"(Ctrl+C to stop)")
    try:
        while True:
            s.sendall(PAYLOAD)
            delay = BASE_INTERVAL + random.uniform(-JITTER, JITTER)
            print(f"[Client:jitter] {time.strftime('%H:%M:%S')} "
                  f"sent (next in {delay:.2f}s)")
            time.sleep(delay)
    except KeyboardInterrupt:
        print("\n[Client:jitter] Stopped.")
    finally:
        s.close()


# ------------------------------------------------------------
# 3) CLI
# ------------------------------------------------------------
USAGE = """\
Usage: python trojan_lab.py <command>

Commands:
  simulate        Print the six-stage RAT lifecycle (no harmful action)
  beacon-fixed    Localhost beacon, fixed 5s interval, port 4444
  beacon-jitter   Localhost beacon, 5s ±2s jitter,  port 4445
"""


def main():
    if len(sys.argv) != 2 or sys.argv[1] in ("-h", "--help"):
        print(USAGE)
        return
    cmd = sys.argv[1]
    if cmd == "simulate":
        run_simulation()
    elif cmd == "beacon-fixed":
        beacon_fixed()
    elif cmd == "beacon-jitter":
        beacon_jitter()
    else:
        print(USAGE)
        sys.exit(1)


if __name__ == "__main__":
    main()
