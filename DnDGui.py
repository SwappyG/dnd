import wdom.tag as Tag
from wdom.document import set_app, get_document
from wdom.server import start
from wdom.themes import bootstrap3
import wdom.themes.bootstrap3 as BootStrap

class StatsContainer(object):
    def __init__(self, parent_node):

        # Declare all the values that can change
        self.vals = {}
        self.vals['STR'] = "10"
        self.vals['DEX'] = "10"
        self.vals['CON'] = "10"
        self.vals['INT'] = "10"
        self.vals['WIS'] = "10"
        self.vals['CHA'] = "10"
        self.vals['HP'] = "8"
        self.vals['AC'] = "15"

        # Make two columns, one for the stat name and one for the stat values
        self.cols = {}
        self.cols['stats'] = BootStrap.Col6(parent=parent_node)
        self.cols['vals'] = BootStrap.Col6(parent=parent_node)

        # Create the stat labels
        self.stats_rows = {}
        self.stats_rows['STR'] = Tag.H4("STR", parent=self.cols['stats'])
        self.stats_rows['DEX'] = Tag.H4("DEX", parent=self.cols['stats'])
        self.stats_rows['CON'] = Tag.H4("CON", parent=self.cols['stats'])
        self.stats_rows['INT'] = Tag.H4("INT", parent=self.cols['stats'])
        self.stats_rows['WIS'] = Tag.H4("WIS", parent=self.cols['stats'])
        self.stats_rows['CHA'] = Tag.H4("CHA", parent=self.cols['stats'])
        self.stats_rows['HP'] = Tag.H4("HP", parent=self.cols['stats'])
        self.stats_rows['AC'] = Tag.H4("AC", parent=self.cols['stats'])

        # Populate with default values
        self.stat_val_rows = {}
        self.stat_val_rows['STR'] = Tag.H4(self.vals["STR"], parent=self.cols['vals'])
        self.stat_val_rows['DEX'] = Tag.H4(self.vals["DEX"], parent=self.cols['vals'])
        self.stat_val_rows['CON'] = Tag.H4(self.vals["CON"], parent=self.cols['vals'])
        self.stat_val_rows['INT'] = Tag.H4(self.vals["INT"], parent=self.cols['vals'])
        self.stat_val_rows['WIS'] = Tag.H4(self.vals["WIS"], parent=self.cols['vals'])
        self.stat_val_rows['CHA'] = Tag.H4(self.vals["CHA"], parent=self.cols['vals'])
        self.stat_val_rows['HP'] = Tag.H4(self.vals["HP"], parent=self.cols['vals'])
        self.stat_val_rows['AC'] = Tag.H4(self.vals["AC"], parent=self.cols['vals'])

    def UpdateVals(vals_dict):
        for name in vals_dict:
            try:
                self.vals[name] = vals_dict[name]
            except KeyError:
                print("Bad key in StatsContainer UpdateVals, <{}>", name)
                continue

