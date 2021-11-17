import sys
import platform
import timeit
if platform.system().lower() == "linux":
	import resource
from collections import deque

nos_expandidos = 0
tamanho_fronteira = 0
tamanho_fronteira_max = 0
profundeza_max = 0
tempo_inicio = 0
tempo_fim = 0

class Puzzle:
	def __init__(self, estado, pai = None, caminho = "Inicio", profundeza = 0):
		self.estado = estado
		self.pai = pai
		self.caminho = caminho
		self.custo = 1
		self.profundeza = profundeza

	def expandir(self):
		global nos_expandidos
		nos_expandidos += 1

		filhos = []

		filho_esquerda = self.mover("esquerda")
		if(filho_esquerda != None):
			filhos.append(Puzzle(filho_esquerda, self, "'Left'", self.profundeza + 1))

		filho_cima = self.mover("cima")
		if(filho_cima != None):
			filhos.append(Puzzle(filho_cima, self, "'Up'", self.profundeza + 1))

		filho_direita = self.mover("direita")
		if(filho_direita != None):
			filhos.append(Puzzle(filho_direita, self, "'Right'", self.profundeza + 1))

		filho_baixo = self.mover("baixo")
		if(filho_baixo != None):
			filhos.append(Puzzle(filho_baixo, self, "'Down'", self.profundeza + 1))

		return filhos

	def mover(self, direcao):
		pos = self.estado.index('0')
		filho = self.estado[:]
		if(direcao.lower() == "cima"):
			if(pos > 5):
				return None
			else:
				filho[pos] = filho[pos+3]
				filho[pos+3] = '0'
				return filho
		elif(direcao.lower() == "direita"):
			if(pos % 3 == 0):
				return None
			else:
				filho[pos] = filho[pos-1]
				filho[pos-1] = '0'
				return filho
		elif(direcao.lower() == "baixo"):
			if(pos < 3):
				return None
			else:
				filho[pos] = filho[pos-3]
				filho[pos-3] = '0'
				return filho
		elif(direcao.lower() == "esquerda"):
			if(pos % 3 == 2):
				return None
			else:
				filho[pos] = filho[pos+1]
				filho[pos+1] = '0'
				return filho

def bfs(puzzle):
	fronteira = deque()
	fronteira.append(puzzle)
	explorado = set()
	global tamanho_fronteira
	global tamanho_fronteira_max
	global profundeza_max

	while(len(fronteira) > 0):
		novo = fronteira.popleft()
		tamanho_fronteira = len(fronteira)
		explorado.add(tuple(novo.estado))

		if(novo.estado == ['1','2','3','4','5','6','7','8','0']):
			return novo

		vizinhos = novo.expandir()

		for vizinho in vizinhos:
			if tuple(vizinho.estado) not in explorado:
				fronteira.append(vizinho)

				if vizinho.profundeza > profundeza_max:
					profundeza_max = vizinho.profundeza

		if(len(fronteira) > tamanho_fronteira_max):
			tamanho_fronteira_max = len(fronteira)


	return False	

def resolver(metodo, puzzle):
	global nos_expandidos
	global tamanho_fronteira
	global tamanho_fronteira_max
	global profundeza_max
	global tempo_inicio
	global tempo_fim

	if(metodo.lower() == "bfs"):
		resposta = bfs(puzzle)
	tempo_fim = timeit.default_timer()
	profundeza = resposta.profundeza + 2

	custo_total = 1
	print("path_to_goal: ", end = '[')

	while(resposta.caminho != "Inicio"):
		custo_total += 1
		print(resposta.caminho, end = '')
		if(resposta.pai.caminho != "Inicio"):
			print(end =', ')
		else:
			print(end = ']')

		resposta = resposta.pai

	custo_total += 1

	print()
	print("cost_of_path: " + str(custo_total))
	print("nodes_expanded: " + str(nos_expandidos))
	print("fringe_size: " + str(tamanho_fronteira))
	print("max_fringe_size: " + str(tamanho_fronteira_max))
	print("search_depth: " + str(profundeza))
	print("max_search_depth: " + str(profundeza_max+2))
	print("running_time: " + str(tempo_fim - tempo_inicio))	
	if(platform.system().lower() == "linux"):
		print("max_ram_usage: " + str(format(resource.getrusage(resource.RUSAGE_SELF).ru_maxrss/1000.0, '.8f')))

def main():
	global tempo_inicio
	metodo = sys.argv[1]
	puzzle = sys.argv[2].split(',')

	puzzle = Puzzle(puzzle, None, "Inicio", 0)

	tempo_inicio = timeit.default_timer()

	resolver(metodo, puzzle)

main()