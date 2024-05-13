import os
import asyncio

import Utils

from CommonClient import ClientCommandProcessor, CommonContext, \
    server_loop, get_base_parser

# TODO figure out save file association

class RustedMossCommandProcessor(ClientCommandProcessor):
    def __init__(self, ctx)
        super.__init__(ctx)

    # TODO add commands for patching, setting save directory, and syncing

class RustedMossContext(CommonContext):
    tags = {"AP"}
    game = "Rusted Moss"
    command_processor = RustedMossCommandProcessor
    items_handling = 0b111
    save_game_folder = os.path.expandvars(r"%localappdata%/Rusted_Moss")

    def __init__(self, server_address, password):
        super().__init__(server_address, password)
        self.game = "Rusted Moss"
        self.save_game_folder = os.path.expandvars(r"%localappdata%/Rusted_Moss")

    async def server_auth(self, password_requested: bool = False):
        if password_requested and not self.password:
            await super().server_auth(password_requested)
        await self.get_username()
        await self.send_connect()

    def clear_rusted_moss_files(self):
        path = self.save_game_folder
        self.finished_game = False
        # TODO clear files that game? or self? write
        # for root, dirs, files in os.walk(path):
        #     for file in files:
        #         if "check.spot" == file or "scout" == file:
        #             os.remove(os.path.join(root, file))
        #         elif file.endswith((".item", ".victory", ".route", ".playerspot", ".mad")):
        #             os.remove(os.path.join(root, file))

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
        async_start(process_rusted_moss_cmd(self, cmd, args))

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
    if cmd == "Connected"
        pass

async def game_watcher(ctx: RustedMossContext):
    # TODO listen for game files and send messages to server
    while not ctx.exit_event.is_set():
        path = ctx.save_game_folder
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
