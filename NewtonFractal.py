
from math import cos

def funcao_f(v):
    '''
    funcao f(x) utilizada no metodo de Newton.
    Definida pela variavel global numero de teste.
    Recebe uma lista com dois numeros reais e retorna o valor associado a funcao.
    '''
    if(numero_do_teste == 1):return v[0]**3 -3*v[0]*v[1]**2 - 1
    elif(numero_do_teste == 2):return v[0]**4 -6*v[0]*v[0]*v[1]*v[1] + v[1]**4 -1
    elif(numero_do_teste == 3): return cos(3*v[0]**2)*v[1]
    elif(numero_do_teste == 4): return v[0]**2 + v[1]**2 - 1

def funcao_g(v):
    '''
    funcao g(x) utilizada no metodo de Newton.
    Definida pela variavel global numero de teste.
    Recebe uma lista com dois numeros reais e retorna o valor associado a funcao.
    '''
    if(numero_do_teste == 1): return 3*(v[0]**2)*v[1] -v[1]**3
    elif(numero_do_teste == 2): return 4*v[1]*v[0]**3 - 4*v[0]*v[1]**3
    elif(numero_do_teste == 3): return cos(3*v[1]**2)*v[0]
    elif(numero_do_teste == 4): return v[0] + v[1]

def modulo(v):
    '''
    funcao recebe uma lista (vetor) com dois numeros e retorna a norma (modulo) dessa lista.
    '''
    return (v[0]*v[0] + v[1]*v[1])**(1/2)

def multMatrizes(A,b):
    '''Multiplica uma matriz quadrada nxn por um vetor de tamanho n'''
    return( [sum( A[i][j]*b[j] for j in range(len(A)) ) for i in range(len(A))] )

def subtrai(a,b):
    '''Subtrai dois vetores de mesmo tamanho'''
    return( [a[i]-b[i] for i in range(len(a))] )

def matrizDerivadas(v):
    '''
    Recebe uma lista com dois elementos e retorna uma matriz com as derivadas
    parciais. As derivadas parciais sao realizadas pelo metodo das diferencas
    finitas centrada, para isso usamos a variavel global h.
    '''
    # derivadas parciais mantem uma variável como constante
    del_f_del_x =  (funcao_f([v[0]+h,v[1]])-funcao_f([v[0]-h,v[1]]))/(2*h)
    del_f_del_y = (funcao_f([v[0],v[1]+h])-funcao_f([v[0],v[1]-h]))/(2*h)
    del_g_del_x = (funcao_g([v[0]+h,v[1]])-funcao_g([v[0]-h,v[1]]))/(2*h)
    del_g_del_y = (funcao_g([v[0],v[1]+h])-funcao_g([v[0],v[1]-h]))/(2*h)
    return [[del_f_del_x, del_f_del_y],[del_g_del_x, del_g_del_y]] # retorna matriz de derivadas parciais

def verificaDet(m):
    """
    recebe matriz e retorna valor booleano.
    Se determinante da matriz de entrada eh zero retorna False,
    caso contrario retorna True.
    """
    det = m[0][0]*m[1][1] - m[0][1]*m[1][0] # determinante
    if (det == 0):
        return False
    return True

def inversa(m):
    '''
    Recebe matriz 2x2 e retorna a inversa dessa matriz.
    Somente usamos essa funcao apos verificar se determinante
    eh diferente de zero.
    '''
    det = m[0][0]*m[1][1] - m[0][1]*m[1][0]
    return [[m[1][1]/det,-m[0][1]/det],[-m[1][0]/det,m[0][0]/det]]

def metodoNewton(v0):
    '''
    Essa funcao realiza o metodo de Newton 2D com relacao a um sistema de funcoes
    previamente determinados f(x,y)=0 e g(x,y)=0. Recebe uma lista com dois elementos e retorna a solucao
    do sistema linear e o numero de iteracoes se o metodo de Newton converge, se o numero de iterações maxima
    nao foi ultrapassado e se o determinante da matriz de derivadas for diferente de zero.
    Caso contrario retorna lista com dois elementos obtidos e numero de iteracoes.
    '''
    if(not verificaDet(matrizDerivadas(v0))): return v0,ITMAX+1 # teste determinante = 0
    i=0
    v = subtrai(v0,multMatrizes(inversa(matrizDerivadas(v0)),[funcao_f(v0),funcao_g(v0)]))
    while(modulo(subtrai(v,v0))>tolerancia_epsilon and i <= ITMAX): # enquanto nao converge e o ITMAX nao foi ultrapassado
        v0 = v
        if(not verificaDet(matrizDerivadas(v0))): return v0,ITMAX+1 # teste determinante = 0
        v = subtrai(v0,multMatrizes(inversa(matrizDerivadas(v0)),[funcao_f(v0),funcao_g(v0)])) # obtemos proximo candidato
        i = i + 1
    if(i > ITMAX): return v0,i # temos que pensar aqui... que a saida da função aqui tem que ser um vetor que leva na cor preta
    return v,i # significa que obtemos raiz com numero de iteracoes menor que ITMAX

def atribuiLambda(corRGB,numIter):
    '''
    Recebe a cor associada a raiz obtida e o numero de iteracoes
    realizado pelo metodo de Newton. E multiplica um fator lambda
    definido pelo numero de iteracoes em cada componente do RGB.
    '''
    lista = corRGB.split()
    fator = (ITMAX - numIter)/ITMAX
    for k in range(3): # sempre tem 3 elementos
        lista[k] = round(int(lista[k])*fator)
        lista[k] =  str(lista[k])
    return ' '.join(lista)

