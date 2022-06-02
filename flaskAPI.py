from flask import Flask, request
from flask_cors import CORS
import convertJSON as cj
import astar as algo
import json

# khoi tao flask server backend
app = Flask(__name__)
CORS(app)


@app.route('/calculate', methods=['GET'])
# ham xu li api
def home():
    raw_input = request.args.get('pntdata').split(',')

    inputSourceLoc = (float(raw_input[0]), float(raw_input[1]))
    inputDestLoc = (float(raw_input[2]), float(raw_input[3]))
    # diem gan nhat
    mappedSourceLoc = cj.getKNN(inputSourceLoc)
    mappedDestLoc = cj.getKNN(inputDestLoc)
    # tim diem gan nhat thuoc duong
    print("nguon:"+str(cj.getOSMId(mappedSourceLoc[0], mappedSourceLoc[1])))
    print("dich:"+str(cj.getOSMId(mappedDestLoc[0], mappedDestLoc[1])))
    # path = algo.aStar(mappedSourceLoc, mappedDestLoc)
    # print(path)
    # return path
    # finalPath, cost = cj.getResponsePathDict(
    #     path, mappedSourceLoc, mappedDestLoc)

    # print("Cost of the path(km): "+str(cost))
    # print(json.dumps(finalPath))
    # return json.dumps(finalPath)
    path = algo.aStar(mappedSourceLoc, mappedDestLoc)
    finalPath, cost = cj.getResponsePathDict(
        path, mappedSourceLoc, mappedDestLoc)

    print("Cost of the path(km): "+str(cost))
    return json.dumps(finalPath)


if __name__ == "__main__":
    app.run(host='0.0.0.0')
