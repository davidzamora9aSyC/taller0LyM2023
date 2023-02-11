# Lista de comandos aceptados por el robot

#Juan Andrés Carrasquilla 202110183
#David Zamora 202113407
commands = [
    'assingTo',
    'goto',
    'move',
    'turn',
    'face',
    'put',
    'pick',
    'moveToThe',
    'moveInDir',
    'jumpToThe',
    'jumpInDir',
    'nop',
]

ctlStructureWords={
    'if:':['then:','else:'],
    'while:':'',
    'repeat:':''
}
directions = [
    "front", "right", "left", "back", "around"
]
alphabet = [
    'a','b','c','d','e','f','g','h','i','j','k','l','m','n','o','p','q','r','s','t','u','v','w','x','y','z'
]

numbers = [
    '1','2','3','4','5','6','7','8','9','0'
]
#Lista de comandos para la instrucción Look
lookCommands = [
    'north',
    'east',
    'west',
    'south'
]
#Lista de condiciones

conditions=[
    'facing',
    'canPut',
    'canPick',
    'canMoveDir',
    'canJumpInDir',
    'canMoveToThe',
    'canJumpToThe',
    'not'
]
#Lista de comandos para la instrucción Check
checkCommands = {
    'C' : True,
    'B' : True
}

#Variables definidas durante la ejecución del programa
definedVariables = {

}

#Caracteres especiales
specialChars = [
    "(",
    ")",
    "[",
    "]",
    ":",
    ";"
]

parametrosProc=[

]



def verifyProgram():
    verificado=True
    """Verifica que las instrucciones ingresadas sean correctas"""
    programString = "" #String que contiene todas las instrucciones leídas en el archivo de texto
    filename = "programaPrueba.txt"
    with open(filename,"r") as file: #Lectura el archivo de texto
        for line in file:
            #line = line.strip('\n') + ' '
            line = line.lstrip()

        
            programString += line #Se añade cada línea leída al String que contiene todo

    programString=programString.strip('\n').lower()
    programList = programString.split('\n')
    
    i=0
    while i < len(programList):
        
        if programList[0] != 'robot_r' and (i==0): #revisa que el programa empiece con ROBOT_R
            verificado=False
            
        if programList[1][0:5]!= "vars " and (i==1): #revisa que la declaracion de variables empiece con VARS
            verificado=False 
        if i ==1:
            variables = programList[1][4:].split(',')
          

            for nombreCandidato in variables:  #revisa que los nombres no contengan espacios en su interior
                nombre = nombreCandidato.strip(' ')
                nombreCandidato = nombreCandidato.strip(';').strip(' ')
                if ' ' in nombreCandidato:
                    verificado=False

            n_1=0
            for variable in variables:          #hace strip a cada nombre para la revision proxima
                variables[n_1] = variable.strip()
                n_1 +=1


            if variables[-1][-1]!= ';':        # revisa que la declaracion de variables termine con ;
                verificado = False
            else:
                variables[-1]= variables[-1].replace(';','').strip(' ')
                parametrosProc.append(variables)

            for nombre in variables:
                if nombre[0].lower() not in alphabet:  #revisa que los nombres empiecen con una letra
                    
                    verificado = False
                for character in nombre:        #revisa que los nombres solo contengan letras o numeros
                    if character.lower() not in alphabet and character not in numbers:
                        verificado = False
        if i==2:
            if programList[2] != 'procs':
                verificado = False
        
        if i==3:
            break
        
            
        i+=1

    programList= programList[3:]

    #print(aislarProcedimiento(programList))

    if aislarProcedimiento(programList) == False:
        verificado = False
    if verificado == True:
        return "Correcto"
    
    return 'ESCRIBA BIEN'