def verifica_se_e_raiz(x,y,listaRaizes):
    """
    Recebe a lista mais recente de raizes e  verifica se o ponto analisado
    eh uma das raizes (isso eh feito verificando se a distancia entre eles
    eh menor que um valor definido 0.01). 
    """
    ponto = [x,y]
    for item in listaRaizes:
        if(modulo(subtrai(item,ponto)) < 10**(-2)): return True



#variaveis globais

branco = '255 255 255'
preto = '0 0 0'
vermelho = '255 0 0'
verde = '0 255 0'
azul = '0 0 255'
amarelo = '255 255 0'
laranja = '255 165 0'
violeta = '159 95 159'


x = open('fractal.ppm','w')
x.write('P3\n800 800\n255')

'''Entrada.txt - Leitura das entradas do programa----------------------------'''

y = open('entrada.txt','r')

entrada=[]
for i in y:
    entrada.append(i)

# NUMERO DO TESTE (funcao que vai ser testada)
numero_do_teste = int(entrada[0])

# EXTREMOS DO INTERVALO
extremos_do_intervalo = entrada[1].split(' ')

# Arrumando o ultimo numero pois tem o '\n' do quebra de linha
aux=[]
for i in extremos_do_intervalo[3]:
    if i=='.' or i=='0' or i=='1' or i=='2' or i=='3' or i=='4' or i=='5' or i=='6' or i=='7' or i=='8' or i=='9' : aux.append(i)
aux = ''.join(aux)
extremos_do_intervalo[3] = aux

a = float( extremos_do_intervalo[0] )
b = float( extremos_do_intervalo[1] )
c = float( extremos_do_intervalo[2] )
d = float( extremos_do_intervalo[3] )

# ESPACAMENTO PARA DERIVADA (h)
h = float(entrada[2])

# ESPACAMENTO PARA DERIVADA (h)
aux2 = entrada[3].split(' ')
ITMAX = int(aux2[0])
#TOLERANCIA DO METODO DE NEWTON
tolerancia_epsilon = float(aux2[1])

#NUMERO DE LINHAS E COLUNAS DA IMAGEM
aux3 = entrada[4].split(' ')
N = int( aux3[0] )
M = int( aux3[1] )

'''Fim da leitura das entradas do programa-----------------------------------'''


def adiciona_pixel(cor):
    '''
    Funcao recebe cor associada a raiz obtida e escreve no arquivo.
    '''
    cor = '\n'+cor
    x.write(cor)


def main():
    '''
    funcao principal
    Responsavel por aplicar o metodo de Newton e definir cor ao ponto. Isso eh feito
    fazendo com que a cada raiz diferente obtida seja adicionada a uma lista de raizes.
    E a cada raiz existe uma cor associada em uma lista de cores. Assim, verificamos o
    indice da raiz obtida na lista de raizes e pegamos a cor associada na lista de cores.
    E definimos a aquele ponto a cor multiplicada por um parametro lambda utilizando o
    numero de iteracoes do metodo de Newton.
    '''
    listaRaizes = []
    listaCores = [vermelho,verde,azul,amarelo,laranja,violeta]
    for j in range(N,0,-1):
        for i in range(1,M+1):
            # ponto (x,y) do plano [a,b]x[c,d]
            x = a + (b-a)*(i-1)/M
            y = c + (d-c)*(j-1)/N
            raiz_estimada, IT = metodoNewton([x,y])

            # esses casos sao os que saem do quadrado definido por [a,b]x[c,d] e portanto pintamos eles de preto
            if raiz_estimada[0]<a: IT=ITMAX + 1
            elif raiz_estimada[0]>b: IT=ITMAX + 1
            elif raiz_estimada[1]<c: IT=ITMAX + 1
            elif raiz_estimada[1]>d: IT=ITMAX + 1

            # Perceba que para verificar se eh raiz, somente testamos o numero de iteracoes
            if (IT > ITMAX): # caso em que raiz obtida nao converge
                adiciona_pixel(preto)

            else:# obtemos uma raiz
                raizExistente = False # assumimos que a raiz nao pertence a lista de raizes
                for item in listaRaizes:
                    if(modulo(subtrai(item,raiz_estimada)) < 10**(-1)):
                        raiz_estimada =  item # trocamos o valor da raiz estimada
                        raizExistente = True # eh uma raiz já obtida.
                        break # se ja eh raiz existente nao eh necessario testar outras - isso interrompe o loop

                if (not raizExistente):
                    listaRaizes.append(raiz_estimada) # eh uma raiz nova. entao, coloco na lista

                if( verifica_se_e_raiz(x,y,listaRaizes) ): adiciona_pixel(branco) # verifica 
                else:
                    indiceCor = listaRaizes.index(raiz_estimada) # identifico qual a posicao na lista
                    adiciona_pixel(atribuiLambda(listaCores[indiceCor],IT)) # atribui a cor daquela posição no arquivo
    #print((listaRaizes))
    print("Guilherme Fernandes G. Silva (NUSP: 10297272)\nVictor Yuji Shimabukuro (NUSP: 9876150)")
    print("Raiz | Cor")
    for index in range(len(listaRaizes)):
        cores = ['vermelho','verde','azul','amarelo','laranja','violeta']
        print(listaRaizes[index], "|", cores[index])
main() # executa a funcao principal

x.close() # fecha o arquivo criado
