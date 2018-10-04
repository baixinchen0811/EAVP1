# -*- coding:utf-8 -*-
import Cap
import FigureOut
import csv

import time
start=time.clock()

show_all = input("Do you want to show all pictures? Please edit 1(Yes) or 0(No):")
r1 = input("Please input R1:") #输入上一级的r1,l1,允许的最大错误
l1 = input("Please input L1:")
err_k = input("Please choose error. Please edit 1 or 2:")
err = input("Please input Max_error:") if show_all == 0 else float("inf")
count = input("Please input max number of cap:")

my_cap = Cap.CapList(count).final() #生成所有电容组合

print len(my_cap)
temp = []
for i in my_cap:
    name, c, r, l, num = i
    if num != 0 and err_k == 2:
        now_error = FigureOut.Myfigure(R1=r1, L1=l1, R2=r, C2=c, L2=l, Name=','.join(name), Num=num).error2(err)

        temp.append([now_error, name, c, r, l]) if now_error != False else None

    if num != 0 and err_k == 1:
        now_error = FigureOut.Myfigure(R1=r1, L1=l1, R2=r, C2=c, L2=l, Name=','.join(name), Num=num).error(err)
        #if now_error <= err:
        temp.append([now_error, name, c, r, l]) if now_error != False else None
temp = sorted(temp, cmp=lambda x,y:cmp(x[0],y[0]))

out = open('result_test.csv', 'wb')
csv_write = csv.writer(out, dialect='excel')
csv_write.writerow(['Error', 'Name', 'C','R', 'L' ])
for i in temp:
    csv_write.writerow(i)
out.close()

k = input("How many combinations do you want to show?")
for i in range(k):
    c,r,l=temp[i][-3:]
    aa=FigureOut.Myfigure(R1=r1,L1=l1,R2=r,C2=c,L2=l,Name=','.join(temp[i][1]),Num=num).figure()

# k = input("How many combinations do you want to show?")
# for i in range(k):
#     print temp[i]

end = time.clock()
print('Running time: %s Seconds'%(end-start))