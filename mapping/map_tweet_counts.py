import pandas as pd
import numpy as np
import shapefile

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


# Return a dict with three elements
#        - state_name
#        - total_area
#        - list of list representing latitudes
#        - list of list representing longitudes
#
#  Input: State Name & ShapeFile Object

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
	
def main():
	# Read the ShapeFile
	dat = shapefile.Reader("./shapefile/USCounties.shp")

	# Create a list of county tuples of (County, State, Color)
	counties = [(i[0], i[1], "#FFFEFF") for i in dat.iterRecords()]

	# Create the Plot

	from bokeh.plotting import *
	output_file("us_counties.html")

	TOOLS="pan,wheel_zoom,box_zoom,reset,previewsave"
	figure(title="Vaccination Tweets by County", tools=TOOLS, plot_width=900, plot_height=800)
	
	hold()
	
	count = 0
	for county in counties:
		data = getDict(county, dat)
		patches(data[(county[0], county[1])]['lat_list'], data[(county[0], county[1])]['lng_list'], \
				fill_color = county[2], line_color = "black")

	show()

main()