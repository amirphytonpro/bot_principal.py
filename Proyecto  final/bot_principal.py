import discord
import os
from Api import get_pokemon_info
import Search as Search
import respuesta
from medio_ambiente import get_weather

intents = discord.Intents.default()
intents.messages = True

IMAGE_DIR = 'imagenes/'
client = discord.Client(intents=intents)
COMANDOS_IMAGENES = {
    'perro': 'perro.jpeg',
    'auto': 'auto.jpeg',
    'moto': 'moto.jpeg',
    'dinosaurio': 'dinosaurio.jpeg',
    'calentamiento': 'calentamiento global.jpeg',
    'oso': 'oso.jpeg',
    'sequia': 'sequia.jpeg'
}
API_KEY = 'TU_API_KEY'


@client.event
async def on_ready():
    print(f'{client.user} está conectado a Discord!')
    print('Listo para recibir comandos')


@client.event
async def on_message(message):
    if message.content.startswith('!hello'):
        await message.channel.send("Hi!")
    elif message.content.startswith('!bye'):
        await message.channel.send("\\U0001f642")
    else:
        await message.channel.send(message.content)
    if 'por favor' in message.content.lower():
        await message.channel.send("¡Por supuesto! Aquí tienes la información que necesitas. ¿Hay algo más en lo que pueda ayudar?")
    elif 'gracias' in message.content.lower():
        await message.channel.send("¡De nada! Si necesitas más ayuda, no dudes en preguntar.")
    if message.content.startswith('!respuesta'):
        query = message.content.split('!respuesta')[1].strip()
        response = respuesta.get_wikipedia_summary(query)
        await message.channel.send(response)
    if message.content.startswith('!clima'):
        city = 'London'
        weather_data = get_weather(API_KEY, city)
        if 'weather' in weather_data:
            weather_description = weather_data['weather'][0]['description']
            await message.channel.send(f"Las condiciones climáticas en {city} son: {weather_description}")
        else:
            await message.channel.send("No se encontraron datos climáticos para esa ciudad.")
    if message.content.startswith('!imagen_'):
        parts = message.content.split('_')
        if len(parts) < 2:
            await message.channel.send('Por favor, proporciona el nombre de la imagen después de `!imagen_`.')
            return

        comando = parts[1]

        if comando not in COMANDOS_IMAGENES:
            await message.channel.send('Comando de imagen no válido.')
            return

        image_name = COMANDOS_IMAGENES[comando]

        image_path = os.path.join(IMAGE_DIR, image_name)
        if not os.path.exists(image_path):
            await message.channel.send(f'No se encontró la imagen {image_name}.')
            return

        with open(image_path, 'rb') as f:
            await message.channel.send(file=discord.File(f))
    if message.content.startswith('!pokemon'):
        parts = message.content.split(' ')
        if len(parts) < 2:
            await message.channel.send('Por favor, proporciona el nombre del Pokémon después de `!pokemon`.')
            return
        pokemon_name = parts[1]

        pokemon_info = get_pokemon_info(pokemon_name)
        if pokemon_info:
            response = f"Nombre: {pokemon_info['name'].capitalize()}\n"
            response += f"ID: {pokemon_info['id']}\n"
            response += "Tipos: "
            for type_entry in pokemon_info['types']:
                response += f"{type_entry['type']['name'].capitalize()}, "
            response = response[:-2] + "\n"
            response += f"Altura: {pokemon_info['height']}\n"
            response += f"Peso: {pokemon_info['weight']}\n"
            response += "Habilidades: "
            for ability_entry in pokemon_info['abilities']:
                response += f"{ability_entry['ability']
                               ['name'].capitalize()}, "
            response = response[:-2]
            await message.channel.send(response)
        else:
            await message.channel.send(f"No se encontró información sobre el Pokémon '{pokemon_name}'.")
    elif message.author == client.user:
        return

    if message.content.startswith('!buscar_imagen'):
        query = message.content[len('!buscar_imagen')+1:]
        resultados = Search.buscar_imagenes(query)
        for resultado in resultados:
            await message.channel.send(resultado)
    elif message.content.startswith('!buscar_videos'):
        query = message.content[len('!buscar_videos')+1:]
        # Reemplaza con tu propia API Key de YouTube Data
        api_key = 'AIzaSyABhLUkcIDza0rr95xm0M2JPlWZ0HzUAUM'
        videos_encontrados = Search.buscar_videos(query, api_key)
        for video in videos_encontrados:
            await message.channel.send(video)

client.run(
    'TU_TOKEN')
