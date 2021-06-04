class pengguna :
    def __init__(self,id,password=None):
        self.__ID = id

    def cus_id (self) :
        return self.__ID

    def info (self):
        print("Ini adalah Admin dengan USERNAME",self.__ID)
        
class customer(pengguna) :
    def __init__(self,Customer_id,password):
        super().__init__(Customer_id)
        self.__pass = password


    def info (self):
        print("Ini adalah custmer dengan ID",self.cus_id())

class admin(pengguna) :
     def __init__(self,Admin_id):
        super().__init__(Admin_id)

    
    

   
