# Welcome to
# __________         __    __  .__                               __
# \______   \_____ _/  |__/  |_|  |   ____   ______ ____ _____  |  | __ ____
#  |    |  _/\__  \\   __\   __\  | _/ __ \ /  ___//    \\__  \ |  |/ // __ \
#  |    |   \ / __ \|  |  |  | |  |_\  ___/ \___ \|   |  \/ __ \|    <\  ___/
#  |________/(______/__|  |__| |____/\_____>______>___|__(______/__|__\\_____>
#
# This file can be a nice home for your Battlesnake logic and helper functions.
#
# To get you started we've included code to prevent your Battlesnake from moving backwards.
# For more info see docs.battlesnake.com

import random
import typing


# info is called when you create your Battlesnake on play.battlesnake.com
# and controls your Battlesnake's appearance
# TIP: If you open your Battlesnake URL in a browser you should see this data
def info() -> typing.Dict:
    print("INFO")

    return {
        "apiversion": "1",
        "author": "Eli Caine",  # TODO: Your Battlesnake Username
        "color": "#6495ED",  # TODO: Choose color
        "head": "all-seeing",  # TODO: Choose head
        "tail": "mlh-gene",  # TODO: Choose tail
    }


# start is called when your Battlesnake begins a game
def start(game_state: typing.Dict):
    print("GAME START")


# end is called when your Battlesnake finishes a game
def end(game_state: typing.Dict):
    print("GAME OVER\n")


# move is called on every turn and returns your next move
# Valid moves are "up", "down", "left", or "right"
# See https://docs.battlesnake.com/api/example-move for available data
'''
def food_finder(food: game_state['board']['food']) -> dict:
  for f in food:
      if f['x'] < close_food_x:
        close_food_x = f['x']
      elif f['y'] < close_food_y:
        close_food_y = f['y']
  return 
'''
    

