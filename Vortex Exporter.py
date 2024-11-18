import json, textwrap
import os
import datetime as dt
import tkinter
from tkinter import *
from tkinter import ttk
from tkinter.filedialog import askopenfilename, askdirectory

# ===================================== settings ============================================
UI_BG_COLOR = "#212121"
UI_FG_COLOR = "#d6d6d6"
UI_BUTTON_COLOR = "#424242"
UI_ALT_BG_COLOR = "#303030"
UI_FONT_NAME = "times new roman"
UI_FONT_SIZE_MAIN = 16
UI_FONT_SIZE_SMALL = 12
UI_FONT_SIZE_VERSION = 8
UI_ACTIVE_COLOR = "#14C38E"
VERSION_NUMBER = 1.1


# ========================================= variables =========================================
selected_file = "Select a vortex backup .json file"
export_path = os.path.abspath("Export/")
backup_data = {}
games_list = []
profiles_list = {}
mods_per_game = {}

# ===================================== Button_functions ======================================


def export_button():
    save_settings()
    selected_game_ids = games_tree.selection()
    selected_games = [games_tree.item(game)["values"][0] for game in selected_game_ids]
    
    selected_profile_ids = profiles_tree.selection()
    selected_profiles = [profiles_tree.item(profile)["values"][0] for profile in selected_profile_ids]
        
    if file_label['text'] != "Select a vortex backup .json file" and export_dir_label["text"] != "Select a location to export to":
        if file_label['text'] and export_dir_label["text"]:
            if len(selected_profiles) > 0:
                status_message_label.config(text=f'Exporting {selected_profiles} mod list')
                export_mod_list_better(selected_profiles)
                status_message_label.config(text=f'Export of {selected_profiles} complete')
                status_message_label.config(text=f"Export complete")
            elif "All" in selected_games:
                for game in games_list:
                    status_message_label.config(text=f"Exporting {game} mod list")
                    export_mod_list(game)
                    status_message_label.config(text=f"Exporting {game} complete")
                status_message_label.config(text=f"Export complete")
            else:
                for game in selected_games:
                    status_message_label.config(text=f"Exporting {game} mod list")
                    export_mod_list(game)
                    status_message_label.config(text=f"Exporting {game} complete")
                status_message_label.config(text=f"Export complete")
        else:
            status_message_label.config(text=f"Select a file and a destination")
    else:
        status_message_label.config(text=f"Select a file and a destination")


def file_selection():
    global selected_file
    selection = askopenfilename(
        filetypes=[('json files', '*.json')],
        title="Select a vortex backup file (.json)",
        initialdir='/'
    )
    selected_file = selection
    file_label.config(text=textwrap.shorten(text=selected_file, width=50, placeholder="..."))
    load_backup_json()


def select_export_path():
    global export_path
    selection = askdirectory(
        title="Select a folder to export to",
        initialdir='/'
    )
    export_path = selection
    export_dir_label.config(text=textwrap.shorten(text=export_path, width=50, placeholder="..."))



# ========================================= Functions =========================================

def load_last_settings():
    global selected_file, export_path
    try:
        with open("Resources/settings.json") as settings:
            options = json.load(settings)
        selected_file = options["selected_file"]
        file_label.config(text=selected_file)
        export_path = options["export_path"]
        export_dir_label.config(text=export_path)
        check_file_name_var.set(options["check_file_name_var"])
        check_state_var.set(options["check_state_var"])
        check_link_var.set(options["check_link_var"])
        if selected_file != "Select a vortex backup .json file":
            load_backup_json()
    except FileNotFoundError:
        # File has not been created yet
        pass


def save_settings():
    with open(file="Resources/settings.json", mode="w") as settings:
        selection = {
            "selected_file": selected_file,
            "export_path": export_path,
            "check_file_name_var": check_file_name_var.get(),
            "check_state_var": check_state_var.get(),
            "check_link_var": check_link_var.get()
        }
        json.dump(selection, settings, indent=4)


def config_button(button):
    button.config(
        bg=UI_BUTTON_COLOR,
        fg=UI_FG_COLOR,
        font=(UI_FONT_NAME, UI_FONT_SIZE_SMALL),
        activebackground=UI_ACTIVE_COLOR,
        activeforeground="black",
        width=10
    )


