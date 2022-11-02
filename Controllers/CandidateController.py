from Repositories.CandidateRepository import CandidateRepository
from Models.Candidate import Candidate

class CandidateController():
    def __init__(self):
        self.candidateRepository = CandidateRepository()
    
    def index(self):
        return self.candidateRepository.findAll()

    def create(self, infoCandidate):
        candidate = Candidate(infoCandidate)
        return self.candidateRepository.save(candidate)
        
    def show(self, id):
        candidate=Candidate(self.candidateRepository.findById(id))
        return candidate.__dict__
    
    def update(self, id, infoCandidate):
        candidate=Candidate(self.candidateRepository.findById(id))
        candidate.dni = infoCandidate["dni"]
        candidate.resolution_number = infoCandidate["resolution_number"]
        candidate.name = infoCandidate["name"]
        candidate.last_name = infoCandidate["last_name"] 
        return self.candidateRepository.save(candidate)

    def delete(self, id):
        return self.candidateRepository.delete(id)

    