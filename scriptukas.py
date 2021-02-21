import os
import base64
import json
import ssl
import sys
import urllib.error
import subprocess
from urllib.request import Request, urlopen
from urllib import parse


def find_riot_games_path():
    directories = ["C:/", "D:/"]
    found_league_path = False

    for directory in directories:
        for folder_name in os.listdir(directory):
            if "Riot" in folder_name:
                riot_games_full_path = f"{directory}/{folder_name}"
                found_league_path = True
                break
        if found_league_path:
            break

    return riot_games_full_path


def find_league_of_legends_path():
    riot_games_path = find_riot_games_path()

    for game in os.listdir(riot_games_path):
        if "League" in game:
            league_full_path = f"{riot_games_path}/{game}"

    return league_full_path


def find_lock_file(league_full_path):
    lock_file_path = None

    for file in os.listdir(league_full_path):
        if file == "lockfile":
            lock_file_path = f"{league_full_path}/{file}"
            break

    if not lock_file_path:
        print("Looks like League of Legends is not turned on!")
        sys.exit()

    return lock_file_path


def read_and_parse_lock_file(league_file_path):
    lock_file_path = find_lock_file(league_file_path)

    lockfile = open(lock_file_path, encoding='UTF-8').read()
    lockfile = lockfile.split(":")

    return lockfile


def find_and_prepare_for_client_api():
    league_file_path = find_league_of_legends_path()
    lockfile = read_and_parse_lock_file(league_file_path)

    # Parse and prepare for requests
    client_api_port = lockfile[2]
    client_api_password = lockfile[3]
    client_api_auth_header = f"riot:{client_api_password}"
    client_api_auth_header = base64.b64encode(client_api_auth_header.encode())
    client_api_auth_header = client_api_auth_header.decode()

    return {"port": client_api_port, "header": client_api_auth_header}


