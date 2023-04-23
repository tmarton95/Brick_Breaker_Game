v = ["apple", "orange", "lemon"]

for count, value in enumerate(v):
    print(count, value)


state_1 = True

state_2 = not state_1

print(state_2)

for i in range(4):
    state_2 = not state_2
    print(state_2)