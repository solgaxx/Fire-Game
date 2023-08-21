from designer import *
from random import randint

MY_PATH = 'C:\\Users\\solen\\OneDrive\\Documents\\UDelaware\\Coding\\Games\\my_fire_game\\'

World = {'plane': DesignerObject,
         'plane speed': int,
         'drops': [DesignerObject],
         'fires': [DesignerObject],
         'score': int,
         'counter': DesignerObject,
         'background': DesignerObject}
def create_world() -> World:
    return {'plane': create_plane(),
            'plane speed': PLANE_SPEED,
            'drops': [],
            'fires': [],
            'score': 0,
            'counter': text('black', 'Score: ', 30, get_width() / 2, 50, font_name = 'Arial'),
            'background': create_background()}

#EXTRA CHALLENGE: BACKGROUND

def create_background() -> DesignerObject:
    background = background_image(MY_PATH + 'fire_game_background.png')
    return background

#PLANE

def create_plane() -> DesignerObject:
    plane = image(MY_PATH + 'fire_plane.png', 200, 100)
    plane['scale'] = 0.4
    return plane

PLANE_SPEED = 3
def move_plane(world: World):
    world['plane']['x'] += world['plane speed']
        
def head_left(world: World):
    world['plane speed'] = -PLANE_SPEED
    world['plane']['flip_x'] = True
    
def head_right(world: World):
    world['plane speed'] = PLANE_SPEED
    world['plane']['flip_x'] = False
    
def bounce_plane(world: World):
    if world['plane']['x'] > get_width():
        head_left(world)
    elif world['plane']['x'] < 0:
        head_right(world)
        
def flip_plane(world: World, key: str):
    if key == 'left':
        head_left(world)
    elif key == 'right':
        head_right(world)
        
#WATER DROPS
        
def create_water_drop() -> DesignerObject:
    return circle('blue', 7)

def move_below(bottom: DesignerObject, top: DesignerObject):
    bottom['y'] = top['y'] + top['height']/2
    bottom['x'] = top['x']

def drop_water(world: World, key: str):
    if key == 'space':
        new_drop = create_water_drop()
        move_below(new_drop, world['plane'])
        world['drops'].append(new_drop)
        
WATER_DROP_SPEED = 5
def make_water_fall(world):
    for drop in world['drops']:
        drop['y'] += WATER_DROP_SPEED
        
def destroy_waters_on_landing(world):
    kept = []
    for drop in world['drops']:
        if (drop['y'] <= get_height()):
            kept.append(drop)
    world['drops'] = kept

#FIRES
    
def create_fire() -> DesignerObject:
    fire = image(MY_PATH + 'fire.png')
    fire['scale_x'] = .01
    fire['scale_y'] = .01
    fire['anchor'] = 'midbottom'
    fire['x'] = randint(0, get_width())
    fire['y'] = get_height()
    return fire

def grow_fire(world: World):
    for fire in world['fires']:
        fire['scale_x'] += .0025
        fire['scale_y'] += .0025
        
def make_fires(world: World):
    not_too_many_fires = len(world['fires']) < 11
    random_chance = randint(1, 10) == 1
    if not_too_many_fires and random_chance:
        world['fires'].append(create_fire())

def there_are_big_fires(world) -> bool:
    any_big_fires_so_far = False
    for fire in world['fires']:
        any_big_fires_so_far = (any_big_fires_so_far) or (fire['scale_x'] >= 1)
    return any_big_fires_so_far

#COLLISIONS

def update_counter(world):
    world['counter']['text'] = str(world['score'])
    
def collide_water_fire(world):
    destroyed_fires = []
    destroyed_drops = []
    # Compare every drop to every fire
    for drop in world['drops']:
        for fire in world['fires']:
            # Check if there are any collisions between each pair
            if colliding(drop, fire):
                # Remember to remove this drop and fire
                destroyed_drops.append(drop)
                destroyed_fires.append(fire)
                # And increase our score accordingly
                world['score'] += 1
    # Remove any fires/drops that were identified as colliding
    world['drops'] = filter_from(world['drops'], destroyed_drops)
    world['fires'] = filter_from(world['fires'], destroyed_fires)

def filter_from(old_list: list, elements_to_not_keep: list) -> list:
    new_values = []
    for item in old_list:
        if item not in elements_to_not_keep:
            new_values.append(item)
    return new_values

def print_score(world):
    print('Your score was', world['score'])

def flash_game_over(world):
    world['counter']['text'] = 'GAME OVER!'

when('starting', create_world)
when('updating', move_plane)
when('updating', bounce_plane)
when('typing', flip_plane)
when('typing', drop_water)
when('updating', make_water_fall)
when('updating', destroy_waters_on_landing)
when('updating', grow_fire)
when('updating', make_fires)
when(there_are_big_fires, pause)
when('updating', update_counter)
when('updating', collide_water_fire)
when(there_are_big_fires, print_score, flash_game_over, pause)
start()