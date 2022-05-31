from typing import Any, Text, Dict, List
from rasa_sdk import Action, Tracker
from rasa_sdk.executor import CollectingDispatcher
from rasa_sdk.events import SlotSet, FollowupAction
from paths import *

import re
from unidecode import unidecode

# Action to answer general questions
class ActionEgErrorMessageExample(Action):

    def name(self) -> Text:
        return "action_eg_error_message_example"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:

        error_message = tracker.latest_message["text"]
        # Remover ponctuation
        ponctuation = '''!()-[]{};:'"\\,<>./?@#$%^&*_~='''
        for ele in ponctuation:
            if ele in ponctuation:
                error_message = error_message.replace(ele, "")
        # Por tudo em minusculas e remover acentos
        error_message = unidecode(error_message.lower()).replace(" ", "")


        regex_string = '(ainstrucaoelsenaopodeterumacomparacao|' \
                       + 'emumacondicaoeprecisocompararumpardeinformaoesmasvoceescreveuapenasumdado|'\
                       + 'aoutilizarifouelifvoceprecisaincluirumacomparacaoporexemploifxaondexaeacomparacao|' \
                       + 'voceutilizouum operadorandouormasescreveuelesmaiusculo|' \
                       + 'acomparacaodeumacondicaodeveserfeitacomdoissinaisdeigualdademasvoceutilizouapenasum|' \
                       + 'emumacondiçãoeprecisoincluirdoispontosaoterminodainstrucaoporexemploifidade18|' \
                       + 'voceesqueceudeumparentesisnadeclaracaousodeumafuncao|' \
                       + 'voceesqueceudeumavirgulaparasepararosparametrosdeumafuncao|' \
                       + 'aocriarumafuncaoeprecisoincluirdoispontosaoterminodainstrucaoporexemplodefnomefuncao|' \
                       + 'repeticoesprecisamterumnofinaldalinhaemquesaocriadasexemploforxinrange5|' \
                       + 'voceutilizouumoperadorandouormasescreveuelesemmaiusculo|' \
                       + 'acomparacaodeumwhiledeveserfeitacomdoissinaisdeigualdademasvoceutilizouapenasum|' \
                       + 'emumarepeticaoeprecisoincluirdoispontosaoterminodainstrucaoporexemploforxinrange10|' \
                       + "emumwhileeprecisocompararumpardeinformacoesmasvoceescreveuapenasumdadoexemplocorretowhilex10|" \
                       + 'aoutilizarwhilevoceprecisaincluirumacomparacaoporexemplowhilex10ondex10eacomparacao|' \
                       + 'vocenaoutilizouooperadorinparaiterarsobreumalistaarrayrangeoustring|' \
                       + 'faltouumpardedadosnousodooperadorinporexemploforxinrange2ondexerangesaoosdadosnecessariosparaiteracao|' \
                       + 'voceescreveuasintaxedowhilesemumacomparacao|' \
                       + 'voceesqueceudeabriroufecharumparentesis|' \
                       + 'vocedeclarouumastringmasesqueceudeincluirasduasaspasaberturaefechamento|' \
                       + 'vocedeclarouumavariavelcomnumerodecimaleutilizouvirgulaquandodeveriaterusadoponto|' \
                       + 'vocedeclarouumavariavelcomdoisigualdadesquandodeveriaterusadoapenas|' \
                       + 'voceutilizouespacononomedeumavariaveleissonaoepermitido|' \
                       + 'vocetentouutilizarumavariavelquenaofoideclarada|' \
                       + 'voceutilizouumacondicaoeestacomparandoasvariáveisvalorescomapenasumaigualdade|' \
                       + 'voceutilizouumacondicaoenaoinformouavariavelvaloremumacomparacao|' \
                       + 'vocenaoincluiuosinaldecomparaçaoounacondicao|' \
                       + 'voceescreveuumacondicaorepeticaooufuncaoenaoincluiuosdois pontos|' \
                       + 'voceescreveuumafuncaoouachamadaaumafuncaoenaocolocouoparentesisdeaberturaeoufechamento|' \
                       + 'voceescreveuumastringenaoincluiuasaspascorretamente|' \
                       + 'vocetentouutilizarumafuncaoouvariavelquenaoexiste|' \
                       + 'voceestaatribuindoumvaloraumavariavelcomduasigualdadesquandodeveriautilizarapenasumaigualdadeporexemplox2)'

        real_error_message = re.search(regex_string, error_message)

        if real_error_message:
            real_error_message = real_error_message.group()
            for message in dict_error_message:
                tmp_message = unidecode(message).lower()
                for ele in ponctuation:
                    if ele in ponctuation:
                        tmp_message = tmp_message.replace(ele, "")
                if tmp_message.replace(" ", "") == real_error_message:
                    path_to_answer = dict_error_message[message]
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
                    return
        else:
            dispatcher.utter_message(text="Desculpe, ainda não estou preparado para essa mensagem. Assim que possível a adicionarei!")
            dispatcher.utter_message(response="utter_anything_else")
            return [FollowupAction("action_listen")]


def check_sugestions(wanted_answer):
    split_sugestions = wanted_answer.split("Sugestões:")
    if len(split_sugestions) == 2:
        return split_sugestions[0], split_sugestions[1].split("<sep>")
    else:
        return wanted_answer, None