def aislarProcedimiento(programList):

    res = True
    primeraLinea = programList[0].split(' ',1)
    
    
    if nameVerif(primeraLinea[0]) == False:
        res =  False

    complementoPrimeraLinea = primeraLinea[1].strip(' ')
    

    if complementoPrimeraLinea[0] != '[':
        res = False

    programList[0] = complementoPrimeraLinea
    
    cadena = ''
    for elemento in programList:
        cadena += elemento
   
    
    
    abiertos =0
    cerrados =0
    k=0
    procedimiento=''
    
    
    while k < len(cadena):
        
        
        if cadena[k] == '[':
            abiertos +=1
        if cadena[k] == ']':
            cerrados +=1
        
        
        if abiertos == cerrados and k>0:
            procedimiento = cadena[1:k]
            break
        
        k+=1

  
   

    if findProcedureParameters(procedimiento) == False:

        res = False
    
    if res == False:
        return False

    return True


def findProcedureParameters(procedimiento): #obtiene los parametros entre simbolos | de un procedimiento
    #print('b')
    
    procedimiento = procedimiento.lstrip(' ')
    #print(procedimiento, 'AAAAAAAAAAAAAAAA')
    res = True    
    if procedimiento[0] != '|':
        res=False
    

    abiertos = 0
    j=0
    ultPos=0

    while j< len(procedimiento):
        if procedimiento[j] == '|':
            abiertos +=1
            if abiertos ==2:
                ultPos = j

        if abiertos >2:
            res = False
            
            break
        j+=1

    parametrosString = procedimiento[1:ultPos] #lo que va dentro 
    paramList=parametrosString.split(',')
    for param in paramList:
        param = param.strip(' ')
        parametrosProc.append(param)
        if nameVerif(param) == False:
            res = False
    procedimientoNuevo = procedimiento[ultPos+1:]

    if revisarBloque(procedimientoNuevo)== False:
        res = False

    if res == False:
        return False
    #print(procedimientoNuevo)
    return True




def revisarBloque(procedimiento):
    res = True
    if verifCommandGeneral(procedimiento) == False and verifCtlStructureGeneral(procedimiento) ==  False:
        res = False

    return res



def verifCommandGeneral(procedimiento): #ya está
    res = True
    procedimiento = procedimiento.replace(' ','')
    comandos = procedimiento.split(";")  #entra un string procedimiento y verifica que los comandos que tiene sean correctos
    for comando in comandos:
        separarComando = comando.split(":")
        nombreComando = separarComando[0]
        variablesComando1 = separarComando[1].split(",")
        if nombreComando in commands:
            res = verificarCommand(nombreComando, variablesComando1)
        else: 
            res = False

    return res


def verifCtlStructureGeneral(procedimiento): #entra un procedimineto str, verifica que esten bien
    res=True
    
    lista = procedimiento.split(' ')
   
    pos = 0
    wordPos = []
    ifInNames = False   #la funcion encuentra las posiciones de las palabras de ctl
    if len(lista)<1:
        res = False
    if lista[0] in ctlStructureWords.keys() and len(lista)>1:
        for name in lista:
            if name == 'if:':
                ifInNames = True
            if ifInNames == True:
                if name in ctlStructureWords['if:']:
                    wordPos.append(pos)
            if name in ctlStructureWords.keys():   #esta parte del codigo pone los indices de las palabras de control en wordPos.
                wordPos.append(pos)
            pos +=1
    
    if verifCtlStructure(wordPos, lista) == False:
        res = False
    return res

