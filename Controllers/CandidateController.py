from Repositories.CandidateRepository import CandidateRepository
from Repositories.PoliticalPartyRepository import PoliticalPartyRepository
from Models.Candidate import Candidate
from Models.PoliticalParty import PoliticalParty

class CandidateController():
    def __init__(self):
        self.candidateRepository = CandidateRepository()
        self.politicalPartyRepository = PoliticalPartyRepository()
    
    def index(self):
        return self.candidateRepository.findAll()

    def create(self, infoCandidate):
        id_politicalParty = infoCandidate.pop("id_politicalParty")
        politicalParty = PoliticalParty(self.politicalPartyRepository.findById(id_politicalParty))
        candidate = Candidate(infoCandidate)
        candidate.politicalParty = politicalParty
        return self.candidateRepository.save(candidate)
        
    def show(self, id):
        candidate=Candidate(self.candidateRepository.findById(id))
        return candidate.__dict__
    
    def update(self, id, infoCandidate):
        politicalParty = PoliticalParty(self.politicalPartyRepository.findById(infoCandidate["id_politicalParty"]))
        candidate=Candidate(self.candidateRepository.findById(id))
        candidate.dni = infoCandidate["dni"]
        candidate.resolution_number = infoCandidate["resolution_number"]
        candidate.name = infoCandidate["name"]
        candidate.last_name = infoCandidate["last_name"]
        candidate.politicalParty = politicalParty 
        return self.candidateRepository.save(candidate)

    def delete(self, id):
        return self.candidateRepository.delete(id)

    