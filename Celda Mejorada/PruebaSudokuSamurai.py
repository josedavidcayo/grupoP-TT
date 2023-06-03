class Celda():
    def __init__(self):
        self.valor=" "
    
    #rellena la celda
    def set_celda(self,dato):
        self.valor=dato
        
    #vacia la celda
    def borrar_celda(self):
        self.valor=" "
        
    def get_celda(self):
        return self.valor
    
