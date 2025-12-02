#!/usr/bin/env python3

import asyncio
import json
import os
import re
import requests
import websockets

ENTITY_REGISTRY_FILE = os.getenv('ENTITY_REGISTRY_FILE', '/config/.storage/core.entity_registry')
HOST = os.getenv('HOST', '127.0.0.1')
PORT = os.getenv('PORT', '8123')
TOKEN = os.getenv('TOKEN', False)


def get_api(api_suffix=""):
    url = f"http://{HOST}:{PORT}/api/{api_suffix}"
    print(f"GET: {url}")

    h = {
        "Authorization": f"Bearer {TOKEN}",
    }

    return requests.get(url, headers=h)


async def ws_api_rename_entity(e_id, new_e_id):
    async with websockets.connect(f"ws://{HOST}:{PORT}/api/websocket") as websocket:
        await websocket.send(json.dumps({
            "type": "auth",
            "access_token": TOKEN
        }))

        auth_response = await websocket.recv()

        print(f"Auth Response: {auth_response}")

        await websocket.send(json.dumps({
            "id": 1,
            "type": "config/entity_registry/update",
            "entity_id": e_id,
            "new_entity_id": new_e_id,
        }))
        update_response = await websocket.recv()
        print(f"Update Response: {update_response}")


def print_and_check_status_code(response):
    print(f"{response.status_code} -> {response.text}")
    if response.status_code != 200:
        print("Error, returned code not 200. Exit 1")
        exit(1)


if TOKEN:
    print_and_check_status_code(get_api())
    print()

with open(ENTITY_REGISTRY_FILE, "r") as f:
    data = json.load(f)

changed = 0

for ent in data["data"]["entities"]:
    unique_id = ent.get("unique_id", "")
    entity_id = ent.get("entity_id", "")

    # Detect unique_id starts from IEEE (example: 0x70ac08fffe3e78d3_battery_zigbee2mqtt)
    m = re.search(r"^0x[0-9a-fA-F]{16}", unique_id)

    if not m:
        continue

    ieee = m.group(0)

    print(f"unique_id: {unique_id}")
    print(f"entity_id: {entity_id}")
    print(f"ieee: {ieee}")

    domain = entity_id.split(".")[0]
    print(f"domain: {domain}")

    suffix = unique_id
    suffix = suffix.replace("_zigbee2mqtt", "")
    suffix = suffix.replace(f"{ieee}_{domain}_", "")
    suffix = suffix.replace(f"{ieee}_{domain}", "")
    suffix = suffix.replace(f"{ieee}_", "")
    print(f"suffix: {suffix}")

    if domain != suffix and suffix != "":
        new_entity_id = f"{domain}.{ieee}_{suffix}"
    else:
        new_entity_id = f"{domain}.{ieee}"

    if entity_id != new_entity_id:
        print(f"{entity_id} -> {new_entity_id}")
        ent["entity_id"] = new_entity_id

        if TOKEN:
            asyncio.run(ws_api_rename_entity(entity_id, new_entity_id))

        changed += 1

    print()

print(f"Processed entities: {changed}")
