import tkinter as tk
from tkinter import ttk
from mysqlFunctions import *
from mongodbFunctions import *


# TODO: try-catch

class MyApp:
    def __init__(self, root):
        self.root = root
        self.root.title("DB project")

        # Create a notebook-style interface
        self.notebook = ttk.Notebook(self.root)

        # Create team tab
        self.team_tab = ttk.Frame(self.notebook)
        self.create_team_tab()

        # Create player tab
        self.player_tab = ttk.Frame(self.notebook)
        self.create_player_tab()

        # Add tabs to notebook
        self.notebook.add(self.team_tab, text='Team')
        self.notebook.add(self.player_tab, text='Player')
        self.notebook.pack(expand=1, fill='both')

        create_db()

    def create_team_tab(self):
        # Team tab elements
        self.label_team_name = ttk.Label(self.team_tab, text='Team name:')
        self.label_team_name.grid(row=0, column=0, padx=5, pady=5)

        self.entry_team_name = ttk.Entry(self.team_tab)
        self.entry_team_name.grid(row=0, column=1, padx=5, pady=5)

        self.hidden_error_team = ttk.Label(self.team_tab, text='', foreground='red')
        self.hidden_error_team.grid(row=1, columnspan=2, padx=5, pady=5)

        self.button_send_team = ttk.Button(self.team_tab, text='send', command=self.on_send_team)
        self.button_send_team.grid(row=2, columnspan=2, padx=5, pady=5)

    def create_player_tab(self):
        # player tab elements
        self.label_name = ttk.Label(self.player_tab, text='name:')
        self.label_name.grid(row=0, column=0, padx=5, pady=5)

        self.entry_name = ttk.Entry(self.player_tab)
        self.entry_name.grid(row=0, column=1, padx=5, pady=5)

        self.label_team = ttk.Label(self.player_tab, text='team:')
        self.label_team.grid(row=1, column=0, padx=5, pady=5)

        # Simulating clickable field (dropdown menu) for team selection
        self.team_options = read_teams()
        team_var = tk.StringVar(self.player_tab)

        self.team_dropdown = ttk.Combobox(self.player_tab, textvariable=team_var, values=self.team_options)
        self.team_dropdown.grid(row=1, column=1, padx=5, pady=5)

        self.hidden_error_player = ttk.Label(self.player_tab, text='', foreground='red')
        self.hidden_error_player.grid(row=2, columnspan=2, padx=5, pady=5)

        self.button_send_player = ttk.Button(self.player_tab, text='send', command=self.on_send_player)
        self.button_send_player.grid(row=3, columnspan=2, padx=5, pady=5)

    def on_send_team(self):
        self.send_team_mysql()

    def on_send_player(self):
        self.send_player_mysql()

    def send_team_mysql(self):
        team_name = self.entry_team_name.get()
        if team_name == "" or team_name is None:
            self.hidden_error_team.config(text="Enter team name!", foreground='red')
            return
        if team_already_in_db(team_name):
            self.hidden_error_team.config(text="This team already exists in the databases!", foreground='red')
            return
        else:
            insert_team(team_name)
            team_id = get_team_id(team_name)

            insert_team_mongodb(team_name, team_id)

            self.hidden_error_team.config(text="Team data inserted successfully!", foreground='green')
            self.entry_team_name.delete(0, tk.END)

    def send_player_mysql(self):
        player_name = self.entry_name.get()
        team_name = self.team_dropdown.get()

        player_problem = not player_name
        team_problem = not team_name

        if player_problem + team_problem == 2:
            self.hidden_error_player.config(text="Enter player and team name!", foreground='red')
        elif player_problem:
            self.hidden_error_player.config(text="Enter player name!", foreground='red')
        elif team_problem:
            self.hidden_error_player.config(text="Enter team name!", foreground='red')
        else:
            team_id = get_team_id(team_name)
            if player_already_in_db(team_id, player_name):
                self.hidden_error_player.config(text="Player is already registered in the team!", foreground='red')
            else:
                insert_player(team_id, player_name)

                player_id = get_player_id(player_name, team_id)
                insert_player_mongodb(team_id, player_name, player_id)

                self.hidden_error_player.config(text="Player data inserted successfully!", foreground='green')
                self.entry_name.delete(0, tk.END)


# Create the main window
root = tk.Tk()
app = MyApp(root)
root.mainloop()
