from ursina import *
from ursina.prefabs.dropdown_menu import DropdownMenu, DropdownMenuButton
from MenuButton import MenuButton
from OptionsMenu import OptionsMenu

app = Ursina()

window.fullscreen = True
background_music = Audio("../assets/background_music.mp3", autoplay=True, loop=True)

button_spacing = .075 * 1.2
menu_parent = Entity(parent=camera.ui, y=.15)
main_menu = Entity(parent=menu_parent)
load_menu = Entity(parent=menu_parent)
#options_menu = Entity(parent=menu_parent)
options_menu = OptionsMenu(menu_parent, background_music, Animator({ 'main_menu': main_menu }), button_spacing)
game_menu = Entity(parent=menu_parent)

background = Entity(parent=menu_parent, model='quad', texture='shore', scale=(camera.aspect_ratio,1), color=color.white, z=1, world_y=0)

state_handler = Animator({
    'main_menu': main_menu,
    'game_menu': game_menu,
    'load_menu': load_menu,
    'options_menu': options_menu,
})

# main menu content
main_menu.buttons = [
    MenuButton('Créer une partie', on_click=Func(setattr, state_handler, 'state', 'game_menu')),
    MenuButton('Rejoindre une partie', on_click=Func(setattr, state_handler, 'state', 'load_menu')),
    MenuButton('Parties en cours', on_click=Func(setattr, state_handler, 'state', 'load_menu')),
    MenuButton('Options', on_click=Func(setattr, state_handler, 'state', 'options_menu')),
    MenuButton('Quitter', on_click=application.quit),
]

for i, e in enumerate(main_menu.buttons):
    e.parent = main_menu
    e.y = (-i-2) * button_spacing

def start_game():
    menu_parent.enabled = False

# load menu content
for i in range(3):
    MenuButton(parent=load_menu, text=f'Partie {i+1}', y=-i * button_spacing, on_click=start_game)

load_menu.back_button = MenuButton(parent=load_menu, text='Retour', y=((-i-2) * button_spacing), on_click=Func(setattr, state_handler, 'state', 'main_menu'))

# options menu content
"""
volume_slider = Slider(0, 1, default=Audio.volume_multiplier, step=.1, text="Volume :", parent=options_menu, x=-.25)
def set_volume_multiplier():
    #Audio.volume_multiplier = volume_slider.value
    background_music.volume = volume_slider.value

volume_slider.on_value_changed = set_volume_multiplier

# TODO: Options d'affichage (plein écran, plein écran fenêtré, fenêtré)

options_back = MenuButton(parent=options_menu, text='Retour', x=-.25, origin_x=-.5, on_click=Func(setattr, state_handler, 'state', 'main_menu'))

for i, e in enumerate((volume_slider, options_back)):
    e.y = -i * button_spacing
"""

# Ajouter la liste des joueurs
player_list = ["Kordik"]
players = Text(text='Liste des joueurs :', scale=2, origin=(0, 1), y=0.25, parent=game_menu)
player1 = Text(text=player_list[0], scale=1.5, origin=(0, 1), y=-0.05, parent=game_menu)
player2 = Text(text='Joueur2', scale=1.5, origin=(0, 1), y=-0.15, parent=game_menu)

def start():
    #from GameGrid import GameGrid
    #from ship_container import ShipContainer
    import sys
    import os
    script_dir = os.path.dirname(__file__)
    module_dir = os.path.join(script_dir, '..')
    sys.path.append(module_dir)

    import main
    menu_parent.enabled = False    
    main.start()
    
# Ajouter le bouton pour démarrer la partie
start_game_button = MenuButton(text='Démarrer la partie', parent=game_menu, y=-0.45, enabled=False, on_click=start)

def update_player_list():
    for player in (player1, player2):
        player.disable()

    # Supprimer les textes de joueurs existants
    i = 0
    for child in game_menu.children:
        if isinstance(child, Text) and child.text != 'Liste des joueurs :':
            print(child.text)
            if i < len(player_list) - 1:
                child.text = player_list[i]
                print("Devenu 1 : " + child.text)
            else:
                child.text = f'Joueur {i+1}'
                print("Devenu 2 : " + child.text)

            i += 1

    #for i, player_name in enumerate(player_list):
        #player_text = Text(parent=game_menu, text=player_name, scale=1.5, origin=(0, 1), y=-0.05 - i*.1)

    if len(player_list) < 2:
        start_game_button.enabled = False
    else:
        start_game_button.enabled = True

def add_player(player_name):
    if len(player_list) < 2:
        player_list.append(player_name)
        update_player_list()

add_ai_button = None

def add_ai_player():
    add_player("IA")

    add_ai_button.text = "Supprimer l'IA"
    add_ai_button.on_click = remove_ai_player

def remove_ai_player():
    player_list.remove("IA")
    update_player_list()

    add_ai_button.text = "Ajouter une IA"
    add_ai_button.on_click = add_ai_player

# Ajouter le bouton pour ajouter une IA
add_ai_button = MenuButton(text='Ajouter une IA', parent=game_menu, y=-0.35, on_click=add_ai_player)

# Ajouter le bouton pour revenir au menu principal
back_button = MenuButton(text='Retour', parent=game_menu, y=-0.55, on_click=Func(setattr, state_handler, 'state', 'main_menu'))


# animate the buttons in nicely when changing menu
for menu in (main_menu, load_menu, options_menu, game_menu):
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

app.run()