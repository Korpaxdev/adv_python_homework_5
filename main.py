import os
from datetime import datetime


def logger_v1(old_function):
    def new_function(*args, **kwargs):
        with open('main.log', 'a') as f:
            date = str(datetime.now())
            func_name = old_function.__name__
            value = old_function(*args, **kwargs)
            f.write(f"{date=} | {func_name=} | {args=} | {kwargs=} | {value=}\n")
        return value

    return new_function


def test_1():
    path = 'main.log'
    if os.path.exists(path):
        os.remove(path)

    @logger_v1
    def hello_world():
        return 'Hello World'

    @logger_v1
    def summator(a, b=0):
        return a + b

    @logger_v1
    def div(a, b):
        return a / b

    assert 'Hello World' == hello_world(), "Функция возвращает 'Hello World'"
    result = summator(2, 2)
    assert isinstance(result, int), 'Должно вернуться целое число'
    assert result == 4, '2 + 2 = 4'
    result = div(6, 2)
    assert result == 3, '6 / 2 = 3'

    assert os.path.exists(path), 'файл main.log должен существовать'

    summator(4.3, b=2.2)
    summator(a=0, b=0)

    with open(path) as log_file:
        log_file_content = log_file.read()

    assert 'summator' in log_file_content, 'должно записаться имя функции'
    for item in (4.3, 2.2, 6.5):
        assert str(item) in log_file_content, f'{item} должен быть записан в файл'


def logger_v2(path='main.log'):
    def __logger(old_function):
        def new_function(*args, **kwargs):
            date = str(datetime.now())
            name = old_function.__name__
            value = old_function(*args, **kwargs)
            with open(path, 'a') as f:
                f.write(f"{date=} | {name=} | {args=} | {kwargs=} | {value=}\n")
            return value

        return new_function

    return __logger


def test_2():
    paths = ('log_1.log', 'log_2.log', 'log_3.log')

    for path in paths:
        if os.path.exists(path):
            os.remove(path)

        @logger_v2(path)
        def hello_world():
            return 'Hello World'

        @logger_v2(path)
        def summator(a, b=0):
            return a + b

        @logger_v2(path)
        def div(a, b):
            return a / b

        assert 'Hello World' == hello_world(), "Функция возвращает 'Hello World'"
        result = summator(2, 2)
        assert isinstance(result, int), 'Должно вернуться целое число'
        assert result == 4, '2 + 2 = 4'
        result = div(6, 2)
        assert result == 3, '6 / 2 = 3'
        summator(4.3, b=2.2)

    for path in paths:

        assert os.path.exists(path), f'файл {path} должен существовать'

        with open(path) as log_file:
            log_file_content = log_file.read()

        assert 'summator' in log_file_content, 'должно записаться имя функции'

        for item in (4.3, 2.2, 6.5):
            assert str(item) in log_file_content, f'{item} должен быть записан в файл'


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


@logger_v2(path='flat_list.log')
def get_flat_list(deep_list):
    return list(flat_list_gen(deep_list))


if __name__ == '__main__':
    test_1()
    test_2()
    list_of_lists_2 = [
        [['a'], ['b', 'c']],
        ['d', 'e', [['f'], 'h'], False],
        [1, 2, None, [[[[['!']]]]], []]
    ]
    get_flat_list(list_of_lists_2)
