import pandas
from collections import namedtuple
from datetime import datetime 
from math import floor
import heapq
import copy

def text_to_date(txt):
	return datetime.strptime(txt, "%Y-%m-%d %H:%M:%S")

files = [
	"csv_Hoche/score.csv",
	"csv_LLG/score.csv"
]

F_HOCHE = 0
F_LLG = 1

submissison_data = [pandas.read_csv(file) for file in files]
Data_point1 = namedtuple("Data_point1", "time points")
Data_point1bis = namedtuple("Data_point1", "time points lycee")

for i in range(0, 2):
    submissison_data[i] = [Data_point1(text_to_date(t.time), t.points) for t in submissison_data[i].itertuples()]

min_event_heap = []
for lycee in range(0, 2):
	for event in submissison_data[lycee]:
		heapq.heappush(min_event_heap, Data_point1bis(event.time, event.points, lycee))

Data_point2 = namedtuple('Data_point2', "time points_Hoche points_LLG")

# construct time_points_table
time_points_table = [Data_point2(text_to_date("2022-10-14 12:00:00"), 0, 0)]

while len(min_event_heap) > 0 :
	prev_point : Data_point2 = time_points_table[-1]
	next_data : Data_point1bis = heapq.heappop(min_event_heap)
	next_point = Data_point2(next_data.time, prev_point.points_Hoche, next_data.points) if next_data.lycee == F_LLG \
				 else Data_point2(next_data.time, next_data.points, prev_point.points_LLG)
	time_points_table.append(next_point)

series_time = [pnt.time for pnt in time_points_table]
series_Hoche = [pnt.points_Hoche for pnt in time_points_table]
series_LLG = [pnt.points_LLG for pnt in time_points_table]

data_frame = pandas.DataFrame({'time' : series_time, 'Hoche points': series_Hoche, 'LLG points' : series_LLG})

outfile = open('scores_llg_hoche.csv', 'w', encoding="utf-8")
outfile.write(data_frame.to_csv(index=False))


outfile.close()
