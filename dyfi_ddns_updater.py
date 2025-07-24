#!/usr/bin/env python3

import os
import time
import random
import argparse
import requests
import base64
import re
from pathlib import Path

STATE_DIR = "/data"
CHECKIP_URL = "http://checkip.dy.fi/"

# 6 days in seconds (refresh before 7-day expiry, with random jitter)
UPDATE_INTERVAL = 6 * 24 * 60 * 60

def log(msg):
    timestamp = time.strftime('%Y-%m-%d %H:%M:%S')
    line = f"[{timestamp}] {msg}"
    print(line)

def get_public_ip():
    try:
        resp = requests.get(CHECKIP_URL, timeout=10)
        resp.raise_for_status()
        # Use regex to extract IP address from HTML
        match = re.search(r'Current IP Address:\s*([\d\.]+)', resp.text)
        ip = match.group(1) if match else None
        log(f"[get_public_ip]: current IP is {ip}")
        if not ip or len(ip.split(".")) != 4:
            raise ValueError("Failed to parse IP from dy.fi checkip page")
        return ip
    except Exception as e:
        log(f"[get_public_ip]: error: {e}")
        return None

def load_state(host):
    state_file = Path(STATE_DIR) / f"dyfi_{host.replace('.', '_')}.state"
    if not state_file.exists():
        return None, 0
    try:
        with open(state_file, "r") as f:
            line = f.read().strip()
            ip, ts = line.split(",")
            return ip, float(ts)
    except Exception:
        return None, 0

def save_state(host, ip):
    state_file = Path(STATE_DIR) / f"dyfi_{host.replace('.', '_')}.state"
    state_file.parent.mkdir(parents=True, exist_ok=True)
    with open(state_file, "w") as f:
        f.write(f"{ip},{time.time()}")

def update_dyfi(username, password, host):
    url = f"https://www.dy.fi/nic/update?hostname={host}"
    auth = base64.b64encode(f"{username}:{password}".encode()).decode()
    try:
        resp = requests.get(url, headers={"Authorization": f"Basic {auth}"}, timeout=30)
        log(f"[{host}] dy.fi update sent, status: {resp.status_code}, response: {resp.text.strip()}")
        return resp.status_code == 200
    except Exception as e:
        log(f"[{host}] dy.fi update error: {e}")
        return False

def main():
    parser = argparse.ArgumentParser(description="dy.fi multi-host DDNS updater")
    parser.add_argument("-u", "--username", type=str, default=os.environ.get("DYFI_USER"), help="dy.fi username")
    parser.add_argument("-p", "--password", type=str, default=os.environ.get("DYFI_PASS"), help="dy.fi password")
    parser.add_argument("-n", "--hosts", type=str, default=os.environ.get("DYFI_HOSTS"), help="Comma-separated dy.fi hostnames")
    parser.add_argument("--interval", type=int, default=600, help="IP check interval (seconds)")
    args = parser.parse_args()

    username = args.username
    password = args.password
    hosts = [h.strip() for h in (args.hosts or "").split(",") if h.strip()]
    if not username or not password or not hosts:
        log("Username, password, and at least one hostname are required (via args or env)")
        exit(1)

    log(f"Starting dy.fi updater for: {', '.join(hosts)}")

    while True:
        ip = get_public_ip()
        if not ip:
            log("Could not get current IP. Will retry...")
            time.sleep(args.interval)
            continue

        now = time.time()
        for host in hosts:
            last_ip, last_update = load_state(host)
            time_since_update = now - last_update
            # Add jitter of +/- 1 hour for each host to avoid a thundering herd
            interval_jitter = UPDATE_INTERVAL + random.randint(-3600, 3600)
            need_update = (ip != last_ip) or (time_since_update > interval_jitter)
            if need_update:
                success = update_dyfi(username, password, host)
                if success:
                    save_state(host, ip)
            else:
                log(f"[{host}] No update needed (IP {ip} unchanged, last update {int(time_since_update/3600)}h ago)")
        time.sleep(args.interval)

if __name__ == "__main__":
    main()