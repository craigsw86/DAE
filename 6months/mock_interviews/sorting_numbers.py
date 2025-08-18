unsorted_list = [1, 3, 5, 4, 2]

sorted_list_ascending = []

def make_sorted_copy(unsorted_list):
    unsorted_list_copy = unsorted_list

    while len(unsorted_list_copy) > 0:
        sorted_list_ascending.append(min(unsorted_list_copy))
        unsorted_list_copy.remove(min(unsorted_list_copy))

    return sorted_list_ascending

print(unsorted_list)
print(make_sorted_copy(unsorted_list))

# sorted_list_descending = []

# def make_sorted_copy_2(unsorted_list):
#     unsorted_list_copy_2 = unsorted_list

#     while(len(unsorted_list_copy_2)) < 100:
#         sorted_list_descending.append(max(unsorted_list_copy_2))
#         unsorted_list_copy_2.remove(max(unsorted_list_copy_2))

#     return sorted_list_descending

# print(unsorted_list)
# print(make_sorted_copy_2(unsorted_list))

