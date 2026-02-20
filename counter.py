# def init_counter(init_value: int):
#     c = init_value
#     def counter() -> int:
#         nonlocal c
#         val = c
#         c += 1
#         return val
#     return counter

# #this way, you have permanet storage across calls
# count_a = init_counter(10)
# count_b = init_counter(5)
# print(count_a()) #11
# print(count_a()) #12
# print(count_b()) #6

# class Counter:
#     def __init__(self) -> None:
#         self.count = 0

#     def __call__(self) -> int:
#         val = self.count
#         self.count = 1
#         return val
# c = Counter()
# print(c())


    # def classify_colors(self, type, status: bool, track: RaceTrack) -> list| None:
    #     if type == 'walls':
    #         all_walls = []
    #         for i in range(8):
    #             walls = track.find_wall_locations(i, status)
    #             if walls:
    #                 for wall in walls:
    #                     all_walls.append(wall, i)
    #         return all_walls
    #     elif type == 'buttons':
    #         all_buttons = []
    #         for i in range(8):
    #             buttons = track.find_buttons(i, status)
    #             if buttons:
    #                 for button in buttons:
    #                     all_buttons.append(button, i)
    #         return all_buttons
    #     else:
    #         return None

    # def classify_room(self, player_loc: Point, track: RaceTrack):
    #     star = track.target
    #     possible_moves = track.find_traversable_cells()
    #     if star in possible_moves:
    #         return (1, track.target)
    #     else:
    #         all_blocking_walls = self.classify_colors('walls', True, track)
    #         for block_wall in all_blocking_walls:
    #             wall, color = block_wall
    #             options = [(-1, 0), (1, 0), (0, -1), (0, 1)]
    #             neighbors = {opt: (wall[0] + opt[0], wall[1] + opt[1]) for opt in options}
    #             safe_options = [(opt, coord) for opt, coord in neighbors.items() if coord in possible_moves]
    #             for adjacent in safe_options:
    #                 _, coord = adjacent
    #                 if coord in possible_moves:
    #                     target = track.find_buttons(color) if track.find_buttons(color) in possible_moves else None
    #                     return (2, target)
    #     return (0, None)
            
    #     #try to classify each room as a node
    #     #catergorize the room as goal room, button room, and dead end room
    #     #from goal room, find walls, which backtrack
    #     ...

        


        # room, target = self.classify_room(player_loc, track)
        # safe = track.find_traversable_cells()
        # # if room == 1:
        # #     target = track.target
        # # elif room == 0:
        # #     buttons = track.find_buttons()
        # #     for button in buttons:
        # #         if button in safe:
        # #             target = button
        # return target


# #do you need to say self.track or just track
#     def goap(self, player_loc: Point, track: RaceTrack):
#         colors_checklist = []
#         explored_rooms = []
#         button_colors = np.unique(self.track.button_colors)
#         player_room, __ = self.room_coords(player_loc, track)
#         # non_blank_buttons = [button_color for button_color in button_colors if button_color !=0] 
#         target_room, target_borders = self.room_coords(self.track.target, track)
#         if player_loc in target_room:
#             return self.track.target
#         else:
#             while True:
#                 explored_rooms.append(target_room)
#                 for border_piece in target_borders:
#                     border_coord, color = border_piece
#                     if color in button_colors:
#                         colors_checklist.append(color)
#                 for color in colors_checklist:
#                     applicable_buttons = track.find_buttons(color)
#                     for applicable_button in applicable_buttons:
#                         if applicable_button in player_room:
#                             return applicable_button
#                 safe = track.find_traversable_cells()
#                 options = [(-1, 0), (1, 0), (0, -1), (0, 1)]

#                 #dont add children of butons to frontier (though the button needs to be in the closed list)
#                 # basically make a board copy every time you're 
#                 # for astar, you need to make sure that it routes around any NON target button (because otherwise it kills you)
#                 neighbors = {opt: (border_coord[0] + opt[0], border_coord[1] + opt[1]) for opt in options}
#                 safe_options = [(opt, coord) for opt, coord in neighbors.items() if coord not in safe]
#                 # for safe_option 
#                 ...
                
#                 #basically, for whatever wall that has a button (but isn't necessarily accessable)
#                 # find a new empty room (area with empty space not in original room) from the wall that has a button (so it's mutable)
#                 #search that, find button, etc