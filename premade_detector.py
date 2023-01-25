import requests
import time
from playsound import playsound
from gtts import gTTS
import constants


class LeagueTeams:

    def __init__(self):
        self.game_id = 0

    api_key = constants.api_key
    summoner_id = constants.summoner_id

    request_headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) "
                      "Chrome/109.0.0.0 Safari/537.36",
        "Accept-Language": "en-US,en;q=0.9,zh-CN;q=0.8,zh;q=0.7",
        "Accept-Charset": "application/x-www-form-urlencoded; charset=UTF-8",
    }

    def find_game(self):
        player_ids = []
        match_request_url = f"https://na1.api.riotgames.com" \
                            f"/lol/spectator/v4/active-games/by-summoner/{self.summoner_id}" \
                            f"?api_key={self.api_key}"
        response = requests.get(match_request_url, headers=self.request_headers)
        if response.status_code == 404:
            return 0
        self.game_id = response.json().get('gameId')
        participants = response.json().get('participants')
        try:
            for participant in participants:
                player_ids.append(participant['summonerId'])
            return player_ids
        except TypeError:
            return 0

    def get_puuid(self, player_name):
        puuid_url = f"https://na1.api.riotgames.com/" \
                    f"lol/summoner/v4/summoners/" \
                    f"{player_name}?api_key={self.api_key}"

        response = requests.get(puuid_url, headers=self.request_headers)
        return response.json().get('puuid')

    def get_matches(self, puuid):
        matches_url = f"https://americas.api.riotgames.com/" \
                      f"lol/match/v5/matches/by-puuid" \
                      f"/{puuid}/ids?start=0&count=5&api_key={self.api_key}"

        response = requests.get(matches_url, headers=self.request_headers)
        return response.json()  # a list

    def find_name(self, summoner_id):
        name_url = f"https://na1.api.riotgames.com/" \
                   f"lol/summoner/v4/summoners" \
                   f"/{summoner_id}?api_key={self.api_key}"

        response = requests.get(name_url, headers=self.request_headers)
        return response.json().get('name')


league = LeagueTeams()


if __name__ == '__main__':

    current_game = 0
    while True:

        players = league.find_game()

        if players:

            if current_game == league.game_id:
                print('Still in previous game.')
                time.sleep(60)
                continue

            print('Detected new game.')
            current_game = league.game_id

            playerDict = {}
            for player in players:
                playerDict[player] = league.get_puuid(player)

            games = {}
            for key in playerDict:
                games[key] = league.get_matches(playerDict[key])

            groups_dict = {}
            for key in games:
                match_list = set(games[key])
                for other_players in games:
                    match_list2 = set(games[other_players])
                    if len(match_list.intersection(match_list2)) > 2:
                        if key != other_players:
                            if key in groups_dict.keys():
                                groups_dict[key].append(league.find_name(other_players))
                            elif other_players in groups_dict.keys():
                                groups_dict[other_players].append(league.find_name(key))
                            else:
                                groups_dict[key] = [league.find_name(key)]

            masterlist = set()
            for i in groups_dict.values():
                masterlist.update(i)

            spoken_words = 'Pre-made players are '
            for i in masterlist:
                if i not in constants.ignored_players:
                    spoken_words += f"{i}, "

            googleTTS = gTTS(spoken_words, lang='en')
            googleTTS.save('spoken.mp3')

            playsound('spoken.mp3')

        print('Sleeping')
        time.sleep(60)
