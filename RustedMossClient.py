import os
import asyncio
import typing

import Utils

from NetUtils import NetworkItem
from CommonClient import ClientCommandProcessor, CommonContext, \
    server_loop, get_base_parser, gui_enabled

# TODO add commands for patching, setting save directory, and syncing
class RustedMossCommandProcessor(ClientCommandProcessor):
    def __init__(self, ctx):
        super().__init__(ctx)


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
        self.titania_pieces_required = 0
        self.hard_maya = False

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
                # TODO verify what files exactly should be cleared
                if file in ["deathlinkFromClient", "deathlinkFromServer", "scoutLocations", "checkedLocations", "endingCompleted", "receivedItems"]:
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
        ctx.titania_pieces_required = args["slot_data"]["titania_pieces_required"]
        ctx.hard_maya = args["slot_data"]["hard_maya"]
        with open(os.path.join(ctx.save_game_folder, "checkedLocations"), "w") as f:
            for location in args["checked_locations"]:
                f.write(str(location) + "\n")
            f.close()
    elif cmd == "LocationInfo":
        # TODO investigate scout handling
        pass
    elif cmd == "Retrieved":
        # TODO only if send Get command
        pass
    elif cmd == "SetReply":
        # TODO only if send Set command
        pass
    elif cmd == "ReceivedItems":
        start_index = args["index"]

        if start_index == 0:
            ctx.items_received = []
        elif start_index != len(ctx.items_received):
            sync_msg = [{"cmd": "Sync"}]
            if ctx.locations_checked:
                sync_msg.append({"cmd": "LocationChecks", "locations": list(ctx.locations_checked)})
            await ctx.send_msgs(sync_msg)
        if start_index == len(ctx.items_received):
            with open(os.path.join(ctx.save_game_folder, "receivedItems"), "w") as f:
                for item in args["items"]:
                    networkItem = NetworkItem(*item)
                    f.write(str(networkItem.item) + "\n")
                    ctx.items_received.append(networkItem)
                f.close()
    elif cmd == "RoomUpdate":
        # TODO write to file which game will use to pull already checked locations on game load
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
                        for location in locations:
                            # TODO translate from what the game writes to location id
                            if int(location) in ctx.server_locations:
                                sending.append(int(location))
                    finally:
                        await ctx.send_msgs([{"cmd": "LocationScouts", "locations": sending, "create_as_hint": 2}])
                        os.remove(os.path.join(root, file))
                if "checkLocations" == file:
                    try:
                        with open(os.path.join(root, file), "r") as f:
                            locations = f.readlines()
                        for location in locations:
                            # TODO translate from what the game writes to location id
                            if int(location) in ctx.server_locations:
                                sending.append(int(location))
                    finally:
                        await ctx.send_msgs([{"cmd": "LocationChecks", "locations": sending}])
                        os.remove(os.path.join(root, file))
                if "endingCompleted" == file:
                    # TODO ending file format and yaml options
                    pass

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
