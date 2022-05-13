from fileinput import filename
import re
from matplotlib.pyplot import axis
import pandas as pd
import numpy as np

# Nhập tên file và đọc file theo từng dòng
while(True):
    global file_name 
    file_name = input("Enter a class file to grade (i.e. class1 for class1.txt): ")
    try:
        with open(file_name+".txt", "r") as file:
            file_lines = file.readlines()
            print("Successfully opened " + file_name +".txt")
            break
    except:
        print("File cannot be found.")


# Lọc các phần tử không phù hợp và thông báo
sum_lines = len(file_lines)
count = 0
print("\n**** ANALYZING ****\n")
lst = []
for line in file_lines:
    # Kiểm tra mỗi dòng có hợp lệ hay không
    if re.search("^N[0-9]{8},", line) == None:
        count+=1
        print("Invalid line of data: N# is invalid")
        print(line)
    else: 
        list_content_line = line.strip().split(',')
        if len(list_content_line) != 26:
            print("Invalid line of data: does not contain exactly 26 values:")
            print(line)
            count+=1
        else:
            lst.extend(list_content_line)
if count == 0:
    print("No errors found!")
valid_lines = sum_lines - count
print("\n**** REPORT ****\n")
print("Total valid lines of data: " + str(valid_lines))
print("Total invalid lines of data: " + str(count) + "\n")

# Đưa vào DataFram bằng pandas và phân tích bằng numpy
lst_name_cols = ["id"]
for i in range(1, 26):
    lst_name_cols.append("c{}".format(i))
lst_name_cols = np.array(lst_name_cols)

row = int(len(lst) / 26)
np_list = np.array(lst).reshape(row, 26)
df = pd.DataFrame(np_list, columns = lst_name_cols)
answer_key = "B,A,D,D,C,B,D,A,C,C,D,B,A,B,A,C,B,D,A,C,A,A,B,D,D".split(',')
for idx_row in range(0, row):
    for idx_col in range(1, 26):
        if df.iloc[idx_row, idx_col] == '':
            df.iloc[idx_row, idx_col] = 0
        elif df.iloc[idx_row, idx_col] == answer_key[idx_col-1]:
            df.iloc[idx_row, idx_col] = 4
        else:
            df.iloc[idx_row, idx_col] = -1
np_sum_score = np.array(df.iloc[:,1:].sum(axis=1), dtype=int)

print("Mean (average) score: " + str(round(np.mean(np_sum_score), 2)))
print("Highest score: " + str(np.max(np_sum_score)))
print("Lowest score: " + str(np.min(np_sum_score)))
print("Range of scores: " + str(np.max(np_sum_score) - np.min(np_sum_score)))
print("Median score: " + str(int(np.median(np_sum_score))) + '\n')

# Tạo báo cáo 
lst_count_skip = []
lst_count_incorrectly = []
## Tạo danh sách số lần bị bỏ qua và bị sai cho mỗi câu hỏi
for col in df.columns[1:]:
    count_incorrectly = 0
    count_skip = 0
    for score in df.loc[ : , col]:
        if score == -1:
            count_incorrectly +=1
        if score == 0:
            count_skip +=1
    lst_count_incorrectly.append(count_incorrectly)
    lst_count_skip.append(count_skip)

## Hàm trả về chuỗi report cho câu hỏi sai và bị bỏ qua
def printInfoCount(lst):
    max_lst = max(lst)
    count = 1
    result = ""
    for i in lst:
        tmp = []
        if i == max_lst:
            result += (str(count) 
                       + " - " 
                       + str(i) 
                       + " - " 
                       + str(round(i / valid_lines,2)) 
                       + ', ')
        count+=1
    return result[ : -2]    
print("Question that most people skip: " + printInfoCount(lst_count_skip))
print("Question that most people answer incorrectly: " + printInfoCount(lst_count_incorrectly))

# Ghi vào file kết qua cho class nhập vào
file_name_grades = file_name + "_grades.txt"
with open(file_name_grades, 'w') as wf:
    for i in range(0, np_sum_score.size):
        wf.write(list(df.loc[:,'id'])[i] 
                 + ',' 
                 + str(np_sum_score[i]) 
                 + '\n')