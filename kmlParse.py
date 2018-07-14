from pykml import parser
from os import path

# путь до кмл файла
root = path.join('f:', 'razrezy.kml')


# Парс кмл
def openkml(kml):
    with open(kml) as f:
        doc = parser.parse(f).getroot()
    return doc


# Возвращает список словарей со значениями id и названием разреза
def fillkml(d):
    razrezylist = []
    placemark = d.Document.Folder.Placemark
    for i in range(0, int(len(placemark))):
        razrezylist.append({'name': placemark[i].ExtendedData.SchemaData.SimpleData[1],
                            'id': placemark[i].ExtendedData.SchemaData.SimpleData[6]})
    #print razrezylist[0]['id']
    return razrezylist


# Поиск (x1 y1) и (x2 y2)
def minmaxkml(dictionary, id):
    placemark = dictionary.Document.Folder.Placemark

    foo = 0
    for i in range(0, len(placemark)):
        if (placemark[i].ExtendedData.SchemaData.SimpleData[6] == id):
            foo = int(str(i))
            break

    placemark = dictionary.Document.Folder.Placemark[foo]
    #print (placemark.MultiGeometry.Polygon.outerBoundaryIs.LinearRing.coordinates)
    coordinates = str(placemark.MultiGeometry.Polygon.outerBoundaryIs.LinearRing.coordinates)

    xarray = coordinates.replace(',', ' ').split()
    yarray = coordinates.replace(',', ' ').split()
    for i in range(0, len(xarray), 1):
        xarray[i] = float(xarray[i])
    for i in range(0, len(yarray), 1):
        yarray[i] = float(yarray[i])
    #latitude
    del xarray[1::2]
    #longitude
    del yarray[0::2]

    #print("x", xarray)
    #print("y", yarray)

    x1 = round(min(xarray), 3)
    x2 = round(max(xarray), 3)
    y1 = round(max(yarray), 3)
    y2 = round(min(yarray), 3)
    print("Координата (y1,x1): " + str(y1) + " " + str(x1))
    print("Координата (y2,x2): " + str(y2) + " " + str(x2))
    return [y1, x1, y2, x2]


if __name__ == "__main__":
    kmlbase = openkml(root)
    kmldict = fillkml(kmlbase)
    minmaxkml(kmlbase, kmldict[2]['id'])

# print kmldict[0]['name']
