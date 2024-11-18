[Usage]
This program is designed to create a list of installed mods from a vortex backup file. Originally created by LoneRaptor, I've added two significant features:
* The ability to generate a mod list of only mods that are enabled,
* The ability to generate a mod list per profile per game.
  

NEXUS MODS LINK: https://www.nexusmods.com/site/mods/1095?tab=description

*** *DISCLAIMER* This mod is very much in a beta state. I originally modified the modlist exporter for my own use, and saw that many comments requested the same features I wanted to implement. The program has only been tested exporting one game's profiles at a time. If you select more than one game at a time it may break the program. Please feel free to submit bug reports and I will continue to upload updates as I get around to fixing things and implementing features. ***

UPDATED INSTRUCTIONS:
To create a list of mods per game run the executable and select a vortex backup file.

*-Vortex creates these automatically in user\AppData\Roaming\Vortex\temp\state_backups_full.
*-You can also manually make a backup to any location you want in settings/workarounds -> create backup
-Select a game from the top list of detected games
-Select one or more profiles from the list of detected profiles (the list will populate once you select a game.)
-Enable or disable "Export only enabled" checkbox to get a text file including disabled mods or not.
-The mod will generate a list of mods per profile selected, separated by the next profile's name, and some dashes to delineate between profiles.


-------------------------------------------------------------------------------------------------------------------

OLD INSTRUCTIONS: (relevant if you choose only a game from the top list, and don't select any profiles)
Copied verbatim from LoneRaptor's : https://www.nexusmods.com/site/mods/485?tab=description

[installation]
- no installation required just extract somewhere and run the Vortex_Exporter.exe

To create a list of mods per game run the executable and select a vortex backup file.
- select one or more games from the list of detected games (the all option exports a list for every game that is detected).
- the export options add additional information to the export if available.
- select a destination for the exported files default is the export folder.
- The program will create separate a timestamped file for every selected game in the chosen directory.



TODO:
Add CSV as an export option
Add error handling for bad json files/ other missed cases
