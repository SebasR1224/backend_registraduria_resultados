import collections
from re import X
from turtle import update
import pymongo
import certifi
from bson import DBRef
from bson.objectid import ObjectId
from typing import Collection, TypeVar, Generic, get_args
import json

T = TypeVar('T')
class InterfaceRepository(Generic[T]):

    #Constructor
    def __init__(self) -> None:
        ca = certifi.where()
        configData = self.loadFileConfig()
        client = pymongo.MongoClient(configData["data-db-connection"], tlsCAFile=ca)
        self.database = client[configData["name-db"]]
        theClass = get_args(self.__orig_bases__[0])
        self.collection = theClass[0].__name__.lower()
    
    def loadFileConfig(self):
        with open('config.json') as f:
            data = json.load(f)
        return data

    def save(self, item: T):
        collection = self.database[self.collection]
        id = ""
        item = self.transformRefs(item)
        if hasattr(item, "_id") and item._id != "":
            id = item._id
            _id = ObjectId(id)
            delattr(item, "_id")            
            item = item.__dict__
            updateItem = {"$set": item}
            x = collection.update_one({"_id": _id}, updateItem)
        else:
            _id = collection.insert_one(item.__dict__)
            id = _id.inserted_id.__str__()
        
        x = collection.find_one({"_id": ObjectId(id)})
        x["_id"] = x["_id"].__str__()
        return self.findById(id)

    def delete(self, id):
        collection = self.database[self.collection]
        count = collection.delete_one({"_id": ObjectId(id)}).deleted_count
        return {"deleted_count": count}

    def update(self, id, item: T):
        collection = self.database[self.collection]
        delattr(item, "_id")
        item = item.__dict__
        updateItem = {"$set": item}
        x = collection.update_one({"_id": ObjectId(id)}, updateItem)
        return {"updated_count": x.matched_count}
    
    def findById(self, id) :
        collection = self.database[self.collection]
        x = collection.find_one({"_id": ObjectId(id)})
        x = self.getValuesDBRef(x)
        if x ==None:
            x = {}
        else:
            x["_id"] = x["_id"].__str__()
        return x

    def findAll(self):
        collection = self.database[self.collection]
        data = []
        for x in collection.find():
            x["_id"] = x["_id"].__str__()
            x = self.transformObjectIds(x)
            x = self.getValuesDBRef(x)
            data.append(x)
        return data
    
    def query(self, query):
        collection = self.database[self.collection]
        data = []
        for x in collection.find(query):
            x["_id"] = x["_id"].__str__()
            x = self.transformObjectIds(x)
            x = self.getValuesDBRef(x)
            data.append(x)
        return data

    def queryAggregation(self, query):
        collection = self.database[self.collection]
        data = []
        for x in collection.aggregate(query):
            x["_id"] = x["_id"].__str__()
            x = self.transformObjectIds(x)
            x = self.getValuesDBRef(x)
            data.append(x)
        return data
    
    def getValuesDBRef(self, x):
        for key in x.keys():
            if isinstance(x[key], DBRef):
                collection = self.database[x[key].collection]
                value = collection.find_one({"_id": ObjectId(x[key].id)})
                value["_id"] = value["_id"].__str__()
                x[key] = value
                x[key] = self.getValuesDBRef(x[key])
            elif isinstance(x[key], list) and len(x[key]) > 0:
                x[key] = self.getValuesDBRefFromList(x[key])
            elif isinstance(x[key], dict):
                x[key] = self.getValuesDBRef(x[key])
        return x
    
    def getValuesDBRefFromList(self, theList):
        newList = []
        collection = self.database[theList[0]._id.collection]
        for item in theList:
            value = collection.find_one({"_id": ObjectId(item.id)})
            value["_id"] = value["_id"].__str__()
            newList.append(value)
        return newList

    def transformObjectIds(self, x):
        for attribute in x.keys():
            if isinstance(x[attribute], ObjectId):
                x[attribute] = x[attribute].__str__()
            elif isinstance(x[attribute], list):
                x[attribute] = self.formatList(x[attribute])
            elif isinstance(x[attribute], dict):
                x[attribute]=self.transformObjectIds(x[attribute])
        return x         

    def formatList(self, x):
        newList = []
        for item in x:
            if isinstance(item, ObjectId):
                newList.append(item.__str__())
        if len(newList) == 0:
            newList = x
        return newList
    
    def transformRefs(self, item):
        theDict = item.__dict__
        keys = list(theDict.keys())
        for key in keys:
            if theDict[key].__str__().count("object") == 1:
                newObject = self.ObjectToDBRef(getattr(item, key))
                setattr(item, key, newObject)
        return item

    def ObjectToDBRef(self, item: T):
        nameCollection = item.__class__.__name__.lower()
        return DBRef(nameCollection, ObjectId(item._id))