import xmltodict
from haversine import haversine
import time
import numpy as np
from sklearn.neighbors import KDTree

# chua cac phuong thuc thuc hien nhiem vu

s = time.time()
doc = {}
with open('data/mapforwalk.graphml') as fd:
    doc = xmltodict.parse(fd.read())
print(time.time()-s)

# lay kinh do, vi do cua 1 nut bang cach truyen OSMId


def getLatLon(OSMId):
    lat, lon = 0, 0
    nodes = doc['graphml']['graph']['node']
    for eachNode in range(len(nodes)):
        if(nodes[eachNode]["@id"] == str(OSMId)):
            lat = float(nodes[eachNode]["data"][0]["#text"])
            lon = float(nodes[eachNode]["data"][1]["#text"])
    return (lat, lon)

# lay OSMId cua 1 nut tu kinh do va vi do cua nut do


def getOSMId(lat, lon):
    OSMId = 0
    nodes = doc['graphml']['graph']['node']
    for eachNode in range(len(nodes)):
        if(nodes[eachNode]["data"][0]["#text"] == str(lat)):
            if(nodes[eachNode]["data"][1]["#text"] == str(lon)):
                OSMId = nodes[eachNode]["data"][2]["#text"]

    return OSMId


def calculateHeuristic(curr, destination):
    return (haversine(curr, destination))

# tao ra cac nut lan can voi nut dang xet


def getNeighbours(OSMId, destinationLetLon):
    # dictionary chua thong tin nguoi hang xom
    neighbourDict = {}

    tempList = []
    # canh
    edges = doc['graphml']['graph']['edge']
    for eachEdge in range(len(edges)):
        # kiem tra nut nguon cua canh co trung voi nut hien tai khong
        if(edges[eachEdge]["@source"] == str(OSMId)):

            temp_nbr = {}

            neighbourCost = 0
            # tim nguoi hang xom, gan ID hang xom la nut con lai cua canh
            neighbourId = edges[eachEdge]["@target"]
            # lay toa do cua hang xom
            neighbourLatLon = getLatLon(neighbourId)

            # tat ca du lieu canh cua 2 diem
            dataPoints = edges[eachEdge]["data"]
            # lay chi phi cua nut hien tai den cac nut hang xom - neighbourCost
            for eachData in range(len(dataPoints)):
                if(dataPoints[eachData]["@key"] == "d9"):
                    neighbourCost = dataPoints[eachData]["#text"]

            # tinh Heuristic cua nut hang xom
            neighborHeuristic = calculateHeuristic(
                neighbourLatLon, destinationLetLon)

            # temp_nbr: luu thong tin ve nut hang xom
            # key: ID
            # value: toa do, chi phi tu nut hien tai den hang xom, chi phi heuristic tu nut hang xom den dich

            temp_nbr[neighbourId] = [neighbourLatLon,
                                     neighbourCost, neighborHeuristic]
            # tempList danh sach luu tru thong tin cac hang xom
            tempList.append(temp_nbr)

    # neighbourDict: luu tru thong tin cac hang xom cua nut dang xet co OSMID
    neighbourDict[OSMId] = tempList
    return (neighbourDict)

# trich xuat thong tin nguoi hang xom


def getNeighbourInfo(neighbourDict):
    neighbourId = 0
    neighbourHeuristic = 0
    neighbourCost = 0
    for key, value in neighbourDict.items():

        neighbourId = key
        neighbourHeuristic = float(value[2])
        neighbourCost = float(value[1])/1000
        neighbourLatLon = value[0]

    return neighbourId, neighbourHeuristic, neighbourCost, neighbourLatLon

# Argument should be tuple


def getKNN(pointLocation):
    # find all node in data
    nodes = doc["graphml"]["graph"]["node"]
    # 1 list luu toa do (x, y) cac node
    locations = []
    for eachNode in range(len(nodes)):
        # add all vi tri cac node
        locations.append(
            (nodes[eachNode]["data"][0]["#text"], nodes[eachNode]["data"][1]["#text"]))
    #
    locations_arr = np.asarray(locations, dtype=np.float32)
    point = np.asarray(pointLocation, dtype=np.float32)

    tree = KDTree(locations_arr, leaf_size=2)
    dist, ind = tree.query(point.reshape(1, -1), k=3)
    print(dist.shape)
    print(ind.shape)
    nearestNeighbourLoc = (
        float(locations[ind[0][0]][0]), float(locations[ind[0][0]][1]))

    return nearestNeighbourLoc

# lay duong dan cuoi cung tu nguon den dich, tra ve cac nut trong duong dan
# va chi phi tu nguon den dich (cong don)


def getResponsePathDict(paths, source, destination):
    # duong dan cuoi cung
    finalPath = []
    # gan nut con = dich
    child = destination
    # child=getOSMId(destination[0], destination[1])
    # source=getOSMId(source[0], source[1])
    # tap nut cha cua nut con
    parent = ()
    cost = 0
    # trong khi cha khac nut nguon
    while(parent != source):

        tempDict = {}
        cost = cost + float(paths[str(child)]["cost"])
        parent = paths[str(child)]["parent"]
        parent = tuple(float(x) for x in parent.strip('()').split(','))

        tempDict["lat"] = parent[0]
        tempDict["lng"] = parent[1]

        finalPath.append(tempDict)
        child = parent
        # lay toa do nut cha
        # tempDict["lat"] = parent[0]
        # tempDict["lng"] = parent[1]

        # finalPath.append(tempDict)
        # finalPath.append(parent)
        child = parent

    return finalPath, cost
