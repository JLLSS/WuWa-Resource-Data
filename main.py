import requests
import os
import json

launcher = {
    "cn": {
        "beta": "https://prod-cn-alicdn-gamestarter.kurogame.com/launcher/launcher/10008_Pa0Q0EMFxukjEqX33pF9Uyvdc8MaGPSz/G152/index.json",
        "live": "https://prod-cn-alicdn-gamestarter.kurogame.com/launcher/launcher/10003_Y8xXrXk65DqFHEDgApn3cpK5lfczpFx5/G152/index.json"
    },
    "os": {
        "beta": "https://prod-volcdn-gamestarter.kurogame.net/launcher/launcher/50013_HiDX7UaJOXpKl3pigJwVxhg5z1wllus5/G153/index.json",
        "live": "https://prod-volcdn-gamestarter.kurogame.net/launcher/launcher/50004_obOHXFrFanqsaIEOmuKroCcbZkQRBC7c/G153/index.json"
    }
}

game = {
    "cn": {
        "beta": "https://prod-cn-alicdn-gamestarter.kurogame.com/launcher/game/G152/10008_Pa0Q0EMFxukjEqX33pF9Uyvdc8MaGPSz/index.json",
        "live": "https://prod-cn-alicdn-gamestarter.kurogame.com/launcher/game/G152/10003_Y8xXrXk65DqFHEDgApn3cpK5lfczpFx5/index.json"
    },
    "os": {
        "beta": "https://prod-alicdn-gamestarter.kurogame.com/launcher/game/G153/50013_HiDX7UaJOXpKl3pigJwVxhg5z1wllus5/index.json",
        "live": "https://prod-alicdn-gamestarter.kurogame.com/launcher/game/G153/50004_obOHXFrFanqsaIEOmuKroCcbZkQRBC7c/index.json"
    }
}

def get_launcher_version(url):
    response = requests.get(url)
    data = response.json()
    return data.get("default", {}).get("resource", None).get("version", None), data

def get_game_version(url):
    response = requests.get(url)
    data = response.json()
    return data.get("default", {}).get("config", {}).get("version", None), data

def save_json_to_file(directory, filename, data):
    if not os.path.exists(directory):
        os.makedirs(directory)
    with open(os.path.join(directory, filename), 'w', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False, indent=4)

def process_urls(url_dict, get_version_func, base_dir):
    for region, types in url_dict.items():
        for type_, url in types.items():
            version, data = get_version_func(url)
            if version:
                directory = f"{base_dir}/{region}/{type_}/{version}"
                save_json_to_file(directory, "index.json", data)
                print(f"Saved JSON to {directory}/index.json")
            else:
                print(f"Version not found for {url}")

process_urls(launcher, get_launcher_version, "launcher")
process_urls(game, get_game_version, "game")
