from django.core.files.uploadedfile import UploadedFile

def read_datarows(file: UploadedFile):
    datarows = []
    for line in file.readlines():
        datarows.append(line)
    return datarows

def row_indexes_to_list(indexes):
    indexes_list = []
    for index in indexes[1:len(indexes)-1].split(','):
        try:
            indexes_list.append(int(index.strip()))
        except Exception as exc:
            print('Row-to-idx exception: ', exc)
    return indexes_list

def is_name_valid(name):
    return len(name) != 0 and name != ''