class CharacterContainer(object):
    def __init__(self, parent_node, player_names):

        # Declare all the variable data
        self.vals = {}
        self.vals['character_name'] = 'Name'
        self.vals['character_job'] = 'Fighter'
        self.vals['character_level'] = 'Level 1'
        self.vals['character_gender_age'] = 'M24'
        self.vals['description'] = "Lorem Ipsum"

        # Two columns, left side is the buttons and the right side is the data
        self.cols = {}
        self.cols['side_bar'] = BootStrap.Col2(parent=parent_node)
        self.cols['main'] = BootStrap.Col10(parent=parent_node)

        # Make a row for each player button + title + summary button
        # self._status_player_rows = []
        # self._status_player_rows.append(BootStrap.Row(parent=self.cols['side_bar']))
        # self._status_player_rows.append(BootStrap.Row(parent=self.cols['side_bar']))
        # self._status_player_rows.append(BootStrap.Row(parent=self.cols['side_bar']))
        # self._status_player_rows.append(BootStrap.Row(parent=self.cols['side_bar']))
        # self._status_player_rows.append(BootStrap.Row(parent=self.cols['side_bar']))
        # self._status_player_rows.append(BootStrap.Row(parent=self.cols['side_bar']))
        # self._status_player_rows.append(BootStrap.Row(parent=self.cols['side_bar']))
        # self._status_player_rows.append(BootStrap.Row(parent=self.cols['side_bar']))

        # Add the status title
        self._title = Tag.H2("Status", parent=self.cols['side_bar'])
        
        # Add the player buttons
        self.buttons = {}
        player_names.append("Summary")
        for player_name in player_names:
            self.buttons[player_name] = BootStrap.Button(player_name, parent=self.cols['side_bar'])

        self.main_rows = {}
        self.main_rows['header'] = BootStrap.Row(parent=self.cols['main'])
        self.main_rows['body'] = BootStrap.Row(parent=self.cols['main'])
        
        # Create Columns for the header row in description
        self.cols['character_name'] = BootStrap.Col2(parent=self.main_rows['header'])
        self.cols['character_job'] = BootStrap.Col6(parent=self.main_rows['header'])
        self.cols['character_level'] = BootStrap.Col2(parent=self.main_rows['header'])
        self.cols['character_gender_age'] = BootStrap.Col2(parent=self.main_rows['header'])

        # Populate the description header row

        self.basic_info = {}
        self.basic_info['character_name'] = Tag.H3(self.vals['character_name'], parent=self.cols['character_name'])
        self.basic_info['job'] = Tag.H3(self.vals['character_job'], parent=self.cols['character_job'])
        self.basic_info['level'] = Tag.H3(self.vals['character_level'], parent=self.cols['character_level'])
        self.basic_info['gender_age'] = Tag.H3(self.vals['character_gender_age'], parent=self.cols['character_gender_age'])

        self.cols['stats'] = BootStrap.Col2(parent=self.main_rows['body'])
        self.cols['items_features'] = BootStrap.Col10(parent=self.main_rows['body'])
        
        self.stats = StatsContainer(self.cols['stats'])

    def UpdateVals(vals_dict):
        for name in vals_dict:
            try:
                self.vals[name] = vals_dict[name]
            except KeyError:
                print("Bad key in CharacterContainer UpdateVals, <{}>", name)
                continue


class DnDGui(BootStrap.Container):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self._document = get_document()
        self._document.register_theme(bootstrap3)
        
        # header
        self._header = BootStrap.Row(parent=self)
        self._title_text = Tag.H1("Welcome to DnD", background_color="lightblue", parent=self._header)

        # import heading
        self._import_body = BootStrap.Row(parent=self)
        self._import_body_cols = []
        self._import_body_cols.append(BootStrap.Col2(parent=self._import_body))
        self._import_body_cols.append(BootStrap.Col2(parent=self._import_body))
        self._import_body_cols.append(BootStrap.Col2(parent=self._import_body))
        self._import_body_cols.append(BootStrap.Col2(parent=self._import_body))
        self._import_body_cols.append(BootStrap.Col2(parent=self._import_body))

        self._import_title_text = Tag.H2("Import", parent=self._import_body_cols[0])
        
        # import buttons
        self._import_buttons = {}
        self._import_buttons['jobs'] = BootStrap.Button("Jobs", parent=self._import_body_cols[1])
        self._import_buttons['options'] = BootStrap.Button("Options", parent=self._import_body_cols[2])
        self._import_buttons['features'] = BootStrap.Button("Features", parent=self._import_body_cols[3])
        self._import_buttons['effects'] = BootStrap.Button("Effects", parent=self._import_body_cols[4])
        for name, button in self._import_buttons.items():
            button.addEventListener('click', self.OnButtonImportClick)

        players = ["Swapnil", "Waqar", "Robin", "Chiem", "Vib", "Lochan"] 
        self._status_body = BootStrap.Row(parent=self)
        self._status = CharacterContainer(self._status_body, players)
        
        # Add event listeners for the player buttons
        for name, button in self._status.buttons.items():
            button.addEventListener('click', self.OnButtonPlayerClick)

        # For testing only
        self._test_body = BootStrap.Container(parent=self)
        self._test_text = Tag.H2("Test Zone", parent=self._test_body)

    def OnButtonPlayerClick(self, event):
        self._test_text.textContent = event.currentTarget.textContent

    def OnButtonImportClick(self, event):
        self._test_text.textContent = event.currentTarget.textContent

if __name__=="__main__":
    set_app(DnDGui())
    start()