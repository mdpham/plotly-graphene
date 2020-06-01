#!/bin/python

import sys
import os
import json
from operator import itemgetter

# plotly defaults
COLOURS = [
  '#1f77b4',  # muted blue
  '#ff7f0e',  # safety orange
  '#2ca02c',  # cooked asparagus green
  '#d62728',  # brick red
  '#9467bd',  # muted purple
  '#8c564b',  # chestnut brown
  '#e377c2',  # raspberry yogurt pink
  '#7f7f7f',  # middle gray
  '#bcbd22',  # curry yellow-green
  '#17becf'   # blue-teal
]

# Kelly's 22 colours of maximum contrast (1965), excluding black and white
# added plotly colours to kelly's 22 colours i.e. 17 unique colours
COLOURS = [
	# '#0067A5', # blue
	# '#F38400', # orange
	# '#008856', # green
	# '#BE0032', # red
	# '#875692', # purple
	# '#882D17', # reddish brown
	# '#E68FAC', # purplish pink
	# '#848482', # grey
	# '#F3C300', # yellow
	# '#A1CAF1', # light blue
	# '#C2B280', # tan
	# '#F99379', # yellowish pink
	# '#604E97', # violet
	# '#F6A600', # orange yellow
	# '#B3446C', # purplish red
	# '#DCD300', # greenish yellow
	# '#8DB600', # yellow green
	# '#654522', # yellowish brown
	# '#E25822', # reddish orange 
	# '#2B3D26' # olive green
  	'#1f77b4',  # muted blue
  	'#ff7f0e',  # safety orange
	'#2ca02c',  # cooked asparagus green
	'#d62728',  # brick red
	'#9467bd',  # muted purple
	'#17becf',  # blue-teal
	'#E68FAC',  # purplish pink
	'#F3C300',  # yellow
	'#8c564b',  # chestnut brown
	'#848482',  # grey
	'#DCD300',  # greenish yellow
	'#F99379',  # yellowish pink
	'#604E97',  # violet
	'#B3446C',  # purplish red
	'#C2B280',  # tan
	'#8DB600',  # yellow green
	'#654522',  # yellowish brown
	# '#E25822',  # reddish orange 
	'#2B3D26'  # olive green
]

def get_cellcount(runID):
	""" given a runID, return the number of cells in the data """
	path = "/usr/src/app/results/{runID}/SEURAT/frontend_groups/groups.tsv".format(runID=runID) 
	if not os.path.isfile(path):
		# try command-line path
		path = "../../results/{runID}/SEURAT/frontend_groups/groups.tsv".format(runID=runID)
		if not os.path.isfile(path):
			return_error("group label file not found ("+path+")")	
	
	with open(path) as group_definitions:
		for count, line in enumerate(group_definitions):
			pass
		return count # don't add one so header not counted

def return_error(msg):
	""" format the error message and perform a system flush before exiting """
	print(json.dumps({"error": msg}))
	sys.stdout.flush()
	sys.exit()

def is_int(cluster_name):
	try:
		test = int(cluster_name)
	except ValueError as e:
		return False
	return True

def sort_traces(trace_objects):
	""" sort the lists of violin, opacity, or scatter objects by cluster name """
	# if all cluster names can be cast to int, sort by their integer value
	if all(is_int(x['name']) for x in trace_objects):
		trace_objects.sort(key=lambda i: int(i['name']))
	# otherwise, sort alphabetically
	else:
		trace_objects.sort(key=lambda i: i['name'])
	return 
