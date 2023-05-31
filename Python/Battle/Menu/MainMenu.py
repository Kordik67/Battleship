from ursina import *
from .OptionsMenu import OptionsMenu
from .MenuButton import MenuButton

class MainMenu(Entity):
    def __init__(self, start_callback,client, **kwargs):
        self.start_callback = start_callback
        self.client=client
        super().__init__(parent=camera.ui, y=.15, **kwargs)
        
        if client.named:
            self.init_main_menu()
        else:
            self.input_pseudo = InputField(default_value="")
            self.input_pseudo.active = True
            self.valid_btn_pseudo = MenuButton(y=-.3 , text="Valider", on_click = self.verif_pseudo)
            
    def verif_pseudo(self):
        if len(self.input_pseudo.text) > 2:
            self.client.setName(self.input_pseudo.text)
            self.input_pseudo.enabled = False
            self.valid_btn_pseudo.enabled = False
            self.init_main_menu()

    def init_main_menu(self):
        self.background_music = Audio("assets/background_music.mp3", autoplay=True, loop=True)
        self.button_spacing = .075 * 1.2

        self.main_menu = Entity(parent=self)
        self.load_menu = Entity(parent=self)
        self.options_menu = OptionsMenu(
            self, self.background_music, Animator({ 'main_menu': self.main_menu }), self.button_spacing
        )
        self.game_menu = Entity(parent=self)
        self.background = Entity(
            parent=self, model='quad', texture='shore', scale=(camera.aspect_ratio,1), color=color.white, z=1, world_y=0
        )
                
        state_handler = Animator({
            'main_menu': self.main_menu,
            'game_menu': self.game_menu,
            'load_menu': self.load_menu,
            'options_menu': self.options_menu,
        })

        # main menu content
        self.main_menu.buttons = [
            MenuButton('Créer une partie', on_click=Sequence(Func(setattr, state_handler, 'state', 'game_menu'), Func(self.client.createGame))),
            MenuButton('Rejoindre une partie', on_click=Sequence(Func(setattr, state_handler, 'state', 'load_menu'), Func(self.client.requestGames))),
            MenuButton('Parties en cours', on_click=Sequence(Func(setattr, state_handler, 'state', 'load_menu'), Func(self.client.requestGames))),
            MenuButton('Options', on_click=Func(setattr, state_handler, 'state', 'options_menu')),
            MenuButton('Quitter', on_click=self.stop),
        ]

        for i, button in enumerate(self.main_menu.buttons):
            button.parent = self.main_menu
            button.y = (-i-2) * self.button_spacing
        
        # load menu content
        #for i in range(3):
            #MenuButton(parent=self.load_menu, text=f'Partie {i+1}', y=-i * self.button_spacing, on_click=self.start_game)

        self.load_menu.back_button = MenuButton(parent=self.load_menu, text='Retour', y=((-i-2) * self.button_spacing), on_click=Func(setattr, state_handler, 'state', 'main_menu'))
        
        # Ajouter la liste des joueurs
        self.player_list = [self.client.name]
        self.players = Text(text='Liste des joueurs :', scale=2, origin=(0, 1), y=0.25, parent=self.game_menu)
        self.player1 = Text(text=self.player_list[0], scale=1.5, origin=(0, 1), y=-0.05, parent=self.game_menu)
        self.player2 = Text(text='Joueur 2', scale=1.5, origin=(0, 1), y=-0.15, parent=self.game_menu)

        self.start_game_button = MenuButton(text='Démarrer la partie', parent=self.game_menu, y=-0.45, enabled=False, on_click=self.start)
        self.start_game_button.enabled = False

        # Ajouter le bouton pour ajouter une IA
        self.add_ai_button = MenuButton(text='Ajouter une IA', parent=self.game_menu, y=-0.35, on_click=self.add_ai_player)
        
        # Ajouter le bouton pour revenir au menu principal
        back_button = MenuButton(text='Retour', parent=self.game_menu, y=-0.55, on_click=Func(setattr, state_handler, 'state', 'main_menu'))


        # animate the buttons in nicely when changing menu
        for menu in (self.main_menu, self.load_menu, self.options_menu, self.game_menu):
            def animate_in_menu(menu=menu):
                for i, e in enumerate(menu.children):
                    e.original_x = e.x
                    e.x += .1
                    e.animate_x(e.original_x, delay=i*.05, duration=.1, curve=curve.out_quad)

                    e.alpha = 0
                    e.animate('alpha', .7, delay=i*.05, duration=.1, curve=curve.out_quad)

                    if hasattr(e, 'text_entity'):
                        e.text_entity_alpha = 0
                        e.text_entity.animate('alpha', 1, delay=i*.05, duration=.1)

        menu.on_enable = animate_in_menu

    def add_player(self, player_name):
        if len(self.player_list) < 2:
            self.player_list.append(player_name)
            self.update_player_list()

    def remove_player(self, player_name):
        if player_name in self.player_list:
            self.player_list.remove(player_name)
            self.update_player_list()

    def add_ai_player(self):
        self.add_player("IA")

        self.add_ai_button.text = "Supprimer l'IA"
        self.add_ai_button.on_click = self.remove_ai_player

    def remove_ai_player(self):
        if "IA" in self.player_list:
            self.player_list.remove("IA")
            self.update_player_list()

        self.add_ai_button.text = "Ajouter une IA"
        self.add_ai_button.on_click = self.add_ai_player

    def update_player_list(self):
        for player, player_name in zip((self.player1, self.player2), self.player_list[:2]):
            player.text = player_name

        if len(self.player_list) < 2:
            self.start_game_button.enabled = False
        else:
            self.start_game_button.enabled = True

        if "IA" not in self.player_list:
            self.player2.text = "Joueur 2"

    def start_game(self):
        self.enabled = False
        self.client.createGame()
        
    def start(self):
        self.enabled = False
        self.start_callback(self.client)
        self.client.startGame("IA" in self.player_list)

    def create_rooms_list(self, waiting_rooms, playing_rooms):
        for i in range(len(waiting_rooms)):
            MenuButton(parent=self.load_menu, text=waiting_rooms[i], y=-i * self.button_spacing, on_click=self.start_game)

        for i in range(len(playing_rooms)):
            MenuButton(parent=self.game_menu, text=waiting_rooms[i], y=-i * self.button_spacing, on_click=self.start_game)


    def stop(self):
        application.quit()
        self.client.stop = True
    