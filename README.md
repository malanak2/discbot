# DiscBot
## Features

### For fun

#### /ping command!
    By using /ping, the bot replies with pong! (If admin role present, bot adds its latency to the reply)
    
#### /roll command!
    /roll rolls a 100 sided dice, and if you roll 42, you might get a role!

### For server managment
#### !These commands require the sender to have admin role!
#### /addrole
    adds specified role to specified user
    
#### /removerole
    removes specified role from specified user
    
#### /purge
    Asks the sender if he is sure, if yes, it deletes all messages in channel (Due to discord bot interactions limit, it will take some time)
    
#### /writelog
    Writes a log file, this includes: All admin commands usage + rolling 42 on /roll commands, all chat messages and when somebody edits or deletes a message! The log file name will be the date and time of the creation
    
## Required packages
                
1. [discord.py](https://pypi.org/project/discord.py/)
2. [dotenv](https://pypi.org/project/python-dotenv/)
                

## Thanks for using discbot!

# By malanak, 2022
