from ast import literal_eval

import discord
from discord import Embed
from discord.ext import commands
from discord.ui import Select, View, Button

import static
from static import SQL, db, color_picker_message_id


class Color_Picker(commands.Cog):

    def __init__(self, bot):
        print(f"loaded User Interaction {self.__cog_name__} Cog")
        self.bot = bot

    @commands.Cog.listener()
    async def on_ready(self):
        if self.bot.user.id == static.bot_id:
            await color_picker(self.bot)


def setup(client):
    client.add_cog(Color_Picker(client))



async def color_picker(client):
    SQL.execute('SELECT * FROM color_picker ORDER BY LOWER(name);')
    res = SQL.fetchall()

    colors = Select(
        placeholder=f"🎨Farben",
        options=[discord.SelectOption(
            label=x[0][1:],
            emoji=x[0][:1],
            value=str(x[1])
        ) for x in res
        ],
        min_values=0,
        max_values=1
    )

    async def callback(interaction: discord.Interaction):
        user: discord.Member = interaction.user

        booster_role = discord.utils.get(interaction.guild.roles, id=static.roles_id['booster'])
        vip_role = discord.utils.get(interaction.guild.roles, id=static.roles_id['vip'])

        if booster_role in user.roles or vip_role in user.roles:
            cost = 50
        else:
            cost = 100

        SQL.execute(f'SELECT coin FROM users WHERE user_id = {user.id}')
        coins = SQL.fetchone()[0]
        if coins < cost:
            await interaction.response.send_message(
                embed=Embed(color=discord.Color.red(), title="Du hast nicht genug Coins"),
                ephemeral=True)
            return

        SQL.execute(f'UPDATE users SET coin = coin - {cost} WHERE user_id = {user.id}')
        db.commit()

        await interaction.response.send_message(
            embed=Embed(color=discord.Color.green(), title=f"Deine Farbe wurde geupdatet"),
            ephemeral=True)

        await remove_roles_(interaction)
        color = interaction.guild.get_role(int(colors.values[0]))
        await user.add_roles(color, reason="Farbe ausgewählt", atomic=True)

    view = View(timeout=None)

    colors.callback = callback
    view.add_item(colors)

    button1 = Button(label="Farbe zurücksetzen", custom_id="reset", style=discord.ButtonStyle.gray)
    button2 = Button(label="Benutzerdefinierte Farbe", custom_id="custom", style=discord.ButtonStyle.blurple)

    view.add_item(button1)
    view.add_item(button2)

    button1.callback = reset_btn_callback
    button2.callback = custom_btn_callback

    txt = ("## __***Farbe mit der Du auf den Server angezeigt wirst:***__\n"
           "> Kostet `100` Duschcoins (für Server Booster und Vip die Hälfte)\n"
           "> Benutzerdefinierte Farbe nur für Server Booster und Vip")

    channel = await client.fetch_channel(1067748613800853555)
    await (await channel.fetch_message(color_picker_message_id)).edit(txt, view=view)




async def remove_roles_(interaction):
    SQL.execute('SELECT role_id FROM color_picker')
    role_ids = SQL.fetchall()
    for i in role_ids:
        role = interaction.guild.get_role(i[0])
        if role in interaction.user.roles:
            await interaction.user.remove_roles(role, atomic=True)

    for role in interaction.user.roles:
        if role.name.startswith("#"):
            await interaction.user.remove_roles(role, atomic=True)

            if len(role.members) == 0:
                await role.delete()




async def reset_btn_callback(interaction):
    await interaction.response.send_message(
        embed=Embed(color=discord.Color.green(), title="Farbe wurde zurückgesetzt"),
        ephemeral=True)

    await remove_roles_(interaction)


async def custom_btn_callback(interaction):
    user: discord.Member = interaction.user

    booster_role = discord.utils.get(interaction.guild.roles, id=static.roles_id['booster'])
    vip_role = discord.utils.get(interaction.guild.roles, id=static.roles_id['vip'])
    if not booster_role in user.roles and not vip_role in user.roles:
        await interaction.response.send_message(
            embed=Embed(color=discord.Color.red(), title="Du bist nicht berechtigt dies zu Tun"),
            ephemeral=True)
        return

    SQL.execute(f'SELECT coin FROM users WHERE user_id = {user.id}')
    coins = SQL.fetchone()[0]
    if coins < 50:
        await interaction.response.send_message(
            embed=Embed(color=discord.Color.red(), title="Du hast nicht genug Coins"),
            ephemeral=True)
        return

    emb, view = await choose_color_page()
    await interaction.response.send_message(embed=emb, view=view, ephemeral=True)



