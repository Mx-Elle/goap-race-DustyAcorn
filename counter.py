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