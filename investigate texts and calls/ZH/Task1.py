"""
下面的文件将会从csv文件中读取读取短信与电话记录，
你将在以后的课程中了解更多有关读取文件的知识。
"""
import csv
with open('texts.csv', 'r') as f:
    reader = csv.reader(f)
    texts = list(reader)

with open('calls.csv', 'r') as f:
    reader = csv.reader(f)
    calls = list(reader)


"""
任务1：
短信和通话记录中一共有多少电话号码？每个号码只统计一次。
输出信息：
"There are <count> different telephone numbers in the records."""
# process texts
tmp = list(zip(*texts))
texts_number_sta = set(tmp[0])
for item in set(tmp[1]):
    texts_number_sta.add(item)
# process calls
tmp = list(zip(*calls))
calls_number_sta = set(tmp[0])
for item in set(tmp[1]):
    calls_number_sta.add(item)
sum_of_numbers = len(texts_number_sta) + len(calls_number_sta)
print("There are {} different "
      "telephone numbers in the records.".format(sum_of_numbers))