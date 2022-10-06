// Aluno: Gustavo Becelli do Nacimento
#include <stdio.h>
#include <stdlib.h>
#include <limits.h>
#include <stdbool.h>
#include "graph.h"

int main(void)
{

    // Criação do grafo
    Graph *g = read_graph("graph_file.txt");
    printGraph(g);

    // Seleção do vértice inicial
    int v = 0;
    do
    {
        printf("Digite o vertice inicial: [1-%d]\n", g->V);
        scanf("%d", &v);
    } while (v < 1 || v > g->V);
    v -= 1;

    // Procurar o caminho mínimo
    int *r = NULL;

    printf("\nAlgoritmo de Dijkstra:\n");
    r = Dijkstra(g, v);
    // Imprimir o caminho mínimo
    for (int i = 0; i < g->V; i++)
        printf("A distancia de V%d ate V%d e de %d u.m.\n", v + 1, i + 1, r[i]);

    printf("\nPrograma finalizado. Pressione qualquer tecla para sair...");
    return 0;
}
