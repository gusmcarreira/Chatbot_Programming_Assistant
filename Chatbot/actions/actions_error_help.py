from typing import Any, Text, Dict, List
from rasa_sdk import Action, Tracker
from rasa_sdk.executor import CollectingDispatcher
from rasa_sdk.events import SlotSet, FollowupAction
from paths import *

import re

# Action to answer general questions
class ActionEgErrorMessageExample(Action):

    def name(self) -> Text:
        return "action_eg_error_message_example"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:

        error_message = tracker.latest_message["text"]
        regex_string = '(A instrução else não pode ter uma comparação|' \
                       + 'Em uma condição é preciso comparar um par de informações\, mas você escreveu apenas um dado|'\
                       + 'Ao utilizar if ou elif você precisa incluir uma comparação\. Por exemplo\: if x \=\= a\, onde x \=\= a é a comparação|' \
                       + 'Você utilizou um operador and ou or\, mas escreveu eles maiúsculo|' \
                       + 'A comparação de uma condição deve ser feita com dois sinais de \=\= \(igualdade\)\, mas você utilizou apenas um =|' \
                       + 'Em uma condição é preciso incluir : \(dois pontos\) ao término da instrução\. Por exemplo\: if idade \> 18|' \
                       + 'Você esqueceu de um parêntesis na declaração\/uso de uma função|' \
                       + 'Você esqueceu de uma \, \(vírgula\) para separar os parâmetros de uma função|' \
                       + 'Ao criar uma função é preciso incluir \: \(dois pontos\) ao término da instrução\. Por exemplo\: def nome\-funcao\(\)\:|' \
                       + 'Repetições precisam ter um \: no final da linha em que são criadas\. Exemplo\: for x in range\(5\)\:|' \
                       + 'Você utilizou um operador and ou or\, mas escreveu eles em maiúsculo|' \
                       + 'A comparação de um while deve ser feita com dois sinais de \=\= \(igualdade\), mas você utilizou apenas um \=|' \
                       + 'Em uma repetição é preciso incluir \: \(dois pontos\) ao término da instrução\. Por exemplo\: for x in range\(10\)\:|' \
                       + "Em um while é preciso comparar um par de informações, mas você escreveu apenas um dado. Exemplo correto: while x <= 10:|" \
                       + 'Ao utilizar while você precisa incluir uma comparação\. Por exemplo\: while x \<\= 10, onde x \<\= 10 é a comparação|' \
                       + 'Você não utilizou o operador in para iterar sobre uma lista\, array\, range ou string|' \
                       + 'Faltou um par de dados no uso do operador in\. Por exemplo\: for x in range\(2\). Onde\, x e range são os dados necessários para iteração|' \
                       + 'Você escreveu a sintaxe do while sem uma comparação|' \
                       + 'Você esqueceu de abrir ou fechar um parêntesis|' \
                       + 'Você declarou uma string\, mas esqueceu de incluir as duas aspas \(abertura e fechamento\)|' \
                       + 'Você declarou uma variável com número decimal e utilizou \, \(vírgula\) quando deveria ter usado \. \(ponto\)|' \
                       + 'Você declarou uma variável com dois \=\= \(igualdades\) quando deveria ter usado apenas um \=|' \
                       + 'Você utilizou espaço no nome de uma variável e isso não é permitido|' \
                       + 'Você tentou utilizar uma variável que não foi declarada|' \
                       + 'Você utilizou uma condição e está comparando as variáveis\/valores com apenas uma igualdade|' \
                       + 'Você utilizou uma condição e não informou a variável\/valor em uma comparação|' \
                       + 'Você não incluiu o sinal de comparação \(\>\, \<\, \>\=\, \<\=\, \=\= ou \!\=\) na condição|' \
                       + 'Você escreveu uma condição\, repetição ou função e não incluiu os \: \(dois pontos\)|' \
                       + 'Você escreveu uma função ou a chamada à uma função e não colocou o parêntesis de abertura e\/ou fechamento \(\)|' \
                       + 'Você escreveu uma String e não incluiu as aspas corretamente)' \


        real_error_message = re.search(regex_string, error_message).group()
        path_to_answer = dict_error_message[real_error_message]
        explanation = open(path_to_answer, "r").read()

        explanation, suggestions = check_sugestions(explanation)

        dispatcher.utter_message(text=explanation)

        if suggestions:
            dispatcher.utter_message(text="Algumas sugestões:")
            buttons = []
            for option in suggestions:
                payload = ('"' + option + '"')
                buttons.append({"title": option, "payload": payload})
            dispatcher.utter_message(buttons=buttons)


def check_sugestions(wanted_answer):
    split_sugestions = wanted_answer.split("Sugestões:")
    if len(split_sugestions) == 2:
        return split_sugestions[0], split_sugestions[1].split("<sep>")
    else:
        return wanted_answer, None