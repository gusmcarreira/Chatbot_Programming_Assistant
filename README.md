# Chatbot_Programming_Assistant
Chatbot criado na plataforma RASA para assistir alunos na introdução à Programação. Projeto desenvolvido no contexto de tese de mestrado na Universidade de Coimbra.

## Índice
* [1. Leonardo](#leonardo)
* [2. Chatbot FrontEnd](#chatbot_frontend)
* [3. Erro de Sintaxe](#erros_sintaxe)
  * [3.1. Localização dos ficheiros](#erros_sintaxe_localizacao)
  * [3.2. Explicação dos ficheiros](#errors_sintaxe_explicacao)
    * [3.2.1 Ficheiros com os caminhos](#ficheiros_caminhos)
    * [3.2.2 Ficheiros com as perguntas](#ficheiros_perguntas)
* [4. Resposta Automática](#resposta_automatica)
* [5. Dados de treino](#dados_treino)
    * [5.1. Possíveis frases dos estudantes](#perguntas_possiveis)
    * [5.2. Respostas](#respostas)
* [6. Deploy](#deploy)
* [7. Problemas TODO](#problemas)
* Erros Lógicos

<a id="leonardo"></a>
## 1. Leonardo
* [Verificar se concorda com as questões que defini e verificar a linguagem usada](#erros_sintaxe)
* [Integrar o componente do chatbot (mais informações no README)](https://github.com/gusmcarreira/Chatbot_Front_End)
* [Base de dados (store da informação pertinente)??](https://github.com/gusmcarreira/Chatbot_Front_End)

<a id="chatbot_frontend"></a>
## 2. Chatbot FrontEnd
Código disponivel em:

* https://github.com/gusmcarreira/Chatbot_Front_End

<a id="erros_sintaxe"></a>
## 3. Erro de Sintaxe

<a id="erros_sintaxe_localizacao"></a>
### 3.1 Localização dos ficheiros
```
├── Chatbot
│   ├── actions
│   ├── custom
│   │   ├── Docs
│   │   │   └── ErrorGuidance
│   │   │   │  └── ...
│   ├── ...
├── ...
```
Há dois tipos de ficheiros, ambos separados por __tipo de erro (Função, Varáivel, Repetição, Condição)__:
* [Os ficheiros que contém os caminhos das perguntas para o erro](https://github.com/gusmcarreira/Chatbot_Front_End)

São os ficheiros de texto que estão diretamente na pasta __ErrorGuidance__
```
├── Chatbot
│   ├── actions
│   ├── custom
│   │   ├── Docs
│   │   │   └── ErrorGuidance
│   │   │   │  └── Condição.txt
│   │   │   │  └── Função.txt
│   │   │   │  └── Repetição.txt
│   │   │   │  └── Variável.txt
│   ├── ...
├── ...
```
* [Os com as perguntas para os erros](https://github.com/gusmcarreira/Chatbot_Front_End)

São os ficheiros de texto que estão __dentro das pastas__ na pasta __ErrorGuidance__
```
├── Chatbot
│   ├── actions
│   ├── custom
│   │   ├── Docs
│   │   │   └── ErrorGuidance
│   │   │   │  └── Condição
│   │   │   │  │   └── ...txt
│   │   │   │  └── Função
│   │   │   │  │   └── ...txt
│   │   │   │  └── Repetição
│   │   │   │  │   └── ...txt
│   │   │   │  └── Variável
│   │   │   │  │   └── ...txt
│   ├── ...
├── ...
```
<a id="errors_sintaxe_explicacao"></a>
### 3.2 Explicação dos ficheiros
* A alteração das perguntas não tem qualquer implicação no código nem no chatbot (ou seja não precisa de ser treinado), desde que siga as regras explicadas [aqui](#ficheiros_perguntas)
* Se alterar a escrita de uma mensagem de error, terá de alterar também o ficheiro onde aponta para o caminho das suas perguntas [aqui](#ficheiros_caminhos)

<a id="ficheiros_caminhos"></a>
#### 3.2.1 Ficheiros com os caminhos

```
Condição sem comparação-->Condição/semComparacao.txt
-###-
Operador lógico maiúsculo-->Condição/andOrMaiusculo.txt
```

* O nome do ficheiro de texto tem de coincidir __exatamente__ com o tipo de erro enviado pela plataforma
* Os caminhos são separados por __-###-__
* As linhas resultam da conjunção de três elementos:
  * mensagem de erro retornada pela plataforma (i.e. Condição sem comparação)
  *  --> 
  *  o caminho para o ficheiro com as perguntas para o determinado erro (i.e. Condição/semComparacao.txt)

<a id="ficheiros_perguntas"></a>
#### 3.2.2 Ficheiros com as perguntas

```
Pergunta:O seu erro parece estar numa condição. Vou-lhe propor um desafio! Dado o seguinte código:

<code>
x = 0

if x ==  :
  print("É verdade!")
</code>

Que é suposto gerar a seguinte saida:

<code_print>É verdade!

Qual é o detalhe que está em falta?<end>
----------------------------------------------------------------------------------<end>
Resposta:0<sep>um zero<sep>zero<end>
----------------------------------------------------------------------------------<end>
Explicação:No código acima falta o segundo dado da comparação, que neste caso é um 0!<end>
----------------------------------------------------------------------------------<end>
-###-
----------------------------------------------------------------------------------<end>
Checkpoint:Quando fazemos uma comparação necessitamos de dois dados, no caso do exemplo temos o x e o número 0!

Agora olhando para o seu algoritmo veja se sempre usou dois dados nas suas comparações e não se esqueceu te nenhum!<end>
```

Os __conjuntos de perguntas__ são compostos pelos seguites tópicos:
* __Pergunta:__ (obrigatória) contém a pergunta que o Chatbot vai retornar ao aluno  
* __Resposta:__ (obrigatória) resposta à pergunta
    * Pode conter mais que uma resposta (formas diferentes de dizer), que devem ser separadas por __\<sep\>__
* __Explicação:__ (obrigatória) contém a explicação da resposta à pergunta
* __Opções_Iniciais:__ (opcional) se presente são as opções de escolha múltipla que são apresentadas aos alunos logo no inicio
    * As opções devem ser separadas por __\<sep\>__
* __Opções:__ (opcional) se presente são as opções de escolha múltipla que são apresentadas aos alunos quando estes erram a resposta
    * As opções devem ser separadas por __\<sep\>__    
    
Ou apenas pelo:
* __Checkpoint:__ (obrigatória) simboliza a última pergunta que contém uma espécie de conclusão

ATENÇÃO:
* Cada conjunto de perguntas, ou seja, cada groupo de Pergunta, Resposta, Explicação,..., deve ser separado por __-###-__
* Cada tópico deve terminar com um __\<end>__
* O display de __código__ é simbolizado por __\<code>__ e __\</code>__
* O display dos resultados dos códigos é simbolizado com __\<code_print>__ (apenas abertura)
* No mesmo tópico para fazer o display da mensagem em __balões de mensagem separados__, as frases devem ser separadas por uma __linha em branco__
* As linhas compostas por -----------, são apenas usadas para diferenciar (como comentários), pode ser usado qualquer coisa desde que não começe como nenhum dos outros tópicos e seja finalizado por __\<end>__

<a id="resposta_automatica"></a>
## 4. Resposta Automática
* A alteração dos ficheiros implica correr o ficheiro em [Chatbot/custom/Docs/Whoosh/index_documents.py](https://github.com/gusmcarreira/Chatbot_Programming_Assistant/tree/main/Chatbot/custom/Docs/Whoosh/index_documents.py)
* A sua alteração não implica voltar a treinar o Chatbot
* Os ficheiros estão separados por pastas
* Precisam ainda de uma grande melhoria

Os documentos estão [aqui](https://github.com/gusmcarreira/Chatbot_Programming_Assistant/tree/main/Chatbot/custom/Docs/Whoosh/MyDocuments)
```
├── Chatbot
│   ├── ...
│   ├── custom
│   │   ├── Docs
│   │   │   └── ...
│   │   │   └── Whoosh
│   │   │   │  └── ...
│   │   │   │  └── MyDocuments
│   │   │   │  │   └── AQUI
│   │   │   │  └── ...
│   ├── ...
├── ...
```

```
Uma variável em Python é uma forma de associar um nome a um valor. Pense em cada variável como uma caixa que guarda algo e que podemos a qualquer momento ir nela para recuperá-lo. Na programação, o que será guardado nas variáveis são dados necessários aos nossos programas.

Exemplo:

<code>
base = 2
altura = 5
area = (base * altura) / 2
print(area)
</code>

<code_print> 5.0

No exemplo acima, criamos uma variável chamada base à qual atribuímos o valor 2, uma variável altura, à qual atribuímos o valor 5, e uma variável area, à qual atribuímos um cálculo envolvendo a base e a altura. 

O sinal de igualdade é necessário para dar a entender ao computador que você deseja criar uma variável e armazenar um dado nela.
-#-
```

* Ao referir-me a bloco, quero dizer o bloco de informação que vai ser retornado ao estudante, onde o modelo diz estar a resposta (ao invés de retornar apenas a resposta).
* Cada bloco é separado por __-#-__
* Para separar as mensagens em vários balões, introduzir uma linha em branco entre as respetivas frases.
* O aluno pode também pedir por exemplos, pelo que os determinados blocos de código devem conter uma linha com __Exemplo:__, seguida por código entre __\<code></code>__ e se pretendido o seu resultados __\<code_print>__

<a id="dados_treino"></a>
## 5. Dados de treino
A modificação de qualquer destes dados requer voltar a treinar o Chatbot, e voltar a correr os servidores:
```
rasa train
```

<a id="perguntas_possiveis"></a>
### 5.1. Possíveis frases dos estudantes
As frases de treino a simbolizar as frases que o aluno poderá mandar ao Chatbot em [Chatbot/data/nlu.yml](https://github.com/gusmcarreira/Chatbot_Programming_Assistant/tree/main/Chatbot/data/nlu.yml).

<a id="respostas"></a>
### 5.2. Respostas
As frases que são retornada pelo Chatbot estão em [Chatbot/domain.yml](https://github.com/gusmcarreira/Chatbot_Programming_Assistant/tree/main/Chatbot/domain.yml).

<a id="deploy"></a>
## 6. Deploy

__Só copiar o ficheiro e correr__

Atenção o ficheiro faz clone do git
```
sh deploy.sh
```

<a id="problemas"></a>
## 7. Problemas TODO (Gustavo)
* Respostas automáticas precisa de uma GRANDE melhoria 
* Apenas fazer scroll depois do estudante ter visto, em vez de ir logo para baixo (tentei de várias maneiras mas ainda não consegui)
* Erros lógicos...
* Questionário