def label_config(label: Label, text: str):
    label.config(
        text=text,
        font=(UI_FONT_NAME, UI_FONT_SIZE_MAIN),
        fg=UI_FG_COLOR,
        bg=UI_BG_COLOR,
        width=35,
        anchor="w"
    )


def small_label_config(label: Label, text: str):
    label.config(
        text=text,
        font=(UI_FONT_NAME, UI_FONT_SIZE_SMALL),
        fg=UI_FG_COLOR,
        bg=UI_BG_COLOR,
        anchor="w"
    )


def update_tree():
    # TODO: if incompatible json file is selected show error
    games_tree.delete(*games_tree.get_children())
    games_tree.insert(
        "",
        tkinter.END,
        values=(
            "All",
            "--")
        )
    for game in games_list:
        games_tree.insert(
            "",
            tkinter.END,
            values=(
                game,
                len(mods_per_game[game])
            )
        )
    middle_frame.grid(row=1, column=0, sticky="EW")

def update_profiles_tree(game):
    profile_list = get_profiles(game)
    profile_data = backup_data["persistent"]["profiles"]
    profiles_tree.delete(*profiles_tree.get_children())

    for profile in profile_list:
        profile = profile_data[profile]
        profiles_tree.insert(
            "",
            tkinter.END,
            values=(
                profile["name"],
                mods_per_profile(profile))
            )
        
    middle_frame.grid(row=1, column=0, sticky="EW")

def update_profiles_tree_multiple(games):
    profile_list = []

    #get all profiled from every game selected
    for game in games:
        profile_list[game] = get_profiles(game)

    #get all profiles from the profile list.
    for profile in profile_list:
        profiles_tree.insert(
            "",
            tkinter.END,
            values=(
                profile,
                mods_per_profile(profile))
            )
        
    middle_frame.grid(row=1, column=0, sticky="EW")

def mods_per_profile(profile):
    count = 0

    for mod in profile["modState"]:
        count+=1
    return count

def mods_per_profile_enabled(profile):
    profile = backup_data["persistent"],["profiles"][profile]
    count = 0

    for mod in profile["modState"]:
        if mod["enabled"] == 'true':
            count+=1
    return count

def load_backup_json():
    global backup_data, games_list, mods_per_game, selected_file
    try:
        with open(file=selected_file, mode="r", encoding="utf8") as backup_file:
            backup_data = json.load(backup_file)

        mods_per_game = backup_data["persistent"]["mods"]
        games_list = [game for game in mods_per_game]
        update_tree()
    except FileNotFoundError:
        # no file selected or previous file does not exist anymore
        selected_file = "Select a vortex backup .json file"
        file_label.config(text="Select a vortex backup .json file")

def on_select(event):
    selected_game_ids = games_tree.selection()
    selected_games = [games_tree.item(game)["values"][0] for game in selected_game_ids]

    if selected_games:
        if len(selected_games) > 1:
            update_profiles_tree_multiple(selected_games)
        else:
            update_profiles_tree(selected_games)

def get_profiles(game, all=False):
    '''
    Get all profiles for the specified game.
    str game: specified game
    bool all: if game is not specified then get all profiles.
    returns a dictionary of profiles.
    '''
    global profiles_list
    game = game[0]
    profiles = {}
    profile_data = backup_data["persistent"]["profiles"]
    for profile in profile_data:
        profile = profile_data[profile]
        if all:
            profiles[profile["id"]] = profile
        elif profile["gameId"] == game.strip().lstrip():
            profiles[profile["id"]] = profile
        profiles_list[profile["name"]] = profile["id"]
    

    '''
    should look like:
    {
        bABDFR36T1: cool profile{...},
        ADVBF122fg: neato profile,
    }
    '''
    
    return profiles

def get_mods(game):
    enabled_mods = {}
    disabled_mods = {}
    combined_mods = {}

    profiles = get_profiles(game)
    for profile in profiles:
        for key, mod in profile["modState"]:
            combined_mods[key] = "enabled: ", mod['enabled']
            if mod["enabled"] == "true":
                enabled_mods[key] = "enabled: ", mod['enabled']
            else:
                disabled_mods[key] = "enabled: ", mod['enabled']

    return [enabled_mods,disabled_mods,combined_mods]

