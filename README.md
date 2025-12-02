# Rename Home Assistant entities

I don't know why, but some Home Assistant entities have name without IEEE (naming based on the "friendly name").

Real example: you can look at your entities at http://homeassistant.local:8123/config/entities

Some of them I'd like to rename to use IEEE, for instance:
```
select.temp_hum_temperature_units -> select.0xc4d8c8fffe1940fd_temperature_units
sensor.manipulator_hall_linkquality -> sensor.0x00124b0035670bcb_linkquality
```

Home Assistant has the entities file `/config/.storage/core.entity_registry`.
This script uses this file to find entities without IEEE and rename them using Home Assistant API.

# Install
SSH to Home Assistant host. Download and unzip the script https://github.com/Alexey-Tsarev/rename_ha_registry_entities/archive/refs/heads/master.zip to `/share/rename_ha_registry_entities` directory.
```
apk add py3-virtualenv
cd /share/rename_ha_registry_entities
virtualenv .venv
. .venv/bin/activate
pip3 install -r requirements.txt
```

# Run
```
cd /share/rename_ha_registry_entities
. .venv/bin/activate
```
## Dry Run
```
./rename_ha_registry_entities.py
```
```
unique_id: 0xa4c138b8b9fe6983_mode_zigbee2mqtt
entity_id: sensor.finger_bot_mode
ieee: 0xa4c138b8b9fe6983
domain: sensor
suffix: mode
sensor.finger_bot_mode -> sensor.0xa4c138b8b9fe6983_mode

unique_id: 0xa4c138b8b9fe6983_linkquality_zigbee2mqtt
entity_id: sensor.finger_bot_linkquality
ieee: 0xa4c138b8b9fe6983
domain: sensor
suffix: linkquality
sensor.finger_bot_linkquality -> sensor.0xa4c138b8b9fe6983_linkquality

unique_id: 0xa4c138b8b9fe6983_last_seen_zigbee2mqtt
entity_id: sensor.finger_bot_last_seen
ieee: 0xa4c138b8b9fe6983
domain: sensor
suffix: last_seen
sensor.finger_bot_last_seen -> sensor.0xa4c138b8b9fe6983_last_seen
```

## Dry Run (short)
```
./rename_ha_registry_entities.py | grep "\->"
```
```
sensor.finger_bot_mode -> sensor.0xa4c138b8b9fe6983_mode
sensor.finger_bot_linkquality -> sensor.0xa4c138b8b9fe6983_linkquality
sensor.finger_bot_last_seen -> sensor.0xa4c138b8b9fe6983_last_seen
```

# Run
Due to the script uses Home Assistant API, you need to provide a token from this page: http://homeassistant.local:8123/profile/security
```
cd /share/rename_ha_registry_entities
. .venv/bin/activate
TOKEN=<TOKEN> ./rename_ha_registry_entities.py
```
```
unique_id: 0xa4c1380a1658f227_switch_type_zigbee2mqtt
entity_id: sensor.relay_corridor_2_old_switch_type
ieee: 0xa4c1380a1658f227
domain: sensor
suffix: switch_type
sensor.relay_corridor_2_old_switch_type -> sensor.0xa4c1380a1658f227_switch_type
Auth Response: {"type":"auth_required","ha_version":"2025.11.3"}
Update Response: {"type":"auth_ok","ha_version":"2025.11.3"}

unique_id: 0xa4c138a0ef36d1dd_radar_sensitivity_zigbee2mqtt
entity_id: sensor.human_presence_toilet_24g_radar_sensitivity
ieee: 0xa4c138a0ef36d1dd
domain: sensor
suffix: radar_sensitivity
sensor.human_presence_toilet_24g_radar_sensitivity -> sensor.0xa4c138a0ef36d1dd_radar_sensitivity
Auth Response: {"type":"auth_required","ha_version":"2025.11.3"}
Update Response: {"type":"auth_ok","ha_version":"2025.11.3"}

unique_id: 0xa4c138a0ef36d1dd_presence_sensitivity_zigbee2mqtt
entity_id: sensor.human_presence_toilet_24g_presence_sensitivity
ieee: 0xa4c138a0ef36d1dd
domain: sensor
suffix: presence_sensitivity
sensor.human_presence_toilet_24g_presence_sensitivity -> sensor.0xa4c138a0ef36d1dd_presence_sensitivity
Auth Response: {"type":"auth_required","ha_version":"2025.11.3"}
Update Response: {"type":"auth_ok","ha_version":"2025.11.3"}
```

Good luck!
