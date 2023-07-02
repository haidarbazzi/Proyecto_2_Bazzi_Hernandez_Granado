from Artwork import Artwork
import pickle

class App():
    def __init__(self):
        self.indexing_name_array = [] #Para la busqueda binaria por nombre.
        self.indexing_code_array = [] #Para la busqueda binaria por código.
        self.principal_array = [] #La que contiene al objeto PPD. 
   
    # Función para cargar la información de los archivos TXT a nuestra BD local.
    def uploadTXT(self):
        """
        Función para traernos la data de los archivos TXT a nuestra BD local. 
        """
        file = open("IndexingNameArray.txt", "rb")
        self.indexing_name_array = pickle.load(file)
        file.close()

        file = open("IndexingCodeArray.txt", "rb")
        self.indexing_code_array = pickle.load(file)
        file.close()

        file = open("PrincipalArray.txt", "rb")
        self.principal_array = pickle.load(file)
        file.close()
    
    # Función para cargar nuestra BD local a los archivos TXT.
    def save(self):
        """
        Salvar la data registrada en el archivo TXT.
        """
        file = open("IndexingNameArray.txt", "wb")
        pickle.dump(self.indexing_name_array, file)
        file.close()

        file = open("IndexingCodeArray.txt", "wb")
        pickle.dump(self.indexing_code_array, file)
        file.close()

        file = open("PrincipalArray.txt", "wb")
        pickle.dump(self.principal_array, file)
        file.close()
    
    def artwork_register(self):

        #Petición y validación del número de cota.
        while True:
            code = input("\nIntroduzca el número de cota 'conformada por 4 letras y 4 dígitos': \n>>> ")
            letter_counter = 0
            number_counter = 0
            for letter in code:
                if letter.isnumeric():
                    number_counter +=1
                elif letter.isalpha():
                    letter_counter +=1
            code = code.upper()
            if (letter_counter == 4) and (number_counter ==4) and self.binary_search(self.indexing_code_array, code) ==-1:
                break
            else:
                print("Secuencia no válida, vuelva a intentarlo.")
        
        #Petición y validación del nombre
        while True:
            name = input("\nIntroduzca el nombre de la obra 'máximo 10 caracteres': \n>>> ")
            name = name.upper()

            if len(name) <=10 and (self.binary_search(self.indexing_name_array, name) == -1): 
                break
            else: 
                print ("Ingresó una secuencia no válida.")
        
        #Petición de precio 
        try:
            price = input("\nIntroduzca el precio de la obra 'no puede ser negativo': \n>>>")
            price = float(price)
        except: 
            print ("Ingresó una secuencia no válida.")

        #Petición de precio 
        while True:
            try:
                year = input("\nIntroduzca el año obra 'no puede ser negativo': \n>>>")
                year = int(year)
                if year <0 or year >2023:
                    raise Exception
                break
            except: 
                print ("Ingresó una secuencia no válida.")
       
        while True:
            status_option= input("\nSeleccione el status de la obra:\n1. EN EXHIBICIÓN\n2. EN MANTENIMIENTO: \n>>> ")
            if status_option == "1":
                status = "EN EXHIBICIÓN"
                break
            elif status_option =="2":
                status = "EN MANTENIMIENTO"
                break
            else: 
                print ("Ingresó una opción no válida.")
            
        artwork = Artwork(code, name, price, year, status,False) # Se guarda con el atributo false NO elimina, util luego para la compactación
        self.principal_array.append(artwork)
        #Introducidos en los arreglos índices de codigo y nombre el atributo correspondiente y la posición donde se almacena en el array principal
        self.indexing_code_array.append([artwork.code,len(self.principal_array)-1])
        self.indexing_name_array.append([artwork.name,len(self.principal_array)-1])
        #Organizamos los arreglos índices de codigo y nombre para que esten organizados y se pueda hacer busqueda binaria. 
        self.indexing_code_array = sorted(self.indexing_code_array, key=lambda x: x[0])
        self.indexing_name_array = sorted(self.indexing_name_array, key=lambda x: x[0])
        
        loop_continue = input("\nDesea guardar sus cambios?:\n1. Si.\n2. No.\n >>> ")
        if loop_continue == "1": 
            self.save()
        self.start()
            
    def binary_search(self, arr, targetValue):
        """
        Algoritmo de búsqueda binaria
        """
        low = 0
        high = len(arr) - 1

        while low <= high:
            mid = (low + high) // 2
            mid_value = arr[mid][0]  #Posición 0 porque es la posición donde se guarda el name o el code. En la posición 1 se guarda el index
            if mid_value == targetValue:
                return mid
            elif mid_value < targetValue:
                low = mid + 1
            else:
                high = mid - 1
        return -1 #Si el elemento no se encuentra se retorna -1
    
    def artwork_search(self):
        selection =""
        result = 0
        while True: 
            selection = input("\nMÓDULO CONSULTAR UNA PINTURA.\n1. Para buscar pintura por COTA.\n2. Para buscar pintura por NOMBRE.\n3. Volver a menu principal.\n>>> ")
            if selection == "1":
                code = input("Indique la cota: >>> ")
                result = self.binary_search(self.indexing_code_array, code)
                # Para obtener el index donde se encuentra el code en el indexing_code_array
                if result != -1:
                    break
                else:
                    print("Esa cota no es válida")
            elif selection == "2":
                name = input("Indique el nombre: >>> ")
                result = self.binary_search(self.indexing_name_array, name)
                # Para obtener el index donde se encuentra el name en el indexing_name_array
                if result != -1:
                    break
                else:
                    print("Esa cota no es válida")
            elif selection == "3":
                break
        
        #Ahora con el index del indexing_array obtenemos la posición directamente del principal_array
        principal_array_index = 0
        if selection == "1":
            principal_array_index = self.indexing_code_array[result][1] 
        if selection == "2":
            principal_array_index = self.indexing_name_array[result][1] 
        if selection == "3":
            self.start()
        #Accedemos a la info del principal_array
        artwork = self.principal_array[principal_array_index]
        print("\nLos detalles de la obra seleccionada son: \n")
        print(artwork.show_attr())


    def start(self):
        print("\nBIENVENIDO AL MUSEO UNIMET")
        self.uploadTXT()
        
        print(self.indexing_name_array)
        print(self.indexing_code_array)
        
        while True: 
            print ("\n--- MENU PRINCIPAL ---")
            option = input ("1. Insertar una nueva pintura.\n2. Consultar una pintura.\n3. Cambiar status de una pintura.\n4. Eliminar una pintura. \n5. Compactar la base de datos. \n6. Salir\n >>> ")
            if option == "1": 
                self.artwork_register()
            elif option == "2": 
                self.artwork_search()
            elif option == "3": 
                break 
            elif option == "4": 
                break ## Para la eliminación artWork tiene un attr que se llama DELETE para que se ponga como true si se elimina y luego asi este atributo es TRUE en la compactación si se saca del principal_array definitivo.
            elif option == "5": 
                break  #Pendiente con lo de arriba del artwork.delete. Los puse como attr del object porque si lo ponia como un array ([artwork, deleteTrue/False]) dentro del principal_array tenía problemas con el pickle
            elif option == "6": 
                break 
            else: 
                print ("Opción no valida, por favor seleccione una opción válida:\n>>>  ")







