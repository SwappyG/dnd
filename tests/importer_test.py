import Importer
from Game import Game
from Library import Library
import os

def MakeLibrary():
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

if __name__=="__main__":

    game = Game()

    library = MakeLibrary()

    stats = {}
    stats['STR'] = 8
    stats['DEX'] = 8 + 6
    stats['CON'] = 8 + 2
    stats['INT'] = 8 + 2
    stats['WIS'] = 8 + 4
    stats['CHR'] = 8 + 6

    jobs = library.GetNameUUIDAsDict('jobs')

    game.ImportToLibrary('effects', "effects_lib.csv")
    game.ImportToLibrary('features', "features_lib.csv")
    game.ImportToLibrary('options', "options_lib.csv")
    game.ImportToLibrary('jobs', "jobs_lib.csv")

    game.AddCharacter("test_name_a", jobs['Card Dealer'], 21, 'F', 'Neutral Good', stats, 15, 12)

    game.AddToInventory('test_name_a', 'Sword', 2)
    game.AddToInventory('test_name_a', 'Shield', 4)
    game.AddToInventory('test_name_a', 'Helmet', 3)
    game.AddToInventory('test_name_a', 'Boots', 8)

    game.Equip('test_name_a', 'Sword', 1)
    game.Equip('test_name_a', 'Shield', 2)

    next_level_options = game.GetContext('next_level_options', character_name='test_name_a')

    selected_options = {}
    for option_uuid in next_level_options:
        selected_options[option_uuid] = []
        option_dict = next_level_options[option_uuid]
        for ii in range(option_dict['num_options']):
            selected_options[option_uuid].append(option_dict['feature_uuids'][ii])

    game.IncrementLevel('test_name_a', selected_options)

    game.Save(os.getcwd(), "test_zip.zip")

    game.Load('test_zip.zip')
