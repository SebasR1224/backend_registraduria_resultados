from Repositories.InterfaceRepository import InterfaceRepository
from Models.Result import Result

from bson import ObjectId

class ResultRepository (InterfaceRepository[Result]):

    def voteList(self, id_table):

        pipeline = [
                        {
                            '$lookup': {
                                'from': 'candidate', 
                                'localField': 'candidate.$id', 
                                'foreignField': '_id', 
                                'as': 'c'
                            }
                        }, {
                            '$lookup': {
                                'from': 'votingtable', 
                                'localField': 'votingTable.$id', 
                                'foreignField': '_id', 
                                'as': 'v'
                            }
                        }, {
                            '$replaceRoot': {
                                'newRoot': {
                                    '$mergeObjects': [
                                        {
                                            '$arrayElemAt': [
                                                '$c', 0
                                            ]
                                        }, '$$ROOT'
                                    ]
                                }
                            }
                        }, {
                            '$lookup': {
                                'from': 'politicalparty', 
                                'localField': 'politicalParty.$id', 
                                'foreignField': '_id', 
                                'as': 'p'
                            }
                        }, {
                            '$project': {
                                'name_candidate': {
                                    '$arrayElemAt': [
                                        '$c.name', 0
                                    ]
                                }, 
                                'lastName_candidate': {
                                    '$arrayElemAt': [
                                        '$c.last_name', 0
                                    ]
                                }, 
                                'total_votes': '$total_votes', 
                                'numer_table': {
                                    '$arrayElemAt': [
                                        '$v.number_table', 0
                                    ]
                                }, 
                                'name_politicalParty': {
                                    '$arrayElemAt': [
                                        '$p.name', 0
                                    ]
                                }
                            }
                        }
                    ]
        if(id_table != None):
            pipeline.insert(0, {"$match": {"votingTable.$id": ObjectId(id_table)}})    
        return self.queryAggregation(pipeline)

    def getVotesCandidates(self, id_table):
        pipeline = [
            {
                '$lookup': {
                    'from': 'candidate', 
                    'localField': 'candidate.$id', 
                    'foreignField': '_id', 
                    'as': 'c'
                }
            }, {
                '$lookup': {
                    'from': 'votingtable', 
                    'localField': 'votingTable.$id', 
                    'foreignField': '_id', 
                    'as': 'v'
                }
            }, {
                '$replaceRoot': {
                    'newRoot': {
                        '$mergeObjects': [
                            {
                                '$arrayElemAt': [
                                    '$c', 0
                                ]
                            }, '$$ROOT'
                        ]
                    }
                }
            }, {
                '$lookup': {
                    'from': 'politicalparty', 
                    'localField': 'politicalParty.$id', 
                    'foreignField': '_id', 
                    'as': 'p'
                }
            }, {
                '$group': {
                    '_id': '$candidate.$id', 
                    'total_votes': {
                        '$sum': '$total_votes'
                    }, 
                    'name_candidate': {
                        '$first': {
                            '$arrayElemAt': [
                                '$c.name', 0
                            ]
                        }
                    }, 
                    'lastName_candidate': {
                        '$first': {
                            '$arrayElemAt': [
                                '$c.last_name', 0
                            ]
                        }
                    }, 
                    'numer_table': {
                        '$first': {
                            '$arrayElemAt': [
                                '$v.number_table', 0
                            ]
                        }
                    }, 
                    'name_politicalParty': {
                        '$first': {
                            '$arrayElemAt': [
                                '$p.name', 0
                            ]
                        }
                    }
                }
            }, {
                '$sort': {
                    'total_votes': -1
                }
            }
        ]
        if(id_table != None):
            pipeline.insert(0, {"$match": {"votingTable.$id": ObjectId(id_table)}})
            
        return self.queryAggregation(pipeline)

    def totalVotesTable(self):
        pipeline =  [
                        {
                            '$lookup': {
                                'from': 'votingtable', 
                                'localField': 'votingTable.$id', 
                                'foreignField': '_id', 
                                'as': 'v'
                            }
                        }, {
                            '$group': {
                                '_id': '$votingTable.$id', 
                                'numer_table': {
                                    '$first': {
                                        '$arrayElemAt': [
                                            '$v.number_table', 0
                                        ]
                                    }
                                }, 
                                'total_votes': {
                                    '$sum': '$total_votes'
                                }, 
                                'registered_documents': {
                                    '$first': {
                                        '$arrayElemAt': [
                                            '$v.registered_documents', 0
                                        ]
                                    }
                                }
                            }
                        }, {
                            '$sort': {
                                'total_votes': -1
                            }
                        }
                    ]
        return self.queryAggregation(pipeline)
    
    def totalVotesPoliticalParty(self, id_table):
        pipeline = [
                        {
                            '$lookup': {
                                'from': 'candidate', 
                                'localField': 'candidate.$id', 
                                'foreignField': '_id', 
                                'as': 'c'
                            }
                        }, {
                            '$replaceRoot': {
                                'newRoot': {
                                    '$mergeObjects': [
                                        {
                                            '$arrayElemAt': [
                                                '$c', 0
                                            ]
                                        }, '$$ROOT'
                                    ]
                                }
                            }
                        }, {
                            '$lookup': {
                                'from': 'politicalparty', 
                                'localField': 'politicalParty.$id', 
                                'foreignField': '_id', 
                                'as': 'p'
                            }
                        }, {
                            '$group': {
                                '_id': '$politicalParty.$id', 
                                'total_votes': {
                                    '$sum': '$total_votes'
                                }, 
                                'name_politicalParty': {
                                    '$first': {
                                        '$arrayElemAt': [
                                            '$p.name', 0
                                        ]
                                    }
                                }
                            }
                        }, {
                            '$sort': {
                                'total_votes': -1
                            }
                        }
                    ]
        if(id_table != None):
            pipeline.insert(0, {"$match": {"votingTable.$id": ObjectId(id_table)}})
            
        return self.queryAggregation(pipeline)   

    def percentageCongress(self):

        pipeline =  [
                        {
                            '$lookup': {
                                'from': 'candidate', 
                                'localField': 'candidate.$id', 
                                'foreignField': '_id', 
                                'as': 'c'
                            }
                        }, {
                            '$replaceRoot': {
                                'newRoot': {
                                    '$mergeObjects': [
                                        {
                                            '$arrayElemAt': [
                                                '$c', 0
                                            ]
                                        }, '$$ROOT'
                                    ]
                                }
                            }
                        }, {
                            '$lookup': {
                                'from': 'politicalparty', 
                                'localField': 'politicalParty.$id', 
                                'foreignField': '_id', 
                                'as': 'p'
                            }
                        }, {
                            '$sort': {
                                'total_votes': -1
                            }
                        }, {
                            '$limit': 15
                        }, {
                            '$group': {
                                '_id': None, 
                                'sum': {
                                    '$sum': '$total_votes'
                                }, 
                                'political': {
                                    '$push': {
                                        '_id': {
                                            '$arrayElemAt': [
                                                '$p._id', 0
                                            ]
                                        }, 
                                        'name': {
                                            '$arrayElemAt': [
                                                '$p.name', 0
                                            ]
                                        }, 
                                        'total_votes': '$total_votes'
                                    }
                                }
                            }
                        }, {
                            '$unwind': {
                                'path': '$political'
                            }
                        }, {
                            '$project': {
                                '_id': '$political._id', 
                                'name': '$political.name', 
                                'votes': '$political.total_votes', 
                                'sum': '$sum', 
                                'percent': {
                                    '$multiply': [
                                        {
                                            '$divide': [
                                                '$political.total_votes', '$sum'
                                            ]
                                        }, 100
                                    ]
                                }
                            }
                        }, {
                            '$group': {
                                '_id': '$_id', 
                                'name': {
                                    '$first': '$name'
                                }, 
                                'sum': {
                                    '$first': '$sum'
                                }, 
                                'total_votes': {
                                    '$sum': '$votes'
                                }, 
                                'percent': {
                                    '$sum': '$percent'
                                }
                            }
                        }, {
                            '$sort': {
                                'percent': -1
                            }
                        }
                    ]
        return self.queryAggregation(pipeline)   