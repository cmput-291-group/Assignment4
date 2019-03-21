import pandas
import folium


class UI:
    def __init__(self):
        pass
    
    def run(self):
        while True:
            choice = self.showMainMenu()
            if choice == '1':
                pass
            elif choice == '2':
                pass
            elif choice == '3':
                pass
            elif choice == '4':
                pass
            elif choice.lower() == 'e':
                break
            else:
                print("Choice is invalid")            
    
    def showMainMenu(self):
        print("Please make a selection")
        options = ["1: Q1","2: Q2","3: Q3","4: Q4","E: Exit"]
        for option in options:
            print(option)
        choice = input("Enter your choice: ")
        return choice
    
    
class Database:
    def __init__(self):
        self.db_path = 'a4-sampled.db'
        self.connection = sqlite3.connect(self.db_path)
        self.cursor = self.connection.cursor()        
    
    def getCrimeByMonth(self,crimeType):
        query = '''SELECT Month,Count(*) as number
                   FROM crime_incidents
                   WHERE Crime_Type = '{}'
                   GROUP BY Month'''.format(crimeType)
        
        
        



if __name__ == "__main__":
    ui = UI()
    ui.run()