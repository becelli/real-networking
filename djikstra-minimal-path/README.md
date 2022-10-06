O arquivo graph_file.txt armazena o grafo a ser estudado. Ele é composto pela seguinte estrutura:
- A primeira linha é o número de vértices existentes.
- As demais linhas são as conexões, sendo o vértice de origem, de destino e o custo dessa conexão, respectivamente.

Por exemplo:
7 -- há sete vértices existentes
2 4 1 -- Conexão do vértice 2 para o vértice 4 com custo 1.
3 1 2 -- Conexão do vértice 3 para o vértice 1 com custo 2.
...
6 3 2 -- Conexão do vértice 6 para o vértice 3 com custo 2.
...

Para compilar, basta executar o comando comando
```sh
gcc main.c -lm -o dijkstra.bin && ./dijkstra.bin

```
Ou, 
```sh
clang main.c -lm -o dijkstra.bin && ./dijkstra.bin
```