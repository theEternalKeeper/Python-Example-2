import csv
import matplotlib.pyplot as plt

#Uppgift 1
def Load_Files(): #Denna funktion hämtar in csv filerna en efter den andra med en try/except function som gör att programmet ej krashar om den inte hittar filerna, och läser sedan in dem till en lista.
    covid19, testade, invanare = [], [], []
        
    try:
        with open ("covid-19_data.csv", "r") as file:
            csv_reader = csv.reader(file, delimiter= ";")
            for rad in csv_reader:
                covid19.append(rad)
    except:
        print("Covid data finns inte")
    try:
        with open ("antal_testade.csv", "r") as file:
            csv_reader = csv.reader(file, delimiter= ";")
            for rad in csv_reader:
                testade.append(rad)
    except:
        print("Test data finns inte")
    try:
        with open ("antal_invanare.csv", "r") as file:
            csv_reader = csv.reader(file, delimiter= ";")
            for rad in csv_reader:
                invanare.append(rad)
    except:
        print("Invånar data finns inte")
    return covid19, testade, invanare #Här returneras listorna så att de kan användas av de andra funktionerna

#Uppgift 2
def Top_Table(cases, pops):
    fall = cases.copy()
    table_list= []
    column_values = []
    
    for colm in range(1, len(fall[0])): #Här skapas en lista med tomma värden som ska sedan användas senare i funktionen för att agera som en spärr
        column_values.append(0)

    for row in range(1, len(fall)):
        for colm in range(1, len(fall[row])):
            value = round(int(fall[row][colm])/int(pops[1][colm])*100000, 1) #Här beräknas antalet sjuka per 100,000
            if value >= column_values[colm-1]: 
                column_values[colm-1] = value
                table_entry = [fall[0][colm], fall[row][0], value]              
                try:
                    for i, index_list in enumerate(table_list): #Här gårs tabellen igenom för att se om det finns en tidigare rad för en given plats och jämför med den nya informationen                       
                        if table_entry[0] in index_list: 
                            index = i
                            if table_entry[2] > table_list[index][2]:
                                table_list.remove(next(x for x in table_list if table_entry[0] in x)) #Här tas bort tidiagre inlägg i listan som kommer publiceras som inte är relevanta
                    table_list.append(table_entry)
                except:    
                    table_list.append(table_entry)
    table_list.sort(key=lambda x: x[0]) #Sorterar listan alfabetiskt så att den blir lättare att läsa
                      
    print("SAMMANSTÄLLNING AV HÖGSTA ANTALET SMITTADE SOM ÄR INRAPPORTERDE UNDER EN DAG TOTALT i RIKET OCH PER REGION MELLAN 2020-02-01 OCH 2020-11-30\n", "======================================================================== \n \n")
    print("Region/riket Datum  Antal smittade per 100 000 inv.")
    print("--------------------------------------------------------------")
    for i in range(len(table_list)):
        print(table_list[i])
    return
        
            

#Uppgift 3
def Infect_Graph(cases, pops):
    fall = cases.copy()
    dates = list(range(0,10))
    months = ["Februari", "Mars", "April", "Maj", "Juni", "Juli", "Augusti", "September", "Oktober", "November"] #Här görs en lista med månadernas namn som kommer visas i grafen
    places = []
       
    for row in range(1, len(fall)):
        for colm in range(1, len(fall[row])):
            fall[row][colm] = round(int(fall[row][colm])/int(pops[1][colm])*100000, 1)

    
    for row_del_dates in range(1, len(fall)):
        del fall[row_del_dates][0] #Trimmar bort datumen från datan
    places = fall.pop(0)

    fall_zip = zip(*fall) #Vänder på listan så att den blir enklare att gå igenom för grafen
    
    turned_fall = list(map(list, fall_zip)) #Gör om fall_zip some blivit en lista av tuples till en lista av listor

    plt.xlabel("Månad")
    plt.ylabel("Antal sjuka per 100,000")
    plt.xticks(dates, months)
    
    for trimming in range(len(turned_fall)):
        plt.plot(dates, turned_fall[trimming][27::30], label = places[trimming]) #Här trimmas listan så att det bara finns ett nummer för varje månad, för att få en bra öveblick över alla månader använde jag den 28:de, och det lägs till grafen. 
        #Behöver inte specifiera färg då med versonen av Python jag har så tilldelas alla en automatiskt
        
    
    plt.legend()
    plt.show()
    return

#Uppgift 4
def Infect_Test(cases, pops, tested):
    total_sjuka = []
    hundk_tested = []
    slut_tabell = []
    dates = list(range(0,10))
    months = ["Februari", "Mars", "April", "Maj", "Juni", "Juli", "Augusti", "September", "Oktober", "November"]
    
    for row in range(1, len(cases)):
        total_sjuka.append(round(int(cases[row][1])/int(pops[1][1])*1000000, 1))
        
    monad_sjuka = total_sjuka[27::30] #Här trimmas listan så att det bara finns ett nummer för varje månad, för att få en bra öveblick över alla månader använde jag den 28:de
    
    for colm in range(1, len(tested[1])):
        hundk_tested.append(round(int(tested[1][colm])/int(pops[1][1])*1000000, 1))
    
    for row in range(len(monad_sjuka)):
        slut_tabell.append(round(monad_sjuka[row-1]/hundk_tested[row-1]*100, 1)) #För att göra det lite fancy gjorde jag så att andelen visas som procent
    
    
    plt.title("Antal sjuka per 100,000 per testade")
    plt.xlabel("Månad")
    plt.ylabel("Antal sjuka per 100,000 per testade i %")
    plt.xticks(dates, months)
    
    plt.plot(dates, slut_tabell)
    
    plt.legend()
    plt.show()

def Meny():
    ran_get_data = False #Detta värde ser kollar om användaren har först laddat datan så att programmet inte kraschar

    while True:
         
        print ('Meny \n===== \n1. Hämta data från fil – uppgift 1 \n2. Analysera data - uppgift 2 \n3. Analysera data - uppgift 3 \n4. Analysera data - uppgift 4 \n5. Avsluta')

        meny_val = input('Välj menyalternativ (1-5): ')


        if (int(meny_val) == 1):
            covid_data, antal_testade, antal_invanare = Load_Files()
            print(covid_data[:3], "\n", antal_testade[:3], "\n", antal_invanare[:3], "\n")
            ran_get_data = True
        elif (int(meny_val) == 2):
            if ran_get_data == True:
                Top_Table(covid_data, antal_invanare)
            else:
                print("Vänlig hämta data först")
        elif (int(meny_val) == 3):
            if ran_get_data == True:
                Infect_Graph(covid_data, antal_invanare)
            else:
                print("Vänlig hämta data först")
        elif (int(meny_val) == 4):
            if ran_get_data == True:
                Infect_Test(covid_data, antal_invanare, antal_testade)
            else:
                print("Vänlig hämta data först")
        elif (int(meny_val) == 5):
            break


Meny()