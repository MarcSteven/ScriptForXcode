#created by Marc Steven in 2017/10/8

import os
import sys
import string
import getopt
import ConfigParser

def count_frame_number(value_list,last_value):
    frame_number = 0
    if len(value_list) != 0:
        if last_value > 0:
            frame_number +=1
        frame_number += value_list.count(1)
        if value_list[len(value_list)-1] == 2:
            frame_number +=1
    return frame_number



def read_file_and_count(input_file_name,start_time,total_time):
    start_flag = 1
    real_start_time = 0
    end_time = 0
    last_value = 0
    value_list = []
    for line in open(input_file_name):
        items = line.split()
        time = float(items[0])
        if start_flag == 0:
            value = int(items[1])
            if time >= real_start_time and time <= end_time:
                value_list.append(value)
            elif time < real_start_time:
                last_value = value
        else:
            real_start_time = time + start_time
            end_time = real_start_time + total_time
            start_flag = 0
    frame_number = count_frame_number(value_list,last_value)
    return frame_number

def read_config_and_run():
    config = ConfigParser.ConfigParser()
    config.readfp(open('app_config.ini'))
    app_name = config.get('Test object','app_name') 
    config.readfp(open('fps_config.ini'))   
    start_time = float(config.get('Time','start_time'))
    total_time = float(config.get('Time','total_time'))
    input_file_name = app_name + '_surfaceflinger_trace.txt'
    frame_number = read_file_and_count(input_file_name,start_time,total_time)
    fps = frame_number * 1.0 / total_time
    result_file = file(app_name + '_fps_result.txt','a')
    result_file.write('start_time\t' + str(start_time) + '\n')
    result_file.write('total_time\t' + str(total_time) + '\n')
    result_file.write('frame_number\t' + str(frame_number) + '\n')
    result_file.write('FPS\t' + str(fps) + '\n')
    result_file.write('------------------------------------------\n')

if __name__ == '__main__':
    read_config_and_run()  
     
