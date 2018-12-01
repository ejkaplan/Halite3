from copy import deepcopy
from hlt.positionals import Direction
from hlt.entity import Ship
from itertools import product
import uuid


class GameState(object):

    def __init__(self, actual_map, players, turn_number, player_turn=0):
        self.game_map = deepcopy(actual_map)
        self.players = deepcopy(players)
        self.turn_number = turn_number
        self.player_turn = player_turn

    def possible_orders(self):
        # Make a 2d lists where each element is a list of possible orders for each ship,
        # Then use itertools to combine those into every possible combination of orders
        dirs = [Direction.NORTH, Direction.South, Direction.East, Direction.West]
        curr_player = self.players[self.player_turn]
        orders = [[s.move(d) for d in dirs] + [s.stay_still()] for s in curr_player.get_ships()] + \
                 [[curr_player.shipyard.spawn(), None]]
        return product(*orders)

    def apply_orders(self, orders):
        new_state = deepcopy(self)
        curr_player = new_state.players[new_state.player_turn]
        for order in orders:
            if order is None:
                continue
            order = order.split(" ")
            if order[0] == "m":
                ship = curr_player.get_ship(int(order[1]))
                new_pos = new_state.game_map.position_in_direction(order[2])
                ship.position = new_pos
                # TODO: Deal with fuel when moving
            if order[1] == "g":
                #TODO: How much halite does a ship start with?
                #TODO: DOn't make the ship if you don't have the building materials.
                ship = Ship(curr_player, uuid.uuid4(), curr_player.shipyard.position, 0)