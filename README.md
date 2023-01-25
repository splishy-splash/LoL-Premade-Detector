# LoL-Premade-Detector
Automatically detects which players in your match are buddies and blasts it over computer speakers.

Requires constants.py which is just 3 fields: 

api_key = ''  # Get this from Riot

The 'id' field of your character: https://developer.riotgames.com/apis#summoner-v4/GET_getBySummonerName
summoner_id = ""  

The SummonerName of you and your friends so you don't hear it out loud every game. 
ignored_players = ('', '', '')


Additionally, it does require these imports: gTTS, playsound, requests, and time. 
