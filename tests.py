from binomialheap import *
import os
import timeit
import csv

path = '/dataset/data'


def heap(lst=[]):
	return BinomialHeap(lst)


def read(method):
	names_of_sets = ['01', '02', '03', '04', '05', '06', '07', '08', '09', '10']
	methods = ['make_heap', 'extract_min', 'min', 'insert', 'union', 'remove_heap']
	number_of_elements_list = [100, 500, 1000]
	csv.reader(path + method + '.csv')
	
	pass

@timeit
def make_heap():
	
	pass


if __name__ == '__main__':
	pass
