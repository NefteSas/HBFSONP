import json
import os
import re

DATABASE_PATH = "database"

class Monument():
    def __init__(self, _id: int
                 , _name: str
                 , _description: str = None
                 , _position_stupid: str = None
                 , _GPSPosition: tuple[float, float] = None
                 , _latitude: float = None
                 , _longitude: float = None,
                 _url: str = None,
                 _img: str = None):
        self.id = _id
        self.name = _name
        self.description = _description
        self.position_stupid = _position_stupid
        self.url = _url
        self.img = _img
        if (_GPSPosition is not None or (_latitude is not None and _longitude is not None)):
            if (_GPSPosition):
                self.GPSPosition = _GPSPosition
            else:
                self.GPSPosition = (_latitude, _longitude)
        else:
            raise ValueError("GIVE ARGS FOR MONUMENT CLASS")
        
    def __str__(self) -> str:
        return f"----ID: {self.id}----- \nNAME: {self.name} \nPOS: {self.position_stupid} \nGPS: {self.GPSPosition} \n"

    @property
    def getName(self):
        return self.name
    
    @property
    def getID(self):
        return self.id
    
    @property
    def getDescription(self) -> str:
        return self.description
    
    @property
    def getStupidPosition(self) -> str:
        return self.position_stupid
    
    @property
    def getGPSPosition(self) -> tuple[float, float]:
        return self.GPSPosition
    
    @property
    def getURL(self) -> str:
        return self.url
    
    @property
    def getIMG(self) -> str:
        return self.img
    
class MonumentsEncoder(json.JSONEncoder):
    @staticmethod
    def default(monumentObject: Monument):
        if isinstance(monumentObject, Monument):
            return {
                '__name__': type(monumentObject).__name__,
                'ID': monumentObject.getID,
                'NAME': monumentObject.getName,
                'DESCRIPTION': monumentObject.getDescription,
                'POSSTUPID': monumentObject.getStupidPosition,
                'GPSPOS': monumentObject.getGPSPosition,
                'URL': monumentObject.getURL,
                'IMG': monumentObject.getIMG
            }
        else:
            raise TypeError(f"WANTED MONUMENT TYPE. GETTED {type(monumentObject)}")
        
class MonumentDecoder(json.JSONDecoder):
    @staticmethod
    def from_dict(monumentJSON: dict):
        if (monumentJSON.get("__name__") == Monument.__name__):
            return Monument(
                _id = monumentJSON['ID'],
                _name = monumentJSON['NAME'],
                _description = monumentJSON['DESCRIPTION'],
                _position_stupid = monumentJSON['POSSTUPID'],
                _GPSPosition = monumentJSON['GPSPOS'],
                _url = monumentJSON['URL'],
                _img = monumentJSON['IMG'] if 'IMG' in monumentJSON.keys() else None,
            )
        else:
            raise json.JSONDecodeError('FAILED')

class MonumentsDatabase():
    def __init__(self):
        if (os.path.exists(DATABASE_PATH)):
            print('VIEWED DATABASEPATH')
        else:
            print('DATABASE PATH IS NULL. GENERATING.')
            os.mkdir(DATABASE_PATH)    
    
    def CreateMonumentFile(self, monument: Monument):
        if (not os.path.exists(f"{DATABASE_PATH}/{monument.getID}.monument")):
            with open(f"{DATABASE_PATH}/{monument.getID}.monument", 'w') as monumentFS:
                json.dump(obj=monument, cls=MonumentsEncoder, fp=monumentFS)
        else:
            raise FileExistsError(f"{DATABASE_PATH}/{monument.getID}.monument is already created" )
        
    def ReadMonumentFile(self, path: str) -> Monument:
        if (os.path.exists(path)):
            with open(path, "r") as monumentFS:
                return MonumentDecoder.from_dict(json.load(monumentFS))
        else:
            raise FileNotFoundError()
        
    def ReadMonumentByID(self, id) -> Monument:
        return self.ReadMonumentFile(f"{DATABASE_PATH}/{id}.monument")

    def UpdateMonumentSaveByIDByClass(self, id: int, newMonumentum: Monument):
        
        if (os.path.exists(f"{DATABASE_PATH}/{newMonumentum.getID}.monument")):
            with open(f"{DATABASE_PATH}/{newMonumentum.getID}.monument", 'w') as monumentFS:
                json.dump(obj=newMonumentum, cls=MonumentsEncoder, fp=monumentFS)
        else:
            self.CreateMonumentFile(newMonumentum)

    def UpdateMonumentSaveByID(self, id: int, name: str=None, desc: str=None, _stupid_pos: str=None, gpsPos: tuple[float, float]=None, url: str=None,img: str = None):
        oldMonument: Monument = self.ReadMonumentByID(id=id)
        newMonument = Monument(id, _name=name if name is not None else oldMonument.getName,
        _description=desc if desc is not None else oldMonument.getDescription,
        _position_stupid=_stupid_pos if _stupid_pos is not None else oldMonument.getStupidPosition,
        _GPSPosition=gpsPos if gpsPos is not None else oldMonument.GPSPosition,
        _url=url if url is not None else oldMonument.getURL,
        _img=img if img is not None else oldMonument.getIMG)
        
        self.UpdateMonumentSaveByIDByClass(id=id, newMonumentum=newMonument)

    def GetUniqueID(self) -> int:
        maxid = 0
        
        for id in self.GetIDS():
            maxid = max(id, maxid)
            
        return maxid + 1
    
    def GetIDS(self) -> list[int]:
        list = self.__GetListOfFilesInDB()
        buffer = []
        for file in list:
            buffer.append(int(re.sub(pattern="\D",string=file,repl='')))
        
        return buffer
            
    def __GetListOfFilesInDB(self) -> list:
        return os.listdir(DATABASE_PATH + "/")
    

    
if (__name__ == '__main__'):
    DB = MonumentsDatabase()
    print(DB.GetUniqueID())

        
    DB.UpdateMonumentSaveByID(1, name="AG")