def export_mod_list_better(profiles):
    filename = export_path + "\\"
    filename += "vortex_export"
    timestamp = dt.datetime.today().strftime("__%d-%m-%Y_%H-%M-%S")
    filename += timestamp + ".txt"
    if check_enabled_name_var.get() == 1:
        enabled_only = True
        print("enabled only!!!")

    first_time = False
    for profile in profiles:
        profile = backup_data["persistent"]["profiles"][profiles_list[profile]]
        first_time = True
        for mod in profile["modState"]:
            modname = mod
            mod = profile["modState"][mod]
            enabled = "enabled" if mod["enabled"] == True else "disabled"
            if enabled_only == True:
                if mod["enabled"] == True:
                    export = "[Mod] " + modname + " | " + enabled
                else:
                    continue
            else:
                export = "[Mod] " + modname + " | " + enabled

            if first_time:
                export_temp = export
                export = f'\n{profile["name"]}\n\n'+('-'*25) + '\n' + export_temp
                first_time = False
            with open(filename, mode="a+") as file:
                file.write(export + "\n")
    print(filename)

def export_mod_list(game):
    filename = export_path + "/"
    filename += game
    timestamp = dt.datetime.today().strftime("__%d-%m-%Y_%H-%M-%S")
    filename += timestamp + ".txt"
    mods = backup_data["persistent"]["mods"][game]
    for mod in mods:
        attributes = mods[mod]["attributes"]
        export = "[Mod] " + attributes["name"]
        try:
            if check_file_name_var.get() == 1:
                export += f" [Filename] {attributes['fileName']}"
        except KeyError:
            # Filename missing ignore
            pass
        try:
            if check_state_var.get() == 1:
                export += f" [state] {mods[mod]['state']}"
        except KeyError:
            # state missing ignore
            pass
        try:
            if check_link_var.get() == 1:
                export += f" [link] {attributes['homepage']}"
        except KeyError:
            # link missing ignore
            pass
        with open(filename, mode="a") as file:
            file.write(export + "\n")

# ===================================== UI setup ============================================

main_window = Tk()
main_window.title(f"Modlist extractor V{VERSION_NUMBER}")
main_window.iconbitmap(bitmap="Resources/Vortex_extractor.ico")
main_window.config(bg=UI_BG_COLOR, pady=20, padx=20)

top_frame = Frame(main_window)
top_frame.config(bg=UI_BG_COLOR)
top_frame.grid(row=0, column=0, sticky="EW")

middle_frame = Frame(main_window)
middle_frame.config(bg=UI_BG_COLOR)
middle_frame.grid(row=1, column=0, sticky="EW")

options_frame = Frame(middle_frame)
options_frame.config(bg=UI_BG_COLOR)
options_frame.grid(row=1, column=3, sticky="EW")

profile_options_frame = Frame(middle_frame)
profile_options_frame.config(bg=UI_BG_COLOR)
profile_options_frame.grid(row=2, column=3, sticky="EW")

bottom_frame = Frame(main_window)
bottom_frame.config(bg=UI_BG_COLOR)
bottom_frame.grid(row=2, column=0, sticky="EW")

style = ttk.Style()
style.theme_use("clam")

# labels

file_label = Label(top_frame)
label_config(file_label, selected_file)
file_label.grid(row=0, column=0)

export_dir_label = Label(bottom_frame)
label_config(export_dir_label, export_path)
export_dir_label.grid(row=0, column=0, pady=10)

export_options_label = Label(options_frame)
export_options_label.config(
    text="Export options",
    font=(UI_FONT_NAME, UI_FONT_SIZE_MAIN),
    fg=UI_FG_COLOR,
    bg=UI_BG_COLOR,
    anchor="w"
    )
export_options_label.grid(row=0, column=0, columnspan=2)

status_message_label = Label(bottom_frame)
small_label_config(status_message_label, "")
status_message_label.grid(row=1, column=0)

tree_label = Label(middle_frame)
small_label_config(tree_label, "Select the games you want to export")
tree_label.grid(row=0, column=0)

