# Cynara-Discord-Bot
### Requirements
```pip install asyncio tinydb discord[voice] praw youtube-dl```
```sudo apt-get install ffmpeg libopus-dev libffi-dev libsodium-dev```
```python 3.5 or greater```

### Running
1. Clone using ```git clone https://github.com/Daltz333/Cynara-Discord-Bot.git```
2. Add your bot token to the ```constants.py``` file
3. Run bot using ```python bot.py``` or ```python3 bot.py```
4. Add the bot to your server.

### Commands
```.help - Displays help message```  
```.setlvl [@USERNAME] [LEVEL] - Sets a users level```  
```.setrole [ROLENAME] [LEVEL - Gives user specified role at level```  
```.delrole [ROLENAME] - Deletes role from database```  
```.ping - returns the estimated bot ping```  
```.lvl [@USERNAME] - Returns specified user's level.```  
```.say [RANDOM TEXT] - Makes the bot say something```  
```.leaderboard - Displays the top ten users on the server```  

### Upcoming
1. .daily command (restricted to level set by server owner)
2. Per server configuration (bot is able to be used on more than one server)
3. Put database in same directory as bot on linux
4. Code cleanup
5. Fix bug where when users type after a player has leveled up, and the bot hasn't said the "congrats" message yet, that the bot will congratulation the wrong users
6. Configure how much xp per message user gets (server owner)
7. Give specified user specified xp for being in voice for specified amount of time
8. Server owner can change prefix
