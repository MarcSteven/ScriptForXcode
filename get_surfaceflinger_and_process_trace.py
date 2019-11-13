import os
import sys
import string
import ConfigParser

def write_line_to_surfaceflinger_file(line,file,time_index,start=0):
        items = line.split()
        time = items[time_index].strip(':')
        if start == 0:
            last_item = items[len(items)-1]
            value = last_item[len(last_item)-1]
            file.write(time + '\t' + value + '\n')
        else:
            file.write(time + '\n')
        return time

def read_configs_and_run():
    config = ConfigParser.ConfigParser()
    config.readfp(open('app_config.ini'))
    app_name = config.get('Test object','app_name')  
    main_activity = config.get('Test object','main_activity')
    process_PID = config.get('PID','process_pid')
    surfaceflinger_PID = config.get('PID','surfaceflinger_pid')
    time_index = int(config.get('Script keys','time_index'))
    input_file_name = config.get('File','input_file')
    surfaceflinger_file = file(app_name + '_surfaceflinger_trace.txt','w')
    app_process_file = file(app_name + '_process_trace.txt','w')
    process_line_key = '<...>-' + str(process_PID)
    surfaceflinger_line_key = 'C|'+ str(surfaceflinger_PID) + '|' + main_activity + '|'
    is_start = 1 
    for line in open(input_file_name):
    	# record start time line
        if is_start == 1 and '<...>-' in line:
            time = write_line_to_surfaceflinger_file(line,surfaceflinger_file,time_index,1)
            app_process_file.write(time + '\n')
            is_start = 0
        if process_line_key in line:
            app_process_file.write(line)
        elif surfaceflinger_line_key in line:
            write_line_to_surfaceflinger_file(line,surfaceflinger_file,time_index)

if __name__ == '__main__':
    read_configs_and_run()	
