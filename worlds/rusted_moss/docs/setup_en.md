# Rusted Moss for Archipelago Setup and Usage Guide

## Required Software
* Latest release of [Archipelago](https://github.com/ArchipelagoMW/Archipelago/releases). Currently tested/working on version 0.4.6.
* The `ArchipelagoRustedMossClient.zip` from the latest [Rusted Moss Archipelago](https://github.com/dgrossmann144/Archipelago/releases) release.
* A legal copy of Rusted Moss version 1.47.
   * Steam version is supported, itch.io version currently untested.
   * These instructions will not work for any past or future versions until updated.

## Downpatching the Steam Version to the Correct Version (1.47)
* General instructions for how to downpatch via steam can be read [here](https://www.makeuseof.com/how-to-downgrade-steam-games/), but the below instructions will be specific for the 1.47 version of Rusted Moss.
1. Open the Steam console by pressing `Win + R` then typing `steam://open/console`.
2. In the Steam console enter the command `download_depot 1772830 1772831 7984789615852015264`. This may take a while to finish.
3. Navigate to the directory that the game was installed to and delete the file `steam_api64.dll`.
   * Alternatively, replace all the files in your Rusted Moss Steam directory with the files downloaded from the steam console and turn off auto update. You  do not have to delete the `steam_api64.dll` if you take this approach.

## Installing the Archipelago Mod to Rusted Moss
1. Run `ArchipelagoRustedMossClient.exe` from the extracted `ArchipelagoRustedMossClient.zip`.
2. In the text box at the bottom enter the command `/patch directory`, where `directory` is the location of the folder containing the data.win file of the 1.47 version of Rusted Moss.
3. Patching successful should be displayed.

## Generating and Hosting a Seed
* If you have not used Archipelago before, I highly recommend reading through the [Archipelago Setup Guide](https://archipelago.gg/tutorial/Archipelago/setup/en) to gain an understanding of how Archipelago works and to better understand the steps below.
1. Download the `rusted_moss.apworld` and `RustedMoss.yaml` files from the latest [Rusted Moss Archipelago](https://github.com/dgrossmann144/Archipelago/releases) release.
2. Put the `rusted_moss.apworld` file in the `/Archipelago/lib/worlds` folder where you installed Archipelago.
3. Edit a copy of the `RustedMoss.yaml` to configure the slot name and game options. Descriptions of the options are contained within.
4. Place the edited `RustedMoss.yaml` in the `/Archipelago/Players` folder.
5. Run `ArchipelagoGenerate.exe` from the `/Archipelago` folder.
6. Upload the `AP_#######.zip` file from `/Archipelago/output` to [Archipelago website](https://archipelago.gg/uploads) to host the game.

## Joining an Archipelago Game in Rusted Moss
* Optional: backup your save files located in `/AppData/Local/Rusted_Moss`
1. Run `ArchipelagoRustedMossClient.exe` from the extracted `ArchipelagoRustedMossClient.zip`.
2. In the text box at the top, type in the connection info and click Connect.
   * If hosting through the Archipelago website, this should be archipelago.gg:\<portNumber\>
3. You will be prompted for a slot name, enter the name field entered in the yaml file you edited. This should establish the connection to the Archipelago server.
4. Open Rusted Moss and create a new file.
   * Testing has only been done in Speedrun mode so far, but I am unaware of any issues that would cause the other modes to fail to work.
5. Picking up an item will still appear to function as it usually would, but will actually send that item in archipelago.