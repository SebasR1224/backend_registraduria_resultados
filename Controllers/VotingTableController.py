from Repositories.VotingTableRepository import VotingTableRepository
from Models.VotingTable import VotingTable
class VotingTableController():
    def __init__(self):
        self.votingTableRepository = VotingTableRepository()

    def index(self):
        return self.votingTableRepository.findAll()
    
    def create(self, infoVotingTable):
        votingTable = VotingTable(infoVotingTable)
        return self.votingTableRepository.save(votingTable)

    def show(self, id):
        votingTable = VotingTable(self.votingTableRepository.findById(id))
        return votingTable.__dict__
    
    def update(self, id, infoVotingTable):
        votingTable = VotingTable(self.votingTableRepository.findById(id))
        votingTable.number_table = infoVotingTable["number_table"]
        votingTable.registered_documents = infoVotingTable["registered_documents"]
        return self.votingTableRepository.save(votingTable)
    
    def delete(self, id):
        return self.votingTableRepository.delete(id)
    
        
    

        