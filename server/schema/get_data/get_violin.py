#!/bin/python

import sys
import os
import json
import csv
import itertools
import loompy
import numpy as np

import get_data.helper
import get_data.minio_functions

colour_counter = 0

loom_file = {
    "bucket": "frontend_normalized",
    "object": "normalized_counts.loom"
}

def add_barcode(plotly_obj, label, barcode, expression_values):
    """ add the barcode+expression to an exisiting group or make a new one in the plotly object """
    if (label in plotly_obj):
        plotly_obj[label]['x'].append(label)
        plotly_obj[label]['y'].append(expression_values[barcode])
    else:
        # label not seen yet, create new group
        plotly_obj[label] = new_violin_group(label, expression_values[barcode])

def label_with_groups(plotly_obj, expression_values, group, labels_tsv):
    # label each barcode with its chosen group
    label_idx = labels_tsv[0].index(str(group))
    group_type = labels_tsv[1][label_idx]
    all_barcodes = {key: True for key in expression_values.keys()}
    if group_type == 'group':
        for row in labels_tsv[2:]:
            barcode = str(row[0])
            if all_barcodes.pop(barcode, None):
                # only add barcodes that exist in expressions dictionary
                label = str(row[label_idx])
                add_barcode(plotly_obj, label, barcode, expression_values)
        # now add the remaining barcodes without a label
        for barcode in all_barcodes.keys():
            label = 'unlabeled'
            add_barcode(plotly_obj, label, barcode, expression_values)
    elif group_type == 'numeric':
        # can't do this for violins
        helper.return_error(group + " is numeric data, not viewable in violin plots")
    else:
        helper.return_error(group + " does not have a valid data type (must be 'group')")

    return plotly_obj

def get_expression(feature, runID):
    """ parses the normalized count matrix to get an expression value for each barcode """
    path = '../minio/{bucket}/{object}'.format(bucket=loom_file['bucket'], object=loom_file['object'])

    with loompy.connect(path) as ds:
        barcodes = ds.ca.CellID
        features = ds.ra.Gene
        feature_idx = next((i for i in range(len(features)) if features[i] == feature), -1)
        if feature_idx >= 0:
            feature_exp = [float(i) for i in ds[feature_idx, :]]
            return dict(zip(barcodes, feature_exp))
        else:
            helper.return_error("Feature Not Found")

def new_violin_group(label, y_coord):
    """ creates a new violin group for the plot """
    global colour_counter
    violin_group = {
        "name": label,
        "type": "violin",
        "spanmode": "hard",
        "fillcolor": "",
        "line": {"color": helper.COLOURS[colour_counter%len(helper.COLOURS)] },
        "points": "jitter",
        "jitter": 0.85,
        "width": 0.75,
        "meanline": {"visible": True},
        "x": [label],
        "y": [y_coord]
    }
    colour_counter += 1
    return violin_group

def categorize_barcodes(group, expression_values, runID, paths, minio_client):
    """ for every group, make a new plotly object and put the barcodes into it """
    metadata = paths["metadata"]
    groups = paths["groups"]

    metadata_exists = minio_functions.object_exists(metadata["bucket"], metadata["object"], minio_client)

    plotly_obj = {}
    if (group in minio_functions.get_first_line(groups["bucket"], groups["object"], minio_client)):
        # groups tsv definition supercedes metadata
        label_with_groups(plotly_obj, expression_values, group, 
            minio_functions.get_obj_as_2dlist(groups["bucket"], groups["object"], minio_client))
    elif (metadata_exists and 
         (group in minio_functions.get_first_line(metadata["bucket"], metadata["object"], minio_client))):
        # it's defined in the metadata
        label_with_groups(plotly_obj, expression_values, group, 
            minio_functions.get_obj_as_2dlist(metadata["bucket"], metadata["object"], minio_client))
    else:
        helper.return_error(group + " is not an available group in groups.tsv or metadata.tsv")

    return plotly_obj.values()


def calculate_bandwidths(plotly_obj):
    """ all expression values now recorded, calculate bandwidths and display violins with null bandwidths as boxplots """
    for violin_group in plotly_obj:
        y_values = violin_group['y']
        #print(y_values.count(0.0)/float(len(y_values))*100)
        if sum(y_values) == 0.0:
            violin_group['type'] = 'box'
        else:
            # replace 0s with 0.1 for kernel density estimate (doesn't perform well on sparse data) 
            mod_values = [0.1 if val == 0.0 else val for val in y_values]
            # calculate Silverman's Rule of Thumb    for bandwidth
            iqr = np.subtract(*np.percentile(mod_values, [75,25]))
            std = np.std(mod_values)
            violin_group['bandwidth'] = 0.9 * min(std, iqr/1.34) * (len(mod_values)**(-1/5.0))

def get_violin_data(group, feature, runID, minio_client):
    """ given a grouping for the cells and a feature of interest, returns the plotly violin object """
    paths = {}
    with open('paths.json') as paths_file:
        paths = json.load(paths_file)
    helper.set_runID(paths, runID)

    expression_values = get_expression(feature, runID)
    plotly_obj = categorize_barcodes(group, expression_values, runID, paths, minio_client)
    calculate_bandwidths(plotly_obj)
    helper.sort_traces(plotly_obj)
    return plotly_obj
