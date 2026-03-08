

def next_bigger(num: int) -> int:
    num_str_list = list(str(num))
    for i in range(len(num_str_list) - 2, -1, -1):
        for j in range(len(num_str_list) - 1, i, -1):
            if num_str_list[j] > num_str_list[i]:

                num_str_list[j], num_str_list[i] = num_str_list[i], num_str_list[j]
                sorted_half = ''.join(sorted(num_str_list[i + 1:]))
                num_str = ''.join(num_str_list[:i + 1]) + sorted_half
                return int(num_str)

    return -1

if __name__ == '__main__':
    print(str(["1", "2"]))

"""
1234
1243
1342
1432
2134

example: 154321
minimum first swap to increase:
from the rightmost number i:
    from the rightmost number j:
        if i > j:
            replace i with j
            save index
            break
we get 254311

            # swaps to decrease as much as possible without going under:
            # from the rightmost number i up to the one we swapped:
            #     from the leftmost up to the number we swapped j:
            #         if i < j:
            #             replace i with j
            #             call itself?
all of that is just a sort


alternative: going left to right and keeping a running count
4323
current = 4
3 < 4
2 < 4
3 < 4
return -1

    
"""


def test_bigger():
    assert next_bigger(12) == 21
    assert next_bigger(21) == -1
    assert next_bigger(513) == 531
    assert next_bigger(2017) == 2071
    assert next_bigger(414) == 441
    assert next_bigger(144) == 414
    assert next_bigger(1432) == 2134
    assert next_bigger(564) == 645
    assert next_bigger(273564) == 273645