# buttons
select_button = Button(master=top_frame, text="Select file", command=file_selection)
config_button(select_button)
select_button.grid(row=0, column=1, sticky="E", padx=5, pady=3)

select_export_button = Button(master=bottom_frame, text="Select folder", command=select_export_path)
config_button(select_export_button)
select_export_button.grid(row=0, column=1, sticky="E", padx=5, pady=3)

export_button = Button(master=bottom_frame, text="Export", command=export_button)
config_button(export_button)
export_button.grid(row=1, column=1, sticky="E", padx=5, pady=3)

# checkboxes
check_file_name_var = IntVar(value=1)
check_file_name = Checkbutton(options_frame)
check_file_name.config(
    background=UI_BUTTON_COLOR,
    indicatoron=False,
    width=2,
    borderwidth=0,
    highlightthickness=0,
    activebackground=UI_BG_COLOR,
    activeforeground=UI_FG_COLOR,
    selectcolor=UI_ACTIVE_COLOR,
    variable=check_file_name_var,
)
check_file_name.grid(row=1, column=1)
check_file_name_label = Label(options_frame)
small_label_config(check_file_name_label, "Filename")
check_file_name_label.grid(row=1, column=0)

check_state_var = IntVar(value=1)
check_state = Checkbutton(options_frame)
check_state.config(
    background=UI_BUTTON_COLOR,
    indicatoron=False,
    width=2,
    borderwidth=0,
    highlightthickness=0,
    activebackground=UI_BG_COLOR,
    activeforeground=UI_FG_COLOR,
    selectcolor=UI_ACTIVE_COLOR,
    variable=check_state_var,
)
check_state.grid(row=2, column=1)
check_state_label = Label(options_frame)
small_label_config(check_state_label, "Install state")
check_state_label.grid(row=2, column=0)

check_link_var = IntVar()
check_link = Checkbutton(options_frame)
check_link.config(
    background=UI_BUTTON_COLOR,
    indicatoron=False,
    width=2,
    borderwidth=0,
    highlightthickness=0,
    activebackground=UI_BG_COLOR,
    activeforeground=UI_FG_COLOR,
    selectcolor=UI_ACTIVE_COLOR,
    variable=check_link_var,
)
check_link.grid(row=3, column=1)
check_link_label = Label(options_frame)
small_label_config(check_link_label, "Mod link")
check_link_label.grid(row=3, column=0)

# Profiles Tree

profiles_tree_columns = ("profile", "mods")
profiles_tree = ttk.Treeview(middle_frame, columns=profiles_tree_columns, show="headings", style="custom.Treeview")
profiles_tree.config(height=10)
profiles_tree.grid(row=2, column=0, pady=10)

profiles_tree.heading('profile', text='Profile')
profiles_tree.heading('mods', text='# Mods')
profiles_tree.column("profile", width=200, minwidth=40)
profiles_tree.column("mods", width=80, minwidth=40)

style.layout("custom.Treeview", [('custom.Treeview.treearea', {'sticky': 'nswe'})])

style.configure(
    "custom.Treeview",
    highlightthickness=0,
    bd=0,
    font=(UI_FONT_NAME, UI_FONT_SIZE_SMALL),
    bg=UI_ALT_BG_COLOR,
    background=UI_ALT_BG_COLOR,
    foreground=UI_FG_COLOR,
)
style.configure(
    "custom.Treeview.Heading",
    highlightthickness=0,
    bd=0,
    font=(UI_FONT_NAME, UI_FONT_SIZE_SMALL),
    bg=UI_ALT_BG_COLOR,
    background=UI_BUTTON_COLOR,
    foreground=UI_FG_COLOR,
    darkcolor=UI_ALT_BG_COLOR,
    lightcolor=UI_ALT_BG_COLOR,
    relief="flat"
)
# change color of selection
style.map("Treeview", background=[("selected", UI_ACTIVE_COLOR)])
style.map("Treeview.Heading", background=[("pressed", UI_ACTIVE_COLOR)])

