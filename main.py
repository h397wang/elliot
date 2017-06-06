import time
import csv
import datetime as DT

file_name = "calendar.csv"

DEBUG = 0

START = 0
END = 1

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

def merge_overlapping_blocks(td1, td2):
	ret = td2
	if td1[START] < td2[START]: # td1 starts before td2
		ret[START] = td1[START]
	if td1[END] > td2[END]: 
		ret[END] = td1[END]
	return ret
	
def main():

	now_datetime = DT.datetime.now()
	latest_datetime = now_datetime + DT.timedelta(days=max_num_days_ahead)
	latest_datetime = latest_datetime.replace(hour = latest_hour, minute = 0, second = 0)

	# Open the CSV file
	f = open(file_name, 'rb')
	reader = csv.reader(f)

	busy_datetime_blocks = []
	for row in reader:
		if len(row) == 0:
			print("There's an empty row in the csv file")
		
		this_busy_block_start_datetime = string_to_datetime(row[1]) # index 0 is userid
		this_busy_block_end_datetime = string_to_datetime(row[2])	
		if len(busy_datetime_blocks) == 0: # Initially empty list
			busy_datetime_blocks = [[this_busy_block_start_datetime, this_busy_block_end_datetime]]
		elif this_busy_block_end_datetime < busy_datetime_blocks[0][START]: # Insert at beginning of list
			busy_datetime_blocks = [[this_busy_block_start_datetime, this_busy_block_end_datetime]] + busy_datetime_blocks
		elif this_busy_block_start_datetime > busy_datetime_blocks[len(busy_datetime_blocks)-1][END]: # Insert at end of list
			busy_datetime_blocks = busy_datetime_blocks + [[this_busy_block_start_datetime, this_busy_block_end_datetime]]			
		else: 
		# busy_datetime_blocks is has length at least 2
			for i in range(0, len(busy_datetime_blocks)-1):
								
				# Insert busy block between two existing busy blocks, no overlaps
				if this_busy_block_start_datetime > busy_datetime_blocks[i][1] and this_busy_block_end_datetime < busy_datetime_blocks[i+1][0]:
					busy_datetime_blocks.insert(i+1, [this_busy_block_start_datetime, this_busy_block_end_datetime])
					break	
				
				# Merge blocks otherwise
				if this_busy_block_start_datetime < busy_datetime_blocks[i][0] or this_busy_block_end_datetime > busy_datetime_blocks[i][1]:
					
					merged_datetime_block = merge_overlapping_blocks([this_busy_block_start_datetime, this_busy_block_end_datetime], busy_datetime_blocks[i])
					if DEBUG == 1:
						print("merged_datetime_block\n")
						print(merged_datetime_block)
					busy_datetime_blocks[i] = merged_datetime_block
					latest_finish_datetime = busy_datetime_blocks[i][1]
					pop_counter = 0
					original_length = len(busy_datetime_blocks)
					while((pop_counter + i) < original_length-1):
						if busy_datetime_blocks[i+1][1] < latest_finish_datetime: # remove redundant blocks from the list
							popped = busy_datetime_blocks.pop(i+1)
							pop_counter = pop_counter + 1	
							if DEBUG == 1:
								print("Popped off block\n")
								print(popped)
						else:
							break 
					break

	if DEBUG == 1:
		print("busy_datetime_blocks\n")
		print(busy_datetime_blocks)
	
	# Check for the biggest valid time interval
	largest_free_block = [now_datetime, now_datetime]
	for i in range(1, len(busy_datetime_blocks)-1): 
		if busy_datetime_blocks[i][END] < now_datetime:
			continue
		if busy_datetime_blocks[i+1][START] > latest_datetime:	
			this_free_block = [busy_datetime_blocks[i][END], latest_datetime]
		
		datetime_curfewed = busy_datetime_blocks[i][END].replace(hour = latest_hour, minute = 0, second = 0)
		if busy_datetime_blocks[i+1][START] > datetime_curfewed:
			this_free_block = [busy_datetime_blocks[i][END], datetime_curfewed]
		else: 
			this_free_block = [busy_datetime_blocks[i][END], busy_datetime_blocks[i+1][START]]

		this_delta = this_free_block[END] - this_free_block[START]
		largest_delta = largest_free_block[END] - largest_free_block[START]		
		if this_delta > largest_delta:
			largest_free_block = [this_free_block[START], this_free_block[END]]
		
		if busy_datetime_blocks[i+1][START] > latest_datetime:
			break

	if (largest_free_block[START] == now_datetime and largest_free_block[END] == now_datetime):
		print("There are no time blocks where everyone is free,  within the valid time intervals")					
	else:
		print("largest_free_block:")  			
		print(largest_free_block)
		print("\n\n")
	f.close()

if __name__ == "__main__": main()

