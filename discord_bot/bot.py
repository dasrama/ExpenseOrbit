import requests
import discord 
from discord.ext import commands
from config import Config


intents = discord.Intents.default()
intents.message_content = True

bot = commands.Bot(command_prefix="!", intents=intents)

@bot.event
async def on_ready():
    print(f"Logged in as {bot.user}")

@bot.command()
async def login(ctx):
    oauth_url = "https://discord.com/oauth2/authorize?client_id={Config.CLIENT_ID}&response_type=code&redirect_uri={Config.REDIRECT_URI}&scope=guilds+identify"
    await ctx.send(f"🔐 Click here to login: {oauth_url}")

@bot.command()
async def get_id(ctx, member: discord.Member = None):
    member = member or ctx.author                                   # Default to the command sender
    await ctx.send(f"{member.name}'s Discord ID is: `{member.id}`")

@bot.command()
async def hello(ctx):
    await ctx.send(f"Hello {ctx.author.name} !, I am Trakr :) ") 

@bot.command()
async def add_expense(ctx, amount: float, category: str):
    response = requests.post(
        f"{Config.API_URL}/transactions/",
        json={"amount": amount, "category": category}
    )

    if response.status_code == 201:
        await ctx.send(f"✅ Expense of {amount} added under '{category}'")
    else:
        await ctx.send("❌ Failed to add expense")

@bot.command()
async def view_expenses(ctx):
    response = requests.get(f"{Config.API_URL}/transactions/")
    
    if response.status_code == 200:
        expenses = response.json()
        if not expenses:
            await ctx.send("📌 No expenses recorded yet!")
        else:
            expense_list = "\n".join([f"{e['amount']} - {e['category']}" for e in expenses])
            await ctx.send(f"📋 Your expenses:\n{expense_list}")
    else:
        await ctx.send("❌ Failed to fetch expenses")

print("Registered Commands:", [command.name for command in bot.commands])


bot.run(Config.TOKEN)

