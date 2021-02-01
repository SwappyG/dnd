from Library import Library
from Character import Character
from pprint import pprint
import Importer

def test():
    print ("===========================")
    print ("===                     ===")
    print ("===  Starting DnD test  ===")
    print ("===                     ===")
    print ("===========================")
    print ("\n")

    library = Library()

    effects = Importer.import_effects("effects_lib.csv")
    library.AddDict("effects", effects)

    features = Importer.ImportFeatures("features_lib.csv", library)
    library.AddDict("features", features)
    
    options = Importer.ImportOptions("options_lib.csv", library)
    library.AddDict("options", options)
    
    jobs = Importer.ImportJobs("jobs_lib.csv", library) 
    library.AddDict("jobs", jobs)

    print("Printing contents of all features\n")
    for feature_uuid in features:
        feature = features[feature_uuid]
        print(("Name <{}>, UUID <{}>, Effects <{}>, Prereqs <{}>, Unlock Level <{}>".format(
            feature.GetName(), str(feature.GetUUID()), str(feature.GetEffects()), str(feature.GetPrereqFeatures()),
            feature.GetUnlockLevel()
        )))

    print("\nPrinting contents of all options\n")
    for option_uuid in options:
        option = options[option_uuid]
        print(("Name <{}>, UUID <{}>, Features <{}>, Prereqs <{}>, Unlock Levels <{}>".format(
            option.GetName(), option.GetUUID(), option.GetAllFeatures(), option.GetPrereqFeatures(),
            option.GetUnlockLevels()
        )))

    print("\nPrinting contents of all jobs\n")
    for job_uuid in jobs:
        job = jobs[job_uuid]
        print(("Name <{}>, UUID <{}>, Features <{}>, Options <{}>".format(
            job.GetName(), job.GetUUID(), job.GetAllFeatures(), job.GetAllOptions()
        )))

    print ("\nMaking a Character\n")

    stats = {}
    stats['STR'] = 8
    stats['DEX'] = 8 + 6
    stats['CON'] = 8 + 2
    stats['INT'] = 8 + 2
    stats['WIS'] = 8 + 4
    stats['CHR'] = 8 + 6

    job_names = library.GetNameUUIDAsDict("jobs")
    character = Character("Ace", job_names["Card Dealer"], 20, "Neutral Good", stats)

    for jj in range(4):
        print(("Incrementing Level {}/2\n".format(jj)))
        
        print ("Grabbing the Options for the next level\n")
        next_level_options = character.GetNextLevelOptions(library)
        
        pprint(next_level_options)

        print ("\nSelecting some features from the options\n")
        selected_options = {}
        for option_uuid in next_level_options:
            selected_options[option_uuid] = []
            option_dict = next_level_options[option_uuid]
            for ii in range(option_dict['num_options']):
                selected_options[option_uuid].append(option_dict['feature_uuids'][ii])

            print(("selecting:", selected_options[option_uuid]))

        print("Passing selections to increment level")

        character.IncrementLevel(library, selected_options)

        print(("Level <{}>, Learned features <{}>".format(character.GetLevel(), character.GetLearnedFeatures())))

    # print "\n", (character.GetNextLevelOptions())
    # selected_options = {}
    # selected_options['Tricked Deck'] = ["Sharpened Diamonds"]

    # character.IncrementLevel(selected_options)
    # print "Learned features <{}>".format(character.GetLearnedFeatures())

    # print "Level <{}>, Stats <{}>".format(character.GetLevel(), character.GetStats())
