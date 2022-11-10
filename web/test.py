def arg_max(state_action):
    arr = [(i, v) for i, v in enumerate(state_action)]
    arr.sort(key=lambda t: t[1])
    return arr[-1][0]

print(arg_max([3, 2, 5]))