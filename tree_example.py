import random
from game_world.racetrack import RaceTrack, load_track
from collections import defaultdict
import heapq
import numpy as np
from copy import deepcopy

track = load_track("./tracks/test_room.pkl")
Point = tuple[int, int]

#toggle walls of some color
# def toggle(color: int, track: RaceTrack):
print(track.wall_colors)
print(track.active)

new_track = deepcopy(track)
new_track.toggle(2)
print(new_track.wall_colors)
print(new_track.active)
