from interactions import Extension, Embed, OptionType, slash_option, Member
from interactions.ext.hybrid_commands import hybrid_slash_command, HybridContext

class Moderation(Extension):
    def __init__(self, bot):
        self.bot = bot

    @hybrid_slash_command(name="mute", description="Mediator Command: Mute a specific User.")
    @slash_option(
    name="username",
    description="Username of the person to greet",
    required=True,
    opt_type=OptionType.STRING
    )
    async def greet_user(self, ctx: HybridContext, username: str):
        await ctx.send(f"Hello {username}!")