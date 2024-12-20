from config.config import cohere_client
from app.services.embedding_handler import prompt_query, generated_query
import re



def context_analysis(question):

    # Verificar si se puede responder con el contexto
    
    prompt_context = f""" 
        La consulta no estara en el mismo idioma que el contexto. 
        Piensa la consulta al inglés para poder responder.
        La CONSULTA se puede responder con el CONTEXTO? 
        Responde únicamente con 'SI' o 'NO'.

        CONTEXTO:
        {prompt_query(question)}

        CONSULTA:
        {question}

        Respuesta:
        """
    
    system_prompt_principal = """Tu tarea es analizar toda la información disponible 
                                 en el contexto. Solo debes responder con monosilabos, responder SI o NO"""
    
    response_context = cohere_client.chat(
            model="command-r-plus-08-2024",
            messages=[{"role": "system", "content": system_prompt_principal},
                      {"role": "user", "content": prompt_context}],
                      seed = 28
            )
    context_check = response_context.message.content[0].text


    return context_check
    


def groundedness_analysis(question):

    prompt_principal = f""" 
            Responde la solicitud siguiendo las instrucciones y basandote en la informacion brindada por el contexto.
            
            ###
            Instrucciones:
            -Piensa la Pregunta en ingles para responder pero no la incluyas en tu respuesta.
            -Responde en ingles.
            -Relaciona la metadata con el contexto.
            -Utiliza metadata para poder citar a los autores adecuados en formato APA dentro del texto.
            -Utiliza la abreviacion et al. para cuando tengas más de dos autores.
            -No listes las referencias
        

            ###
            Contexto:
            {prompt_query(question)['documents']}

            ###
            Metadata:
            {prompt_query(question)['metadatas']}

            ###
            Pregunta:
            {question}

            ###
            Respuesta:
            
            
            ###
            Ejemplo:
            Pregunta: ¿Que es una lipasa?
            Respuesta: Enzymes are proteins that act as catalysts in chemical reactions within organisms (Smith, 2020; Pérez, 2019). Santos et al. clarifies that they are essential to accelerate and regulate various biological functions, such as digestion and the synthesis of molecules (Santos et al., 2023).
            """

    system_prompt_principal = """Tu tarea es responder la solicitud
                               utilizando los documentos brindados y metadata. 
                               Tu respuesta será introducida en un texto cientifico.
                               Solo debes incorporar información respaldada"""
    response = cohere_client.chat(
            model="command-r-plus-08-2024",
            messages=[{"role": "system", "content": system_prompt_principal},
                     {"role": "user", "content": prompt_principal}],
                    seed = 42,
                    temperature = 0.2
                        )
        
    answer = response.message.content[0].text

        

    #Separar la respuesta en oraciones
    sentences_generated = re.split(r'(?<=[.!?]) +', answer)
    

    grounded_count = 0
    threshold = 0.75  # Umbral para considerar una afirmación como respaldada

    for sentence_generated in sentences_generated:
        # Buscar en la colección
        result = generated_query(sentence_generated)
    
        # Verificar la similitud máxima
        max_score = result["distances"][0][0]
        
    
        if (1-max_score) > threshold:
            grounded_count += 1
        
    # Calcular la groundedness
    groundedness = round(grounded_count / len(sentences_generated),2)

    return groundedness, answer

def traductor(answer):
    prompt_idioma = f""" 
            ###
            Instrucciones:
            -Traduce al español el texto aportado sin perder la información de cita de autores. 
            -Manten la expresión "et al."         
                
            Texto: {answer}
    
            Tu respuesta debe ser solamente la traduccion, sin incluir el idioma identificado.
                """
    
    response = cohere_client.chat(
                model="c4ai-aya-expanse-32b",
                messages=[
                     {"role": "user", "content": prompt_idioma}],
                     seed = 42
                 )
        
    respuesta_al_usuario = response.message.content[0].text

    return respuesta_al_usuario


def RAG_answer(question):
    """Ejecuta flujo para la estrategia del promt

    Parameters
    ----------
    question : str
        Pregunta del usuario
    """
    respuesta_analizador_consulta = context_analysis(question)

    if respuesta_analizador_consulta == 'SI':
        groundedness = groundedness_analysis(question)[0]
        respuesta = traductor(groundedness_analysis(question)[1])
        

    else:
        respuesta = "No tengo información para responder tu consulta"
        groundedness = None

    return respuesta, groundedness
    



