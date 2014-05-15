import pandas as pd
import numpy as np
import shapefile
import sys
import math
import bokeh.plotting as bp

# Hack: append common/ to sys.path
sys.path.append("../common")
sys.path.append("../queries")

import anova

# Given a shapeObject return a list of list for latitude and longitudes values
#       - Handle scenarios where there are multiple parts to a shapeObj

def getParts ( shapeObj ):

    points = []

    num_parts = len( shapeObj.parts )
    end = len( shapeObj.points ) - 1
    segments = list( shapeObj.parts ) + [ end ]

    for i in range( num_parts ):
        points.append( shapeObj.points[ segments[i]:segments[i+1] ] )

    return points


# Return a dict with two elements
#        - list of list representing latitudes
#        - list of list representing longitudes
#
#  Input: County tuple & ShapeFile Object

def getDict ( county, shapefile ):

    countyDict = {(county[0], county[1]): {} }

    rec = []
    shp = []
    points = []


    # Select only the records representing the
    # "state_name" and discard all other
    for i in shapefile.shapeRecords( ):

        if i.record[0] == county[0] and i.record[1] == county[1]:
            rec.append(i.record)
            shp.append(i.shape)


    # For each selected shape object get
    # list of points while considering the cases where there may be
    # multiple parts  in a single record
    for j in shp:
        for i in getParts(j):
            points.append(i)

    # Prepare the dictionary
    # Seperate the points into two separate lists of lists (easier for bokeh to consume)
    #      - one representing latitudes
    #      - second representing longitudes

    lat = []
    lng = []
    for i in points:
        lat.append( [j[0] for j in i] )
        lng.append( [j[1] for j in i] )

    countyDict[(county[0], county[1])]['lat_list'] = lat
    countyDict[(county[0], county[1])]['lng_list'] = lng

    return countyDict
	
def get_color(score, min_score, palette):
	index = int(math.floor((score / min_score) * len(palette)))
	if score == min_score:
		index = 8
	return palette[index]
	
def county_means(county_results):
	means = {key: np.mean(val) for key, val in county_results.iteritems()}
	return means
	
def generate_webpage():
	# Read the ShapeFile
	dat = shapefile.Reader("./shapefile/USCounties.shp")
	
	d = anova.average_user_scores()
	d2 = anova.county_results(d)
	average_scores = county_means(d2)
	
	a2 = dict()
	for key in average_scores.keys():
		new_key = key[0].strip('City').strip('County').strip(' ')
		a2[(new_key, key[1])] = average_scores[key]
	
	min_score = min(a2.values())
	palette = ["#FFF7EC", "#FEE8C8", "#FDD49E", "#FDBB84", "#FC8D59", "#EF6548", "#D7301F", "#B30000", "#7F0000"]
	
	colors = dict()
	for county in a2:
		colors[county] = get_color(a2[county], min_score, palette)

	# Create a list of county tuples of (County, State)
	counties = [(i[0], i[1]) for i in dat.iterRecords()]

	# Create the Plot
	bp.output_file("us_counties.html")

	TOOLS="pan,wheel_zoom,box_zoom,reset,previewsave"
	bp.figure(title="Vaccination Tweets by County", tools=TOOLS, plot_width=900, plot_height=800)
	
	bp.hold()
	
	count = 0
	for county in counties:
		data = getDict(county, dat)
		if county in colors:
			fill = colors[county]
		else:
			fill = "EEE9E9"
		bp.patches(data[(county[0], county[1])]['lat_list'], data[(county[0], county[1])]['lng_list'], \
				fill_color = fill, line_color = "black")

	show()
	
def main():
	generate_webpage()

main()

