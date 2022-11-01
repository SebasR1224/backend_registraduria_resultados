from Models.Candidate import Candidate

class CandidateController():
    def __init__(self) -> None:
        print("CandidateController creado")
    
    def index(self):
        print("Listar todos los candidatos")
        candidate = {
            "_id": "abc123",
            "dni": "1014176356",
            "resolution_number": "123456",
            "name": "Sebastián",
            "last_name": "Rodríguez"
        }
        return [candidate]

    def create(self, infoCandidate):
        print("Crear candidato")
        candidate = Candidate(infoCandidate)
        return candidate.__dict__
        
    def show(self, id):
        print("Dandidato con id", id)

        candidate = {
            "_id": id,
            "dni": "1014176356",
            "resolution_number": "123456",
            "name": "Sebastián",
            "last_name": "Rodríguez"
        }
        return candidate
    
    def update(self, id, infoCandidate):
        print("Actualizando el candidato con id", id)
        candidate = Candidate(infoCandidate)
        return candidate.__dict__

    def delete(self, id):
        print("Eliminando el candidato con id", id)
        return {"deleted_count": 1}

    