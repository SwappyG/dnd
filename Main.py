from Library import Library
from Character import Character
from pprint import pprint
import Importer

from flask import Flask, render_template, request
from random import randint

app = Flask(__name__)

def makeLibrary():
    library = Library()

    effects = Importer.ImportEffects("effects_lib.csv")
    library.AddDict("effects", effects)

    features = Importer.ImportFeatures("features_lib.csv", library)
    library.AddDict("features", features)
    
    options = Importer.ImportOptions("options_lib.csv", library)
    library.AddDict("options", options)
    
    jobs = Importer.ImportJobs("jobs_lib.csv", library) 
    library.AddDict("jobs", jobs)
    return library

def makeCharacter(library, i):
    stats = {}
    stats['STR'] = 8
    stats['DEX'] = 8 + 6
    stats['CON'] = 8 + 2
    stats['INT'] = 8 + 2
    stats['WIS'] = 8 + 4
    stats['CHR'] = 8 + 6

    job_names = library.GetNameUUIDAsDict("jobs")
    
    character = Character("Ace" + str(i), job_names["Card Dealer"], 20, 'M', "Neutral Good", stats)
    character.AddToInventory('Sword', 2)
    character.AddToInventory('Shield', 4)
    character.AddToInventory('Helmet', 3)
    character.AddToInventory('Boots', 8)
    character.AddToInventory('Gloves', 3)
    character.AddToInventory('Pants', 5)
    character.AddToInventory('Shirt', 2)
    character.AddToInventory('Apple', 6)
    character.AddToInventory('Brick', 34)

    character.Equip('Sword')
    character.Equip('Shield')
    character.Equip('Helmet')
    character.Equip('Boots')
    character.Equip('Gloves')
    character.Equip('Pants')
    character.Equip('Shirt')

    for _ in range(3): 
        next_level_options = character.GetNextLevelOptions(library)

        selected_options = {}
        for option_uuid in next_level_options:
            selected_options[option_uuid] = []
            option_dict = next_level_options[option_uuid]
            for ii in range(option_dict['num_options']):
                selected_options[option_uuid].append(option_dict['feature_uuids'][ii])

        character.IncrementLevel(library, selected_options)
    return character

library = makeLibrary()
characters = [makeCharacter(library, i) for i in range(3)]
character = characters[0]

@app.route('/', methods=['GET'])
def index():
    return render_template('index.html', characters=characters, character=character)

@app.route('/import', methods=['GET', 'PUT'])
def importFile():
    filename = request.args.get("importfile")
    type = request.args.get("type")
    if type == 'effects':
        effects = Importer.ImportEffects(filename)
        library.AddDict('effects', effects)
    elif type == 'features':
        features = Importer.ImportFeatures(filename, library)
        library.AddDict('features', features)
    elif type == 'options':
        options = Importer.ImportOptions(filename, library)
        library.AddDict('options', options)
    elif type == 'jobs':
        jobs = Importer.ImportOptions(filename, library)
        library.AddDict('jobs', jobs)
    elif type == 'items':
        pass
    return render_template('index.html', characters=characters, character=character)


if __name__ == '__main__':
    app.run(debug=True)

