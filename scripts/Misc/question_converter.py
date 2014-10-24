import xml.etree.ElementTree as ET
import csv

import os


def main():
    os.makedirs("C:\\Users\\Sharang\\Desktop\\My stuff\\My work\\Question Banks for HW Central\\MathVII\\")
    a = [];
    i = 0;
    csvReader = csv.reader(open('math.txt', 'r'), delimiter='\t');
    for row in csvReader:
        a.append(row);

    for x in range(1, len(a)):
        question = ET.Element('question')
        question.set("type", "1")
        question.set("chapter", sanitize(a[x][0]))
        question.set("subject", "Math")
        question.set("difficulty", sanitize(a[x][7]))
        Q = ET.SubElement(question, 'Q')
        Q.text = sanitize(a[x][1])
        options = ET.SubElement(question, 'options')
        CO = ET.SubElement(options, 'CO')
        CO.text = sanitize(a[x][2])
        CO.set("unit", sanitize(a[x][8].decode("utf8")))
        y = 3;
        for z in range(0, 3):
            O = ET.SubElement(options, 'O')
            O.text = sanitize(a[x][y])
            O.set("unit", sanitize(a[x][8]))
            z += 1
            y += 1
        if (a[x][6] != ''):
            img = ET.SubElement(question, 'img')
            img.text = sanitize(a[x][6])
        indent(question)
        filename = str(x) + ".xml"
        print "<?xml version=\"1.0\" encoding=\"UTF-8\"?>"
        ET.dump(question)
        chapter = a[x][0]
        counter = "C:\\Users\\Sharang\\Desktop\\My stuff\\My work\\Question Banks for HW Central\\MathVII\\" + chapter + "\\"
        fileverify = counter + filename
        if not os.path.exists(counter):
            os.makedirs(counter)
            os.chdir(counter)
        if os.path.exists(counter):
            os.chdir(counter)
            if not os.path.exists(fileverify):
                file = open(filename, "w")
                file.write("<?xml version=\"1.0\" encoding=\"UTF-8\"?>\n")
                file.write(ET.tostring(question))
                file.close()

        file = open(filename, "w")
        file.write("<?xml version=\"1.0\" encoding=\"UTF-8\"?>\n")
        file.write(ET.tostring(question))
        file.close()


def indent(elem, level=0):
    i = "\n" + level * "  "
    if len(elem):
        if not elem.text or not elem.text.strip():
            elem.text = i + "  "
        if not elem.tail or not elem.tail.strip():
            elem.tail = i
        for elem in elem:
            indent(elem, level + 1)
        if not elem.tail or not elem.tail.strip():
            elem.tail = i
    else:
        if level and (not elem.tail or not elem.tail.strip()):
            elem.tail = i


def sanitize(a):
    return a.strip('\" ').decode("utf8", 'ignore')


main();

