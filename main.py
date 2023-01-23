import os
from datetime import datetime


def logger(path='main.log'):
    def __logger(old_function):
        def new_function(*args, **kwargs):
            date = str(datetime.now())
            name = old_function.__name__
            value = old_function(*args, **kwargs)
            print(value)
            with open(path, 'w') as f:
                f.write(f"{date=} | {name=} | {args=} | {kwargs=} | {value=}\n")
            return value

        return new_function

    return __logger


def flat_list_gen(deep_list):
    cursors = [0]
    old = []
    current = deep_list
    while cursors:
        index = cursors[-1]
        if index >= len(current):
            current = old.pop() if old else []
            cursors.pop()
            continue
        item = current[index]
        if isinstance(item, list):
            cursors[-1] = index + 1
            cursors.append(0)
            old.append(current)
            current = item
            continue
        cursors[-1] = index + 1
        yield item


@logger(path='flat_list.log')
def get_flat_list(deep_list):
    return list(flat_list_gen(deep_list))


if __name__ == '__main__':
    list_of_lists_2 = [
        [['a'], ['b', 'c']],
        ['d', 'e', [['f'], 'h'], False],
        [1, 2, None, [[[[['!']]]]], []]
    ]
    get_flat_list(list_of_lists_2)
