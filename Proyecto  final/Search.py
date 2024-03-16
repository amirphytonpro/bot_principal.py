import requests


def buscar_imagenes(query):
    api_key = 'tu_api_key'
    search_engine_id = '45943969396f04539'
    url = f'https://www.googleapis.com/customsearch/v1?key={
        api_key}&cx={search_engine_id}&q={query}&searchType=image'

    response = requests.get(url)
    data = response.json()

    if 'items' in data:
        return [item['link'] for item in data['items']]
    else:
        return []


def buscar_videos(query, api_key):
    url = f'https://www.googleapis.com/youtube/v3/search?key={
        api_key}&q={query}&part=snippet&type=video'

    response = requests.get(url)
    data = response.json()

    if 'items' in data:
        return [f"https://www.youtube.com/watch?v={item['id']['videoId']}" for item in data['items']]
    else:
        return []
