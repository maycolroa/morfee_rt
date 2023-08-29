# from django.conf import settings
from morfee_rt_dev.settings import CUSTOM_URI_MONGO, CUSTOM_DB_MONGO
from pymongo import MongoClient, DeleteOne, InsertOne, UpdateOne
from bson.json_util import dumps
import math

class Mongo:

    def __init__(self, colect=None, db=None):
        self.isConnect = False
        self.cliente = None
        self.coleccion = colect
        self.dbase = CUSTOM_DB_MONGO if db == None else db
        self.conectar()

    def conectar(self):
        try:
            self.cliente = MongoClient(CUSTOM_URI_MONGO)
            self.isConnect = True
        except:
            self.cliente = None
            self.isConnect = False

    def getCliente(self, colect=None):
        if colect != None:
            self.coleccion = colect
        if self.coleccion == None:
            return self.cliente[self.dbase]
        else:
            return self.cliente[self.dbase][self.coleccion]

    def find(self, filtro={}, page=0, cantidad=100, attach=None, pro=None, orden=None):
        if page > 0:
            salto = cantidad * (page - 1)
            datos = self.getCliente().find(filtro, projection=pro).skip(salto).limit(cantidad)
            rs = dumps({'attach': attach, 'datos': datos}) if attach != None else dumps(datos)
            self.cliente.close()
            return rs
        else:
            datos = self.getCliente().find(filtro, projection=pro, sort=orden)
            rs = dumps({'attach': attach, 'datos': datos}) if attach != None else dumps(datos)
            self.cliente.close()
            return rs

    def findPaginate(self, filtro={}, pagina=1, cantidad=100, calcular=True):
        salto = cantidad * (pagina - 1)
        datos = self.getCliente().find(filtro).skip(salto).limit(cantidad)
        total = -1
        if calcular:
            try:
                total = self.getCliente().find(filtro).count()
            except:
                total = -1
        paginas = -1 if calcular == False else math.ceil(total / cantidad)
        self.cliente.close()
        calculado = 'yes' if calcular else 'no'
        return dumps({'datos': datos, 'pagina_actual': pagina, 'total': total, 'paginas': paginas, 'calculado': calculado}, allow_nan=False)

    def findOne(self, filtro, pro=None, raw=False):
        dato = self.getCliente().find_one(filtro, projection=pro)
        if raw:
            return dato
        else:
            return dumps(dato)

    def insertOne(self, doc):
        if self.isConnect:
            try:
                mnu = self.getCliente().insert_one(doc)
                self.cliente.close()
                return mnu
            except:
                return False
        else:
            return False

    def insertMany(self, docs):
        if self.isConnect:
            try:
                mnu = self.getCliente().insert_many(docs)
                self.cliente.close()
                return mnu
            except:
                return False
        else:
            return False

    def insertManyChunk(self, docs):
        if self.isConnect:
            try:
                mnu = self.getCliente().insert_many(docs, False)
                return len(mnu.inserted_ids)
            except:
                return 0
    
    def updateMany(self, filtro, campo):
        if self.isConnect:
            try:
                mnu = self.getCliente().update_many(filtro, campo)
                return mnu.modified_count
            except:
                return 0

    def updateOne(self, filtro, cambios, newdoc=False, operation="$set"):
        if self.isConnect:
            try:
                mnu = self.getCliente().update_one(filtro, {operation: cambios}, newdoc)
                return True
            except:
                return False
    
    def deleteOne(self, filtro):
        if self.isConnect:
            try:
                mnu = self.getCliente().delete_one(filtro)
                return True
            except:
                return False
    
    def deleteMany(self, filtro):
        if self.isConnect:
            try:
                mnu = self.getCliente().delete_many(filtro)       # SUGGEST
                return True
            except:
                return False

    def aggregate(self, arr):
        if self.isConnect:
            try:
                dato = self.getCliente().aggregate(arr)
                self.cliente.close()
                return dumps(dato)
            except:
                return dumps([])
    
    def distinct(self, key):
        if self.isConnect:
            try:
                dato = self.getCliente().distinct(key)
                self.cliente.close()
                return dumps(dato)
            except:
                return dumps([])

    def removeImport(self, ctr):
        if self.isConnect:
            # mnu = self.getCliente().remove({'ctr': ctr})          # DEPRECATED
            mnu = self.getCliente().delete_many({'ctr': ctr})       # SUGGEST
            self.cliente.close()
            return True
        else:
            return False
    
    def bulkWrite(self):
        pass

    def pageCount(self, filtro={}, memory=None):
        total = 0
        if(memory == None):
            total = self.getCliente().find(filtro).count()
        else:
            total = memory
        return total

    def dumps(self, arg):
        return dumps(arg)

    def close(self):
        self.cliente.close()
    
    def Index(self,arg):
        if self.isConnect:
            try:
                dato = self.getCliente().index_information()
                self.cliente.close()
                return dumps(dato)
            except:
                return dumps([])
                
    def OpcionIndex(self, arg, opt):
        indexes =  arg.split(',')
        dato = 0
        if self.isConnect:
            try:
                for x in indexes:
                    if opt == 'add':
                        if self.getCliente().create_index(x):
                            dato = dato + 1
                    if opt == 'drop':
                        if self.getCliente().drop_index(x+'_1'):
                            dato = dato + 1
                self.cliente.close()
                return dato
            except:
                return dato
        else:
            return dato
            
    def listarColecciones(self):
        dato = self.getCliente().list_collection_names()
        return dumps(dato)
    
          

        
