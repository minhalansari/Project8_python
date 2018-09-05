####################################################################################################
#Project 8
#Asks user to input a file
#Reads the file and creates a dictionary with year as the key and another dictionary as the value
#the second dictionary has hurricane name as the key and all the data as the value
#asks user to enter a year
#displays data for the hurricanes in the file for that year
#asks user to if they want to plot data and plots data if yes
####################################################################################################


import pylab as py
from operator import itemgetter

def open_file():
    '''prompts user to enter a file name, opens the file and returns it. 
    If there is an error it tells the user then prompts for another filename.'''
    filename = input("Input a file name: ")  #File entered by user
    #whileloop that runs while the file is not an empty string
    while filename != ' ': 
        #try and except which checks if the file is valid
        try:
            fp = open(filename, 'r') #filepointer opened for reading
        
            return fp #returns the file pointer
            break    #breaks the while look once filepointer is returned
        except FileNotFoundError:
            print("Unable to open file. Please try again.") #displays this message if theres an error findind the file
            filename = input("Input a file name: ")     #prompts user to enter another filename
    

def update_dictionary(dictionary, year, hurricane_name, data):
    '''receives dictionary, new year, name and data to add to the existing dictionary given
    and ccreates a new key if year is not in dictionary, if key is in dictionary then
    it creates a new key within the year values for the specific hurricane and adds the data.
    returns the dictionary'''
    #if statement checking if the year is not already in the dictionary
    if year not in dictionary:
        dictionary[year] = {} #creates a new key for the year
    #if statement if the hurricane name isnot a value for the specfied year, adds it and all its data
    if hurricane_name not in dictionary[year]:
        dictionary[year][hurricane_name] = []
        
    dictionary[year][hurricane_name].append(data)  #adds the data
    return dictionary    #returns the dictionary
    
def create_dictionary(fp):
    '''receives a file pointer and reads the file
    and returns a dictionary'''
    #intialize empty dictionary
    dict1 = {}
    #for loop going through each line in the file and separating it out
    for line in fp:
        line = line.strip()
        line = line.split()
        year = line [0]     #year hurricane occured in
        hurricane_name = line[1]    #name of hurricane
        lat = float(line[3])    #lattitude of hurricane
        lon = float(line[4])    #longitude of hurricane
        date = line[5]          #data of hurricane
        #Try and except loop to display the wind speed as a float and if it isnt there then display zero
        try:   
            wind = float(line[6])  #wind speed of hurricane
        
        except ValueError:
            wind = 0
        #try and except to display the pressure as a float and as zero if is not a number
        try:
            pressure= float(line[7])    #pressure of hurricane
        except ValueError:
            pressure = 0
        tup1 = (lat, lon, date, wind, pressure) #tuple containing all the info to add to dictionary
        
        
        dict2 = update_dictionary(dict1, year, hurricane_name, tup1) #creates dictionary by calling the update_dictionary function
    return dict2   #returns the dictionary
def display_table(dictionary, year):
    '''takes a dictionary and a given year and prints a display table for data in that year sorted by wind
    speed, lattitude and longitude'''
    dict = sorted(dictionary[year].items()) #sorts dictionary to be in alphabetical order
    print("{:^70s}".format("Peak Wind Speed for the Hurricanes in " + year))  #prints table title
    print("{:15s}{:>15s}{:>20s}{:>15s}".format("Name","Coordinates","Wind Speed (knots)","Date"))   #prints table headers
    #for loop going through each key, value pair in the sorted dictionary and sorting it
    for k,v in dict:
        name = (k) #hurricane name
        tup = v   #tuple of hurricane data
        sorteddata = sorted(tup, key =itemgetter(3, 0,1)) #sorts data based off of windspeed, latitude, and the longitude
        data = sorteddata[-1] #takes the hurricane with the highest windspeed
        print("{:15s}( {:>.2f},{:>.2f}){:>20.2f}{:>15s}".format(name,data[0],data[1],data[3],data[2])) #prints out data in table
def get_years(dictionary):
    '''takes a dictionary and returns a tuple with the oldest and most recent years in the dictionary'''
    sortedkeys = sorted(dictionary.keys())  #sorts dictionary based off of years
    tuple1 = (sortedkeys[0], sortedkeys[-1]) #tuple with oldest and most recent years
    return tuple1 #returns tuple
def prepare_plot(dictionary, year):
    '''takes a dictionary and a year. Returns a tuple of three lists:
        hurricane names, hurricane coordinates, and a list of all
        maximum speeds of hurricanes'''
    dict1 = sorted(dictionary[year].items()) #dictionary sorted by hurricane names
    names = [] #initialize empty names list
    wind = [] #initialize empty wind speeds lists
    coordinates = [] #initialize first coordinates list
    coordinates1 = [] #initialize second coordinates list
    coordinates2= [] #initialize third coordinates list
    finalcoordinates = [] #initialize final coordinates list
    #for loop going through each key value pair in sorted dict and creating a name list
    for k,v in dict1: 
        name = k #hurricane name
        nametup2= (name) #tuple with hurricane name
        names.append(nametup2) #append name to list
    #for loop going through each value in the dictionary for that year
    for v in dictionary[year].values():
        tup3 = v  #tuple of all the data 3
        sorteddata = sorted(tup3, key = itemgetter (3))  #sort data in tuple based off of wind speed
        winddata = sorteddata[-1][3] #take the maximum windspeed
        wind.append(winddata) #append to windspeed list
        lat1 = tup3[0][1]  #latitude of first line
        lon1 = tup3[0][0]  #longitude of first line
        lat2 = tup3[1][1]  #latitude of second line
        lon2 = tup3[1][0]  #longitude of second line
        #append all the values to the coordinates list
        coordinates.append(lon1)
        coordinates.append(lat1)
        coordinates.append(lon2)
        coordinates.append(lat2)
    #create sets of coordinates
    firstcoordinates = (coordinates[0], coordinates[1])
    secondcoordinates = (coordinates[2], coordinates[3])
    #append to second coordinates list
    coordinates1.append(firstcoordinates)
    coordinates1.append(secondcoordinates)
    #create second sets of coordinates
    firstcoordinates2 =(coordinates[4], coordinates[5])
    secondcoordinates2 = (coordinates[6], coordinates[7])
    #append to third coordinates list
    coordinates2.append(firstcoordinates2)
    coordinates2.append(secondcoordinates2)
    #append second and third cooridnates lists to final coordinates list
    finalcoordinates.append(coordinates1)
    finalcoordinates.append(coordinates2)
    #create a tuple containing a list of names, list of coordinates, and list of max wind speeds
    finaltup = (names,finalcoordinates, wind)
    return finaltup #return final tuple
    
