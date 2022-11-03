from flask import Flask
from flask import jsonify
from flask import request
from flask_cors import CORS
import json
from waitress import serve

app=Flask(__name__)
cors = CORS(app)

#controllers instance
from Controllers.CandidateController import CandidateController
candidateController = CandidateController()
from Controllers.PoliticalPartyController import PoliticalPartyController
politicalPartyController = PoliticalPartyController()

@app.route("/",methods=['GET'])
def test():
    json = {}
    json["message"]="Server running ..."
    return jsonify(json)

#-------------------methods Candidates -----------------------------------
@app.route("/candidates", methods=['GET'])
def getCandidates():
    json =  candidateController.index()
    return jsonify(json)
@app.route("/candidates", methods=['POST'])
def createCandidate():
    data = request.get_json()
    json = candidateController.create(data)
    return jsonify(json)
@app.route("/candidates/<string:id>",methods=['GET'])
def getCandidate(id):
    json =  candidateController.show(id)
    return jsonify(json)
@app.route("/candidates/<string:id>", methods=['PUT'])
def updateCandidate(id):
    data = request.get_json()
    json = candidateController.update(id, data)
    return jsonify(json)
@app.route("/candidates/<string:id>", methods=['DELETE'])
def deleteCandidate(id):
    json = candidateController.delete(id)
    return jsonify(json)
#------------------- end methods Candidates -------------------------------
    
#-------------------methods Political Parties -----------------------------
@app.route("/politicalParties", methods=['GET'])
def getPoliticalParties():
    json =  politicalPartyController.index()
    return jsonify(json)
@app.route("/politicalParties", methods=['POST'])
def createPoliticalParty():
    data = request.get_json()
    json = politicalPartyController.create(data)
    return jsonify(json)
@app.route("/politicalParties/<string:id>",methods=['GET'])
def getPoliticalParty(id):
    json =  politicalPartyController.show(id)
    return jsonify(json)
@app.route("/politicalParties/<string:id>", methods=['PUT'])
def updatePoliticalParty(id):
    data = request.get_json()
    json = politicalPartyController.update(id, data)
    return jsonify(json)
@app.route("/politicalParties/<string:id>", methods=['DELETE'])
def deletePoliticalParty(id):
    json = politicalPartyController.delete(id)
    return jsonify(json)
#------------------- end methods Political Parties -------------------------

def loadFileConfig():
    with open('config.json') as f:
        data = json.load(f)
    return data

if __name__=='__main__':
    dataConfig = loadFileConfig()
    print("Server running : "+"http://"+dataConfig["url-backend"]+":" + str(dataConfig["port"]))
    serve(app,host=dataConfig["url-backend"],port=dataConfig["port"])