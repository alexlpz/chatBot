# -*- coding: utf-8 -*-

from chatterbot import ChatBot # Importa la clase ChatBot
from chatterbot.trainers import ChatterBotCorpusTrainer
from chatterbot.response_selection import get_most_frequent_response
from chatterbot.comparisons import JaccardSimilarity
from chatterbot.comparisons import LevenshteinDistance
from chatterbot.conversation import Statement
from chatterbot.trainers import ListTrainer


def aprende(inputAnterior, correct_response):
    f = open("./trainer/auto_aprendizaje.yml","a+")
    f.write("\n- - "+inputAnterior+"\n  - "+correct_response)
    f.close()
    trainer.train("./trainer/auto_aprendizaje.yml")
    

def feedback(inputAnterior):
    print("Que debo decir")
    correct_response = Statement(text=input())
    aprende(inputAnterior, correct_response.text)
    
    return "He aprendido algo nuevo"
    
if __name__== "__main__":
    chatbot = ChatBot(  'Emily',
    
    storage_adapter='chatterbot.storage.SQLStorageAdapter',
    response_selection_method=get_most_frequent_response,
    preprocessors=[
        'chatterbot.preprocessors.clean_whitespace',
        'chatterbot.preprocessors.unescape_html',
        'chatterbot.preprocessors.convert_to_ascii'
    ],
    # filters=[filters.get_recent_repeated_responses],
    logic_adapters=[
        # 'chatterbot.logic.MathematicalEvaluation',
        # 'chatterbot.logic.TimeLogicAdapter',
        {
         "import_path": "chatterbot.logic.BestMatch",
            "statement_comparison_function": "chatterbot.comparisons.levenshtein_distance",
            "response_selection_method": "chatterbot.response_selection.get_first_response"
        }
        # {
        #     'import_path': 'chatterbot.logic.SpecificResponseAdapter',
        #     'input_text': 'Puedes ayudarme',
        #     'output_text': 'Claro, ¿Qué puedo hacer por ti?'
        # }
        
    ],
    database_uri='sqlite:///DB/database.sqlite1'
    )

    trainer = ChatterBotCorpusTrainer(chatbot)

    trainer.train("chatterbot.corpus.spanish")
    trainer.train("./trainer/IA.yml")
    trainer.train("./trainer/conversación.yml")
    trainer.train("./trainer/dinero.yml")
    trainer.train("./trainer/emociones.yml")
    trainer.train("./trainer/saludos.yml")
    trainer.train("./trainer/perfilBot.yml")
    trainer.train("./trainer/psicología.yml")
    trainer.train("./trainer/trivia.yml")
    trainer.train("./trainer/cruises_ES.yml")
    trainer.train("./trainer/auto_aprendizaje.yml")
    
    levenshtein_distance = LevenshteinDistance()

    inputAnterior = ""
    aprender = Statement(text="Emily aprende")
    while True:
        try:
            inputUser = Statement(text=input())
            # if "Emily aprende" not in inputUser.text:
            if levenshtein_distance.compare(inputUser,aprender)>0.51:
                print(feedback(inputAnterior.text))
            else:
                bot_output = chatbot.get_response(inputUser)
                print(bot_output)
                inputAnterior=inputUser
                
            
        except(KeyboardInterrupt, EOFError, SystemExit) as e:
            print(e)
            break