import pandas as pd
import folium
import sqlite3
import matplotlib.pyplot as plt
import tkinter as tk
import webbrowser


class UI:
    def __init__(self,root):
        # init all instance attributes
        
        self.db = Database()
        # get GUI root
        self.win = root
        self.win.title("Crime Stats")
        # counters for naming purpose when saving results
        self.Q1Counter = 0
        self.Q2Counter = 0
        self.Q3Counter = 0
        self.Q4Counter = 0

    def run(self):
        self.buildMainMenu()    
    
    def clearRoot(self):
        # clear the window of the current frame
        
        for el in root.winfo_children():
            el.destroy()
            
    def buildFrame(self,contents):
        # adds contents to parent frame
        # contents is a list of UI elements
        
        for item in contents:
            # pack from the top down
            item.pack(side="top")
    
    def buildMainMenu(self):
        # builds the main menu UI
        
        # clear window
        self.clearRoot()
        # delcare a frame to hold menu contents
        self.mainFrame = tk.Frame(self.win)
        self.mainFrame.pack(expand=True,fill="both")
        # add top label
        prompt = "Please make a selection"
        self.mainLabel = tk.Label(self.mainFrame,text=prompt)
        # define main menu buttons
        self.Q1Button = tk.Button(self.mainFrame,text="1: Q1",command=lambda: self.buildBarPlotMenu())
        self.Q2Button = tk.Button(self.mainFrame,text="2: Q2",command=lambda: self.buildQ2Menu())
        self.Q3Button = tk.Button(self.mainFrame,text="3: Q3",command=lambda: self.buildQ3Menu())
        self.Q4Button = tk.Button(self.mainFrame,text="4: Q4",command=lambda: self.buildQ4Menu())
        # build the frame
        self.mainMenuContents = [self.mainLabel,self.Q1Button,self.Q2Button,self.Q3Button,self.Q4Button]
        self.buildFrame(self.mainMenuContents)

    def getbpEntries(self):
        # retrieves and validates the user input, and generates the bar plot
        
        try:
            # get the user input
            lower = int(self.beLowerText.get())
            upper = int(self.beUpperText.get())
            # get a list of all acceptable crime types
            cTypes = self.db.getCrimeTypes()
            crime = self.beCrimeText.get()
            
            # check for valid crime type
            if not crime in cTypes.values:
                raise ValueError
            
            # current menu is no longer needed, recreate main menu
            self.buildMainMenu()
            
            # get crime frequencies
            data = self.db.getCrimeByMonth(crime,lower,upper)
            if data.empty:
                raise ValueError
            
            # plot graph and save png to local folder
            plot = data.plot.bar(x="Month")
            plt.plot()
            self.Q1Counter += 1
            plt.savefig("Q1-{}.png".format(self.Q1Counter))            
            plt.show() 
        
        # alert the user to invalid input    
        except ValueError:
            tk.messagebox.showerror("Error","Invalid input given")

    def buildBarPlotMenu(self):
        # builds the bar plot menu UI
        
        # clear window
        self.clearRoot()
        # declare new frame
        self.barEntryFrame = tk.Frame(self.win)
        self.barEntryFrame.pack(expand=True,fill="both")
        # add top label
        prompt = "Enter a year range and crime type"
        self.topLabel = tk.Label(self.barEntryFrame,text=prompt)
        # add text entry boxes with labels for all needed information
        self.beUpperLabel = tk.Label(self.barEntryFrame,text="Year Upper Bound:")
        self.beUpperText = tk.Entry(self.barEntryFrame)
        self.beLowerLabel = tk.Label(self.barEntryFrame,text="Year Lower Bound")
        self.beLowerText = tk.Entry(self.barEntryFrame)
        self.beCrimeLabel = tk.Label(self.barEntryFrame,text="Crime Type")
        self.beCrimeText = tk.Entry(self.barEntryFrame)
        # add confirm button
        self.beConfirm = tk.Button(self.barEntryFrame,text="Confirm",command=lambda: self.getbpEntries())
        # build frame
        self.beMenuContents = [self.topLabel,self.beUpperLabel,self.beUpperText,
                               self.beLowerLabel,self.beLowerText,self.beCrimeLabel,
                               self.beCrimeText,self.beConfirm]
        self.buildFrame(self.beMenuContents)

    def buildQ2Menu(self):
        # builds Q2 menu UI

        # clear window
        self.clearRoot()
        # declare a new frame
        self.Q2EntryFrame = tk.Frame(self.win)
        self.Q2EntryFrame.pack(expand=True, fill="both")
        # add top label
        prompt = "Enter a number of neighbourhoods"
        self.Q2topLabel = tk.Label(self.Q2EntryFrame, text=prompt)
        self.Q2NText = tk.Entry(self.Q2EntryFrame)
        # add confirm button
        self.Q2Confirm = tk.Button(self.Q2EntryFrame, text="Confirm", command=lambda: self.getQ2Entries())
        # build the menu
        self.Q2MenuContents = [self.Q2topLabel, self.Q2NText, self.Q2Confirm]
        self.buildFrame(self.Q2MenuContents)

    def getQ2Entries(self):
        # get the user input then render and output the map

        try:
            # get user input
            N = int(self.Q2NText.get())
            # init the map
            m = folium.Map(location=[53.5444, -113.323], zoom_start=11)

            # get top N areas in the given range
            data = self.db.getQ2Info(N)
            #if data.empty:
                #raise ValueError

                # add a circle on the map for every area of interest
            for i in range(N*2):
                row = data.iloc[i]
                name = row["name"]
                population = int(row["popNum"])
                long = float(row["long"])
                lat = float(row["lat"])
                # create and add the circle to the map
                folium.Circle(
                    location=[lat, long],
                    popup="{} <br> {}".format(name, population),
                    radius= population/10 + 1,
                    fill=True,
                    fill_color='crimson'
                ).add_to(m)

            # save the hmtl to the local folder
            self.Q2Counter += 1
            filename = "Q2-{}.html".format(self.Q2Counter)
            m.save(filename)
            # open map in default web browser
            webbrowser.open(filename, new=2)
            # return to main menu
            self.buildMainMenu()

        except ValueError:
            tk.messagebox.showerror("Error", "Invalid input given")

    def buildQ3Menu(self):
        # builds Q4 menu UI

        # clear window
        self.clearRoot()
        # declare a new frame
        self.Q3EntryFrame = tk.Frame(self.win)
        self.Q3EntryFrame.pack(expand=True, fill="both")
        # add top label
        prompt = "Enter a year range, crime type, and number of neighbourhoods"
        self.Q3topLabel = tk.Label(self.Q3EntryFrame, text=prompt)
        # add text entry fields with labels
        self.Q3UpperLabel = tk.Label(self.Q3EntryFrame, text="Year Upper Bound:")
        self.Q3UpperText = tk.Entry(self.Q3EntryFrame)
        self.Q3LowerLabel = tk.Label(self.Q3EntryFrame, text="Year Lower Bound")
        self.Q3LowerText = tk.Entry(self.Q3EntryFrame)
        self.Q3NLabel = tk.Label(self.Q3EntryFrame, text="Top N Neighborhoods")
        self.Q3NText = tk.Entry(self.Q3EntryFrame)
        self.Q3CrimeLabel = tk.Label(self.Q3EntryFrame,text="Crime Type")
        self.Q3CrimeText = tk.Entry(self.Q3EntryFrame)
        # add confirm button
        self.Q3Confirm = tk.Button(self.Q3EntryFrame, text="Confirm", command=lambda: self.getQ3Entries())
        # build the menu
        self.Q3MenuContents = [self.Q3topLabel, self.Q3UpperLabel, self.Q3UpperText,
                               self.Q3LowerLabel, self.Q3LowerText, self.Q3NLabel,
                               self.Q3NText, self.Q3CrimeLabel, self.Q3CrimeText, self.Q3Confirm]
        self.buildFrame(self.Q3MenuContents)

    def getQ3Entries(self):
        # get the user input then render and output the map

        try:
            # get user input
            lower = int(self.Q3LowerText.get())
            upper = int(self.Q3UpperText.get())
            N = int(self.Q3NText.get())
            cTypes = self.db.getCrimeTypes()
            crime = self.Q3CrimeText.get()
            # check for valid crime type
            if crime not in cTypes.values:
                raise ValueError

            # init the map
            m = folium.Map(location=[53.5444, -113.323], zoom_start=11)

            # get top N areas in the given range
            data = self.db.getQ3Info(upper, lower, N, crime)
            if data.empty:
                raise ValueError

                # add a circle on the map for every area of interest
            for i in range(N):
                row = data.iloc[i]
                name = row["name"]
                crime_sum = int(row["sum"])
                long = float(row["long"])
                lat = float(row["lat"])
                # create and add the circle to the map
                folium.Circle(
                    location=[lat, long],
                    popup="{} <br> {}".format(name, crime_sum),
                    radius=crime_sum,
                    fill=True,
                    fill_color="crimson"
                ).add_to(m)

            # save the hmtl to the local folder
            self.Q3Counter += 1
            filename = "Q3-{}.html".format(self.Q3Counter)
            m.save(filename)
            # open map in default web browser
            webbrowser.open(filename, new=2)
            # return to main menu
            self.buildMainMenu()

        except ValueError:
            tk.messagebox.showerror("Error", "Invalid input given")

    def buildQ4Menu(self):
        # builds Q4 menu UI
        
        # clear window
        self.clearRoot()
        # declare a new frame
        self.Q4EntryFrame = tk.Frame(self.win)
        self.Q4EntryFrame.pack(expand=True,fill="both")
        # add top label
        prompt = "Enter a year range and number of neighbourhoods"
        self.Q4topLabel = tk.Label(self.Q4EntryFrame,text=prompt)
        # add text entry fields with labels
        self.Q4UpperLabel = tk.Label(self.Q4EntryFrame,text="Year Upper Bound:")
        self.Q4UpperText = tk.Entry(self.Q4EntryFrame)
        self.Q4LowerLabel = tk.Label(self.Q4EntryFrame,text="Year Lower Bound")
        self.Q4LowerText = tk.Entry(self.Q4EntryFrame)
        self.Q4NLabel = tk.Label(self.Q4EntryFrame,text="Top N Neighborhoods")
        self.Q4NText = tk.Entry(self.Q4EntryFrame)
        # add confirm button
        self.Q4Confirm = tk.Button(self.Q4EntryFrame,text="Confirm",command=lambda: self.getQ4Entries())
        # build the menu
        self.Q4MenuContents = [self.Q4topLabel,self.Q4UpperLabel,self.Q4UpperText,
                               self.Q4LowerLabel,self.Q4LowerText,self.Q4NLabel,
                               self.Q4NText,self.Q4Confirm]
        self.buildFrame(self.Q4MenuContents)

    def getQ4Entries(self):
        # get the user input then render and output the map
        
        try:
            # get user input
            lower = int(self.Q4LowerText.get())
            upper = int(self.Q4UpperText.get())
            N = int(self.Q4NText.get())
            # init the map
            m = folium.Map(location=[53.5444,-113.323],zoom_start=11)
            
            # get top N areas in the given range
            data = self.db.getQ4Info(lower,upper,N)
            if data.empty:
                raise ValueError            
            
            # add a circle on the map for every area of interest
            for i in range(N):
                row = data.iloc[i]
                name = row["name1"]
                ratio = float(row["ratio"])
                long = float(row["long"])
                lat = float(row["lat"])
                # get the most common crime for the current area
                commonCrime = self.db.getMostCommonCrimeType(name,lower,upper)["cType"][0]
                # create and add the circle to the map
                folium.Circle(
                    location=[lat,long],
                    popup="{} <br> {} <br> {}".format(name,commonCrime,ratio),
                    radius=3000*ratio,
                    fill=True,
                    fill_color="crimson"
                ).add_to(m)
            
            # save the hmtl to the local folder
            self.Q4Counter += 1
            filename = "Q4-{}.html".format(self.Q4Counter)
            m.save(filename)
            # open map in default web browser
            webbrowser.open(filename,new=2)
            # return to main menu
            self.buildMainMenu()
                    
        except ValueError:
            tk.messagebox.showerror("Error","Invalid input given")
    
    
