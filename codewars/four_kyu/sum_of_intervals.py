"""
Write a function called sumIntervals/sum_intervals that accepts an array of intervals, and returns the sum of all the interval lengths. Overlapping intervals should only be counted once.

Intervals
Intervals are represented by a pair of integers in the form of an array. The first value of the interval will always be less than the second value. Interval example: [1, 5] is an interval from 1 to 5. The length of this interval is 4.

Overlapping Intervals
List containing overlapping intervals:

[
   [1, 4],
   [7, 10],
   [3, 5]
]
The sum of the lengths of these intervals is 7. Since [1, 4] and [3, 5] overlap, we can treat the interval as [1, 5], which has a length of 4.
"""

"""
first approach:
Optimize intervals into non-overlapping intervals:
    per interval add it to a list of tuples
    if the left number (min) is within the range of an existing interval and the right number (max) is bigger than the 
    then the right number of the existing then change the interval to be the min to the max, same if other way around 
    (as in minimum is smaller) 
    this is O(n^2) because per interval we have to check every interval that came before it in a worst case scenario
    if the list is sorted we can make an optimization to stop the loop if the min number is greater than the min number
    so we don't iterate unnecessarily, but its still O(n^2) worst case, and O(n) memory but that's fine since we get an 
    array that is n length as input.

    then return the added sums

second approach:
    sort the intervals by min value first priority max value second priority, O(nlog(n)), two sorts
    so you would have
    (1,5), (1, 4), (1, 3), (2, 6), (3, 4), (10, 15) for example
    save 5
    keep the sum of 4
    iterate until 1 is no longer the min num, disregarding everything until then
    for next one, check if 2 < 5, if so then replace two with 5 and add to sum (2, 6), we treat like (5,6) so +1
    sum = 5
    for (3, 4) 3 < 6 so we have (6, 4) which does nothing
    for (10, 15) 10 !< 6 so we keep 10 and add 4 to the sum
    answer is 10

second approach without two sorts:
    one sort, by min value
    (1, 2), (1, 5), (1, 3), (2, 6), (3, 4), (10, 15)
1.  save 2
    sum = 2 - 1 = 1
2.  2 !< 1 ignore
    2 < 5
    (sum += 5 - 2) = 4
    save 5 
3.  5 !< 1  ignore
    5 !< 3 ignore
4.  5 !< 2 ignore
    5 < 6
    (sum += 6 - 5) = 5
    save 6
5.  6 !< 3 ignore
    6 !< 4 ignore
6.  6 < 10
    save 10
    (sum += 15 - 10) = 10
    save 15
"""

def sum_of_intervals(intervals: list[tuple[int, int]]) -> int:
    intervals_sum = 0
    intervals = sorted(intervals, key=lambda x: x[0])  # Sorted by min value
    current_max_number = intervals[0][0]  # Smallest number

    for interval in intervals:
        if current_max_number < interval[0]:
            intervals_sum += interval[1] - interval[0]
            current_max_number = interval[1]
        elif current_max_number < interval[1]:
            intervals_sum += interval[1] - current_max_number
            current_max_number = interval[1]

    return intervals_sum


def test_normal():
    assert sum_of_intervals([(1, 5)]) == 4
    assert sum_of_intervals([(1, 5), (6, 10)]) == 8
    assert sum_of_intervals([(1, 5), (1, 5)]) == 4
    assert sum_of_intervals([(1, 4), (7, 10), (3, 5)]) == 7

def test_large():
    assert sum_of_intervals([(-1_000_000_000, 1_000_000_000)]) == 2_000_000_000
    assert sum_of_intervals([(0, 20), (-100_000_000, 10), (30, 40)]) == 100_000_030