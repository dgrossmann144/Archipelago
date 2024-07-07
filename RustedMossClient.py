import os
import asyncio
import typing
import bsdiff4
import hashlib

import Utils

from worlds.rusted_moss.Utils import gameLocationToLocationName
from worlds import AutoWorldRegister
from NetUtils import NetworkItem, ClientStatus
from CommonClient import ClientCommandProcessor, CommonContext, \
    server_loop, get_base_parser, gui_enabled
from MultiServer import mark_raw

RAWDATAHASH: str = "e435e374cab856df1b1f00570347b6ff"
MODDEDDATAHASH: str = "75c2c65539d7e43b329bc5e950d03138"

# TODO add command for resyncing items/locations
class RustedMossCommandProcessor(ClientCommandProcessor):
    def __init__(self, ctx):
        super().__init__(ctx)

    @mark_raw
    def _cmd_patch(self, directory: str = ""):
        """Provide path to game install folder to patch the data.win file to modify the game."""
        if isinstance(self.ctx, RustedMossContext):
            dataWinPath = os.path.join(directory, "data.win")
            if not os.path.isfile(dataWinPath):
                self.output("ERROR: Could not find data.win file to patch in the folder provided.")
            else:
                basemd5 = hashlib.md5()
                with open(dataWinPath, "rb") as file:
                    base_data_bytes = bytes(file.read())
                    file.close()
                basemd5.update(base_data_bytes)
                if RAWDATAHASH != basemd5.hexdigest():
                    self.output("ERROR: MD5 hash of data.win file does not match correct hash. Make sure you have downpatched to the correct version (1.47)")
                else:
                    bsdiff4.file_patch_inplace(dataWinPath, os.path.join(os.getcwd(), "data/rusted_moss_patch.bsdiff"))
                    moddedmd5 = hashlib.md5()
                    with open(dataWinPath, "rb") as file:
                        modded_data_bytes = bytes(file.read())
                        file.close()
                    moddedmd5.update(modded_data_bytes)
                    if MODDEDDATAHASH != moddedmd5.hexdigest():
                        self.output("ERROR: MD5 hash of moddified data.win file does not match correct hash. Try again or contact mod owner.")
                    else:
                        self.output("Patching successful")


class RustedMossContext(CommonContext):
    tags = {"AP"}
    game = "Rusted Moss"
    command_processor = RustedMossCommandProcessor
    items_handling = 0b111
    save_game_folder = os.path.expandvars(r"%localappdata%/Rusted_Moss")
    deathlink_status = False
    titania_pieces_required = 0
    hard_maya = False

    def __init__(self, server_address, password):
        super().__init__(server_address, password)
        self.game = "Rusted Moss"
        self.got_deathlink = False
        self.save_game_folder = os.path.expandvars(r"%localappdata%/Rusted_Moss")
        self.deathlink_status = False
        self.hard_maya = False
        self.ending = 0

    async def server_auth(self, password_requested: bool = False):
        if password_requested and not self.password:
            await super().server_auth(password_requested)
        await self.get_username()
        await self.send_connect()

    def clear_rusted_moss_files(self):
        path = self.save_game_folder
        self.finished_game = False
        for root, dirs, files in os.walk(path):
            for file in files:
                if file in ["deathlinkFromClient", "deathlinkFromServer", "checkedLocations", "receivedItems", "newItems", "scoutLocations", "newLocations", "endingAchieved"]:
                    os.remove(os.path.join(root, file))

    async def connect(self, address: typing.Optional[str] = None):
        self.clear_rusted_moss_files()
        await super().connect(address)

    async def disconnect(self, allow_autoreconnect: bool = False):
        self.clear_rusted_moss_files()
        await super().disconnect(allow_autoreconnect)

    async def connection_closed(self):
        self.clear_rusted_moss_files()
        await super().connection_closed()

    async def shutdown(self):
        self.clear_rusted_moss_files()
        await super().shutdown()

    def on_package(self, cmd: str, args: dict):
        if cmd == "Connected":
            self.game = self.slot_info[self.slot].game
        Utils.async_start(process_rusted_moss_cmd(self, cmd, args))

    def run_gui(self):
        from kvui import GameManager

        class RustedMossManager(GameManager):
            logging_pairs = [
                ("Client", "Archipelago")
            ]
            base_title = "Archipelago Rusted Moss Client"

        self.ui = RustedMossManager(self)
        self.ui_task = asyncio.create_task(self.ui.async_run(), name="UI")

    def on_deathlink(self, data: typing.Dict[str, typing.Any]):
        self.got_deathlink = True
        super().on_deathlink(data)

