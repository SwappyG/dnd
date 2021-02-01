from Library import Library
from Character import Character
from pprint import pprint
import Importer

from flask import Flask, render_template, request
from random import randint

app = Flask(__name__)

def makeLibrary():
    library = Library()

    effects = Importer.import_effects("effects_lib.csv")
    library.AddDict("effects", effects)

    features = Importer.ImportFeatures("features_lib.csv", library)
    library.AddDict("features", features)
    
    options = Importer.ImportOptions("options_lib.csv", library)
    library.AddDict("options", options)
    
    jobs = Importer.ImportJobs("jobs_lib.csv", library) 
    library.AddDict("jobs", jobs)
    return library

def makeCharacter(server, i):
    stats = {}
    stats['STR'] = 8
    stats['DEX'] = 8 + 6
    stats['CON'] = 8 + 2
    stats['INT'] = 8 + 2
    stats['WIS'] = 8 + 4
    stats['CHR'] = 8 + 6

    job_names = server._library.GetNameUUIDAsDict("jobs")
    server.AddCharacter("Ace" + str(i), job_names["Card Dealer"], 20, 'M', "Neutral Good", stats, 99, 11)
    server.AddToInventory('Ace' + str(i), 'Sword', 2)
    server.AddToInventory('Ace' + str(i), 'hield', 4)
    server.AddToInventory('Ace' + str(i), 'elmet', 3)
    server.AddToInventory('Ace' + str(i), 'Boots', 8)
    server.AddToInventory('Ace' + str(i), 'loves', 3)
    server.AddToInventory('Ace' + str(i), 'Pants', 5)
    server.AddToInventory('Ace' + str(i), 'Shirt', 2)
    server.AddToInventory('Ace' + str(i), 'Apple', 6)
    server.AddToInventory('Ace' + str(i), 'rick', 34)

    server.Equip('Ace' + str(i), 'Sword', 1)
    server.Equip('Ace' + str(i), 'hield', 1)
    server.Equip('Ace' + str(i), 'elmet', 1)
    server.Equip('Ace' + str(i), 'Boots', 1)
    server.Equip('Ace' + str(i), 'loves', 1)
    server.Equip('Ace' + str(i), 'Pants', 1)
    server.Equip('Ace' + str(i), 'Shirt', 1)
    server.IncrementLevel('Ace' + str(i))
    server.IncrementLevel('Ace' + str(i))
    server.IncrementLevel('Ace' + str(i))


from BackendServer import BackendServer

server = BackendServer()
for i in range(3):
    makeCharacter(server, i)

@app.route('/', methods=['GET'])
def index():
    return render_template('index.html', context=server.GetContext())

@app.route('/character', methods=['GET', 'POST'])
def character():
    character_name = request.form.get('currcharacter')

    server.GetContext()['curr_character'] = server.GetContext()['characters'][character_name]
    return render_template('index.html', context=server.GetContext())

@app.route('/character/inventory', methods=['GET', 'PUT'])
def inventory():
    character_name = server.GetContext()['curr_character']['name']
    item_name = request.args.get('item')
    action = request.args.get('action')
    if action == 'decrement':
        server.RemoveFromInventory(character_name, item_name, 1)
    else:
        server.AddToInventory(character_name, item_name, 1)
    server.GetContext()['curr_character'] = server.GetContext()['characters'][character_name]
    return render_template('index.html', context=server.GetContext())

@app.route('/character/equiped', methods=['GET', 'PUT'])
def equiped():
    character_name = server.GetContext()['curr_character']['name']
    item_name = request.args.get('item')
    action = request.args.get('action')
    print(character_name, item_name, action)
    if action == 'decrement':
        print('decrementing')
        server.Unequip(character_name, item_name, 1)
    else:
        server.Equip(character_name, item_name, 1)

    server.GetContext()['curr_character'] = server.GetContext()['characters'][character_name]
    return render_template('index.html', context=server.GetContext())

@app.route('/import', methods=['GET', 'PUT'])
def importFile():
    filename = request.args.get("importfile")
    dict_type = request.args.get("type")

    server.ImportToLibrary(dict_type, filename)
    return render_template('index.html', context=server.GetContext())


if __name__ == '__main__':
    app.run(debug=True)