def check_current_champ_select_session():
    api = find_and_prepare_for_client_api()

    client_api_root = f"https://127.0.0.1:{api['port']}"
    current_summer_path = "/lol-summoner/v1/current-summoner"
    champ_select_path = "/lol-champ-select/v1/session"

    context = ssl._create_unverified_context()

    req_current = Request(client_api_root + current_summer_path)
    req_current.add_header("Authorization", "Basic " + api['header'])

    req = Request(client_api_root + champ_select_path)
    req.add_header("Authorization", "Basic " + api['header'])

    try:
        # content_summoner = urlopen(req_current, context=context)
        # summoner = json.load(content_summoner)
        #
        # content = urlopen(req, context=context)
        # champ_select_session = json.load(content)

        champ_select_session = {'actions': [[{'actorCellId': 0, 'championId': 777, 'completed': True, 'id': 0, 'isAllyAction': False, 'isInProgress': False, 'type': 'ban'}, {'actorCellId': 1, 'championId': 35, 'completed': True, 'id': 1, 'isAllyAction': False, 'isInProgress': False, 'type': 'ban'}, {'actorCellId': 2, 'championId': 114, 'completed': True, 'id': 2, 'isAllyAction': False, 'isInProgress': False, 'type': 'ban'}, {'actorCellId': 3, 'championId': 24, 'completed': True, 'id': 3, 'isAllyAction': False, 'isInProgress': False, 'type': 'ban'}, {'actorCellId': 4, 'championId': 81, 'completed': True, 'id': 4, 'isAllyAction': False, 'isInProgress': False, 'type': 'ban'}, {'actorCellId': 5, 'championId': 86, 'completed': True, 'id': 5, 'isAllyAction': True, 'isInProgress': False, 'type': 'ban'}, {'actorCellId': 6, 'championId': 25, 'completed': True, 'id': 6, 'isAllyAction': True, 'isInProgress': False, 'type': 'ban'}, {'actorCellId': 7, 'championId': 875, 'completed': True, 'id': 7, 'isAllyAction': True, 'isInProgress': False, 'type': 'ban'}, {'actorCellId': 8, 'championId': 360, 'completed': True, 'id': 8, 'isAllyAction': True, 'isInProgress': False, 'type': 'ban'}, {'actorCellId': 9, 'championId': 38, 'completed': True, 'id': 9, 'isAllyAction': True, 'isInProgress': False, 'type': 'ban'}], [{'actorCellId': -1, 'championId': 0, 'completed': True, 'id': 103, 'isAllyAction': False, 'isInProgress': False, 'type': 'ten_bans_reveal'}], [{'actorCellId': 0, 'championId': 103, 'completed': True, 'id': 10, 'isAllyAction': False, 'isInProgress': False, 'type': 'pick'}], [{'actorCellId': 5, 'championId': 0, 'completed': False, 'id': 11, 'isAllyAction': True, 'isInProgress': True, 'type': 'pick'}, {'actorCellId': 6, 'championId': 0, 'completed': False, 'id': 12, 'isAllyAction': True, 'isInProgress': True, 'type': 'pick'}], [{'actorCellId': 1, 'championId': 0, 'completed': False, 'id': 13, 'isAllyAction': False, 'isInProgress': False, 'type': 'pick'}, {'actorCellId': 2, 'championId': 0, 'completed': False, 'id': 14, 'isAllyAction': False, 'isInProgress': False, 'type': 'pick'}], [{'actorCellId': 7, 'championId': 122, 'completed': False, 'id': 15, 'isAllyAction': True, 'isInProgress': False, 'type': 'pick'}, {'actorCellId': 8, 'championId': 0, 'completed': False, 'id': 16, 'isAllyAction': True, 'isInProgress': False, 'type': 'pick'}], [{'actorCellId': 3, 'championId': 0, 'completed': False, 'id': 17, 'isAllyAction': False, 'isInProgress': False, 'type': 'pick'}, {'actorCellId': 4, 'championId': 0, 'completed': False, 'id': 18, 'isAllyAction': False, 'isInProgress': False, 'type': 'pick'}], [{'actorCellId': 9, 'championId': 0, 'completed': False, 'id': 19, 'isAllyAction': True, 'isInProgress': False, 'type': 'pick'}]], 'allowBattleBoost': False, 'allowDuplicatePicks': False, 'allowLockedEvents': False, 'allowRerolling': False, 'allowSkinSelection': True, 'bans': {'myTeamBans': [], 'numBans': 0, 'theirTeamBans': []}, 'benchChampionIds': [], 'benchEnabled': False, 'boostableSkinCount': 0, 'chatDetails': {'chatRoomName': 'c7a21eb8-d2f3-4c81-b1a6-bcd4488687e2@champ-select.pvp.net', 'chatRoomPassword': None}, 'counter': 19, 'entitledFeatureState': {'additionalRerolls': 0, 'unlockedSkinIds': []}, 'gameId': 4888056023, 'hasSimultaneousBans': True, 'hasSimultaneousPicks': False, 'isCustomGame': False, 'isSpectating': False, 'localPlayerCellId': 5, 'lockedEventIndex': -1, 'myTeam': [{'assignedPosition': 'jungle', 'cellId': 5, 'championId': 0, 'championPickIntent': 0, 'entitledFeatureType': 'NONE', 'selectedSkinId': 0, 'spell1Id': 4, 'spell2Id': 11, 'summonerId': 36701619, 'team': 2, 'wardSkinId': 1}, {'assignedPosition': 'bottom', 'cellId': 6, 'championId': 0, 'championPickIntent': 0, 'entitledFeatureType': 'NONE', 'selectedSkinId': 0, 'spell1Id': 4, 'spell2Id': 7, 'summonerId': 108616999, 'team': 2, 'wardSkinId': -1}, {'assignedPosition': 'top', 'cellId': 7, 'championId': 0, 'championPickIntent': 122, 'entitledFeatureType': 'NONE', 'selectedSkinId': 0, 'spell1Id': 4, 'spell2Id': 6, 'summonerId': 58248219, 'team': 2, 'wardSkinId': -1}, {'assignedPosition': 'utility', 'cellId': 8, 'championId': 0, 'championPickIntent': 0, 'entitledFeatureType': 'NONE', 'selectedSkinId': 0, 'spell1Id': 3, 'spell2Id': 4, 'summonerId': 52512503, 'team': 2, 'wardSkinId': -1}, {'assignedPosition': 'middle', 'cellId': 9, 'championId': 0, 'championPickIntent': 0, 'entitledFeatureType': 'NONE', 'selectedSkinId': 0, 'spell1Id': 4, 'spell2Id': 14, 'summonerId': 22220026, 'team': 2, 'wardSkinId': -1}], 'rerollsRemaining': 0, 'skipChampionSelect': False, 'theirTeam': [{'assignedPosition': '', 'cellId': 0, 'championId': 103, 'championPickIntent': 0, 'entitledFeatureType': '', 'selectedSkinId': 103000, 'spell1Id': 0, 'spell2Id': 0, 'summonerId': 0, 'team': 1, 'wardSkinId': -1}, {'assignedPosition': '', 'cellId': 1, 'championId': 0, 'championPickIntent': 0, 'entitledFeatureType': '', 'selectedSkinId': 0, 'spell1Id': 0, 'spell2Id': 0, 'summonerId': 0, 'team': 1, 'wardSkinId': -1}, {'assignedPosition': '', 'cellId': 2, 'championId': 0, 'championPickIntent': 0, 'entitledFeatureType': '', 'selectedSkinId': 0, 'spell1Id': 0, 'spell2Id': 0, 'summonerId': 0, 'team': 1, 'wardSkinId': -1}, {'assignedPosition': '', 'cellId': 3, 'championId': 0, 'championPickIntent': 0, 'entitledFeatureType': '', 'selectedSkinId': 0, 'spell1Id': 0, 'spell2Id': 0, 'summonerId': 0, 'team': 1, 'wardSkinId': -1}, {'assignedPosition': '', 'cellId': 4, 'championId': 0, 'championPickIntent': 0, 'entitledFeatureType': '', 'selectedSkinId': 0, 'spell1Id': 0, 'spell2Id': 0, 'summonerId': 0, 'team': 1, 'wardSkinId': -1}], 'timer': {'adjustedTimeLeftInPhase': 29995, 'internalNowInEpochMs': 1603623285651, 'isInfinite': False, 'phase': 'BAN_PICK', 'totalTimeInPhase': 30000}, 'trades': []}
        summoner = {}
        summoner['summonerId'] = 36701619

        print(summoner['summonerId'])
        print(champ_select_session)
        return summoner['summonerId'], champ_select_session
    except urllib.error.HTTPError:
        print("Looks like you're not in a champion select!")
        sys.exit()


