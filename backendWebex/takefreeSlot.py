#list = [["A-NA - 1 / 3"], ["A-NA - 4 / 8"], ["A-NA - 9 / 13"], ["B-NA - 2 / 5"], ["B-NA - 8 / 15"]]

# Esempio di mappa che associa ogni cabinet alla sua dimensione massima
#cabinet_max_sizes = {"A-NA": 20, "B-NA": 20}

def check_space_for_device(device_size, list, cabinet_max_sizes):
    
    result= []

    id_cabinets = []
    
    for i in range(len(list)):
        # Estrai l'identificativo del cabinet e i numeri di slot occupati e totali
        cabinet_id, occupied_total = list[i][0].split(" - ")

        if cabinet_id not in id_cabinets:
            id_cabinets.append(cabinet_id)

        

    for id in id_cabinets:

        dimensions = []

        f_istance = 0
        value_f= []
        value = []

        for i in range(len(list)):

            cabinet_id, occupied_total = list[i][0].split(" - ")    
            first, last = map(int, occupied_total.split(" / "))

            

            if i != len(list)-1:
                
                cabinet_id_next, occupied_total_next = list[i+1][0].split(" - ")
                first_next, last_next = map(int, occupied_total_next.split(" / "))

            else:
                cabinet_id_next = None
            value=[]

            if cabinet_id == id:

                if cabinet_id_next != None and cabinet_id == cabinet_id_next  and i != len(list)-1:
                
                    if first > 1 and f_istance == 0 and (first - 1) >= device_size:
                        
                        value_f.append(cabinet_id)
                        value_f.append(1)
                        value_f.append(first-1)
                        value_f.append(device_size)
                        dimensions.append(value_f)
                    
                    f_istance=1

                    if (first_next - last - 1) >= device_size and f_istance==1:
                        
                        value.append(cabinet_id)
                        value.append(last+1)
                        value.append(last+device_size)
                        value.append(device_size)
                        dimensions.append(value)
                    
                elif (cabinet_id_next == None or cabinet_id != cabinet_id_next) and cabinet_max_sizes[cabinet_id]-last >= device_size:
                    
                    value.append(cabinet_id)
                    value.append(last+1)
                    value.append(last+device_size)
                    value.append(device_size)
                    dimensions.append(value)

                elif i == len(list)-1 and cabinet_max_sizes[cabinet_id]-last >= device_size:
                

                    value.append(cabinet_id)
                    value.append(last+1)
                    value.append(last+device_size)
                    value.append(device_size)
                    dimensions.append(value)

        result.append(dimensions)
            

    return result 
                    


#print(check_space_for_device(2, list, cabinet_max_sizes))


def cleanResult(result, dimension, dictionary_max_dimensions):
    response = []
    all_free = []

    lista = []

    
    for list in result:
        if list[1] != "-" and list[1] != '0':
            response.append([list[1]])

        if list[0] not in lista:
            lista.append(list[0])
        
    print(lista)

    
    for key in dictionary_max_dimensions:

        if key not in lista and dictionary_max_dimensions[key] >= dimension :
            print(key)
            l = []
            l.append(key)
            l.append(1)
            l.append(dimension)
            l.append(dimension)
            all_free.append(l)
      
    return response, all_free

