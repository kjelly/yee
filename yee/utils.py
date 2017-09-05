import csv


def read_csv_field(path, delimiter):
    with open(path, 'rb') as csvfile:
        reader = csv.reader(csvfile, delimiter=delimiter, quotechar='|')
        return reader.next()


def read_csv(path, delimiter):
    ret = {
        'data': [],
        'keys': {
        }
    }
    with open(path, 'r') as ftr:
        reader = csv.reader(ftr, delimiter=delimiter, quotechar='|')
        fields = reader.next()
        for i in range(len(fields)):
            ret['keys'][fields[i]] = i
        for j in reader:
            ret['data'].append(j)
    return ret
