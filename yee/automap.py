#!/usr/bin/env python
import collections

from .utils import read_csv_field, read_csv


def list_sub(x, y):
    return [item for item in x if item not in y]


class AutoMap(object):
    def __init__(self, file_list, delimiter):
        self.delimiter = delimiter
        self.data = {}
        for i in file_list:
            self.data[i] = {
                'keys': read_csv_field(i, delimiter)
            }
        self.graph = collections.defaultdict(
            lambda: collections.defaultdict(lambda: []))

    def build_graph(self):
        for i in self.data:
            path = i
            keys = self.data[i]['keys']
            for j in keys:
                self.graph[j][path] = list_sub(keys, [j])

    def find_path(self, src, dest, exclude_file):
        keys = self.graph[src]
        valid_keys = list_sub(keys, exclude_file)
        if len(valid_keys) == 0:
            return None
        for i in valid_keys:
            if dest in self.graph[src][i]:
                return [(src, dest, i)]
            else:
                for j in self.graph[src][i]:
                    v = self.find_path(j, dest, exclude_file + [i])
                    if v is not None:
                        return [(src, j, i)] + v

    def get_map(self, src, dest):
        paths = self.find_path(src, dest, [])
        d = collections.defaultdict(lambda: [])
        raw_data = read_csv(paths[0][2], self.delimiter)
        for i in raw_data['data']:
            src_index = raw_data['keys'][paths[0][0]]
            dest_index = raw_data['keys'][paths[0][1]]
            d[i[src_index]].append(i[dest_index])

        for i in paths[1:]:
            raw_data = read_csv(i[2], ',')
            data_dict = collections.defaultdict(lambda: [])
            for j in raw_data['data']:
                key = j[raw_data['keys'][i[0]]]
                value = j[raw_data['keys'][i[1]]]
                data_dict[key].append(value)
            new_d = {}
            for k in d:
                new_list = []
                for j in d[k]:
                    new_list.extend(data_dict.get(j, []))
                new_d[k] = new_list
            d = new_d
        return d


def main():
    pass


if __name__ == '__main__':
    main()
