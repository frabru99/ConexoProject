
def foundFields(data):

    search_key_prod = "producer" #per il producer
    search_key_year="year"
    search_key_production="production"
    search_key_serial="serial"

    #chiavi di ricerca nel dict

    producer = [val for key, val in data.items() if search_key_prod in key.lower() ] #genero una lista in cui appendo i valori delle chiavi che corrispondono ai criteri 
    year_of_prod =  [val for key, val in data.items() if search_key_year and search_key_production in key.lower() ]
    serial_number = [val for key, val in data.items() if search_key_serial in key.lower() ]

    return producer, year_of_prod, serial_number




#TEST 
if __name__ == "__main__":

    data = {"serialNumber": "1111222233334444", "producer": "Cisco", "yearOfProduction":  "2022"}
    data2 = {"numberSerial": "1111222233334444", "ProducerName": "Cisco", "productionYear":  "2022"}

    prod, year, serial = foundFields(data2)

    print(prod)
    print(year)
    print(serial)




