import os

import requests

# Get the data from the API
URL = 'https://pokeapi.co/api/v2/'
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
    response = requests.get(f"{URL}pokemon/{pokemon}")
    if response.status_code == 200:
        data = response.json()
        name = data['name']
        id = data['id']
        types = data['types']
        image = data['sprites']['front_default']
        baseExperience = data['base_experience']
        weight = data['weight']
        height = data['height']
        stats = {stat['stat']['name']: stat['base_stat'] for stat in data['stats']}
        abilities = [ability['ability']['name'] for ability in data['abilities']]
        doubleDamageFrom = []
        doubleDamageTo = []
        evolution = None
        evolutionChainUrl = data['species']['url']
        evolutionChainResponse = requests.get(evolutionChainUrl)
        ability_descriptions = {}

        if evolutionChainResponse.status_code == 200:
            evolutionChainData = evolutionChainResponse.json()
            evolutionChainId = evolutionChainData['evolution_chain']['url'].split('/')[-2]
            evolutionChainResponse = requests.get(f"{URL}evolution-chain/{evolutionChainId}")

            if evolutionChainResponse.status_code == 200:
                evolutionChainData = evolutionChainResponse.json()
                evolution = []
                chain = evolutionChainData['chain']
                while chain['evolves_to']:
                    species = chain['species']['name']
                    speciesResponse = requests.get(f"{URL}pokemon/{species}")
                    if speciesResponse.status_code == 200:
                        speciesData = speciesResponse.json()
                        evolution.append({'name': species, 'image': speciesData['sprites']['front_default']})
                    else:
                        evolution.append({'name': species, 'image': None})
                    chain = chain['evolves_to'][0]
                species = chain['species']['name']
                speciesResponse = requests.get(f"{URL}pokemon/{species}")
                if speciesResponse.status_code == 200:
                    speciesData = speciesResponse.json()
                    speciesImage = speciesData['sprites']['front_default']
                    evolution.append({'name': species, 'image': speciesData['sprites']['front_default']})
                else:
                    evolution.append({'name': species, 'image': None})
            else:
                evolution = None
        else:
            evolution = None

        for ability_name in abilities:
            abilityUrl = f"{URL}ability/{ability_name}"
            ability_response = requests.get(abilityUrl)
            if ability_response.status_code == 200:
                ability_data = ability_response.json()
                for effect in ability_data['effect_entries']:
                    if effect['language']['name'] == 'en':
                        ability_descriptions[ability_name] = effect['short_effect']
                        break

        for type in types:
            type_url = type['type']['url']
            type_response = requests.get(type_url)
            if type_response.status_code == 200:
                type_data = type_response.json()
                for damage in type_data['damage_relations']['double_damage_from']:
                    doubleDamageFrom.append(damage['name'])
                for damage in type_data['damage_relations']['double_damage_to']:
                    doubleDamageTo.append(damage['name'])

        return {
            'name': name,
            'id': id,
            'types': types,
            'image': image,
            'stats': stats,
            'abilities': abilities,
            'ability_descriptions': ability_descriptions,
            'DoubleDamageFrom': doubleDamageFrom,
            'DoubleDamageTo': doubleDamageTo,
            'evolution': evolution,
            'baseExperience': baseExperience,
            'weight': weight,
            'height': height,
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
        <title>{data['name'].capitalize()} - {data['id']}</title>
        <style>
            body {{
                background-color: {fontAndBackgroundColors[data['types'][0]["type"]["name"]]["background"]};
                color: {fontAndBackgroundColors[data['types'][0]["type"]["name"]]["font"]};
                font-family: Arial, sans-serif;
                font-size: 16px;
            }}
            .container {{
                display: flex;
                flex-direction: column;
                align-items: center;
                padding: 20px;
                margin: 20px;
            }}
            .column {{
                display: flex;
                flex-direction: row;
                justify-content: space-between;
                margin-top: 20px;
            }}
            .column > div {{
                padding: 30px;
                margin: 20px;
                text-align: left;
            }}
            .evolutions {{
                display: flex;
                flex-wrap: wrap;
                justify-content: center;
                padding: 30px;
                margin: 20px;
            }}
            .evolutions > div {{
                padding: 10px;
                margin: 10px;
                text-align: center;
            }}
            img {{
                width: 200px;
                height: 200px;
            }}
        </style>
    </head>
    <body>
        <div class="container">
            <div style="text-align: center;">
                <h1>{data['name'].capitalize()} - {data['id']}</h1>
                <img src="{data['image']}" alt="{data['name']}">
                <p>Base Experience: {data['baseExperience']}</p>
                <p>Weight: {data['weight']}</p>
                <p>Height: {data['height']}</p>
            </div>
            <div class="column">
                <div>
                    <h3>Types</h3>
                    <p>
                        <ul>
                            {"".join([f'<li>{type["type"]["name"].capitalize()}</li>' for type in data['types']])}
                        </ul>
                    </p>
                    <h3>Stats</h3>
                    <p> 
                        <ul>
                            {"".join([f'<li>{stat.capitalize()}: {data["stats"][stat]}</li>' for stat in data['stats']])}
                        </ul>
                    </p>
                </div>
                <div>
                    <h3>Abilities</h3> 
                    <ul>
                        {"".join([f'<li>{ability.capitalize()}: {data["ability_descriptions"][ability]}</li>' for ability in data['abilities']])}
                    </ul>
                    <h3>Double damage from:</h3>
                    <p>
                        <ul>
                            {"".join([f'<li>{type.capitalize()}</li>' for type in data['DoubleDamageFrom']])}
                        </ul>
                    </p>
                    <h3>Double damage to:</h3>
                    <p>
                        <ul>
                            {"".join([f'<li>{type.capitalize()}</li>' for type in data['DoubleDamageTo']])} 
                        </ul>
                    </p>
                </div>
            </div>
            <div class="evolutions">
                <h3>Evolutions:</h3>
                <br/>
                <br/>
                <ol style="display: flex; padding: 0; padding-top: 50px; margin: 0;">
                    {"".join([f'<li><p>{evolution["name"].capitalize()}</p><img src="{evolution["image"]}" alt="{evolution["name"]}"></li>' for evolution in data['evolution']])}
                </ol>
            </div>
        </div>
    </body>
    </html>
    '''
    return html


def createHTMLFile(data):
    if not os.path.exists('outputs'):
        os.makedirs('outputs')
    with open(f'outputs/{data["name"]}.html', 'w') as file:
        file.write(htmlTemplate(data))


def main():
    pokemons = ['pikachu', 'bulbasaur', 'charmander', 'squirtle']
    for pokemon in pokemons:
        data = getPokemonData(pokemon)
        if data:
            createHTMLFile(data)
            print(f'{pokemon} created')
        else:
            print(f'{pokemon} not found')


if __name__ == '__main__':
    main()
