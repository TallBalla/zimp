from Commands import Commands
from Database import Database

if __name__ == "__main__":
    Database().connect_to_database()
    Commands().cmdloop()
