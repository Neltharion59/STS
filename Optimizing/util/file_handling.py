import os
root_path = os.path.dirname(os.path.dirname(os.path.realpath(__file__)))


def write(sub_path, content):
    path = os.path.join(root_path, sub_path)
    with open(path, 'w+', encoding='utf-8') as file:
        file.write(content)
        file.flush()
        os.fsync(file)


def append(sub_path, content):
    path = os.path.join(root_path, sub_path)
    with open(path, 'a+', encoding='utf-8') as file:
        file.write(content)
        file.flush()
        os.fsync(file)


def read(sub_path):
    path = os.path.join(root_path, sub_path)
    with open(path, 'r', encoding='utf-8') as file:
        result = file.read()
    return result


def exists(sub_path):
    path = os.path.join(root_path, sub_path)
    try:
        with open(path, 'r', encoding='utf-8') as file:
            for _ in file:
                break
    except FileNotFoundError:
        return False

    return True
