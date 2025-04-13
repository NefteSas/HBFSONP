import json
import os

DATABASE_PATH = "database"

class Monument():
    def __init__(self, _id: int, _name: str, _description: str = None, _position_stupid: str = None, _GPSPosition: tuple[float, float] = None, _x: float = None, _y: float = None):
        self.id = _id
        self.name = _name
        self.description = _description
        self.position_stupid = _position_stupid
        if (_GPSPosition is not None or (_x is not None and _y is not None)):
            if (_GPSPosition):
                self.GPSPosition = _GPSPosition
            else:
                self.GPSPosition = (_x, _y)
        else:
            raise ValueError("GIVE ARGS FOR MONUMENT CLASS")
        
    def __str__(self) -> str:
        return f"--------- \n ID: {self.id} \n ---------"

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
                'GPSPOS': monumentObject.getGPSPosition
            }
        else:
            raise TypeError(f"WANTED MONUMENT TYPE. GETTED {type(o)}")
        
class MonumentDecoder(json.JSONDecoder):
    @staticmethod
    def from_dict(monumentJSON: dict):
        if (monumentJSON.get("__name__") == Monument.__name__):
            return Monument(
                _id = monumentJSON['ID'],
                _name = monumentJSON['NAME'],
                _description = monumentJSON['DESCRIPTION'],
                _position_stupid = monumentJSON['POSSTUPID'],
                _GPSPosition = monumentJSON['GPSPOS']
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
                return json.load(monumentFS, cls=MonumentDecoder)
        else:
            raise FileNotFoundError()
        
    def ReadMonumentByID(self, id) -> Monument:
        return self.ReadMonumentFile(f"{DATABASE_PATH}/{id}.monument")

            
if (__name__ == '__main__'):
    DB = MonumentsDatabase()
    try:
        DB.CreateMonumentFile(Monument(1, "Z", _x = 0, _y = 0))
    except FileExistsError:
        print(DB.ReadMonumentByID(1))
