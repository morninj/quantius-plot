import json
from pprint import pprint
import collections
import plotly.plotly as py
import plotly.graph_objs as go
import subprocess
import argparse

# Get command line arguments
parser = argparse.ArgumentParser(description='Parse and plot Quantius data')
parser.add_argument('-f', '--filename', help='JSON data file from Quantius')
parser.add_argument('-o', '--output', help='directory to store plot images')
args = parser.parse_args()

# Define the filename containing the JSON data
input_data_file = 'sample-data.json'
if args.filename: input_data_file = args.filename

# Define the output image directory
output_image_dir = 'imagesfolder'
if args.output: output_image_dir = args.output

# Save data for any annotation tool
crosshair_points = [] # Count tool
lines = []            # Line tool  
multilines = []       # Multiline tool
polygons = []         # Polygon tool

def create_image_dir():
    '''Create image output directory.

    Clear it if it already exists.
    '''
    subprocess.call([
        'rm',
        '-rf',
        output_image_dir
    ])
    subprocess.call([
        'mkdir',
        output_image_dir
    ])

def process_annotations():
    '''Process each annotation.

    "annotation" = one user's analysis of a single image
    '''
    # Load the JSON data
    print 'Loading Quantius data from %s...\n' % input_data_file
    print '-' * 80
    with open(input_data_file) as f:
        results = json.load(f)
    # Loop through annotations
    i = 0
    for annotation in results:
        i = i + 1
        # Retrieve the data for each annotation
        print 'Annotation #%s:' % str(i)
        print '    Image filename: %s' % annotation['image_filename']
        print '    Annotation type: %s' % annotation['annotation_type']
        print '    Worker ID: %s' % annotation['worker_id']
        print '    Time when completed: %s' % annotation['time_when_completed']
        # Retrieve coordinates for each annotation tool
        if annotation['annotation_type'] == 'count':
            print 'TODO' # TODO plot as points, not as shape
        output_shapes = []
        if annotation['annotation_type'] == 'polygon' or \
            annotation['annotation_type'] == 'line' or \
            annotation['annotation_type'] == 'multiline' or \
            annotation['annotation_type'] == 'crosshairs': # TODO plot crosshairs as points, not shape
            # Load polygon data from the raw_shape field in the input JSON file
            current_shapes = annotation['raw_data']
            print '    Number of shapes: %s' % len(current_shapes)
            # Loop through shapes
            for this_shape in current_shapes:
                x_coords = []
                y_coords = []
                # Loop through points in the current shape
                for point in this_shape:
                    x_coords.append(point['x'])
                    y_coords.append(512 - point['y']) # TODO set based on original image dimension
                # Close polygons
                if annotation['annotation_type'] == 'polygon':
                    x_coords.append(x_coords[0])
                    y_coords.append(y_coords[0])
                # Save this shape
                output_shape = {
                    'x_coords': x_coords,
                    'y_coords': y_coords
                }
                output_shapes.append(output_shape)
        # Plot this annotation
        plot_points(output_shapes, str(i), annotation['image_filename']) # TODO replace i with incremenet for each filename

    print '-' * 80
    print '\n'
    print 'Done. Images stored in the %s/ folder.' % output_image_dir

# Plot data with Plotly
def plot_points(shapes, annotation, image_filename):
    '''Plot points with Plotly. '''
    data = []
    # Add each shape to the data list
    for shape in shapes:
        trace = go.Scatter(
            x = shape['x_coords'],
            y = shape['y_coords'],
            mode = 'lines',
        )
        data.append(trace)
    # Set layout
    layout = go.Layout(
        autosize=False,
        # TODO set based on original image dimension
        width=512,
        height=512,
        paper_bgcolor='rgba(0,0,0,0)', # Transparent background
        plot_bgcolor='rgba(0,0,0,0)',
        # No margins
        margin=go.Margin(
            l=0,
            r=0,
            b=0,
            t=0,
            pad=0
        ),
        # No axes
        xaxis=dict(
            range=[0, 512], # TODO set based on original image dimension
            autotick=False,
            showgrid=False,
            zeroline=False,
            ticks='',
            showticklabels=False
        ),
        yaxis=dict(
            range=[0, 512], # TODO set based on original image dimension
            autotick=False,
            showgrid=False,
            zeroline=False,
            ticks='',
            showticklabels=False
        ),
        showlegend=False,
    )
    # Plot all shapes for this annotation and save image
    fig = go.Figure(data=data, layout=layout)
    plot_url = py.image.save_as(
        fig,
        filename=output_image_dir + '/' + image_filename + '-plot-' + annotation + '.png'
    )

def main():
    create_image_dir()
    process_annotations()

if __name__ == '__main__':
    main()