async def process_rusted_moss_cmd(ctx: RustedMossContext, cmd: str, args: dict):
    # TODO handle server commands https://github.com/ArchipelagoMW/Archipelago/blob/main/docs/network%20protocol.md#server---client
    print("cmd: " + cmd)
    print("args:")
    print(args)
    if cmd == "Connected":
        if not os.path.exists(ctx.save_game_folder):
            os.mkdir(ctx.save_game_folder)
        ctx.deathlink_status = args["slot_data"]["deathlink"]
        await ctx.update_death_link(ctx.deathlink_status)
        ctx.hard_maya = args["slot_data"]["hard_maya"]
        ctx.ending = args["slot_data"]["ending"]
        with open(os.path.join(ctx.save_game_folder, "checkedLocations"), "w") as f:
            for location in args["checked_locations"]:
                f.write(str(location) + "\n")
            f.close()
    elif cmd == "LocationInfo":
        # TODO investigate scout handling
        pass
    elif cmd == "ReceivedItems":
        start_index = args["index"]

        if start_index == 0:
            ctx.items_received = []
            try:
                os.remove(os.path.join(ctx.save_game_folder, "receivedItems"))
            except OSError:
                pass
        elif start_index != len(ctx.items_received):
            sync_msg = [{"cmd": "Sync"}]
            if ctx.locations_checked:
                sync_msg.append({"cmd": "LocationChecks", "locations": list(ctx.locations_checked)})
            await ctx.send_msgs(sync_msg)
        if start_index == len(ctx.items_received):
            for item in args["items"]:
                ctx.items_received.append(NetworkItem(*item))
            with open(os.path.join(ctx.save_game_folder, "receivedItems"), "a") as f:
                for index, item in enumerate(ctx.items_received):
                    f.write(str(index) + "\n")
                    f.write(ctx.item_names[item.item] + "\n")
                f.close()
            with open(os.path.join(ctx.save_game_folder, "newItems"), "w") as f:
                f.close()
    elif cmd == "RoomUpdate":
        # TODO handle location getting marked as checked from server
        pass


async def game_watcher(ctx: RustedMossContext):
    while not ctx.exit_event.is_set():
        if ctx.got_deathlink:
            ctx.got_deathlink = False
            with open(os.path.join(ctx.save_game_folder, "deathlinkFromServer"), "w") as f:
                f.close()
        
        sending = []
        for root, dirs, files in os.walk(ctx.save_game_folder):
            for file in files:
                if "deathlinkFromClient" in file:
                    if "DeathLink" in ctx.tags:
                        await ctx.send_death()
                    os.remove(os.path.join(root, file))
                if "scoutLocations" == file:
                    try:
                        with open(os.path.join(root, file), "r") as f:
                            locations = f.readlines()
                            f.close()
                        for location in locations:
                            locationName = gameLocationToLocationName[location.strip()]
                            locationId = AutoWorldRegister.world_types[ctx.game].location_name_to_id[locationName]
                            if locationId in ctx.server_locations:
                                sending.append(locationId)
                    finally:
                        await ctx.send_msgs([{"cmd": "LocationScouts", "locations": sending, "create_as_hint": 2}])
                        os.remove(os.path.join(root, file))
                if "newLocations" == file:
                    try:
                        locations = []
                        with open(os.path.join(root, file), "r") as f:
                            locations = f.readlines()
                        with open(os.path.join(ctx.save_game_folder, "checkedLocations"), "a") as f:
                            for location in locations:
                                locationName = gameLocationToLocationName[location.strip()]
                                locationId = AutoWorldRegister.world_types[ctx.game].location_name_to_id[locationName]
                                if locationId in ctx.server_locations:
                                    sending.append(locationId)
                                    f.write(str(locationId) + "\n")
                            f.close()
                    finally:
                        await ctx.send_msgs([{"cmd": "LocationChecks", "locations": sending}])
                        os.remove(os.path.join(root, file))
                if "endingAchieved" == file:
                    with open(os.path.join(root, file), "r") as f:
                        endingNumber = int(f.readline().strip())
                        sendVictory = False
                        if ctx.ending == 0 and endingNumber <= 3:
                            sendVictory = True
                        elif ctx.ending == 1 and endingNumber <= 2:
                            sendVictory = True
                        elif ctx.ending == 2 and endingNumber <= 2:
                            sendVictory = True
                        elif ctx.ending == 3 and endingNumber == 3:
                            sendVictory = True
                        elif ctx.ending == 4:
                            sendVictory = True

                        if not ctx.finished_game and sendVictory:
                            await ctx.send_msgs([{"cmd": "StatusUpdate", "status": ClientStatus.CLIENT_GOAL}])
                            ctx.finished_game = True
                        f.close()
                    os.remove(os.path.join(root, file))

        ctx.locations_checked = sending

        await asyncio.sleep(0.1)

def main():
    Utils.init_logging("RustedMossClient", exception_logger="Client")

    async def _main():
        ctx = RustedMossContext(None, None)
        ctx.server_task = asyncio.create_task(server_loop(ctx), name="server loop")
        asyncio.create_task(game_watcher(ctx), name="RustedMossProgressionWatcher")

        if gui_enabled:
            ctx.run_gui()
        ctx.run_cli()

        await ctx.exit_event.wait()
        await ctx.shutdown()

    import colorama
    colorama.init()
    asyncio.run(_main())
    colorama.deinit()

if __name__ == "__main__":
    parser = get_base_parser(description="Rusted Moss Client, for text interfacing.")
    args = parser.parse_args()
    main()