scroll_barr = ttk.Scrollbar(middle_frame, orient="vertical", command=profiles_tree.yview)
profiles_tree.configure(yscrollcommand=scroll_barr.set)
scroll_barr.grid(row=2, column=1, pady=10, sticky="NS")


style.map("Vertical.TScrollbar", background=[("pressed", UI_ACTIVE_COLOR)])

style.configure(
    "Vertical.TScrollbar",
    troughcolor=UI_ALT_BG_COLOR,
    arrowcolor=UI_FG_COLOR,
    background=UI_BUTTON_COLOR,
    gripcount=0,
    bordercolor=UI_ALT_BG_COLOR,
    arrowsize=15,
    lightcolor=UI_BUTTON_COLOR,
    darkcolor=UI_BUTTON_COLOR
)

# Profiles export options

profiles_export_options_label = Label(profile_options_frame)
profiles_export_options_label.config(
    text="Profile export options",
    font=(UI_FONT_NAME, UI_FONT_SIZE_MAIN),
    fg=UI_FG_COLOR,
    bg=UI_BG_COLOR,
    anchor="w"
    )
profiles_export_options_label.grid(row=0, column=0, columnspan=2)

# Profiles button

check_enabled_name_var = IntVar(value=1)
check_enabled_name = Checkbutton(profile_options_frame)
check_enabled_name.config(
    background=UI_BUTTON_COLOR,
    indicatoron=False,
    width=2,
    borderwidth=0,
    highlightthickness=0,
    activebackground=UI_BG_COLOR,
    activeforeground=UI_FG_COLOR,
    selectcolor=UI_ACTIVE_COLOR,
    variable=check_enabled_name_var,
)
check_enabled_name.grid(row=1, column=1)
check_enabled_name_label = Label(profile_options_frame)
small_label_config(check_enabled_name_label, "Export only enabled")
check_enabled_name_label.grid(row=1, column=0)

# Tree
tree_columns = ("game", "mods")
games_tree = ttk.Treeview(middle_frame, columns=tree_columns, show="headings", style="custom.Treeview")
games_tree.config(height=10)
games_tree.grid(row=1, column=0)

games_tree.heading('game', text='Game')
games_tree.heading('mods', text='# mods')
games_tree.column("game", width=200, minwidth=40)
games_tree.column("mods", width=80, minwidth=40)

style.layout("custom.Treeview", [('custom.Treeview.treearea', {'sticky': 'nswe'})])

style.configure(
    "custom.Treeview",
    highlightthickness=0,
    bd=0,
    font=(UI_FONT_NAME, UI_FONT_SIZE_SMALL),
    bg=UI_ALT_BG_COLOR,
    background=UI_ALT_BG_COLOR,
    foreground=UI_FG_COLOR,
)
style.configure(
    "custom.Treeview.Heading",
    highlightthickness=0,
    bd=0,
    font=(UI_FONT_NAME, UI_FONT_SIZE_SMALL),
    bg=UI_ALT_BG_COLOR,
    background=UI_BUTTON_COLOR,
    foreground=UI_FG_COLOR,
    darkcolor=UI_ALT_BG_COLOR,
    lightcolor=UI_ALT_BG_COLOR,
    relief="flat"
)
# change color of selection
style.map("Treeview", background=[("selected", UI_ACTIVE_COLOR)])
style.map("Treeview.Heading", background=[("pressed", UI_ACTIVE_COLOR)])

scroll_barr = ttk.Scrollbar(middle_frame, orient="vertical", command=games_tree.yview)
games_tree.configure(yscrollcommand=scroll_barr.set)
scroll_barr.grid(row=1, column=1, sticky="NS")


style.map("Vertical.TScrollbar", background=[("pressed", UI_ACTIVE_COLOR)])

style.configure(
    "Vertical.TScrollbar",
    troughcolor=UI_ALT_BG_COLOR,
    arrowcolor=UI_FG_COLOR,
    background=UI_BUTTON_COLOR,
    gripcount=0,
    bordercolor=UI_ALT_BG_COLOR,
    arrowsize=15,
    lightcolor=UI_BUTTON_COLOR,
    darkcolor=UI_BUTTON_COLOR
)

load_last_settings()

games_tree.bind("<<TreeviewSelect>>", on_select)

main_window.mainloop()