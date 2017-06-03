import time
import csv
import datetime as DT
file_name = "calendar.csv"

# Time restrictions
max_num_days_ahead = 7
earliest_hour = 8 # 8 AM
latest_hour = 22 # 10 PM

def string_to_datetime(timedate_string):
	[empty, date, time] = timedate_string.split(" ")
	[year, month, day] = date.split("-")
	[hour, min, sec] = time.split(":")
	ret = DT.datetime(int(year),int(month), int(day), int(hour), int(min), int(sec))
	return ret	

def merge_overlapping_blocks(t1, t2):
	ret = t2
	if t1[0] < t2[0]: # t1 starts before t2
		ret[0] = t1[0]
	if t1[1] > t2[1]: # t0 ends after t2
		ret[1] = t1[1]
	return ret
	
def main():

	today = DT.datetime.now()
	latest = today + DT.timedelta(days=7)
	latest = latest.replace(hour = latest_hour, minute = 0, second = 0)

	# Open the CSV file
	f = open(file_name, 'rb')
	reader = csv.reader(f)

	busy_datetimes = []
	for row in reader:
		if len(row) == 0:
			print("There's an empty row in the csv file")
		
		start_datetime = string_to_datetime(row[1]) # index 0 is userid
		end_datetime = string_to_datetime(row[2])	
		if len(busy_datetimes) == 0: # Initially empty list
			busy_datetimes = [[start_datetime, end_datetime]]
		elif end_datetime < busy_datetimes[0][0]: # Insert at beginning of list
			busy_datetimes = [[start_datetime, end_datetime]] + busy_datetimes
		elif start_datetime > busy_datetimes[len(busy_datetimes)-1][1]: # Insert at end of list
			busy_datetimes = busy_datetimes + [[start_datetime, end_datetime]]			
		else: 
		# busy_datetimes is has length at least 2
			for i in range(0, len(busy_datetimes)-1):
								
				# Insert busy block between two existing busy blocks, no overlaps
				if start_datetime > busy_datetimes[i][1] and end_datetime < busy_datetimes[i+1][0]:
					busy_datetimes.insert(i+1, [start_datetime, end_datetime])
					break	
				
				# Merge blocks otherwise
				if start_datetime < busy_datetimes[i][0] or end_datetime > busy_datetimes[i][1]:
					
					merged_block = merge_overlapping_blocks([start_datetime, end_datetime], busy_datetimes[i])
					print("merged_block")
					print(merged_block)
					busy_datetimes[i] = merged_block
					latest_finish_datetime = busy_datetimes[i][1]
					pop_counter = 0
					original_length = len(busy_datetimes)
					while((pop_counter + i) < original_length-1):
						if busy_datetimes[i+1][1] < latest_finish_datetime: # remove redundant blocks from the list
							busy_datetimes.pop(i+1)
							pop_counter = pop_counter + 1	
							print("Popped off")
						else:
							break 
					break
	print("busy_datetimes\n")
	print(busy_datetimes)
	
	# Check for the biggest valid time interval
	largest_free_block = [today, today]
	for i in range(1, len(busy_datetimes)-1): 
		if busy_datetimes[i][1] < today:
			continue
		if busy_datetimes[i+1][0] > latest:	
			this_free_block = [busy_datetimes[i][1], latest]
		
		datetime_curfewed = busy_datetimes[i][1].replace(hour = latest_hour, minute = 0, second = 0)
		if busy_datetimes[i+1][0] > datetime_curfewed:
			this_free_block = [busy_datetimes[i][1], datetime_curfewed]
		else: 
			this_free_block = [busy_timedates[i][1], busy_timedata[i+1][0]]

		this_delta = this_free_block[1] - this_free_block[0]
		largest_delta = largest_free_block[1] - largest_free_block[0]		
		if this_delta > largest_delta:
			largest_free_block = [this_free_block[0], this_free_block[1]]
		
		if busy_datetimes[i+1][0] > latest:
			break
	print("largest_free_block")  			
	print(largest_free_block)
	if (largest_free_block[0] == today and largest_free_block[1] == today):
		print("There are no time blocks where everyone is free,  within the valid time intervals")					
	f.close()

if __name__ == "__main__": main()

