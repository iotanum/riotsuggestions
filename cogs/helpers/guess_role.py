import requests


def pull_data():
    r = requests.get("http://cdn.merakianalytics.com/riot/lol/resources/latest/en-US/championrates.json")
    j = r.json()
    data = {}

    for champion_id, positions in j["data"].items():
        champion_id = int(champion_id)
        play_rates = {}
        for position, rates in positions.items():
            play_rates[position.upper()] = rates["playRate"]
        for position in ("TOP", "JUNGLE", "MIDDLE", "BOTTOM", "UTILITY"):
            if position not in play_rates:
                play_rates[position] = 0.0
        data[champion_id] = play_rates

    return data


def guess_role(data, champ_ids, friendly_team=False):
    all_roles = ['TOP', 'JUNGLE', "MIDDLE", 'BOTTOM', 'UTILITY']

    possible_roles = {'TOP': None, 'JUNGLE': None, "MIDDLE": None, "BOTTOM": None, "UTILITY": None}

    for champ_id, play_rate in data.items():
        for idx in champ_ids:
            if idx == champ_id:
                role_possibility = max([possibility for possibility in data[champ_id].values()])
                for role, possibility in data[champ_id].items():
                    if possibility == role_possibility:
                        possible_roles[role] = champ_id

                    if possible_roles[role] is not None:
                        if possibility > role_possibility:
                            possible_roles[role] = champ_id
                        else:
                            break
                    possible_roles[role] = champ_id
                    break

    for role, champ_id in list(possible_roles.items()):
        if champ_id is None:
            values = list(possible_roles.values())

            if 0 not in values and friendly_team is True:
                my_needed_role_from_msg = all_roles[champ_ids.index(0)]
                possible_roles[my_needed_role_from_msg] = 0

            if possible_roles[role] is None:
                possible_roles[role] = -1

    return possible_roles