def plot_map(year, size, names, coordinates):
    '''takes year, size of data, list of hurricane names, and list of
    hurricane coordinates and plots a map.'''
    
    # The the RGB list of the background image
    img = py.imread("world-map.jpg")

    # Set the max values for the latitude and longitude of the map
    max_longitude, max_latitude = 180, 90
    
    # Set the background image on the plot
    py.imshow(img,extent=[-max_longitude,max_longitude,\
                          -max_latitude,max_latitude])
    
    # Set the corners of the map to cover the Atlantic Region
    xshift = (50,190) 
    yshift = (90,30)
    
    # Show the atlantic ocean region
    py.xlim((-max_longitude+xshift[0],max_longitude-xshift[1]))
    py.ylim((-max_latitude+yshift[0],max_latitude-yshift[1]))
	
    # Generate the colormap and select the colors for each hurricane
    cmap = py.get_cmap('gnuplot')
    colors = [cmap(i/size) for i in range(size)]
    
    
    # plot each hurricane's trajectory
    for i,key in enumerate(names):
        lat = [ lat for lat,lon in coordinates[i] ]
        lon = [ lon for lat,lon in coordinates[i] ]
        py.plot(lon,lat,color=colors[i],label=key)
    

     # Set the legend at the bottom of the plot
    py.legend(bbox_to_anchor=(0.,-0.5,1.,0.102),loc=0, ncol=3,mode='expand',\
              borderaxespad=0., fontsize=10)
    
    # Set the labels and titles of the plot
    py.xlabel("Longitude (degrees)")
    py.ylabel("Latitude (degrees)")
    py.title("Hurricane Trayectories for {}".format(year))
    py.show() # show the full map


def plot_wind_chart(year,size,names,max_speed):
    '''takes hurricane year, data size, list of hurricane names, and a list of 
    hurricane maximum speeds. returns a chart with the wind data for the hurricanes. '''
    
    # Set the value of the category
    cat_limit = [ [v for i in range(size)] for v in [64,83,96,113,137] ]
    
    
    # Colors for the category plots
    COLORS = ["g","b","y","m","r"]
    
    # Plot the Wind Speed of Hurricane
    for i in range(5):
        py.plot(range(size),cat_limit[i],COLORS[i],label="category-{:d}".format(i+1))
        
    # Set the legend for the categories
    py.legend(bbox_to_anchor=(1.05, 1.),loc=2,\
              borderaxespad=0., fontsize=10)
    
    py.xticks(range(size),names,rotation='vertical') # Set the x-axis to be the names
    py.ylim(0,180) # Set the limit of the wind speed
    
    # Set the axis labels and title
    py.ylabel("Wind Speed (knots)")
    py.xlabel("Hurricane Name")
    py.title("Max Hurricane Wind Speed for {}".format(year))
    py.plot(range(size),max_speed) # plot the wind speed plot
    py.show() # Show the plot
    

def main():
    '''calls all the other functions in order for the program to run properly.'''
    fp = open_file() #calls open file function to allow user to enter a file and opens it
    print("Hurricane Record Software") #prints title
    dictionary = create_dictionary(fp) #calls the create_dictionary function to create a dictionary with the given file
    year_tuple = get_years(dictionary) #a tuple of the oldest and most recent years
    print("Records from {:4s} to {:4s}".format(year_tuple[0], year_tuple[1])) #prints title
    year = input("Enter the year to show hurricane data or 'quit': ") #prompts user to enter a year
    #while loop that runs until the user enters quit instead of a year
    while year.lower() != 'quit':
        #try and except to check if a valid year is entered
        try:
            display_table(dictionary, year) #prints data in display table 
            answer = input("\nDo you want to plot? ") #prompts user to plot
            #if statement that checks if user wants to plot
            if answer.lower() == 'yes':
                namesccspeed = prepare_plot(dictionary,year) #tuple with a list of names, hurricane coordinates, and max wind speeds
                size = len(dictionary[year]) #size of the data
                plot_map(year, size, namesccspeed[0],namesccspeed[1]) #plots the data on a map
                plot_wind_chart(year,size,namesccspeed[0],namesccspeed[2]) #plots a chart with the wind speed data 
            year = input("Enter the year to show hurricane data or 'quit': ") #prompts user to enter another year or quit
            
        except KeyError:
            print("Error with the year key! Try another year") #prints if incorrect year is entered
            year = input("Enter the year to show hurricane data or 'quit': ")   #prompts user to enter another year or quit
    
if __name__ == "__main__":
    main()
