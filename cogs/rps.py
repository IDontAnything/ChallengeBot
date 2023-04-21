import discord
from discord.ext import commands

class Buttons(discord.ui.View):
    def __init__(self, ctx, challenger_id, challenged_id, *, timeout=180):
        super().__init__(timeout=timeout)
        self.ctx=ctx
        self.challenger_id = challenger_id
        self.challenged_id = challenged_id
        self.pressed = []
        self.choices = {}

    async def announce_winner(self, winner):
        if winner:
            loser_id = self.challenged_id if winner == self.challenger_id else self.challenger_id
            await self.ctx.send(f"<@{winner}> won!")
            member = self.ctx.guild.get_member(loser_id)
            if self.ctx.author.voice:  # check if the loser is in a voice channel
                await member.move_to(None)  # kick the loser out of the voice channel
                await self.ctx.send(f"Kicking <@{loser_id}> from voice channel.")
        else:
            await self.ctx.send("It's a tie.")

    async def check_choices(self):
        if len(self.choices) == 2:
            user_1_choice = self.choices.get(self.challenger_id)
            user_2_choice = self.choices.get(self.challenged_id)
            winner = None
            if user_1_choice == user_2_choice:
                pass  # tie
            elif (user_1_choice == "rock" and user_2_choice == "scissors") or \
                 (user_1_choice == "paper" and user_2_choice == "rock") or \
                 (user_1_choice == "scissors" and user_2_choice == "paper"):
                winner = self.challenger_id
            else:
                winner = self.challenged_id

            await self.announce_winner(winner)

    async def interaction_check(self, interaction: discord.Interaction) -> bool:
        if interaction.user.id not in [self.challenger_id, self.challenged_id]:
            await interaction.response.send_message("Go Away.", ephemeral=True)
            return False
        elif interaction.user.id in self.pressed:
            await interaction.response.send_message("You have already chosen.", ephemeral=True)
            return False
        else:
            self.pressed.append(interaction.user.id)
            print(self.choices)
            return True


    @discord.ui.button(label="rock", style=discord.ButtonStyle.blurple)
    async def rock_button(self, interaction: discord.Interaction, button: discord.ui.Button):
        self.choices[interaction.user.id] = 'rock'
        await interaction.response.send_message("you chose rock", ephemeral=True)
        print(f"{interaction.user.id} chose rock")
        if len(self.choices) == 2:
            await self.check_choices()

    @discord.ui.button(label="paper", style=discord.ButtonStyle.green)
    async def paper_button(self, interaction: discord.Interaction, button: discord.ui.Button):
        self.choices[interaction.user.id] = 'paper'
        await interaction.response.send_message("you chose paper", ephemeral=True)
        print(f"{interaction.user.id} chose paper")
        if len(self.choices) == 2:
           await self.check_choices()

    @discord.ui.button(label="scissors", style=discord.ButtonStyle.red)
    async def scissors_button(self, interaction: discord.Interaction, button: discord.ui.Button):
        self.choices[interaction.user.id] = 'scissors'
        await interaction.response.send_message("you chose scissors", ephemeral=True)
        print(f"{interaction.user.id} chose scissors")
        if len(self.choices) == 2:
            await self.check_choices()
        

class rps(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_ready(self):
        print('clickme cog loaded')

    @commands.command()
    async def challenge(self, ctx, member: discord.Member):
        challenger_id = ctx.author.id
        challenged_id = member.id
        view = Buttons(ctx, challenger_id, challenged_id)
        await ctx.send(f"{member.mention} Fight Me", view=view, delete_after=60.0)


async def setup(bot):
    await bot.add_cog(rps(bot))