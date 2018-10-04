import  csv
def cap_init(self, file = 'prodcharas330' ):
    with open(file, 'rb') as capfile:
        data = csv.reader(capfile)
        for j in data:
            self.capdict[j[0]] = j[1:] + [1]
    capfile.close()


self.capdict()
