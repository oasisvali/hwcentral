# # This script creates a mysql table filled with school info which can then easily be imported into other tables

import urllib2
import string
import re

from MySQLdb import connect




# # GLOBALS

SRC_URL = "http://cbse.nic.in/physports/sportsgames/CLUS%20#.TXT"
TEMP_DIR = 'temp/'
DATA_FILE_EXT = '.txt'
DATA_FILE_PREFIX = 'data_'

CLUSTER_LIST = ['I',
                'II',
                'III',
                'IV',
                'V',
                'VI',
                'VII',
                'VIII',
                'IX',
                'X',
                'XI',
                'XII',
                'XIII',
                'XIV',
                'XV',
                'XVI']

DATA_LIST = []


def grab_data():
    global DATA_LIST
    for clusterNum in CLUSTER_LIST:
        print 'Grabbing info file for Cluster: ' + clusterNum
        DATA_LIST += [urllib2.urlopen(string.replace(SRC_URL, '#', clusterNum)).read()]

    return


def write_data():
    global DATA_LIST
    for i in xrange(len(CLUSTER_LIST)):
        print 'Writing info file for Cluster: ' + CLUSTER_LIST[i]
        f = open(TEMP_DIR + CLUSTER_LIST[i] + DATA_FILE_EXT, 'w')
        f.write(DATA_LIST[i])
        f.close()

    return


def read_data():
    global DATA_LIST
    DATA_LIST = []
    for clusterNum in CLUSTER_LIST:
        print 'Reading info file for Cluster: ' + clusterNum
        f = open(TEMP_DIR + DATA_FILE_PREFIX + clusterNum + DATA_FILE_EXT, 'r')
        DATA_LIST += [f.read()]
        f.close()

    return


# takes the string containing the name and address and seperates the name and address and removes excess whitespace
def format(string):
    lineList = string.split('\n')
    for i in xrange(len(lineList)):
        lineList[i] = lineList[i].strip()

    return lineList[0], '\n'.join(lineList[1:])


def extract_info():
    global DATA_LIST
    for i in xrange(len(DATA_LIST)):

        data = DATA_LIST[i]
        pattern = re.compile(
            r'AFF\s*NO\s*:\s*(\w+)\s*(\(\s*EXAM\s*NO\s*:\s*(\w+)\))?\s*THE\s*PRINCIPAL\s*([\s\S]+?)Pin:(\d+)?')
        matches = pattern.findall(data)

        print str(len(matches)) + ' schools found for Cluster: ' + str(i + 1)

        for match in matches:

            aff_num = None  # As aff_num coumn in db is non-null, this will raise error as soon as any aff_num is missed
            name = '?????'
            address = '?????'
            pin = None
            exam_num = None

            if match[0]:
                aff_num = match[0]
            if match[2]:
                exam_num = match[2]
            if match[3]:
                name, address = format(match[3])
            if match[4]:
                pin = int(match[4])

            row = SchoolRow(i + 1, aff_num, name, address, pin, exam_num)
            row.save()

    return


# splits 2 column text file into single column of data, which is easier to parse
def prepare_files():
    for clusterNum in CLUSTER_LIST:
        print 'Preparing data file for Cluster: ' + clusterNum
        col1 = ''
        col2 = ''
        f = open(TEMP_DIR + clusterNum + DATA_FILE_EXT, 'r')
        for line in f:
            if len(line.strip()) == 0:
                continue
            elif len(line) >= 39:
                col1 += line[:39] + '\n'
                col2 += line[39:]
            else:
                col1 += line + '\n'
        f.close()
        f = open(TEMP_DIR + DATA_FILE_PREFIX + clusterNum + DATA_FILE_EXT, 'w')
        f.write(col1 + col2)
        f.close()

    return


class SchoolRow(object):
    def __init__(self, cluster, aff_num, name, address, pin=None, exam_num=None):  # None in python = null in MySQL
        self.cluster = cluster
        self.aff_num = aff_num
        self.name = name
        self.address = address
        self.pin = pin
        self.exam_num = exam_num

    def save(self):
        conn = connect(host="localhost",
                       user="root",
                       passwd="makeitbig",
                       db="store")
        curs = conn.cursor()

        curs.execute(
            "INSERT INTO school_info (aff_num, exam_num, name, address, pin, cluster) VALUES (%s, %s, %s, %s, %s, %s)",
            (self.aff_num, self.exam_num, self.name, self.address, self.pin, self.cluster))

        curs.close()
        conn.commit()
        conn.close()


if __name__ == '__main__':
    #grab_data()
    #write_data()
    #prepare_files()
    read_data()
    extract_info()