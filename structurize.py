# import libraries
import numpy as np
import pandas as pd
import os
from datetime import datetime

# scan log files
launch_directory = os.getcwd()
files = []
for file in os.listdir():
    if file.startswith("log_"):
        files.append(file)
#print(files)

# sort info by datetime
datetimes = []
for file in files:
    datetime_elem = datetime.strptime(file, "log_%d_%m_%Y__%H_%M_%S.txt")
    datetimes.append(datetime_elem)

zipped_dates_and_files = zip(datetimes, files)
zipped_dates_and_files_sorted = sorted(zipped_dates_and_files, key = lambda tup: tup[0])
files_sorted = [elem[1] for elem in zipped_dates_and_files_sorted]
#print(files_sorted)

# get messages to store
data_heap = []
for file in files_sorted:
    with open(file, "r") as raw_data:
        raw_data_string = raw_data.read()
        data_splitted = raw_data_string.split("========")
        data_clean_list = []
        for elem in data_splitted:
            candidate_message = elem.strip("\n").replace("\n", " ")
            if candidate_message.startswith("#"):
                data_clean_list.append(candidate_message)
        if data_clean_list:
            data_heap.append(data_clean_list)

print("\n")
print(data_heap)

# tags execution
objects = []
stages = []
tasks = []

for elem in data_heap:
    for el in elem:
        #objects
        objects.append(el.split(" ")[0])
        #stages
        if el.split(" ")[1].startswith("#"):
            stages.append(el.split(" ")[1])
        else:
            stages.append("")
        #tasks
        if el.split(" ")[2].startswith("#"):
            tasks.append(el.split(" ")[2])
        else:
            tasks.append("")
        
# print(objects)
# print(stages)
# print(tasks)       

# tag grouping (same tags to same list)
# find unique tags
tags_complete = []
for i in range(len(objects)):
    tag = objects[i] + stages[i] + tasks[i]
    tags_complete.append(tag)

tags_unique = list(set(tags_complete))
print(tags_unique)

# flatten data heap
flat_data_heap = []
for elem in data_heap:
    for part in elem:
        flat_data_heap.append(part)
print(flat_data_heap)

# group lists of messages
grouped_messages_lists = []
for tag in tags_unique:
    same_tag_message_list = []
    for message in flat_data_heap:
        if message.startswith(tag):
            same_tag_message_list.append(message)
    grouped_messages_lists.append(same_tag_message_list)
print(grouped_messages_lists)

# dataframe by grouped messages
data = pd.DataFrame(data = grouped_messages_lists)
data = data.T
data.columns = tags_unique
print(data)

# xlsx by dataframe
data.to_excel("Channel report " + datetime.strftime(datetime.now(), "%d_%m_%Y__%H_%M_%S") + ".xlsx")