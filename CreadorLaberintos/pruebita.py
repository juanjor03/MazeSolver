

import csv
import os

with open(os.path.join(os.path.dirname(__file__), 'maze_5x5.csv'), 'rt') as f:
    reader = csv.reader(f)
    for row in reader:
        if row:
            print(row)
