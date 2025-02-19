import pandas as pd
import random
from datetime import datetime, timedelta
import requests

# Configurações gerais do dataset
n_linhas = 45000  # Definindo o número de linhas
ids = list(range(101, 101 + n_linhas))

# Função para obter cidades e estados do Brasil via API do IBGE
def obter_cidades_e_estados():
    url = 'https://servicodados.ibge.gov.br/api/v1/localidades/municipios'
    response = requests.get(url)
    if response.status_code == 200:
        municipios = response.json()
        cidades = []
        estados = []
        for municipio in municipios:
            cidades.append(municipio['nome'])
            estados.append(municipio['microrregiao']['mesorregiao']['UF']['sigla'])
        return cidades, estados
    else:
        print("Erro ao obter dados dos municípios.")
        return [], []

# Carregar cidades e estados do Brasil
cidades_lista, estados_lista = obter_cidades_e_estados()

# Dados possíveis para gerar aleatoriamente com proporções ajustadas
idades = [random.randint(18, 60) for _ in range(n_linhas)]
generos = random.choices(["Feminino", "Masculino"], weights=[60, 40], k=n_linhas)

# Gera cidades e estados de forma aleatória, mas mantendo a correspondência
cidades_selecionadas = random.choices(cidades_lista, k=n_linhas)
estados_selecionados = [estados_lista[cidades_lista.index(cidade)] for cidade in cidades_selecionadas]

# Gerar nomes fictícios únicos para cada ID
nomes_masculinos = ["Luiz", "João", "Carlos", "Pedro", "Lucas", "Ricardo", "Fernando", "Mateus", "Henrique", "Tiago"]
nomes_femininos = ["Cristiane", "Maria", "Ana", "Clara", "Fernanda", "Juliana", "Patrícia", "Bianca", "Camila", "Larissa"]
nomes_clientes = []

for i in range(n_linhas):
    if generos[i] == "Masculino":
        nome = nomes_masculinos[i % len(nomes_masculinos)]
    else:
        nome = nomes_femininos[i % len(nomes_femininos)]
    nomes_clientes.append(f"{nome}{ids[i]}")  # Adiciona o ID ao nome para garantir unicidade

# Lista mais diversificada de produtos
produtos_variados = {
    "Eletrônicos": ["Smartphone", "Notebook", "Tablet", "Fone de Ouvido", "Câmera Digital", "Smartwatch"],
    "Vestuário": ["Tênis", "Meia", "Camiseta", "Jaqueta", "Calça", "Boné", "Chinelo", "Vestido", "Blusa"],
    "Acessórios": ["Relógio", "Óculos", "Mochila", "Carteira", "Pulseira", "Colar", "Anel"],
    "Livros e Cultura": ["Livro de Ficção", "Livro de Não-Ficção", "Revista", "Quadrinho"],
    "Beleza e Saúde": ["Shampoo", "Condicionador", "Maquiagem", "Perfume", "Suplemento"],
    "Casa e Decoração": ["Sofá", "Mesa", "Luminária", "Cortina", "Tapete"],
    "Serviços": ["Assinatura", "Transporte", "Curso Online"],
    "Brinquedos": ["Boneca", "Carrinho", "Jogo de Tabuleiro", "Quebra-Cabeça"],
    "Eletrodomésticos": ["Liquidificador", "Micro-ondas", "Aspirador de Pó", "Máquina de Café"]
}
produtos_pesos = {
    "Eletrônicos": 20,
    "Vestuário": 30,
    "Acessórios": 15,
    "Livros e Cultura": 10,
    "Beleza e Saúde": 10,
    "Casa e Decoração": 5,
    "Serviços": 5,
    "Brinquedos": 3,
    "Eletrodomésticos": 2
}

avaliacoes = ["Excelente", "Boa", "Neutra", "Ruim", "Péssimo"]
avaliacoes_pesos = [30, 40, 20, 7, 3]  # Mais clientes avaliam como "Boa" ou "Excelente"
pagamentos = ["Pix", "Crédito", "Débito", "Dinheiro"]
pagamentos_pesos = [40, 30, 20, 10]  # Pix é o mais utilizado

# Expandir os dados para ter cada produto e seu respectivo valor em linhas separadas com avaliações e pagamentos diferentes
expanded_data = []
for i in range(n_linhas):
    cliente_id = ids[i]
    nome = nomes_clientes[i]
    idade = idades[i]
    genero = generos[i]
    cidade = cidades_selecionadas[i]
    estado = estados_selecionados[i]

    # Gerar um número aleatório de produtos que o cliente comprou
    num_produtos = random.randint(1, 6)
    categorias_escolhidas = random.choices(
        list(produtos_variados.keys()),
        weights=[produtos_pesos[cat] for cat in produtos_variados.keys()],
        k=num_produtos
    )
    produtos_comprados = [
        random.choice(produtos_variados[categoria]) for categoria in categorias_escolhidas
    ]
    valores = [round(random.uniform(10, 1000), 2) for _ in produtos_comprados]  # Valores mais realistas
    data_inicial = datetime(2023, 1, 1)
    datas_compras = [data_inicial + timedelta(days=random.randint(0, 365)) for _ in produtos_comprados]

    avaliacoes_aleatorias = random.choices(avaliacoes, weights=avaliacoes_pesos, k=len(produtos_comprados))
    pagamentos_aleatorios = random.choices(pagamentos, weights=pagamentos_pesos, k=len(produtos_comprados))

    for produto, valor, data_compra, avaliacao, pagamento in zip(
        produtos_comprados, valores, datas_compras, avaliacoes_aleatorias, pagamentos_aleatorios
    ):
        expanded_data.append({
            "Nome": nome,
            "ID": cliente_id,
            "Idade": idade,
            "Gênero": genero,
            "Cidade": cidade,
            "Estado": estado,
            "Produto": produto,
            "Valor": f"R${valor:.2f}",
            "Data_Compra": data_compra.strftime("%Y-%m-%d"),
            "Avaliacao": avaliacao,
            "Pagamento": pagamento
        })

# Criar um novo DataFrame com os dados atualizados
df_expanded = pd.DataFrame(expanded_data)

# Definir o caminho do arquivo onde você deseja salvar
file_path = "/home/luiz/Downloads/Projetos_One/machine_learning/dataset_clientes_final.csv"

# Salvar o DataFrame em um arquivo CSV no diretório específico
df_expanded.to_csv(file_path, index=False, encoding="utf-8")

print(f"Arquivo CSV salvo em: {file_path}")