

from libs.file_library import read_json


paths = read_json('swagger.json')

list_paths = []
for key, _ in paths[1].items():
    # Split the string by the '.' character
    substrings = key.split('/')
    # print(substrings)

    # Keep only the first two substrings and join them back with '.'
    list_paths.append('.'.join(substrings[1:3]) + '.')
paths = []
for i in set(list_paths):
    paths.append(f".{i}")
paths.sort()
# for j in paths:
#     print(j)
    
print(paths)