from Repositories.PoliticalPartyRepository import PoliticalPartyRepository
from Models.PoliticalParty import PoliticalParty

class PoliticalPartyController():
    def __init__(self):
        self.politicalPartyRepository = PoliticalPartyRepository()
    
    def index(self):
        return self.politicalPartyRepository.findAll()

    def create(self, infoPoliticalParty):
        politicalParty = PoliticalParty(infoPoliticalParty)
        return self.politicalPartyRepository.save(politicalParty)
    
    def show(self, id):
        politicalParty = PoliticalParty(self.politicalPartyRepository.findById(id))
        return politicalParty.__dict__
    def update(self, id, infoPoliticalParty):
        politicalParty = PoliticalParty(self.politicalPartyRepository.findById(id))
        politicalParty.name = infoPoliticalParty["name"]
        politicalParty.motto = infoPoliticalParty["motto"]
        return self.politicalPartyRepository.save(politicalParty)
    
    def delete(self, id):
        return self.politicalPartyRepository.delete(id)



