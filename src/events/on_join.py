import discord
from discord import Embed
from discord.ext import commands
from easy_pil import Editor, load_image_async
from PIL import ImageFont

import static


class On_Join(commands.Cog):

    def __init__(self, bot):
        print(f"loaded Event {self.__cog_name__} Cog")
        self.bot = bot

    @commands.Cog.listener()
    async def on_join(self, member: discord.Member):
        await self.bot.change_presence(activity=discord.Game(name=f"👋 {member}"))

        await welcome_msg(member, self.bot)
        await invite_log(member, self.bot)


def setup(client):
    client.add_cog(On_Join(client))


async def welcome_msg(member, client):
    f75 = ImageFont.truetype("assets/fonts/ARLRDBD.TTF", 75)
    f50 = ImageFont.truetype("assets/fonts/ARLRDBD.TTF", 50)
    background = Editor(f"assets/img/welcome.png")
    if not member.avatar:
        profile = await load_image_async(str(member.default_avatar))
    else:
        profile = await load_image_async(str(member.avatar.url))

    profile = Editor(profile).resize((192, 192)).circle_image()

    ima = Editor("assets/img/welcome.png")
    background.blend(image=ima, alpha=.5, on_top=False)

    background.ellipse(
        (156, 106),
        height=200,
        width=200,
        fill="#ffffff"
    )

    background.paste(profile, (160, 110))

    if member.discriminator == "0":
        member = member.name

    name = f"{str(member)[:16]}..." if len(str(member)) > 16 else str(member)
    background.text((256, 310), f"Willkommen", font=f75, color="#FFFFFF", align="center")
    background.text((256, 400), name, font=f50, color="#FFFFFF", align="center")

    card = discord.File(fp=background.image_bytes, filename="welcome.png")
    welcome_channel = await client.fetch_channel(static.channels_id['welcome'])
    await welcome_channel.send(f"**Willkommen auf :shower:𝖣𝗎𝗌𝖼𝗁𝗉𝖺𝗅𝖺𝗌𝗍:shower:, {member.mention}!!**", file=card)


async def invite_log(member, client):
    logs = await client.fetch_channel(static.channels_id['log'])

    if not member.avatar:
        pfp = member.default_avatar
    else:
        pfp = member.avatar.url

    eme = Embed(description="Just joined the server", color=0x03d692, title=" ")
    eme.set_author(name=str(member), icon_url=pfp)
    eme.set_footer(text="ID: " + str(member.id))
    eme.timestamp = member.joined_at

    invs_before = static.invites
    invs_after = await member.guild.invites()
    static.invites = invs_after
    for invite in invs_before:
        try:
            if invite.uses < await find_invite_by_code(invs_after, invite.code).uses:
                if not invite.expires_at:
                    expire = None
                else:
                    expire = f"<t:{int(invite.expires_at.timestamp())}>"
                eme.add_field(name="Used invite",
                              value=f"Inviter: {invite.inviter.mention} (`{invite.inviter}` | `{str(invite.inviter.id)}`)\nCode: `{invite.code}`\nUses: `{str(invite.uses + 1)}`\nExpires at: {expire}",
                              inline=False)
        except:
            continue

    await logs.send(embed=eme)


async def find_invite_by_code(inv_list, code):
    for inv in inv_list:
        if inv.code == code:
            return inv
