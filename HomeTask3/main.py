# This is a sample Python script.

# Press Shift+F10 to execute it or replace it with your code.
# Press Double Shift to search everywhere for classes, files, tool windows, actions, and settings.


def print_result(index, name):
    # Use a breakpoint in the code line below to debug your script.
    print(f"[{index}] - {name}")  # Press Ctrl+F8 to toggle the breakpoint.


# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    i = 1
    input_str = "Python is the best programming language in the world"
    result_str = input_str[5:-7]
    print_result(i, result_str)

    i = 2
    input_str = "Guido van Rossum is the benevolent dictator for life"
    result_str = input_str[2::3]
    print_result(i, result_str)

    i = 4
    input_str = "You have a problem with authority, Mr. Anderson."
    elements_list = list(input_str)
    elements_set = set(elements_list)
    elements_count = list(map(elements_list.count, elements_set))
    result_dict = dict(zip(elements_set, elements_count))
    print_result(i, result_dict)

# See PyCharm help at https://www.jetbrains.com/help/pycharm/
