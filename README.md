# DEPÓSITO DE BEBIDAS 🍺
Essa API foi desenvolvida para gerenciar o estoque de um depósito de bebidas: buscar, adicionar, editar e deletar produtos. Ela utiliza Flask e SQLite3 para a manipulação e consulta ao banco de dados e conta com uma documentação OpenAPI integrada.

### DESCRIÇÃO 📜 
O principal objetivo ao criar esse projeto, é que ele realmente pudesse ser usado na vida real. Foram feitas entradas onde coloco o nome, recipiente (em litros), quantidade e valor do produto. Tive o cuidado de não permitir que NOME e RECIPIENTE pudessem ser adicionados duas vezes, pois posso ter duas coca-colas porém uma pode ser de 2L e a outra de 0.6L e são produtos diferentes. Coloquei alguns "Toast" para que as ações feitas durante o uso da API ficasse clara ao usuário.

### PRINCIPAIS RECURSOS 📍
 - CRIAR: está funcionalidade me permite criar um novo produto na tabela.
 - BUSCAR: está funcionalidade me permite buscar os produtos já existentes na tabela.
 - EDITAR: está funcionalidade me permite atualizar produtos já existentes na tabela.
 - DELETAR: está funcionalidade me permite deletar produtos já existentes na tabela.

### Como executar ⚙️
Será necessário ter todas as libs python listadas no `requirements.txt` instaladas.
Após clonar o repositório, é necessário ir ao diretório raiz, pelo terminal, para poder executar os comandos descritos abaixo.

- É fortemente indicado o uso de ambientes virtuais do tipo [virtualenv](https://virtualenv.pypa.io/en/latest/installation.html).

(env)$ pip install -r requirements.txt

Este comando instala as dependências/bibliotecas, descritas no arquivo `requirements.txt`.

Para executar a API  basta executar:

(env)$ flask run --host 0.0.0.0 --port 5000

Em modo de desenvolvimento é recomendado executar utilizando o parâmetro reload, que reiniciará o servidor
automaticamente após uma mudança no código fonte. 

(env)$ flask run --host 0.0.0.0 --port 5000 --reload

Abra o (http://localhost:5000/#/) no navegador para verificar o status da API em execução.
