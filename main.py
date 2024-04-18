
import random, time

from random import shuffle
import re
from collections import defaultdict, deque

tamanho_adj = {}
coloracao_vertice = {}


def parse_grammar(grammar_text):
  adj = {}
  tamanho_grafo=0
  lines = grammar_text.split('\n')
  for line in lines:
    if not line.strip():
      continue
    linha = re.split(r'[,\s]+', line)
    left = linha[0]
    right = linha[1]
    if left not in adj:
      tamanho_grafo += 1
      adj[left] = set()
      tamanho_adj[left] = 0
      coloracao_vertice[left] = set()
      coloracao_vertice[left] = 0
    if right not in adj:
      tamanho_grafo += 1
      adj[right] = set()
      tamanho_adj[right] = 0
      coloracao_vertice[right] = set()
      coloracao_vertice[right] = 0
    adj[left].add(right)
    tamanho_adj[left] += 1
    adj[right].add(left)
    tamanho_adj[right] += 1
  return adj , tamanho_grafo


def read_grammar_file(file_path):
  with open(file_path, 'r') as file:
    grammar_text = file.read()
  return parse_grammar(grammar_text)


def shuffle_dict_keys(dicionario):
  chaves_embaralhadas = list(dicionario.keys())
  random.shuffle(chaves_embaralhadas)
  return {chave: dicionario[chave] for chave in chaves_embaralhadas}


def color_graph(ordem):
  for i in ordem:
    cores_vizinhos = set()

    for vizinho in ordem[str(i)]:
      if(coloracao_vertice[str(vizinho)] != 0):
        cores_vizinhos.add(coloracao_vertice[str(vizinho)])
        
    cor_atual = 1
    while cor_atual in cores_vizinhos:
        cor_atual += 1
      
    coloracao_vertice[str(i)] = cor_atual

    
    


def shift_porcentagem(ordem, porcentagem):
  tamanho_porcentagem = int(round(len(ordem) * (porcentagem % 100) /
                                  100))  # Determina o tamanho do shift
  novo_ordem = ordem[
      tamanho_porcentagem:] + ordem[:tamanho_porcentagem]  # Realiza o shift
  return novo_ordem  # Retorna o novo vetor


def swap_porcentagem(ordem, porcentagem):
  num_elementos = len(ordem)
  num_trocas = int(round(num_elementos * (porcentagem % 100) /
                         100))  # Determina o número de trocas

  novo_ordem = ordem[:]  # Cria uma cópia do vetor para evitar modificação do original

  for i in range(num_trocas):
    indice1 = i
    indice2 = num_elementos - i - 1
    novo_ordem[indice1], novo_ordem[indice2] = novo_ordem[indice2], novo_ordem[
        indice1]  # Realiza a troca

  return novo_ordem  # Retorna o novo vetor

def colore_min(grafo,vertice_inicial):
      
      for vertice in coloracao_vertice:
        coloracao_vertice[vertice] = 0
      fila = deque([vertice_inicial])
      visitados = set()
      while fila:
          vertice = fila.popleft()
          cores_vizinhos = set()

          for vizinho in grafo[str(vertice)]:
            if(coloracao_vertice[str(vizinho)] == 0):
              fila.append(vizinho)
            elif(coloracao_vertice[str(vizinho)] != 0):
              cores_vizinhos.add(coloracao_vertice[str(vizinho)])
          if vertice not in visitados:
            visitados.add(vertice)
          cor_atual = 1
          while cor_atual in cores_vizinhos:
              cor_atual += 1

          coloracao_vertice[str(vertice)] = cor_atual
  
  
  

