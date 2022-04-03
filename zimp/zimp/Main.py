from Commands import Commands
from Database import Database
     
if __name__ == "__main__":
    #db = Database("zimp")
    
    #db.drop_table("tiles")
    #db.drop_table("devcards")
    
    #db.create_devcards()
    #db.create_tiles()

    #print(db.select_data("devcards")[0][0])
    #print()
    #print(db.select_data("tiles"))
        
    Commands().cmdloop()