def move(game_state: typing.Dict) -> typing.Dict:

    is_move_safe = {"up": True, "down": True, "left": True, "right": True}

    # We've included code to prevent your Battlesnake from moving backwards
    my_head = game_state["you"]["body"][0]  # Coordinates of your head
    my_neck = game_state["you"]["body"][1]  # Coordinates of your "neck"

    if my_neck["x"] < my_head["x"]:  # Neck is left of head, don't move left
        is_move_safe["left"] = False

    elif my_neck["x"] > my_head["x"]:  # Neck is right of head, don't move right
        is_move_safe["right"] = False

    elif my_neck["y"] < my_head["y"]:  # Neck is below head, don't move down
        is_move_safe["down"] = False

    elif my_neck["y"] > my_head["y"]:  # Neck is above head, don't move up
        is_move_safe["up"] = False
      
    #board_width = game_state['board']['width']
    #board_height = game_state['board']['height']
      
    # TODO: Step 1 - Prevent your Battlesnake from moving out of bounds
    if my_head["x"] == 10:
      if my_head["y"] == 10:                
        is_move_safe['up'] = False
      if my_head["y"] == 0:
        is_move_safe['down'] = False
      is_move_safe['right'] = False

    if my_head["x"] == 0:
      if my_head["y"] == 10:
        is_move_safe['up'] = False
      elif my_head["y"] == 0:
        is_move_safe['down'] = False
      is_move_safe['left'] = False

    if (my_head["y"] == 10) and (my_head["x"] > 0 and my_head["x"] < 10):
      is_move_safe['up'] = False
    if (my_head["y"] == 0 and (my_head["x"] > 0 and my_head["x"] < 10)):
      is_move_safe['down'] = False
      
    # TODO: Step 2 - Prevent your Battlesnake from colliding with itself
    my_body = game_state['you']['body']


    for body_part in my_body:
      if (my_head['x'] == body_part['x'] + 1) and (my_head['y'] == body_part['y']): # if body is to the left of head
        is_move_safe['left'] = False
      elif (my_head['x'] == body_part['x'] - 1) and (my_head['y'] == body_part['y']): # if body is to the right of head
        is_move_safe['right'] = False
      elif (my_head['y'] == body_part['y'] - 1) and (my_head['x'] == body_part['x']): # if body is above head
        is_move_safe['up'] = False
      elif (my_head['y'] == body_part['y'] + 1) and (my_head['x'] == body_part['x']): # if body is below head
        is_move_safe['down'] = False
        
    # TODO: Step 3 - Prevent your Battlesnake from colliding with other Battlesnakes
    opponents = game_state['board']['snakes']

    for op in opponents:
      for op_body in op['body']:
        # logic for staying away from opponents body and head on collisions 
        if op_body['x'] == my_head['x'] + 1 and op_body['y'] == my_head['y']:
          if game_state['you']['length'] > op['length']:
            is_move_safe['right'] = True
          else:
            is_move_safe['right'] = False
        elif op_body['x'] == my_head['x'] - 1 and op_body['y'] == my_head['y']:
          if game_state['you']['length'] > op['length']:
            is_move_safe['left'] = True
          else:
            is_move_safe['left'] = False
        elif op_body['y'] == my_head['y'] + 1 and op_body['x'] == my_head['x']:
          if game_state['you']['length'] > op['length']:
            is_move_safe['up'] = True
          else:
            is_move_safe['up'] = False
        elif op_body['y'] == my_head['y'] - 1 and op_body['x'] == my_head['x']:
          if game_state['you']['length'] > op['length']:
            is_move_safe['down'] = True
          else:
            is_move_safe['down'] = False
      #head on collions if opp head is one block distance between 
      # ex: ourhead = (2,4) ophead= (3,3), if we are bigger -> , move right and kill
      op_head = op['head']
      if op_head['x'] == my_head['x'] + 1 and op_head['y'] == my_head['y'] - 1 and  game_state['you']['length'] > op['length']:
        is_move_safe['right'] = True
      else:
        is_move_safe['right'] = False
        
        
    
      
    # Are there any safe moves left?
    safe_moves = []
    for move, isSafe in is_move_safe.items():
        if isSafe:
            safe_moves.append(move)
        print(safe_moves)

    if len(safe_moves) == 0:
        print(f"MOVE {game_state['turn']}: No safe moves detected! Moving down")
        return {"move": "down"}

    # Choose a random move from the safe ones
    

    # TODO: Step 4 - Move towards food instead of random, to regain health and survive longer
  
    food = game_state['board']['food']
    
    close_food_x = food[0]['x']
    close_food_y = food[0]['y']
    '''
    for f in food:
      if f['x'] < :
        close_food_x = f['x']
      elif f['y'] < close_food_y:
        close_food_y = f['y']
    '''
    print("food coordinates x: " + str(close_food_x) + "  y: " + 
       str(close_food_y))
    print("health: " + str(game_state['you']['health']))

  
    next_move = random.choice(safe_moves)
    
    if game_state['you']['health'] < 80:
      if my_head['x'] >= close_food_x:
        if my_head['x'] > close_food_x:
          if ('left' in safe_moves):
            next_move = 'left'
        elif (my_head['x'] == close_food_x):
          if my_head['y'] < close_food_y and 'up' in safe_moves:
            next_move = 'up'
          elif my_head['y'] > close_food_y and 'down' in safe_moves:
            next_move = 'down'
    
      if my_head['x'] <= close_food_x:
        if my_head['x'] < close_food_x:
          if ('right' in safe_moves):
            next_move = 'right'
        elif (my_head['x'] == close_food_x):
          if my_head['y'] < close_food_y and 'up' in safe_moves:
            next_move = 'up'
          elif my_head['y'] > close_food_y and 'down' in safe_moves:
            next_move = 'down'
     
    
    print(f"MOVE {game_state['turn']}: {next_move}")
    return {"move": next_move}


# Start server when `python main.py` is run
if __name__ == "__main__":
    from server import run_server

    run_server({"info": info, "start": start, "move": move, "end": end})
