def dir_reduc(arr: list[str]):
    directions: dict[str, str] = {"NORTH": "SOUTH", "SOUTH": "NORTH", "EAST": "WEST", "WEST": "EAST"}
    directions_indices_to_remove: list[int] = [-1]

    while len(directions_indices_to_remove):
        directions_indices_to_remove = []
        i = 0

        while i < len(arr) - 1:
            if arr[i] == directions[arr[i + 1]]:
                directions_indices_to_remove += [i, i+1]
                i += 1
            i += 1

        for items_removed, direction_index in enumerate(directions_indices_to_remove):
            arr.pop(direction_index - items_removed)

    return arr
# N  N N N N N N S S S S S S S 10 2 per cycle 5 cycles of everything and it scales with n so n * n = n^2

def test_dir_reduc():
    a = ["NORTH", "SOUTH", "SOUTH", "EAST", "WEST", "NORTH", "WEST"]
    assert dir_reduc(a) == ['WEST']
    a = ["NORTH", "WEST", "SOUTH", "EAST"]
    assert dir_reduc(a) == ["NORTH", "WEST", "SOUTH", "EAST"]
    a = ["NORTH", "SOUTH", "SOUTH", "EAST", "WEST", "NORTH", "WEST"]  # ['WEST']
    assert dir_reduc(a) == ['WEST']
    a = ["NORTH", "SOUTH", "EAST", "WEST", "NORTH", "NORTH", "SOUTH", "NORTH", "WEST", "EAST"]  # ['NORTH', 'NORTH']
    assert dir_reduc(a) == ['NORTH', 'NORTH']
    a = []  # []
    assert dir_reduc(a) == []
    a = ["NORTH", "SOUTH", "SOUTH", "EAST", "WEST", "NORTH"]  # []
    assert dir_reduc(a) == []
    a = ["NORTH", "SOUTH", "SOUTH", "EAST", "WEST", "NORTH", "NORTH"]  # ["NORTH"]
    assert dir_reduc(a) == ["NORTH"]
    a = ["EAST", "EAST", "WEST", "NORTH", "WEST", "EAST", "EAST", "SOUTH", "NORTH", "WEST"]  # ["EAST", "NORTH"]
    assert dir_reduc(a) == ["EAST", "NORTH"]
    a = ["NORTH", "EAST", "NORTH", "EAST", "WEST", "WEST", "EAST", "EAST", "WEST", "SOUTH"]  # ["NORTH", "EAST"])
    assert dir_reduc(a) == ["NORTH", "EAST"]
    a = ["NORTH", "WEST", "SOUTH", "EAST"]  # ["NORTH", "WEST", "SOUTH", "EAST"])
    assert dir_reduc(a) == ["NORTH", "WEST", "SOUTH", "EAST"]
    a = ['NORTH', 'NORTH', 'EAST', 'SOUTH', 'EAST', 'EAST', 'SOUTH', 'SOUTH', 'SOUTH', 'NORTH']
    assert dir_reduc(a) == ['NORTH', 'NORTH', 'EAST', 'SOUTH', 'EAST', 'EAST', 'SOUTH', 'SOUTH']