def coloracao_minima_dicionario(grafo, vertice_inicial):
  # Dicionário para armazenar as cores de cada vértice

  cores = {}
  
  # Fila para BFS
  fila = deque()
  
  # Realiza a BFS a partir de cada vértice
  for vertice in grafo:
      # Adiciona o vértice à fila para iniciar a BFS
      fila.append(vertice_inicial)
  
      while fila:
          vertice_atual = fila.popleft()
  
          # Encontra a próxima cor disponível para o vértice atual
          proxima_cor_disponivel = 0
          vizinhos_coloridos = set()
          for vizinho in grafo[str(vertice_inicial)]:
              if vizinho in cores:
                  vizinhos_coloridos.add(cores[vizinho])
  
          while proxima_cor_disponivel in vizinhos_coloridos:
              proxima_cor_disponivel += 1
  
          # Pinta o vértice atual com a próxima cor disponível
          cores[vertice_atual] = proxima_cor_disponivel
  
          # Adiciona os vizinhos do vértice atual à fila
          for vizinho in grafo[str(vertice_atual)]:
              if vizinho not in cores:
                  fila.append(vizinho)
  
  return cores, len(set(cores.values()))

# ========================================
# Tratar a entrada e salvar como um dicionário... não teremos mais uma matriz
#  - No ajuste da entrada, já calcular de uma vez o grau (ou algum outro parâmetro que precisar) e salvar no dicionário
# Ajustar oq já foi feito para funcionar com a estrutura do dicionário
# implementar a função gulosa
#  - Ordenar os vértices do dicionário e o vetor solução será a lista de vértices ordenados
#  - Saída vai ser um dicionário do vértice referenciando uma cor e a quantidade de cores
# Função da heurística que estavamos fazendo na primeira vez
#  - Ler qual será o vértice inicial
#  - Implementar uma busca em largura a partir do vértice inicial
#  - A partir da busca em largura, implementar um método para colorir os vértices
#  - Saída vai ser um dicionário do vértice referenciando uma cor e a quantidade de cores (***Só interessa a melhor saída)
# =======================================

# Define uma semente de acordo com o tempo atual para garantir que seja diferente a cada execução

def bfs(graph, start):
    visited = set()
    queue = deque([start])
    subgraph = {}

    while queue:
        vertex = queue.popleft()
        if vertex not in visited:
            visited.add(vertex)
            subgraph[vertex] = graph[vertex]
            queue.extend(graph[vertex] - visited)
    
    return subgraph

def find_disconnected_subgraph(graph):
    visited = set()
    disconnected_subgraphs = []

    for vertex in graph:
        if vertex not in visited:
            subgraph = bfs(graph, vertex)
            disconnected_subgraphs.append(subgraph)
            visited.update(subgraph)

    return disconnected_subgraphs


def main():
  inicio = time.time()
  grammar_file = 'dataset3.txt'
  ordem, menor_cores = read_grammar_file(grammar_file)
  
  solucao = shuffle_dict_keys(ordem)
  tam_grafo = len(solucao)
  print("==============================================")
  # print("ordem: ", ordem)
  # print("solucao: ", solucao)
  color_graph(solucao)  #Passando a solução... solução é a ordem embaralhada
  # print("\nColoração Vértices: ", coloracao_vertice)
  print("\nNúmero de Vértices: ", menor_cores)
  print("\nNúmero de Cores: ", max(coloracao_vertice.values()))
  
  

  for vertice in solucao: 
    # Marca o tempo inicial 
    print(vertice)
    

    tempo_inicial = time.time()
    colore_min(solucao, vertice)
    # Marca o tempo final
    tempo_final = time.time()
    # Calcula o tempo de execução
    tempo_decorrido = tempo_final - tempo_inicial
    cores_total =  max(coloracao_vertice.values())
    
    #minimo de cores
    if cores_total < menor_cores:
       menor_cores = cores_total
       tempo = tempo_decorrido
       vetorResultado = coloracao_vertice
    
  print("Vetor de cores:")
  print(vetorResultado)
  print("Menor quantidade de cores: ", menor_cores)
  # Imprime o tempo decorrido
  
  # disconnected_subgraphs = find_disconnected_subgraph(ordem)
  # for i, subgraph in enumerate(disconnected_subgraphs, 1):
  #     print(f"Subgrafo desconectado {i}: {subgraph}")

  fim = time.time()
  tempo_total = fim - inicio
  print("\nTempo de execução: ", tempo_total, "segundos")

if __name__ == "__main__":
  main()
