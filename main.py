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

from Controllers.ResultController import ResultController
resultController = ResultController()

from Controllers.VotingTableController import VotingTableController
votingTableController = VotingTableController()


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
@app.route("/political-parties", methods=['GET'])
def getPoliticalParties():
    json =  politicalPartyController.index()
    return jsonify(json)
@app.route("/political-parties", methods=['POST'])
def createPoliticalParty():
    data = request.get_json()
    json = politicalPartyController.create(data)
    return jsonify(json)
@app.route("/political-parties/<string:id>",methods=['GET'])
def getPoliticalParty(id):
    json =  politicalPartyController.show(id)
    return jsonify(json)
@app.route("/political-parties/<string:id>", methods=['PUT'])
def updatePoliticalParty(id):
    data = request.get_json()
    json = politicalPartyController.update(id, data)
    return jsonify(json)
@app.route("/political-parties/<string:id>", methods=['DELETE'])
def deletePoliticalParty(id):
    json = politicalPartyController.delete(id)
    return jsonify(json)
#------------------- end methods Political Parties ------------------------

#-------------------methods Results -----------------------------
@app.route("/results", methods=['GET'])
def getResults():
    json =  resultController.index()
    return jsonify(json)
@app.route("/results", methods=['POST'])
def createResult():
    data = request.get_json()
    json = resultController.create(data)
    return jsonify(json)
@app.route("/results/<string:id>",methods=['GET'])
def getResult(id):
    json =  resultController.show(id)
    return jsonify(json)
@app.route("/results/<string:id>", methods=['PUT'])
def updateResult(id):
    data = request.get_json()
    json = resultController.update(id, data)
    return jsonify(json)
@app.route("/results/<string:id>", methods=['DELETE'])
def deleteResult(id):
    json = resultController.delete(id)
    return jsonify(json)
#------------------- end methods Results ------------------------

#-------------------methods Voting tables -----------------------
@app.route("/voting-tables", methods=['GET'])
def getVotingTables():
    json =  votingTableController.index()
    return jsonify(json)
@app.route("/voting-tables", methods=['POST'])
def createVotingTable():
    data = request.get_json()
    json = votingTableController.create(data)
    return jsonify(json)
@app.route("/voting-tables/<string:id>",methods=['GET'])
def getVontingTable(id):
    json =  votingTableController.show(id)
    return jsonify(json)
@app.route("/voting-tables/<string:id>", methods=['PUT'])
def updateVotingTable(id):
    data = request.get_json()
    json = votingTableController.update(id, data)
    return jsonify(json)
@app.route("/voting-tables/<string:id>", methods=['DELETE'])
def deleteVotingTable(id):
    json = votingTableController.delete(id)
    return jsonify(json)
#------------------- end methods Voting tables -------------------

#-------------------methods reporsts -----------------------

@app.route("/vote-list/<string:id_table>", methods=['GET'])
@app.route("/vote-list", methods=['GET'])
def voteList(id_table=None):
    json = resultController.voteList(id_table)
    return jsonify(json)

@app.route("/get-votes-candidates/<string:id_table>", methods=['GET'])
@app.route("/get-votes-candidates", methods=['GET'])
def getVotesCandidates(id_table=None):
    json = resultController.getVotesCandidates(id_table)
    return jsonify(json)


@app.route("/total-votes-table", methods=['GET'])
def totalVotesTable():
    json = resultController.totalVotesTable()
    return jsonify(json)

@app.route("/total-votes-political-party/<string:id_table>", methods=['GET'])
@app.route("/total-votes-political-party", methods=['GET'])
def totalVotesPoliticalParty(id_table=None):
    json = resultController.totalVotesPoliticalParty(id_table)
    return jsonify(json)


@app.route("/percentage-congress", methods=['GET'])
def percentageCongress():
    json = resultController.percentageCongress()
    return jsonify(json)   

#------------------- end reporsts -------------------

def loadFileConfig():
    with open('config.json') as f:
        data = json.load(f)
    return data

if __name__=='__main__':
    dataConfig = loadFileConfig()
    print("Server running : "+"http://"+dataConfig["url-backend"]+":" + str(dataConfig["port"]))
    serve(app,host=dataConfig["url-backend"],port=dataConfig["port"])