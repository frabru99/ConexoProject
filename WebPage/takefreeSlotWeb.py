

"""

CHECK_SPACE_FOR_CABINET: Funzione utile ad elencare tutte le massime dimensioni disponibili contigue.

Input:
- list: [["A-NA - 1 / 3"], ["A-NA - 4 / 8"], ["A-NA - 9 / 13"], ["B-NA - 2 / 5"], ["B-NA - 8 / 15"]]), che rappresenta gli slot occupati.
- cabinet_max_sizes: Dizionario con le dimensioni massime di ogni cabinet. {"A-NA": 20, "B-NA": 15 ecc...}


Output:
- Valore massimo di spazio contigup vuoto.

"""


def check_space_for_cabinet(list, cabinet_max_sizes):
    
    result= {}

    id_cabinets = []

    contigent = []
    
    for i in range(len(list)):
        
        # Estrai l'identificativo del cabinet e i numeri di slot occupati e totali
        cabinet_id, occupied_total = list[i][0].split(" - ")

        if cabinet_id not in id_cabinets:
            id_cabinets.append(cabinet_id)

    
    for id in id_cabinets:


        f_istance = 0
        value_f= 0
        value = 0

        contigent = []

        for i in range(len(list)):

            cabinet_id, occupied_total = list[i][0].split(" - ")    
            first, last = map(int, occupied_total.split(" / "))

    
            if i != len(list)-1:
                
                cabinet_id_next, occupied_total_next = list[i+1][0].split(" - ")
                first_next, last_next = map(int, occupied_total_next.split(" / "))

            else:
                cabinet_id_next = None
            
            value=0

            if cabinet_id == id:

                
                if first > 1 and f_istance == 0:
                        
                    value_f = first-1
                    contigent.append(value_f)
                    
                f_istance=1

                if cabinet_id_next != None and cabinet_id == cabinet_id_next and i != len(list)-1:
                
 
                    if first_next-last-1 > 0:
                        
                        value = first_next-last-1
                        contigent.append(value)
                
                elif (cabinet_id_next == None or cabinet_id != cabinet_id_next) and cabinet_max_sizes[cabinet_id]-last>0:
                    
                    value = cabinet_max_sizes[cabinet_id]-last
                    contigent.append(value)

                elif i == len(list)-1 and cabinet_max_sizes[cabinet_id]-last>0:
                    
                    value = cabinet_max_sizes[cabinet_id]-last                
                    contigent.append(value)

                else:
                    result[id] = 0
            



    if(len(contigent) != 0):
        result[id] = max(contigent)
        
    print("Result: ")
    print(result)
    print(type(result))
    
    return result


"""
Clen_Result: funzione che permette di "pulire" e preprare i dati per le funzioni sovrastanti.

Input:
- result: Risultato della query. 
- dimension: Dimensione inserita del dispositivo.
- cabinet_max_sizes: Dizionario con le dimensioni massime di ogni cabinet. {"A-NA": 20, "B-NA": 15 ecc...}


Output:
- Consiste in due liste:
    - response: lista da passare alle funzioni precedenti ([["A-NA - 1 / 3"], ["A-NA - 4 / 8"], ...])
    - all_free: Tutti i cabinet completamente liberi, verranno gestiti sepratamente prima di restituire la risposta al bot.


"""

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

            if dimension >  0: 
                print(key)
                l = []
                l.append(key)
                l.append(1)
                l.append(dimension)
                l.append(dimension)
                all_free.append(l)
            else:
                all_free.append(dictionary_max_dimensions[key]) #Posso usare questa funzione anche per lo scopo di capire il massimo spazio contiguo disponibile, passando dimension = 0

        
      
    return response, all_free



#TEST
#list = [["A-NA - 1 / 3"], ["A-NA - 4 / 8"], ["A-NA - 9 / 13"], ["B-NA - 2 / 5"], ["B-NA - 8 / 15"]]

#Esempio di mappa che associa ogni cabinet alla sua dimensione massima
#cabinet_max_sizes = {"A-NA": 20, "B-NA": 20}



#print(check_space_for_cabinet(list, cabinet_max_sizes))