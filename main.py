import requests
import json
import flask

# Get the data from the API
URL = 'https://pokeapi.co/api/v2/pokemon'
fontAndBackgroundColors = {
    'fire': {
        'background': 'red',
        'font': 'white'
    },
    'water': {
        'background': 'blue',
        'font': 'white'
    },
    'grass': {
        'background': 'green',
        'font': 'black'
    },
    'electric': {
        'background': 'yellow',
        'font': 'black'
    },
}


def getPokemonData(pokemon):
    response = requests.get(f'{URL}/{pokemon}')
    if response.status_code == 200:
        data = response.json()
        name = data['name']
        id = data['id']
        types = data['types']
        image = data['sprites']['front_default']
        stats = {stat['stat']['name']: stat['base_stat'] for stat in data['stats']}
        abilities = [ability['ability']['name'] for ability in data['abilities']]
        ability_descriptions = {}
        for ability_name in abilities:
            ability_url = f"https://pokeapi.co/api/v2/ability/{ability_name}"
            ability_response = requests.get(ability_url)
            if ability_response.status_code == 200:
                ability_data = ability_response.json()
                for effect in ability_data['effect_entries']:
                    if effect['language']['name'] == 'en':
                        ability_descriptions[ability_name] = effect['short_effect']
                        break
                        


        return {
            'name': name,
            'id': id,
            'types': types,
            'image': image,
            'stats': stats,
            'abilities': abilities,
            'ability_descriptions': ability_descriptions
        }
    else:
        return None

def htmlTemplate(data):
    html = f'''
    <!DOCTYPE html>
    <html lang="en">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>{data['name'].capitalize()}</title>
    </head>
    <body>
        <h1>{data['name'].capitalize()}</h1>
        <img src="{data['image']}" alt="{data['name']}">
        <p>Types: 
            {"".join([f'<span style="background-color: {fontAndBackgroundColors[type["type"]["name"]]["background"]}; color: {fontAndBackgroundColors[type["type"]["name"]]["font"]}; padding: 5px; border-radius: 5px; margin: 5px;">{type["type"]["name"]}</span>' for type in data['types']])}
        </p>
        <p>Stats: 
            <ul>
                {"".join([f'<li>{stat}: {data["stats"][stat]}</li>' for stat in data['stats']])}
            </ul>
        </p>
        <p>Abilities: 
            <ul>
                {"".join([f'<li>{ability}: {data["ability_descriptions"][ability]}</li>' for ability in data['abilities']])}
            </ul>
        </p>
    </body>
    </html>
    '''
    return html

def createHTMLFile(data):
    html = htmlTemplate(data)
    with open('pokemon.html', 'w') as file:
        file.write(html)

#
#
# def createHTMLFile(data):
#     with open('pokemon.html', 'w') as file:
#         file.write('<!DOCTYPE html>')
#         file.write('<html>')
#         file.write('<head>')
#         getBackgroundAndFont()
#         # Pokemon name
#
#         file.write(f'<h1>{data["name"]}</h1>')
#         # Pokemon types
#         file.write('<p>Type: ')
#         for type in data['types']:
#             file.write(
#                 f'<span style="background-color: {fontAndBackgroundColors[type["type"]["name"]]["background"]}; color: {fontAndBackgroundColors[type["type"]["name"]]["font"]}; padding: 5px; border-radius: 5px; margin: 5px;">{type["type"]["name"]}</span>')
#         file.write('</p>')


def getBackgroundAndFont():
    with open('pokemon.html', 'w') as file:
        file.write('<style>')
        file.write('body {')
        file.write('background-color: #f3f4f6;')
        file.write('font-family: Arial, sans-serif;')
        file.write('}')
        file.write('</style>')
        file.write('</head>')
        file.write('<body>')




def main():
    pokemon = 'charmander'
    data = getPokemonData(pokemon)
    # createHTMLFile(data)
    print('File created successfully')
    print(data)
    createHTMLFile(data)


if __name__ == '__main__':
    main()
