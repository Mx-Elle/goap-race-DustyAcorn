import random
from game_world.racetrack import RaceTrack
from collections import defaultdict
import heapq
import numpy as np
from copy import deepcopy

Point = tuple[int, int]

class Bot:
    def __init__(self):
        self.target: Point| None = None
        self.path: list[Point] = []

    def manhattan_dist(self, a: Point, b: Point) -> int:
        return abs(a[0] - b[0]) + abs(a[1] - b[1])

    def board_copy(self, toggle_color, current_track) -> RaceTrack:
        new_track = deepcopy(current_track)
        revised_track = new_track.toggle(toggle_color)
        return revised_track


    def astar(self, start_cell: Point, end_cell: Point, track: RaceTrack) -> list[Point]:
        mines = track.find_buttons() #this is a set
        if end_cell in mines:
            mines.remove(end_cell)
        closed = set() # explored
        if not start_cell or not end_cell:
            return None
        g_scores = defaultdict(lambda: float('inf'))
        g_scores[start_cell] = 0
        f_scores = defaultdict(lambda: float('inf'))
        f_scores[start_cell] = self.manhattan_dist(start_cell, end_cell)

        frontier = [(f_scores[start_cell], start_cell)]
        prev: dict[Point, Point| None] = {start_cell: None}

        while True:
            _, current_cell = heapq.heappop(frontier)
            if current_cell == end_cell:
                break
            safe = track.find_traversable_cells()
            options = [(-1, 0), (1, 0), (0, -1), (0, 1)]
            neighbors = {opt: (current_cell[0] + opt[0], current_cell[1] + opt[1]) for opt in options}
            safe_options = [(opt, coord) for opt, coord in neighbors.items() if coord in safe and coord != mines]
            for neighbor in safe_options:
                _, move_coord = neighbor
                if move_coord in closed:
                    continue
                temp_g = g_scores[current_cell] + 1
                if temp_g < g_scores[move_coord]:
                    g_scores[move_coord] = temp_g
                    f_scores[move_coord] = temp_g + self.manhattan_dist(move_coord, end_cell)
                    prev[move_coord] = current_cell
                    heapq.heappush(frontier, (f_scores[move_coord], move_coord))        
            closed.add(current_cell)
            
        path = []
        # reconstruct the path from prev
        key = end_cell
        while key != None:
            path.append(key)
            key = prev[key]
        return path[::-1]

#do you need to say self.track or just track
    def goap_target(self, player_loc: Point, track: RaceTrack):
        explored_states = []
        child_states = []
        goal_state = None
        current_state, avalible_buttons, goal = self.flood_fill(player_loc, track)
        start_state = frozenset(current_state)
#(previous_state, button)
        prev: dict[frozenset[Point], tuple[frozenset, Point]] = {}
        if goal == True:
            return [track.target]
        else:
            while goal != True:
                for avalible_button in avalible_buttons:
                    color = track.button_colors[avalible_button]
                    new_track = self.board_copy(color, track)
                    new_state, new_avalible_buttons, new_goal = self.flood_fill(player_loc, new_track)
                    if new_state in explored_states:
                        continue
                    prev[frozenset(new_state)] = (frozenset(current_state), avalible_button)
                    if new_goal == True:
                        goal_state = new_state
                        break
                    child_states.append((new_state, new_avalible_buttons, new_goal))
                explored_states.append(current_state)
                current_state, avalible_button, goal = child_states.pop(0)
            
            if goal_state == None:
                return []
            path = []
            # reconstruct the path from prev
            key = frozenset(goal_state)
            while key != start_state:
                key, decision = prev[key]
                path.append(decision)
            return path[::-1]
            
    def flood_fill(self, start_location: Point, track: RaceTrack):
        closed_list = set()
        button_locations = track.find_buttons()
        buttons_in_state = []
        goal = False
        #this includes the coordinate and the color in the form (border_coord, color_of_border_coord)
        frontiers = [start_location]

        while frontiers:
            current_cell = heapq.heappop(frontiers)
            if current_cell == track.target:
                goal = True

            safe = track.find_traversable_cells()
            options = [(-1, 0), (1, 0), (0, -1), (0, 1)]
            neighbors = {opt: (current_cell[0] + opt[0], current_cell[1] + opt[1]) for opt in options}

            safe_options = []
            unsafe_options = []
            for opt, coord in neighbors.items():
                if coord in safe:
                    safe_options.append((opt, coord))
                if coord not in safe:
                    unsafe_options.append((opt, coord))

            for neighbor in safe_options:
                if current_cell in button_locations:
                    buttons_in_state.append(current_cell)
                    break
                _, move_coord = neighbor
                if move_coord in closed_list:
                    continue
                heapq.heappush(frontiers, (move_coord))     
            closed_list.add(current_cell)

        return (closed_list, buttons_in_state, goal)



    # def bad_move(self, loc: Point, track: RaceTrack) -> Point:
    def __call__(self, loc: Point, track: RaceTrack) -> Point:
        if loc == self.target and self.path:
            self.target = self.path.pop(0)
        if self.target == None:
            self.path = self.goap_target(loc, track)
            if self.path:
                self.target = self.path.pop(0)

        #still no target?
        if self.target == None:
            return (0, 0)
        strip = self.astar(loc, self.target, track)[1:]

        safe = track.find_traversable_cells()
        options = [(-1, 0), (1, 0), (0, -1), (0, 1)]
        neighbors = {opt: (loc[0] + opt[0], loc[1] + opt[1]) for opt in options}
        safe_options = [(opt, coord) for opt, coord in neighbors.items() if coord in safe]

        if not safe_options:
            print("shit")
            return (0, 0)

        curr_move = heapq.heappop(strip)
        for option in safe_options:
            opt, coord = option
            if curr_move == coord:
                return opt
        print("shit")
        move, _  = random.choice(safe_options)
        return move

bad_move = Bot()

