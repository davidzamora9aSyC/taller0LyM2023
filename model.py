# Lista de comandos aceptados por el robot
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
    'if:':['then','else'],
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
lookCommands = {
    'north' : True,
    'east' : True,
    'west' : True,
    'south' : True
}
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



def wordInCommands(word):
    """Verifica si una instrucción se encuentra dentro de la lista de comandos."""
    if word in commands.keys():
        return True
    else:
        return False


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

    programString=programString.strip('\n')
    programList = programString.split('\n')
    
    i=0
    while i < len(programList):
        
        if programList[0] != 'ROBOT_R' and (i==0): #revisa que el programa empiece con ROBOT_R
            verificado=False
            
        if programList[1][0:5]!= "VARS " and (i==1): #revisa que la declaracion de variables empiece con VARS
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


            for nombre in variables:
                if nombre[0].lower() not in alphabet:  #revisa que los nombres empiecen con una letra
                    
                    verificado = False
                for character in nombre:        #revisa que los nombres solo contengan letras o numeros
                    if character.lower() not in alphabet and character not in numbers:
                        verificado = False
        if i==2:
            if programList[2] != 'PROCS':
                verificado = False
        
        if i==3:
            break
        
            
        i+=1

    programList= programList[3:]
    #print(programList)
    print(aislarProcedimiento(programList, verificado))
    ''' 
    
    verificacionProcedimiento, procedimiento = procedureVerif(programList, verificado)
    if procedureVerif(programList, verificado)[0] == False:
        verificado = False
    '''
    
   
    if verificado == True:
        return "Correcto"
    
    return 'ESCRIBA BIEN'

def aislarProcedimiento(programList, verificado):
    primeraLinea = programList[0].split(' ',1)
    
    
    if nameVerif(primeraLinea[0]) == False:
        verificado =  False
    
    complementoPrimeraLinea = primeraLinea[1].strip(' ')
    

    if complementoPrimeraLinea[0] != '[':
        verificado = False

    programList[0] = complementoPrimeraLinea
    
    cadena = ''
    for elemento in programList:
        cadena += elemento
   
    
    
    abiertos =0
    cerrados =0
    k=0
    procedimiento=''
    cadena = cadena.replace(' ','')
    
    while k < len(cadena):
        
        
        if cadena[k] == '[':
            abiertos +=1
        if cadena[k] == ']':
            cerrados +=1
        
        
        if abiertos == cerrados and k>0:
            #return cerrados, abiertos, 'b'
            procedimiento = cadena[1:k]
            break
        
        k+=1
    
    return verificarProc(procedimiento,verificado)


def verificarProc(procedimiento, verificado):
    verificado = True 
    if procedimiento[0] != '|':
        verificado=False
    

    abiertos = 0
    j=0
    ultPos=0

    while j< len(procedimiento):
        if procedimiento[j] == '|':
            abiertos +=1
            if abiertos ==2:
                ultPos = j

        if abiertos >2:
            verificado = False
            
            break
        j+=1

    parametrosString = procedimiento[1:ultPos]
    paramList=parametrosString.split(',')
    for param in paramList:
        if nameVerif(param) == False:
            verificado = False
    procedimientoNuevo = procedimiento[ultPos+1:]
    a = procedimientoNuevo.split(";")

    print(procedimientoNuevo)
    return paramList, a

def verifCommandGeneral(procedimiento, verificado, variables):
    comandos = procedimiento.split(";")
    for comando in comandos:
        separarComando = comando.split(":")
        nombreComando = separarComando[0]
        variablesComando1 = separarComando[1].split(",")
        if nombreComando in commands:
            verificarCommand(nombreComando, variablesComando1, verificado, variables)
        ctlStructureB = verifCtlStructure(nombreComando)

def verifCtlStructureGeneral(procedimiento):
    res=False
    lista = procedimiento.split(' ')
    pos = 0
    wordPos = []
    ifInNames = False
    if lista[0] in ctlStructureWords.keys():
        for name in lista:
            if name == 'if:':
                ifInNames = True
            if ifInNames == True:
                if name in ctlStructureWords['if:']:
                    wordPos.append(pos)
            if name in ctlStructureWords.keys():   #esta parte del codigo pone los indices de las palabras de control en wordPos.
                wordPos.append(pos)
            pos +=1
        
    

        
    
            


    



def verificarCommand(nombreComando, variablesComando, verificado, variables):
    if len(variablesComando)==1:
        variable1=variablesComando[0]
    else:
        variable2=variablesComando[1]
    if nombreComando=="move" and (variable1.type()!=int or variable1 not in variables):
        verificado=False
    elif nombreComando=="turn" and variable1 not in directions:
        verificado=False
    elif nombreComando=="face" and variable1 not in lookCommands:
        verificado=False
    elif nombreComando=="movetothe" and (variable2 not in directions or variable1.type()!=int or variable1 not in variables):
        verificado=False
    elif nombreComando=="pick" and (variable1.type()!=int or variable1 not in variables or variable2!="chips" or variable2!="balloon"):
        verificado=False
    elif nombreComando=="put" and (variable1.type()!=int or variable1 not in variables or variable2!="chips" or variable2!="balloon"):
        verificado=False
    elif nombreComando=="moveindir" and (variable2 not in lookCommands or variable1.type()!=int or variable1 not in variables):
        verificado=False
    elif nombreComando=="jumptothe" and (variable2 not in directions or variable1.type()!=int or variable1 not in variables):
        verificado=False
    elif nombreComando=="moveindir" and (variable2 not in lookCommands or variable1.type()!=int or variable1 not in variables):
        verificado=False
    elif nombreComando=="goto" and (variable2.type()!=int or variable1.type()!=int or variable1 not in variables or variable2 not in variables):
        verificado=False
    
    return verificado





#def verifControlStructure():

def verifCommand(string):
    res = False
    if string in commands:
        res = True
    return res



def nameVerif(string:str):
    j=0
    i = len(string)
    if string[0] in alphabet:
        while j < i:
            if string[j].lower() in alphabet or string[j] in numbers:
                return True
    return False

    
   

print(verifyProgram())