def parse_champion_picks(champ_select_session, team="myTeam", summoner_id=None):
    team_picks = {'top': None, 'jungle': None, "middle": None, 'bottom': None, 'utility': None}
    for my_team_pick in champ_select_session[team]:
        if team is 'myTeam':
            team_role = my_team_pick['championPickIntent'] if my_team_pick['championId'] is 0 else my_team_pick['championId']
            team_picks[my_team_pick['assignedPosition']] = -1 if team_role is 0 else team_role

        else:
            for role, champ_id in list(team_picks.items()):
                if champ_id is None:
                    team_picks[role] = -1 if my_team_pick['championId'] is 0 else my_team_pick['championId']
                    break

        if team is not 'theirTeam':
            if summoner_id and my_team_pick['summonerId'] == summoner_id:
                team_picks[my_team_pick['assignedPosition']] = 0

    return team_picks


def copy_to_clipboard(my_team, enemy_team):
    my_team_picks = " ".join(str(x) for x in my_team.values())
    their_team_picks = " ".join(str(y) for y in enemy_team.values())

    command_text = f'!pick ({my_team_picks} : {their_team_picks})'
    subprocess.Popen(f'echo {command_text} | clip', shell=True)

    post_request(my_team, enemy_team)


def post_request(my_team, enemy_team):
    data = parse.urlencode({**my_team, **enemy_team}).encode()
    req = Request("http://localhost:8090/get", data=data)
    resp = urlopen(req)


if __name__ == '__main__':
    summoner_id, champ_select_session = check_current_champ_select_session()

    my_team_picks = parse_champion_picks(champ_select_session, summoner_id=summoner_id)
    their_team_picks = parse_champion_picks(champ_select_session, team="theirTeam")

    copy_to_clipboard(my_team_picks, their_team_picks)
    print(f"My team: {my_team_picks}", f"\nTheir team: {their_team_picks}")
