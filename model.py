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

alphabet = [
    'a','b','c','d','e','f','g','h','i','j','k','l','m','n','o','p','q','r','s','t','u','v','w','x','y','z'
]

numbers = [
    '1','2','3','4','5','6','7','8','9','0'
]
#Lista de comandos para la instrucción Look
lookCommands = {
    'N' : True,
    'E' : True,
    'W' : True,
    'S' : True
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
                    print(nombre[0])
                    verificado = False
                for character in nombre:        #revisa que los nombres solo contengan letras o numeros
                    if character.lower() not in alphabet and character not in numbers:
                        verificado = False
        if i==2:
            if programList[2] != 'PROCS':
                verificado = False
                
        
        i+=1

    print(programList)
    if verificado == True:
        return "Correcto"

    return 'ESCRIBA BIEN'
   

print(verifyProgram())