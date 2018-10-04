# -*- coding:utf-8 -*-
import csv


class CapList(object):
    def __init__(self, Nums):
        '''初始化'''

        self.capdict = {}    # capdict[name] = [C, R, L, nums]
        self.nums = Nums
        #self.para = [C, R, L]


    def cap_init(self, file = 'test.csv' ):
        '''生成初始电容库'''

        with open(file, 'rb') as capfile:
            data = csv.reader(capfile)
            for j in data:
                self.capdict[j[0]] = j[1:] + [1]
        capfile.close()
        del self.capdict['Name']

        for i, j in self.capdict.items():
            self.capdict[i] = list(map(lambda x:float(x), j))


    def cap_parallel(self, nums):
        '''通过相同电容并联产生新电容，且并联个数最多不超过nums个'''

        new_capdict = {}
        for i in range(len(self.capdict)):
            for j in range(2,nums+1):
                for name, value in self.capdict.items():
                    new_capdict[str(j)+'^'+name] = [value[0]*j] + list(map(lambda x: x/j, value[1:3])) + [value[-1]+j -1]
        self.capdict.update(new_capdict)
        self.capdict['None'] = [0.0, 0.0, 0.0, 0]


    def cap_series(self, nums):
        '''总个数相当于  (X+Y-1)C(Y) 个'''
        self.temp_capdict = []
        for name, value in self.capdict.items():
            self.temp_capdict.append([[name]]+value)

        if nums <= 0 or not self.temp_capdict: return None

        temp = [i for i in self.temp_capdict]
        temp2 = [i[0][0] for i in self.temp_capdict]
        for _ in range(nums-1):
            lenth = len(temp)
            for i in range(lenth):
                now = temp.pop(0)
                for j in range(temp2.index(now[0][-1]), len(temp2)):
                    if now[1] != 0 and self.temp_capdict[j][1] != 0:
                        C = (now[1] * self.temp_capdict[j][1])/(now[1] + self.temp_capdict[j][1])
                    else:
                        C = now[1] if now[1] != 0 else self.temp_capdict[j][1]
                    name = now[0] + self.temp_capdict[j][0]
                    R = now[2] + self.temp_capdict[j][2]
                    L = now[3] + self.temp_capdict[j][3]
                    count = now[4] + self.temp_capdict[j][4]

                    # if self.temp_capdict[j][0][0] == 'None' or now[0] == 'None':
                    #     name = now[0] + self.temp_capdict[j][0]
                    #     C = now[1]
                    #     R = now[2]
                    #     L = now[3]
                    #     count = now[4] + self.temp_capdict[j][4]
                    # else:
                    #     name = now[0]+self.temp_capdict[j][0]
                    #     C = (now[1] * self.temp_capdict[j][1])/(now[1] + self.temp_capdict[j][1])
                    #     R = now[2] + self.temp_capdict[j][2]
                    #     L = now[3] + self.temp_capdict[j][3]
                    #     count = now[4] + self.temp_capdict[j][4]
                    if count <= nums:
                        temp.append([name, C, R, L, count])

        self.final = {}
        for i in temp:
            self.final[' '.join(i[0])] = i[1:]

        return temp


    def final(self):
        self.cap_init()
        self.cap_parallel(self.nums)
        finalcap = self.cap_series(self.nums)

        return finalcap
    # def cap_choose(self, K=1):
    #     """从生成的电容组合中选取 K 个最接近的组合"""
    #
    #     temp = []
    #     lenth= len(self.final)
    #     for _ in range(lenth):
    #         now = self.final.popitem()
    #         flag = True
    #         error = 0
    #         for j in range(3):
    #             if error > 10:
    #                 flag = True
    #                 break
    #             else:
    #                 error += abs(now[1][j]- self.para[j])/self.para[j]
    #         if flag == True and error < 10:
    #             temp.append([now[0],error])
    #
    #     temp = sorted(temp, cmp=lambda x,y:cmp(x[1],y[1]))
    #
    #     return temp[0:K]


    # def cap_series_old(self, nums = 3):
    #     "通过不同电容串联产生新电容，且串联个数不超过nums个"
    #
    #     self.temp_capdict = []
    #     for name, value in self.capdict.items():
    #         self.temp_capdict.append([name]+value)
    #
    #     amount = len(self.temp_capdict)
    #     lenth, i = len(self.temp_capdict), 1
    #     while i <= lenth:
    #         A = self.temp_capdict[0]
    #         len_ini = len(self.temp_capdict)
    #         tempp = self.cal_count2(A, nums)
    #         for j in range(1,len_ini): #len(self.temp_capdict)
    #             B = self.temp_capdict[j]
    #             self.temp_capdict += self.cal_count(A, B, nums)
    #         self.temp_capdict += tempp
    #         i += 1
    #         A = self.temp_capdict.pop(0)
    #
    #     for i in range(len(self.temp_capdict)):
    #         self.capdict[self.temp_capdict[i][0]] = self.temp_capdict[i][1:]
    # def cal_count(self, A, B, nums):
    #     "计算AX+BY<=C 的整数解"
    #     A_name, A_C, A_R, A_L, A_COUNT = A
    #     B_name, B_C, B_R, B_L, B_COUNT = B
    #     ans = []
    #
    #     if nums/A_COUNT == 0 or nums/B_COUNT == 0: return ans
    #
    #     for i in range(1,int(nums/A_COUNT)+1):
    #         for j in range(1,int(nums/B_COUNT)+1):
    #             if i*A_COUNT + j*B_COUNT <= nums:
    #                 ans.append(['('+str(i)+"*"+A_name+'+'+str(j)+"*"+B_name+')', A_C/i*B_C/j/(A_C/i+B_C/j), A_R*i+B_R*j, A_L*i+B_L*j, A_COUNT*i+B_COUNT*j])
    #             else:
    #                 break
    #     return ans
    # def cal_count2(self, A, nums):
    #     A_name, A_C, A_R, A_L, A_COUNT = A
    #     ans = []
    #
    #     if nums / A_COUNT == 0 : return ans
    #
    #     for i in range(1,int(nums/A_COUNT)+1):
    #         if i*A_COUNT <= nums:
    #             ans.append(['('+str(i)+"*"+A_name+')', A_C/i, A_R*i, A_L*i, A_COUNT*i])
    #         else:
    #             break
    #     return ans

# a = CapList(3).final()
# print len(a)
# b = 0
# for i, j in enumerate(a):
#     if j[0] == ['1','1','1']:
#         print i
#         for k in range(3):
#             print "%.11f" % j[k+1]
#
# print b