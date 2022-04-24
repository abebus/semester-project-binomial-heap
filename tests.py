from binomialheap import *
import time
import random
import csv

path = 'dataset/data/'
measure_results = 'res'

names_of_sets = ['01', '02', '03', '04', '05', '06', '07', '08', '09', '10']
methods = ['make_heap', 'extract_min', 'min', 'insert', 'union', 'remove_heap']
number_of_elements_list = [100,  500, 1000, 5000, 75000, 100000, 250000, 500000]


def heap(lst=[]):
	return BinomialHeap(lst)


def time_m(func):
	def wrapper(*args, **kwargs):
		a = time.time()
		f = func(*args, **kwargs)
		b = time.time()
		return (b - a)*1000, *f
	
	return wrapper


def read(method, set_, number_of_elem):
	b = f'{method}/{set_}/{number_of_elem}.csv'
	a = list(csv.reader(open(path + b)))
	return a


@time_m
def make_heap(s, n, m='make_heap'):
	h = heap(read(m, s, n))
	for _ in h:
		pass
	return m, s, n


@time_m
def extract_min(s, n, m='extract_min'):
	h = heap(read(m, s, n))
	h.extract_min()
	return m, s, n


@time_m
def min(s, n, m='min'):
	h = heap(read(m, s, n))
	h.min()
	return m, s, n


@time_m
def insert(s, n, m='insert'):
	h = heap(read(m, s, n))
	h[random.randint(0, 10 ** 9)] = random.randint(0, 10 ** 9)
	return m, s, n


@time_m
def union(s, n, m='union'):
	h1 = heap(read(m, s, n))
	h2 = heap(read(m, '01', n))
	h1 += h2
	return m, s, n


@time_m
def remove_heap(s, n, m='remove_heap'):
	h = heap(read(m, s, n))
	while h:
		h.extract_min()
	return m, s, n


if __name__ == '__main__':
	with open('results.txt', 'w') as outfile:
		outfile.write('millisecs\tname\tset\tn in set\n')
		for s in names_of_sets:
			for n in number_of_elements_list:
				line = [make_heap(s, n),
				        extract_min(s, n),
				        min(s, n),
				        insert(s, n),
				        union(s, n),
				        remove_heap(s, n)]
				for row in line:
					for elem in row:
						outfile.write(str(elem) + '\t')
					outfile.write('\n')