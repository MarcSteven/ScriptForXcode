#created by Marc Steven in 2017/10/8
import os
import sys
import string
import ConfigParser

def get_performtraversals_time_list(app_name,minimum_time,start_time,end_time,time_index):
    time_list = []
    child_func_number = 0
    current_time = 0
    longest_frame_length = 0
    longest_frame_start_time = 0
    start_time_offset = 0
    for line in open(app_name + '_process_trace.txt'):
        items = line.split()
        if len(items) == 1:
            start_time_offset = float(items[0])	
            start_time += float(items[0])
            end_time += float(items[0])
            continue
        time = float(items[time_index].strip(':'))
        last_item = items[-1]
        if ': B' in line:
            if 'performTraversals' in last_item:
                current_time = time
            else:
                child_func_number += 1
        elif ': E' in line:
            if child_func_number == 0:
                delta_time = time - current_time
                time_tuple = (current_time,delta_time)
				
                if delta_time >= minimum_time and current_time >= start_time and current_time <= end_time:
                    time_list.append(time_tuple)
                    if longest_frame_length < delta_time:
                        longest_frame_length = delta_time
                        longest_frame_start_time = current_time	
            else:
                child_func_number -= 1
        #else:
        #    print last_item
    longest_frame_start_time -= start_time_offset	
    return time_list,longest_frame_start_time,longest_frame_length


def write_performtraversals_time_file(time_list,app_name,minimum_time,start_time,end_time,longest_frame_start_time,longest_frame_length):
    time_file = file(app_name + '_performtraversals_' + str(int(minimum_time*1000)) +'.txt','w')
    for items in time_list:
        time_file.write(str(items[0]) + '\t' + str(items[1]) + '\n')
    total_number = len(time_list)
    frequency = total_number * 1.0 / (end_time - start_time)
    time_file.write('Start time:\t' + str(start_time) + '\n')
    time_file.write('End time:\t' + str(end_time) + '\n')
    time_file.write('Total:\t' + str(len(time_list)) + '\n')
    time_file.write('Frequency:\t' + str(frequency) + '\n')
    time_file.write('Longest frame start time:\t' + str(longest_frame_start_time) + '\n')
    time_file.write('Longest frame length:\t' + str(longest_frame_length) + '\n')	

def read_configs_and_run():
    config = ConfigParser.ConfigParser()
    config.readfp(open('app_config.ini'))
    app_name = config.get('Test object','app_name') 
    time_index = int(config.get('Script keys','time_index'))
    config.readfp(open('performtraversals_config.ini'))
    minimum_time = float(config.get('Time','minimum_time'))
    start_time = float(config.get('Time','start_time'))
    end_time = float(config.get('Time','end_time'))
    #travert unit to 's'
    minimum_time /= 1000
    time_list,longest_frame_start_time,longest_frame_length = get_performtraversals_time_list(app_name,minimum_time,start_time,end_time,time_index)
    write_performtraversals_time_file(time_list,app_name,minimum_time,start_time,end_time,longest_frame_start_time,longest_frame_length)

if __name__ == '__main__':
    read_configs_and_run()