def verifCtlStructure(wordPos, lista): #wordPos lista con indices de palabras de ctl. Lista es una lista de un procedimiento o un bloque de instrucciones partidas por espacios
    res = True
    for pos in wordPos:   #wordPos = [1,5,6,9]
        if lista[pos]=='if:':
            if lista[wordPos[wordPos.index(pos)+1]]!='then:':
                res = False

            else:
                nuevoProcedimiento =''
                abiertos = 0
                cerrados =0
                k=0
                ultPos=0
                for element in lista[pos:]:
                    if element == '[':
                        abiertos +=1
                    if element == ']':
                        cerrados +=1
                    if abiertos == cerrados and k >0:
                        ultPos = k
                    k+=1                    
                for element in lista[pos:ultPos]:
                    nuevoProcedimiento +=element
                if revisarBloque(nuevoProcedimiento) == False:
                    res = False

            condicion = lista[pos+1 : wordPos[wordPos.index(pos)+1]]
            if verificarCondicion(condicion) == False:
                res = False

        if lista[pos]=='while:':
            if lista[wordPos[wordPos.index(pos)+1]]!='do:':
                res = False

            else:
                nuevoProcedimiento =''
                abiertos = 0
                cerrados =0
                k=0
                ultPos=0
                for element in lista[pos:]:
                    if element == '[':
                        abiertos +=1
                    if element == ']':
                        cerrados +=1
                    if abiertos == cerrados and k >0:
                        ultPos = k
                    k+=1                    
                for element in lista[pos:ultPos]:
                    nuevoProcedimiento +=element
                if revisarBloque(nuevoProcedimiento) == False:
                    res = False

            condicion = lista[pos+1 : wordPos[wordPos.index(pos)+1]]
            if verificarCondicion(condicion) == False:
                res = False
        if lista[pos]=='repeat:':
            if lista[pos+1] not in numbers:
                res = False

    return res

def verificarCondicion(condicion):
    variables= parametrosProc
    nombre = condicion[0]
    variable1= condicion[1]
    variable2 = condicion[3]
    res = True
    if nombre=="facing:" and (condicion[1] not in lookCommands):
        res=False
    elif nombre=="canput" and ((variable1 not in numbers and variable1 not in variables) or (variable2!="chips" and variable2!="balloons")):
        res =False
    elif nombre=="canpick" and ( (variable1 not in numbers and variable1 not in variables) or (variable2!="chips" and variable2!="balloons")):
        res=False
    elif nombre=="canmoveindir:" and (variable2 not in lookCommands or (variable1 not in numbers)) :
        res=False
    elif nombre=="canjumpindir:" and (variable2 not in lookCommands or (variable1 not in numbers)) :
        res=False
    elif nombre=="canmovetothe:" and (variable2 not in directions or (variable1 not in numbers)) :
        res=False
    elif nombre=="canjumptothe:" and (variable2 not in directions or (variable1 not in numbers)) :
        res=False
    elif nombre=="not:" and verificarCondicion(condicion[4:]) :
        res=False
    return res

            


def verificarCommand(nombreComando, variablesComando):
    variables= parametrosProc
    verificado=True
    variable1=variablesComando[0]
    if len(variablesComando)>1:
        variable2=variablesComando[1]
    if nombreComando=="move" and (variable1 not in numbers and variable1 not in variables):
        verificado=False
    elif nombreComando=="turn" and variable1 not in directions:
        verificado=False
    elif nombreComando=="face" and variable1 not in lookCommands:
        verificado=False
    elif nombreComando=="movetothe" and (variable2 not in directions or (variable1 not in numbers and variable1 not in variables)):
        verificado=False
    elif nombreComando=="pick" and ((variable1 not in numbers and variable1 not in variables) or (variable2!="chips" and variable2!="balloons")):
        verificado=False
    elif nombreComando=="put" and ( (variable1 not in numbers and variable1 not in variables) or (variable2!="chips" and variable2!="balloons")):
        verificado=False
    elif nombreComando=="moveindir" and (variable2 not in lookCommands or (variable1 not in numbers and variable1 not in variables)):
        verificado=False
    elif nombreComando=="jumptothe" and (variable2 not in directions or (variable1 not in numbers and variable1 not in variables)):
        verificado=False
    elif nombreComando=="moveindir" and (variable2 not in lookCommands or (variable1 not in numbers and variable1 not in variables)):
        verificado=False
    elif nombreComando=="goto" and ( (variable2 not in variables and variable2 not in numbers) or (variable1 not in numbers and variable1 not in variables) ):
        verificado=False
    
    return verificado




def nameVerif(string:str):
    j=0
    i = len(string)
    if string[0].lower() in alphabet:
        while j < i:
            if string[j].lower() in alphabet or string[j] in numbers:
                return True
            j +=1
    return False


   
#print(verifCommandGeneral('while: canMovetoThe : 1 , north do: [ moveInDir : 1 , north ]'))
print(verifyProgram())