class Database:
    def __init__(self):
        # init instance variables for database usage
        
        self.db_path = 'a4-sampled.db'
        self.connection = sqlite3.connect(self.db_path)
        self.cursor = self.connection.cursor()        

    def getCrimeByMonth(self,crimeType,lower,upper):
        # get crime frequency by month for a given range of years for a given crime type
        # crimeType is a the crime type of interest
        # lower is the lower bound year
        # upper is the upper bound year
        
        query = '''SELECT Month,Count(CASE WHEN Crime_Type = '{}' THEN 1 ELSE NULL END) as number
                   FROM crime_incidents
                   WHERE Year <= {} AND Year >= {}
                   GROUP BY Month'''.format(crimeType,upper,lower)
        
        result = pd.read_sql_query(query,self.connection)
        return result
    
    def getCrimeTypes(self):
        # gets all possible crime types in the database
        
        query = '''SELECT Crime_Type
                   FROM crime_incidents
                   GROUP BY Crime_Type'''
        result = pd.read_sql_query(query,self.connection)
        return result["Crime_Type"]

    def getQ2Info(self, limit):
        # gets the most and lest populous neighbourhoods
        # limit is the N neighbourhoods for most and lest

        query = '''SELECT population.Neighbourhood_Name as name,(population.CANADIAN_CITIZEN + 
                population.NON_CANADIAN_CITIZEN + population.NO_RESPONSE) as popNum,
                coordinates.Latitude as lat, coordinates.Longitude as long
                FROM population
                INNER JOIN coordinates ON coordinates.Neighbourhood_Name = population.Neighbourhood_Name
                WHERE (lat != 0) AND (popNum != 0) AND ((popNum >= (
                SELECT pop
                FROM (
                    SELECT (population.CANADIAN_CITIZEN + population.NON_CANADIAN_CITIZEN + population.NO_RESPONSE) as pop, coordinates.Latitude as lat, coordinates.Longitude as long
                    FROM population
                    INNER JOIN coordinates ON coordinates.Neighbourhood_Name = population.Neighbourhood_Name
                    WHERE (pop != 0) AND (lat != 0)
                    )
                ORDER BY pop DESC
                LIMIT 1
                OFFSET {}
                )) OR (popNum <= (
                SELECT pop
                FROM (
                    SELECT (population.CANADIAN_CITIZEN + population.NON_CANADIAN_CITIZEN + population.NO_RESPONSE) as pop, coordinates.Latitude as lat, coordinates.Longitude as long
                    FROM population
                    INNER JOIN coordinates ON coordinates.Neighbourhood_Name = population.Neighbourhood_Name
                    WHERE (pop != 0) AND (lat != 0)
                    )
                ORDER BY pop ASC
                LIMIT 1
                OFFSET {}
                )))
                ORDER BY popNum DESC'''.format(limit - 1, limit - 1)

        result = pd.read_sql_query(query, self.connection)

        return result

    def getQ3Info(self, upper, lower, limit, crime):

        query = '''SELECT crime_incidents.Neighbourhood_Name as name, SUM(Incidents_Count) as sum, 
            coordinates.Latitude as lat, coordinates.Longitude as long
            FROM crime_incidents
            INNER JOIN coordinates ON coordinates.Neighbourhood_Name = crime_incidents.Neighbourhood_Name
            WHERE (Year <= {}) AND (Year >= {}) AND (Crime_Type = '{}') AND (lat != 0)
            GROUP BY crime_incidents.Neighbourhood_Name
            HAVING SUM(Incidents_Count) >= 
                (SELECT sum
                FROM (
                    SELECT SUM(crime_incidents.Incidents_Count) as sum, coordinates.Latitude as lat
                    FROM crime_incidents
                    INNER JOIN coordinates ON coordinates.Neighbourhood_Name = crime_incidents.Neighbourhood_Name
                    WHERE (Year <= 2013) AND (Year >= 2011) AND (Crime_Type = 'Assault') AND (lat != 0)
                    GROUP BY crime_incidents.Neighbourhood_Name
                    )
            ORDER BY sum DESC
            LIMIT 1 OFFSET {}
            )
            ORDER BY SUM(Incidents_Count) DESC'''.format(upper, lower, crime, limit - 1)
        result = pd.read_sql_query(query, self.connection)

        return result

    def getQ4Info(self,lower,upper,limit):
        # gets the name, crime to population ratio and coordinates of the top N relevant areas in a given year range
        # lower is the lower bound year
        # upper is the upper bound year
        # limit a number for the top N areas to look at
        
        query = '''SELECT name1, (crimeNum*1.0/popNum) as ratio, c.longitude as long,
                   c.latitude as lat
                   FROM (
                         SELECT Neighbourhood_Name as name1, COUNT(*) as crimeNum
                         FROM crime_incidents
                         WHERE Year <= {} AND Year >= {}
                         GROUP BY Neighbourhood_Name),
                         (SELECT Neighbourhood_Name as name2,(NO_RESPONSE+CANADIAN_CITIZEN+NON_CANADIAN_CITIZEN) as popNum
                         FROM population
                         WHERE popNum != 0
                         GROUP BY Neighbourhood_Name),
                         coordinates c
                    WHERE name1 = name2 AND name1 = c.Neighbourhood_Name
                    AND long != 0 AND lat != 0
                    ORDER BY ratio DESC
                    LIMIT {}'''.format(upper,lower,limit)
        result = pd.read_sql_query(query,self.connection)
        
        return result
    
    
    def getMostCommonCrimeType(self,area,lower,upper):
        # gets the most common crime type for an area in a given year range
        # area is the neighbourhood of interest
        # lower is the lower bound year
        # upper is the upper bound year
        
        query = '''SELECT name,cType,num
                   FROM(
                        SELECT Neighbourhood_Name as name,Crime_Type as cType, COUNT(Crime_Type) as num
                        FROM crime_incidents
                        WHERE name = '{}' AND Year <= {} AND Year >= {}
                        GROUP BY name,Crime_Type)
                   GROUP BY name
                   HAVING MAX(num)'''.format(area,upper,lower)
        result = pd.read_sql_query(query,self.connection)
        return result
        

if __name__ == "__main__":
    # get tkinter window root
    root = tk.Tk()
    # set default window size
    root.geometry('500x500')
    # pass root UI and run
    ui = UI(root)
    ui.run()
    root.mainloop()