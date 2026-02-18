import random
from game_world.racetrack import RaceTrack
from collections import defaultdict
import heapq
import numpy as np

Point = tuple[int, int]

# class Bot:
#     def __init__(self, track: RaceTrack):
#         self.track = track
#         self.target = None

def manhattan_dist(a: Point, b: Point) -> int:
    return abs(a[0] - b[0]) + abs(a[1] - b[1])

def astar(start_cell: Point, end_cell: Point, track: RaceTrack) -> list[Point] | None:
    closed = set() # explored
    if not start_cell or not end_cell:
        return None
    g_scores = defaultdict(lambda: float('inf'))
    g_scores[start_cell] = 0
    f_scores = defaultdict(lambda: float('inf'))
    f_scores[start_cell] = manhattan_dist(start_cell, end_cell)

    frontier = [(f_scores[start_cell], start_cell)]
    prev = {start_cell: None}

    while True:
        _, current_cell = heapq.heappop(frontier)
        if current_cell == end_cell:
            break
        safe = track.find_traversable_cells()
        options = [(-1, 0), (1, 0), (0, -1), (0, 1)]
        neighbors = {opt: (current_cell[0] + opt[0], current_cell[1] + opt[1]) for opt in options}
        safe_options = [(opt, coord) for opt, coord in neighbors.items() if coord in safe]
        for neighbor in safe_options:
            _, move_coord = neighbor
            if move_coord in closed:
                continue
            temp_g = g_scores[current_cell] + 1
            if temp_g < g_scores[move_coord]:
                g_scores[move_coord] = temp_g
                f_scores[move_coord] = temp_g + manhattan_dist(move_coord, end_cell)
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

def goap(player_loc: Point, track: RaceTrack):
    room, target = classify_room(player_loc, track)
    safe = track.find_traversable_cells()
    # if room == 1:
    #     target = track.target
    # elif room == 0:
    #     buttons = track.find_buttons()
    #     for button in buttons:
    #         if button in safe:
    #             target = button
    return target

def classify_colors(type, status, track: RaceTrack) -> list| None:
    if type == 'walls':
        all_walls = []
        for i in range(8):
            walls = track.find_wall_locations(i, status)
            if walls:
                for wall in walls:
                    all_walls.append(wall, i)
        return all_walls
    elif type == 'buttons':
        all_buttons = []
        for i in range(8):
            buttons = track.find_buttons(i, status)
            if buttons:
                for button in buttons:
                    all_buttons.append(button, i)
        return all_buttons
    else:
        return None

def classify_room(player_loc: Point, track: RaceTrack):
    star = track.target
    possible_moves = track.find_traversable_cells()
    if star in possible_moves:
        return (1, track.target)
    else:
        all_blocking_walls = classify_colors('walls', True, track)
        for block_wall in all_blocking_walls:
            wall, color = block_wall
            options = [(-1, 0), (1, 0), (0, -1), (0, 1)]
            neighbors = {opt: (wall[0] + opt[0], wall[1] + opt[1]) for opt in options}
            safe_options = [(opt, coord) for opt, coord in neighbors.items() if coord in possible_moves]
            for adjacent in safe_options:
                _, coord = adjacent
                if coord in possible_moves:
                    target = track.find_buttons(color) if track.find_buttons(color) in possible_moves else None
                    return (2, target)
    return (0, None)
        
    #try to classify each room as a node
    #catergorize the room as goal room, button room, and dead end room
    #from goal room, find walls, which backtrack
    ...

def bad_move(loc: Point, track: RaceTrack) -> Point:
    target = goap(loc, track)
    strip = astar(loc, target, track)[1:]

    safe = track.find_traversable_cells()
    options = [(-1, 0), (1, 0), (0, -1), (0, 1)]
    neighbors = {opt: (loc[0] + opt[0], loc[1] + opt[1]) for opt in options}
    safe_options = [(opt, coord) for opt, coord in neighbors.items() if coord in safe]

    if not safe_options:
        print("shit")
        return None

    curr_move = heapq.heappop(strip)
    for option in safe_options:
        opt, coord = option
        if curr_move == coord:
            return opt
    print("shit")
    return None


