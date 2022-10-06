
#define white 0
#define gray 1
#define black 2

typedef struct edge
{
    int vertex;
    int w;
    struct edge *next;
} Edge;

typedef struct
{
    Edge *neighbors;
} Vertex;

typedef struct
{
    int V;
    int E;
    Vertex *vertex;
} Graph;

Graph *createGraph(int v);
Graph *read_graph(char *filename);
Edge *createEdge(int v, int w);
bool addEdge(Graph *g, int u, int v, int w);
bool isntVisited(Graph *g, bool *Q);
int minimal_distance(Graph *g, bool *Q, int *d);
void relax(Graph *g, int u, int v, int *d, int *pi);
void initValues(Graph *g, int s, int *d, int *pi);
int *Dijkstra(Graph *g, int s);
void print_graph(Graph *g);

// Graph structure related functions
Graph *createGraph(int v)
{
    // Iniciar o grafo
    Graph *g = (Graph *)malloc(sizeof(Graph));
    g->E = 0;
    g->V = v;

    // Alocar memória para os vértices
    g->vertex = (Vertex *)malloc(v * sizeof(Vertex));
    for (int i = 0; i < v; i++)
        g->vertex[i].neighbors = NULL;

    return g;
}

Graph *read_graph(char *filename)
{
    FILE *f;
    f = fopen(filename, "r");

    // read first line && create n vertices in the graph
    char line[100];
    fgets(line, 100, f);
    Graph *g = createGraph(atoi(line));

    // read 3 values in each following line && create an edge between them
    int u, v, w;
    while (fscanf(f, "%d %d %d", &u, &v, &w) != EOF)
        addEdge(g, u - 1, v - 1, w);

    fclose(f);
    return g;
}

Edge *createEdge(int v, int w)
{
    Edge *aux = (Edge *)malloc(sizeof(Edge));
    aux->vertex = v;
    aux->w = w;
    aux->next = NULL;
    return aux;
}

bool addEdge(Graph *g, int u, int v, int w)
{
    // Verificar se o grafo é válido e se os vértices estão dentro dele.
    if (g == NULL)
        return false;
    if (v < 0 || v >= g->V)
        return false;
    if (u < 0 || u >= g->V)
        return false;

    // Criar a aresta
    g->E++;
    Edge *new = createEdge(v, w); // Criar a aresta ligando a v com peso w
    // a aresta tem origem em u
    new->next = g->vertex[u].neighbors; // A aresta é inserida no início da lista de adjacências de u (lista ligada)
    g->vertex[u].neighbors = new;

    return true;
}
// Dijkstra only functions
bool isntVisited(Graph *g, bool *Q)
{
    for (int i = 0; i < g->V; i++) // Percorre todos os vértices e retorna verdadeiro se houver algum Q
        if (Q[i])
            return true;
    return false;
}

int minimal_distance(Graph *g, bool *Q, int *d)
{
    int i;
    // Encontrar um vértice que não tenha sido visitado
    for (i = 0; i < g->V; i++)
        if (Q[i])
            break;

    while (i < g->V)
        if (Q[i])
            break;
        else
            i++;

    // Caso não haja vértice não visitado, retornar -1
    if (g->V == i)
        return -1;

    // Procurar outro vértice que tenha a menor distância
    int lower = i;
    for (i = lower + 1; i < g->V; i++)
        if ((Q[i]) && (d[i] < d[lower]))
            lower = i;
    return lower;
}

// Dijkstra && Minimal Path auxiliar functions
void relax(Graph *g, int u, int v, int *d, int *pi)
{
    // Encontrar a aresta uv
    Edge *aux = g->vertex[u].neighbors;
    while (aux != NULL && aux->vertex != v)
        aux = aux->next;

    // Se a aresta não existir, não há nada a fazer.
    // Se a aresta existir, atualizar a distância do vértice v caso a distância do vértice u for menor que a distância do vértice v
    // printf("d[v] = %d      d[u] = %d e aux[w] = %d\n", d[v], d[u], aux->w);
    if (aux != NULL && d[v] > d[u] + aux->w)
    {
        d[v] = d[u] + aux->w;
        pi[v] = u;
    }
}

void initValues(Graph *g, int s, int *d, int *pi)
{
    // Iniciar o grafo com todas as distâncias infinitas e os vértices sem antecessor
    for (int vertex = 0; vertex < g->V; vertex++)
    {
        d[vertex] = INT_MAX;
        pi[vertex] = -1;
    }
    // A distância do vértice s para ele mesmo é zero
    d[s] = 0;
}

// Função principal para o algoritmo de Dijkstra
int *Dijkstra(Graph *g, int s)
{
    // s =  vértice inicial
    int *d = (int *)malloc(g->V * sizeof(int)); // d[i] = distância do vértice s até o i
    int pi[g->V];                               // pi[i] = vértice anterior ao i
    bool Q[g->V];                               // Q[i] = vértice i ainda não foi visitado?

    for (int i = 0; i < g->V; i++) // Inicializar todos os vértices como não visitados
        Q[i] = true;
    initValues(g, s, d, pi); // Inicializar os valores de d e pi

    while (isntVisited(g, Q)) // Enquanto houver vértices não visitados
    {
        int u = minimal_distance(g, Q, d); // Encontrar o vértice com a menor distância
        Q[u] = false;
        Edge *v = g->vertex[u].neighbors; // Para cada aresta que o vértice u possui
        for (; v != NULL; v = v->next)
            if (Q[v->vertex])
                relax(g, u, v->vertex, d, pi); // Relaxar a aresta u para v
    }
    return d;
}

// função de print
void printGraph(Graph *g)
{
    for (int i = 0; i < g->V; i++)
    {
        printf("Vertice %d possui o(s) vizinho(s):", i + 1);
        Edge *aux = g->vertex[i].neighbors;

        // Para cada aresta que o vértice possui
        while (aux)
        {
            printf(" - Vertice %d (%d)", aux->vertex + 1, aux->w);
            aux = aux->next;
        }
        puts("");
    }
    puts("");
}
