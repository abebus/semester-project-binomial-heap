import csv
import os
import random

names_of_sets = ['01', '02', '03', '04', '05', '06', '07', '08', '09', '10']
methods = ['make_heap', 'extract_min', 'min', 'insert', 'union', 'remove_heap']
number_of_elements_list = [100,  500, 1000, 5000, 75000, 100000, 250000, 500000]
border = 10 ** 9

path_to_dataset = os.path.join(os.getcwd(), "data")
for method in methods:
    path_to_method = os.path.join(path_to_dataset, method)
    os.mkdir(path_to_method)

    for set_ in names_of_sets:
        path_to_set = os.path.join(path_to_method, set_)
        os.mkdir(path_to_set)

        for number_of_elements in number_of_elements_list:
            path_to_file = os.path.join(path_to_set, str(number_of_elements) + '.csv')
            data = []
            data.clear()

            for _ in range(number_of_elements):
                data.append((random.randint(0, border), random.randint(0, border)))
                
            file = open(path_to_file, "w", newline='')

            with file:
                writer = csv.writer(file)
                writer.writerows(data)
                