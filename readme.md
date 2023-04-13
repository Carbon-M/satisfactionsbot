
# Satisfactions Bot

A bot for Discord to make your next Satisfactory playthrough a little more interesting

With this bot, you can create factions in Discord and invite any member of the server to join your faction. There is also a point tracking system, intended to be used to award a faction a point for completing a space elevator stage.

The goal is to complete the most amount of stages and the winner is the faction with the most stages complete once all stages are finished.

Unfortunately do to limitations in Satisfactory Modding with multiplayer, this can not integrate directly into the game and relies on self reporting and an honor system. 
That's why this bot is only recommended to be used in small groups and either in a private server, or private section of a public server.

Once you're able to use mods with multiplayer in Satisfactory, I will update this bot to add integration with a Satisfactory Mod to greatly increase the user experience.  

## Features

- Manage factions including creation, renaming, user management, and deletion
- Each faction receives a private channel/role only given to members
- TBD

## Setup and Environment Variables

To run this project, first you will need to create an application in the Discord Developer Port, along with a companion Bot.

You will then need to add the following environment variables to your .env file

`DISCORD_TOKEN` - The Bot token from your Discord Application  
`CMD_PREFIX` - The prefix to use for commands  
`DB_HOST` - The database host ip  
`DB_PORT` - The database port  
`DB_USER` - The username to use for accessing the database  
`DB_PASSWORD` - The password for the specified user account   

## Documentation

[Documentation](https://github.com/Carbon-M/satisfactionsbot/wiki)