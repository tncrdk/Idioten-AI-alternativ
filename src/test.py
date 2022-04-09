a = ([1, 2, 3], {"a": [10], "b": [20], "c": [30]})

d = a[1]

new_a = d["a"].append(20)

print(a)
print(new_a)
