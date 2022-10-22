# -*- coding: utf-8 -*-
import os
import sys

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from bobotinho.bot import Bobotinho
from bobotinho.ext.config import config

HEADER = "---\nid: {cog_id}\ntitle: {cog_name}\n---\n\n{cog_description}"
COMMAND = "\n\n### `%{command_name}`"
ALIASES = " ({command_aliases})"
DESCRIPTION = "\n{command_description}"
USAGE = "\n```\n{command_usage}\n```"

if __name__ == "__main__":
    bot = Bobotinho(
        token=config.token,
        prefix=config.prefix,
        case_insensitive=True,
    )
    bot.load_modules(cogs=[f"{config.cogs_path}.{cog}" for cog in config.cogs])

    for cog in bot.cogs.values():
        cog_id = cog.name.lower()
        cog_name, cog_description = cog.__doc__.split("\n\n")
        cog_name = cog_name.strip()
        cog_description = cog_description.strip()

        text = HEADER.format(cog_id=cog_id, cog_name=cog_name, cog_description=cog_description)

        for command in cog.commands.values():
            command_name = command.name
            command_aliases = ", ".join([f"`%{alias}`" for alias in command.aliases]) if command.aliases else None
            command_description = command.description[0].upper() + command.description[1:] if hasattr(command, "description") else None
            command_usage = command.usage.replace("para usar: ", "") if hasattr(command, "usage") else None

            text += COMMAND.format(command_name=command_name)
            if command_aliases:
                text += ALIASES.format(command_aliases=command_aliases)
            if command_description:
                text += DESCRIPTION.format(command_description=command_description)
            if command_usage:
                text += USAGE.format(command_usage=command_usage)

        text += "\n"

        with open(f"docs/{cog_id}.md", "w") as f:
            f.write(text)
