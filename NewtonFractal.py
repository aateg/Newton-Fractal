def funcao_f(v):
    return v[0]**3 -3*v[0]*v[1]**2 - 1

def funcao_g(v):
    return 3*(v[0]**2)*v[1] -v[1]**3
    
def modulo(v):
    return (v[0]*v[0] + v[1]*v[1])**(1/2)
    
def multMatrizes(A,b):
    '''Multiplica uma matriz quadrada nxn por um vetor de tamanho n'''
    # creditos BRUNO haha
    return( [sum( A[i][j]*b[j] for j in range(len(A)) ) for i in range(len(A))] )
    
def subtrai(a,b):
    '''Subtrai dois vetores de mesmo tamanho'''
    return( [a[i]-b[i] for i in range(len(a))] )
    
def matrizDerivadas(v,h=10**(-4)):
    ''' Parâmetro h é pra fazer a derivada por diferenças finitas centrada '''
    # derivadas parciais mantem uma variável como constante
    del_f_del_x =  (funcao_f([v[0]+h,v[1]])-funcao_f([v[0]-h,v[1]]))/(2*h)
    del_f_del_y = (funcao_f([v[0],v[1]+h])-funcao_f([v[0],v[1]-h]))/(2*h)
    del_g_del_x = (funcao_g([v[0]+h,v[1]])-funcao_g([v[0]-h,v[1]]))/(2*h)
    del_g_del_y = (funcao_g([v[0],v[1]+h])-funcao_g([v[0],v[1]-h]))/(2*h)
    return [[del_f_del_x, del_f_del_y],[del_g_del_x, del_g_del_y]] # retorna matriz de derivadas parciais

def inversa(matrix):
    '''  Recebe matriz 2x2 e devolve a inversa dessa matriz'''
    m = matrix
    det = m[0][0]*m[1][1] - m[0][1]*m[1][0] # determinante
    if (det == 0):
        return [100,100]
    return [[m[1][1]/det,-m[0][1]/det],[-m[1][0]/det,m[0][0]/det]] 
    
def metodoNewton(v0):
    '''
    Essa função realiza o método de Newton 2D com relação a um sistema de funções
    previamente determinados. Recebe uma lista com dois elementos e retorna a raiz 
    do sistema linear se o método de Newton converge e se o número de iterações máxima
    não foi ultrapassado. Caso contrário retorna valor default.
    '''
    # seja v = x_{k+1} do metodo de newton
    i=0
    ITMAX = 40 # numero de iteracoes maxima
    v = subtrai(v0,multMatrizes(inversa(matrizDerivadas(v0)),[funcao_f(v0),funcao_g(v0)]))
    while(modulo(subtrai(v,v0))>10**(-5) and i < ITMAX):
        v0 = v 
        v = subtrai(v0,multMatrizes(inversa(matrizDerivadas(v0)),[funcao_f(v0),funcao_g(v0)]))
        i = i + 1
    if(i > ITMAX): return [100,100],i # temos que pensar aqui... que a saida da função aqui tem que ser um vetor que leva na cor preta
    return v,i   

def atribuiLambda(corRGB,numIter):
    '''
    multiplica um fator lambda em cada componente do RGB
    '''
    lista = corRGB.split()
    fator = (ITMAX - numIter)/ITMAX
    for k in range(3): # sempre tem 3 elementos
        lista[k] = round(int(lista[k])*fator)
        lista[k] =  str(lista[k])
    return ' '.join(lista)
    
        
#variaveis globais
ITMAX = 40 #NUMERO MAX DE ITERAÇÕES
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

def adiciona_pixel(cor):
	cor = '\n'+cor
	x.write(cor)

    
def main():
    N=800
    M=800
    a=-0.7
    b=1.1
    c=-1
    d=1 
    listaRaizes = []
    listaCores = [vermelho,verde,azul,amarelo,laranja,violeta,violeta,violeta,violeta,violeta,violeta,violeta,violeta,violeta,violeta,violeta,violeta,violeta,violeta,violeta,violeta,violeta,violeta,violeta,violeta,violeta,violeta,violeta,violeta,violeta,violeta,violeta,violeta,violeta,violeta,violeta,violeta,violeta,violeta,violeta,violeta,violeta,violeta,violeta,violeta,violeta,violeta,violeta,violeta]
    for i in range(N):
        for j in range(M):
            x = a + (b-a)*(i-1)/M
            y = c + (d-c)*(j-1)/N
            raiz_estimada, IT = metodoNewton([x,y])
            #print(IT)
            
            if raiz_estimada[0]<a: IT=ITMAX
            elif raiz_estimada[0]<b: IT=ITMAX
            elif raiz_estimada[1]<c: IT=ITMAX
            elif raiz_estimada[1]>d: IT=ITMAX
            
            if IT > ITMAX:  
                adiciona_pixel(preto)
                #print(preto)
            else:# obtemos uma raiz
                raizExistente = False # assumimos que a raiz não pertence a lista de raizes
                for item in listaRaizes: 
                    if(modulo(subtrai(item,raiz_estimada))<10**(-3)):
                        raiz_estimada =  item
                        raizExistente = True # eh uma raiz já obtida.
                        # sai do loop PENSAR EM COMO SAIR DO LOOP QUANDO ESSA CONDIÇÃO JÁ FOR SATISFEITA
                if (not raizExistente): listaRaizes.append(raiz_estimada) # eh uma raiz nova. então, coloco na lista
                indiceCor = listaRaizes.index(raiz_estimada) #identifico qual posição
                adiciona_pixel(atribuiLambda(listaCores[indiceCor],IT)) # atribui cor aquela posição
                #print(listaCores[indiceCor]) 
              
                
              	
main()
  
  
  
    



x.close()


