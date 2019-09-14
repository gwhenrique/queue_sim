## Simulador de fila simples

Para utilizar o simulador, faça um arquivo `*.json`, seguindo o exemplo do `input.json`. . Caso seja desejado que execute somente uma seed, faça uma lista de um elemento.

Caso seja desejado simular uma fila com capacidade infinita, basta omitir o parâmetro `capacity` na declaração da fila.

A declaração de conexões deve ser feita utilizando uma lista com JSONs internamente. Caso deseje somente adicionar uma conexão, faça que nem foi feito com a seed, criando uma lista de um elemento só.

Alguns exemplos foram criados para melhor entendimento do programa e facilidade de testes. Os arquivos foram criados tanto para esta versão do simulador quanto para a versão em Java, por motivos de comparação de resultados.

O simulador foi construído utilizando Python na versão 3.6.4. O simulator não requer dependências externas, dependendo somente da biblioteca principal do Python.

Para executar o simulador, utilize `python Main.py <json_file>`.
