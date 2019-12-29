import os
import zipfile
import jsonpickle
from pprint import pprint

import pandas as pd
import uuid

from Effect import Effect
from Feature import Feature
from Option import Option
from Job import Job

def Import(library, dict_name, file_path):
    # TODO: Add exception handling
    if dict_name == 'effects':
        effects = ImportEffects(file_path)
        library.AddDict('effects', effects)
    elif dict_name == 'features':
        features = ImportFeatures(file_path, library)
        library.AddDict('features', features)
    elif dict_name == 'options':
        options = ImportOptions(file_path, library)
        library.AddDict('options', options)
    elif dict_name == 'jobs':
        jobs = ImportOptions(file_path, library)
        library.AddDict('jobs', jobs)
    elif dict_name == 'items':
        print("Item importing is not implemented yet")
        return False

    return True

def ImportCSV(file_path):
    data_frame = pd.read_csv(file_path, index_col='Name', sep="|")
    return data_frame.to_dict('index')

def ImportEffects(file_path):
    effects_dict = ImportCSV(file_path)
    effects = {}
    for name in effects_dict:
        print("importing Effect <{}>".format(name))
        this_uuid = uuid.uuid4()
        duration = effects_dict[name]['Duration']
        effect_type = effects_dict[name]['Type']
        description = effects_dict[name]['Description']
        effects[this_uuid] = Effect(name, this_uuid, effect_type, duration, description)
        
    return effects

def ImportFeatures(file_path, library):
    # Import the CSV file
    features_dict = ImportCSV(file_path)
    
    # Dict of all our imported features
    features = {}

    # Create UUIDs for all the features first
    features_name_uuid_dict = {}
    for name in features_dict:
        features_name_uuid_dict[name] = uuid.uuid4() 

    # Create all the features
    for name in features_dict:
        print("importing Feature <{}>".format(name))
        description = features_dict[name]['Description']
        
        # Try to find the UUIDs for all the effects that are listed
        try:
            effect_names = features_dict[name]['Effects'].split(";") if features_dict[name]['Effects'] != "None" else []
            effects = [library.GetUUIDFromName("effects", ii) for ii in effect_names]
        except:
            print("Failed to import feature <{}>, failed to parse effects likely due to duplication or invalid names, got effects <{}>".format(name, effect_names))
            continue

        # Try to find the UUIDs (that we just made) for all the prereqs that are listed
        # TODO: if can't find in this list, also check library
        try:
            prereq_feature_names = features_dict[name]['Prereq Features'].split(";") if features_dict[name]['Prereq Features'] != "None" else []
            prereq_features = [features_name_uuid_dict[ii] for ii in prereq_feature_names]
        except:
            print("Failed to import feature <{}>, failed to parse prereqs likely due to duplication or invalid names, got prereq features <{}>".format(name, prereq_feature_names))
            continue

        unlock_level = features_dict[name]['Unlock Level'] 

        # Instantiate this feature and add it to our dict
        this_uuid = features_name_uuid_dict[name]
        features[this_uuid] = Feature(name, this_uuid, description, effects, prereq_features, unlock_level)

    print("\n")
    return features

def ImportOptions(file_path, library):
    options_dict = ImportCSV(file_path)
    options = {}

    # Create UUIDs for all the options first
    options_name_uuid_dict = {}
    for option in options_dict:
        options_name_uuid_dict[option] = uuid.uuid4()

    # Create all the Option instances
    for name in options_dict:
        print("Importing Option <{}>".format(name))
        description = options_dict[name]['Description']

        # Try to get UUIDs for all the features in this option
        try:
            feature_names = options_dict[name]['Features'].split(";")
            features = [library.GetUUIDFromName("features", ii) for ii in feature_names]
        except:
            print("Failed to import option <{}>, failed to get UUID for features <{}>".format(name, feature_names))
            continue

        # Try to get UUIDs for all the prereqs in this option
        try:
            prereq_feature_names = options_dict[name]['Prereq Features'].split(";") if options_dict[name]['Prereq Features'] != "None" else []
            prereq_features = [library.GetUUIDFromName("features", ii) for ii in prereq_feature_names]
        except:
            print("Failed to import option <{}>, failed to get UUID for prereq features <{}>".format(name, prereq_feature_names))
            continue

        # Create an instance of this option and add it to our dict
        unlock_levels = options_dict[name]['Unlock Levels'].split(";")
        this_uuid = options_name_uuid_dict[name]
        options[this_uuid] = Option(name, this_uuid, description, features, prereq_features, unlock_levels)

    print("\n")    
    return options

def ImportJobs(file_path, library):
    jobs_dict = ImportCSV(file_path)
    jobs = {}
    for name in jobs_dict:
        print("Importing Job <{}>".format(name))
        this_uuid = uuid.uuid4()

        description = jobs_dict[name]['Description']
        
        try:
            feature_names = jobs_dict[name]['Features'].split(";")
            features = [library.GetUUIDFromName("features", ii) for ii in feature_names]
        except:
            print("Failed to import job <{}>, failed to get UUID for features <{}>".format(name, feature_names))
            continue

        try:
            option_names = jobs_dict[name]['Options'].split(";")
            options = [library.GetUUIDFromName("options", ii) for ii in option_names]
        except:
            print("Failed to import job <{}>, failed to get UUID for options <{}>".format(name, feature_names))
            continue
        
        jobs[this_uuid] = Job(name, this_uuid, description, features, options)

    print("\n")
    return jobs

def ImportCharacter(file_path):
    try:
        with open(file_path, 'r') as a_file:
            return jsonpickle.decode(a_file.read())
    except Exception as e:
        print(("Failed to open file with path [{}], got [{}]".format(file_path, e)))
        return None

def ExportCharacter(file_path, this_character):
    try:
        name = this_character.GetName()
        json_string = jsonpickle.encode(this_character)
    except Exception as e:
        print(("Failed to serial object [{}], got [{}]".format(name, e)))
    
    with open(file_path, 'w+') as a_file:
        a_file.write(json_string)

def Save(folderpath, zip_name, library, characters):
    files_to_zip = []
    for character in characters:
        this_file = "/character/" + character + ".json" 
        os.makedirs(os.path.dirname(folderpath + this_file), exist_ok=True)
        Pickle(folderpath + this_file, characters)
        files_to_zip.append((this_file, folderpath))

    this_file = "/library.json" 
    os.makedirs(os.path.dirname(folderpath + this_file), exist_ok=True)
    Pickle(folderpath + this_file, library)
    files_to_zip.append((this_file, folderpath))

    Zip(folderpath, zip_name, files_to_zip)

def Load(zip_name):
    with zipfile.ZipFile(zip_name) as zip:
        with zip.open('library.json') as library_json:
            Depickle(library_json)

def Zip(location, zip_name, files):
    # shutil.make_archive("test","zip")
    with zipfile.ZipFile(zip_name, 'w') as zipf:
        for filename, folder in files:
            zipf.write(folder + filename, filename)

def Depickle(filepath):
    try:
        with open(filepath, 'r') as a_file:
            return jsonpickle.decode(a_file.read())
    except Exception as e:
        print(("Failed to open file with path [{}], got [{}]".format(file_path, e)))
        return None

def Pickle(filepath, obj):
    try: 
        json_string = jsonpickle.encode(obj)
    except Exception as e:
        print(("Failed to serialize object, got [{}]".format(e)))
        return False

    with open(filepath, 'w+') as a_file:
        a_file.write(json_string)

    return True

def Main():
    effects = CreateEffects("test_effects.csv")

if __name__=="__main__":
    Main()