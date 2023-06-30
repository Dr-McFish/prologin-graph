import pandas
from collections import namedtuple
from recordclass import recordclass
from datetime import datetime 
from math import floor
import heapq
import copy

def text_to_date(txt):
	return datetime.strptime(txt, "%Y-%m-%d %H:%M:%S")

CSV_Data_point = namedtuple('CSV_Data_point', 'time n_subm')
Data_point2 = namedtuple('Data_point2', 'time n_subm problem')

initial_point = CSV_Data_point(text_to_date("2022-10-14 12:00:00"), 0)

files = [
	"1-choix-complexe.csv",
	"2-mise_en_boites.csv",
	"3-pas_malin-dromes.csv",
	"4-greve.csv",
	"5-stabilisateurs.csv",
	"6-refroidissement.csv",
	"7-extension_strategique.csv"
]

submissison_data = [pandas.read_csv(file) for file in files]

for i in range(0, 7):
    submissison_data[i] = [CSV_Data_point(text_to_date(t.Time), t.unique_submissions) for t in submissison_data[i].itertuples()]

min_event_heap = []
for i in range(0, 7):
	problem_no = i + 1
	for event in submissison_data[i]:
		heapq.heappush(min_event_heap, Data_point2(event.time, event.n_subm, problem_no))

Time_point = recordclass('Time_point', "date_time problem_submissions total_score")

# construct time_points_table
time_points_table = [Time_point(text_to_date("2022-10-14 12:00:00"), [0 for _ in range(0,7)], 0)]

while len(min_event_heap) > 0 :
	prev_point : Time_point = time_points_table[-1]
	next_data : Data_point2 = heapq.heappop(min_event_heap)
	next_point = Time_point(next_data.time, copy.copy(prev_point.problem_submissions), 0 )
	assert(next_point.problem_submissions[next_data.problem - 1] +1 == next_data.n_subm)
	next_point.problem_submissions[next_data.problem - 1] += 1
	time_points_table.append(next_point)

pb_reward = [64, 256, 256, 1024, 4096, 16384, 60074]
pb_est_weight = [1, 1, 1, 1, 1, 1, 1]


for time_point in time_points_table :
	for i in range(0, 7) :
		time_point.total_score += floor(time_point.problem_submissions[i] * pb_reward[i] * pb_est_weight[i])


series_time = [pnt.date_time for pnt in time_points_table]
series_points = [pnt.total_score for pnt in time_points_table]

data_frame = pandas.DataFrame({'time' : series_time, 'points': series_points})

outfile = open('score.csv', 'w', encoding="utf-8")
outfile.write(data_frame.to_csv(index=False))


outfile.close()
