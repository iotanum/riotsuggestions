import requests


def pull_data():
    r = requests.get("https://ddragon.leagueoflegends.com/cdn/10.21.1/data/en_US/champion.json")
    j = r.json()

    return j


def map_to_name(champion_id):
    champion_data = pull_data()

    for champion, information in champion_data["data"].items():
        champ_id = int(information['key'])

        if champ_id == champion_id:
            return champion
