import discord
from discord.ext import commands

intents = discord.Intents.default()
intents.members = True

bot = commands.Bot(command_prefix='!', intents=intents)

# Función para detectar mensajes de spam
@bot.event
async def on_message(message):
    if len(message.content) > 100:  # Definir el límite de caracteres para considerar spam
        await message.delete()
        await message.channel.send(f'{message.author.mention}, por favor evita el spam.')
    await bot.process_commands(message)

# Función para detectar contenido inapropiado
@bot.event
async def on_message(message):
    inappropriate_words = ["palabra1", "palabra2", "palabra3"]  # Lista de palabras inapropiadas
    for word in inappropriate_words:
        if word in message.content.lower():
            await message.delete()
            await message.channel.send(f'{message.author.mention}, por favor evita el lenguaje inapropiado.')
            break
    await bot.process_commands(message)

# Función para asignar un rol a los nuevos miembros
@bot.event
async def on_member_join(member):
    role = discord.utils.get(member.guild.roles, name='Nuevo Miembro')  # Nombre del rol para nuevos miembros
    await member.add_roles(role)

# Función para registrar las acciones de moderación
@bot.event
async def on_command_error(ctx, error):
    if isinstance(error, commands.CommandNotFound):
        return
    # Aquí puedes implementar la lógica para registrar el error, como guardar en un archivo de registro o enviar un mensaje a un canal de registros.

# Comando para expulsar a un usuario
@bot.command()
async def kick(ctx, member: discord.Member, *, reason=None):
    await member.kick(reason=reason)
    await ctx.send(f'{member.mention} ha sido expulsado por {ctx.author.mention}.')

# Comando para banear a un usuario
@bot.command()
async def ban(ctx, member: discord.Member, *, reason=None):
    await member.ban(reason=reason)
    await ctx.send(f'{member.mention} ha sido baneado por {ctx.author.mention}.')

# Comando para eliminar mensajes
@bot.command()
async def clear(ctx, amount: int):
    await ctx.channel.purge(limit=amount + 1)
    await ctx.send(f'Se han eliminado {amount} mensajes.')

bot.run('tu_token')
