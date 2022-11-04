from Repositories.ResultRepository import ResultRepository
from Repositories.VotingTableRepository import VotingTableRepository
from Repositories.CandidateRepository import CandidateRepository

from Models.Result import Result
from Models.VotingTable import VotingTable
from Models.Candidate import Candidate

class ResultController():
    def __init__(self):
        self.resultRepository = ResultRepository()
        self.votingTableRepository = VotingTableRepository()
        self.candidateRepository = CandidateRepository()
    
    def index(self):
        return self.resultRepository.findAll()
    
    """
    Asignacion mesa de votación y candidatos
    """
    def create(self, infoResult):
        id_votingTable = infoResult.pop("id_votingTable")
        id_candidate = infoResult.pop("id_candidate") 
        votingTable = VotingTable(self.votingTableRepository.findById(id_votingTable))
        candidate = Candidate(self.candidateRepository.findById(id_candidate))    
        result = Result(infoResult)
        result.votingTable = votingTable
        result.candidate = candidate
        return self.resultRepository.save(result)

    def show(self, id):
        result = Result(self.resultRepository.findById(id))
        return result.__dict__
    
    def update(self, id, infoResult):
        result = Result(self.resultRepository.findById(id))
        votingTable = VotingTable(self.votingTableRepository.findById(infoResult["id_votingTable"]))
        candidate = Candidate(self.candidateRepository.findById(infoResult["id_candidate"]))
        result.votingTable = votingTable
        result.candidate = candidate
        result.total_votes = infoResult["total_votes"]
        return self.resultRepository.save(result)
    
    def delete(self, id):
        return self.resultRepository.delete(id)


