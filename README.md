# Agent0-minotauro-A-Star
## Feito Por:
- Bruno Brum
- Diogo Carreiro
- Tiago Filipe

## Sobre o projeto:
O projeto Agent0_minotauro permite explorar a interação entre um agente e um ambiente.
O ambiente consiste num tabuleiro retangular de casas quadradas, que podem conter obstáculos, perigos ou objetivos. Para se movimentar neste ambiente, o agente pode deslocar-se em frente ou mudar de direção. O agente, dependendo da sua capacidade, pode também inspecionar o tabuleiro e as suas casas.
O agente pode usar diversos algoritmos para chegar ao seu objetivo. Para os visualizar, é possível marcar as casas com várias cores.
  
A interação entre o agente e o ambiente é comandada através de um cliente e acontece no servidor.

## Como instalar
Para correr o servidor e o cliente, o utilizador deve ter instalada a versão 3 do Python. Além do Python 3, o cliente necessita da biblioteca Pillow
  
### Instalar o Python 3:
 
**Nota: para facilitar a utilização no Windows, o Python deve ser adicionado ao PATH**  
- Windows: https://docs.python.org/3/using/windows.html  
- Mac: https://docs.python.org/3/using/mac.html  
- Linux: https://docs.python.org/3/using/unix.html#on-linux  
  
### Instalar a biblioteca Pillow:
  Após instalar o Python, executar na linha de comandos:  
    ```python3 -m pip install --upgrade pip```  
    ```python3 -m pip install --upgrade Pillow```  

## Como correr:
### Para correr o servidor:  
Na linha de comandos, **a partir do diretório principal do projeto**, executar:  
    ```python3 server/main.py```  
  
### Para correr o cliente:  
Na linha de comandos, **a partir do diretório principal do projeto**, executar:  
    ```python3 client/client.py```  

### Para correr um agente (que faz uso do cliente):  
Na linha de comandos, **a partir do diretório principal do projeto**, executar, por exemplo:  
    ```python3 client/example.py```  

## Como comandar o agente:  
Ao correr o client.py o utilizador consegue dar inputs para o movimento do agente através do input "command" seguido de : 
"forward" movimenta o nosso agente para a sua frente;"backward" movimenta o agente para trás;"left" e "right" altera a direção 
onde o agente está voltado para esquerda e direita respetivamente.
Através do input "info" e seguido de: "direction" é nos dado a direção para onde o agente está voltado atualmente;
"view" retorna uma descrição do objeto em frente do agente;"weights" retorna os pesos do node em frente do agente;
"map" retornam os pesos de todos os nodes no mapa;"obstacles" retornam os obstáculos não invisíveis presentes no mapa;
"goal" retorna a posição do node objetivo;"position" retorna a posição x,y atual do agente.

Existe outros commandos para o agente estes não são tão importantes e não foram usados na resolução do algoritmo.

### Para correr o agente(uso do cliente) usando algoritmo A*:
Na linha de comandos, a partir do diretório principal do projeto, executar, por exemplo:
    
  ```python3 client/search_run_A_star.py```

Aqui, será feita uma pesquisa tendo em conta os obstáculos visíveis e invisíveis. Para além disto, o agente irá arranjar o caminho de menor custo, sendo este custo a soma dos custos de transição com a distância dos nodes ao Goal(destino).  

## Como configurar:  
A configuração do ambiente e do agente é feita no ficheiro **config.json**, através da alteração dos valores associados a cada string.  
  
## Erros conhecidos:  
A interface gráfica do servidor bloqueia enquanto espera pela conexão do cliente. No Windows, por exemplo, é necessário fechar o programa à força caso se queira terminá-lo antes de conectar o cliente.

## Contribuidores do Codigo Base(sem A*):
 - Gil Silva
 - José Cascalho
