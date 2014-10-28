'''
Created on Oct 27, 2014

@author: alejandro
'''

import random
import files
from wxPython._wx import NULL

def gradient_descent(xs, ys, alpha, tolerance, iterations):
	m = len(xs)
	if m == len(ys):
		for row in xs:
			row.insert(0,1)
		ranges = get_ranges(xs)
		r = len(xs[0])
		thetas = [None] * r
		list_cost_functions = []
		cost_function = NULL
		for n in range(0, r):
			thetas[n] = random.uniform(-1, 1)
		for n in range(0, iterations):
			new_cost_function = 0
			for j in range(0, r):
				theta = 0
				for i in range(0, m):
					sumh = 0
					for h in range(0, r):
						sumh += xs[i][h] * thetas[h]
					theta += ((sumh - ys[i][0]) * xs[i][j])
				theta = alpha * theta / m
				thetas[j] = thetas[j] - theta
			new_cost_function = get_cost_function(thetas, xs, ys)
			list_cost_functions.append(str(new_cost_function))
			if cost_function != NULL and abs(cost_function - new_cost_function) <= tolerance:
				break
			cost_function = new_cost_function;
		files.writeFile("costFunction", list_cost_functions)
		return thetas
	return NULL


def get_cost_function(thetas, xs, ys):
	m = len(xs)
	r = len(xs[0])
	cost_function = 0
	for i in range(0, m):
		summ = 0
		for j in range(0, r):
			summ = thetas[j] * xs[i][j]
		summ -= ys[i][0]
		summ = summ * summ
		cost_function += summ
	cost_function = cost_function / ( 2 * m )
	return cost_function


def get_ranges(rows):
	result = []
	r = len(rows[0])
	for x in range(0, r):
		xmax = rows[0][x]
		xmin = rows[0][x]
		for row in rows:
			if row[x] > max:
				xmax = row[x]
			elif row[x] < min:
				xmin = row[x]
		result.append([xmin, xmax])
	return result