async def choose_color_page(r=0, g=0, b=0, which=0):
    view = View(timeout=300)

    buttons = [
        Button(label="-1", custom_id=f"[-1, {r}, {g}, {b}, {which}]", style=discord.ButtonStyle.blurple, row=1),
        Button(label="-10", custom_id=f"[-10, {r}, {g}, {b}, {which}]", style=discord.ButtonStyle.blurple, row=1),
        Button(label="-100", custom_id=f"[-100, {r}, {g}, {b}, {which}]", style=discord.ButtonStyle.blurple, row=1),
        Button(label="+1", custom_id=f"[+1, {r}, {g}, {b}, {which}]", style=discord.ButtonStyle.blurple, row=2),
        Button(label="+10", custom_id=f"[+10, {r}, {g}, {b}, {which}]", style=discord.ButtonStyle.blurple, row=2),
        Button(label="+100", custom_id=f"[+100, {r}, {g}, {b}, {which}]", style=discord.ButtonStyle.blurple, row=2),
        Button(label="Letzte Farbe", custom_id=f"['last', {r}, {g}, {b}, {which}]", style=discord.ButtonStyle.gray, row=3, disabled=which == 0),
        Button(label="Nächste Farbe", custom_id=f"['next', {r}, {g}, {b}, {which}]", style=discord.ButtonStyle.gray, row=3, disabled=which == 2),
        Button(label="Abbrechen", custom_id=f"['cancel', {r}, {g}, {b}, {which}]", style=discord.ButtonStyle.red, row=4),
        Button(label="Fertig", custom_id=f"['done', {r}, {g}, {b}, {which}]", style=discord.ButtonStyle.green, row=4)
                ]

    colors = [f"Rot: {r}", f"Grün: {g}", f"Blau: {b}"]
    colors[which] = f"`{colors[which]}`"


    for btn in buttons:
        view.add_item(btn)
        btn.callback = choose_color_callback


    emb=Embed(color=discord.Color.from_rgb(r, g, b),
              title="Wähle deine Farbe"
                    "\n<- Die Farbe sieht aktuell so aus",
                description="Du musst 3 Werte zwischen `0 - 255` wählen"
                            f"\nWerte:"
                            f"\n{colors[0]}"
                            f"\n{colors[1]}"
                            f"\n{colors[2]}")


    return emb, view



async def choose_color_callback(interaction: discord.Interaction):
    content, r, g, b, which = literal_eval(interaction.custom_id)
    rgb = [r, g, b]

    if content == 'next':
        which += 1
    elif content == 'last':
        which -= 1
    elif content == 'cancel':
        await interaction.response.edit_message(embed=Embed(color=0xff0000, title="Abgebrochen", description="Du kannst nun die nachricht löschen"), view=None)
        return
    elif content == 'done':
        await custom_role(interaction, r, g, b)
        return

    else:
        rgb[which] = rgb[which] + content
        if rgb[which] < 0:
            rgb[which] = 0
        elif rgb[which] > 255:
            rgb[which] = 255

    emb, view = await choose_color_page(rgb[0], rgb[1], rgb[2], which)
    await interaction.response.edit_message(embed=emb, view=view)


async def custom_role(interaction, r, g, b):
    await remove_roles_(interaction)

    SQL.execute(f'UPDATE users SET coin = coin - 50 WHERE user_id = {interaction.user.id}')
    db.commit()

    color = '#{:02x}{:02x}{:02x}'.format(r, g, b).upper()

    for role in interaction.guild.roles:
        if role.name == color:
            await interaction.user.add_roles(role)
            await interaction.response.edit_message(
                embed=Embed(color=0x00ff00, title="Fertig, Deine Farbe wurde aktualisiert", description="Du kannst nun die nachricht löschen"),
                view=None)
            return

    role = await interaction.guild.create_role(name=color, color=discord.Color.from_rgb(r, g, b), permissions=discord.Permissions.none())
    await role.edit(position=(interaction.guild.get_role(static.roles_id['bot']).position - 1))
    await interaction.user.add_roles(role)

    await interaction.response.edit_message(
        embed=Embed(color=0x00ff00, title="Fertig, Deine Farbe wurde aktualisiert",
                    description="Du kannst nun die nachricht löschen"),
        view=None)

