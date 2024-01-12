import json
import time

from environs import Env
from google.cloud import dialogflow


def create_intent(project_id, display_name, training_phrases_parts, message_texts):
    intents_client = dialogflow.IntentsClient()

    parent = dialogflow.AgentsClient.agent_path(project_id)
    training_phrases = []
    for training_phrases_part in training_phrases_parts:
        part = dialogflow.Intent.TrainingPhrase.Part(text=training_phrases_part)
        training_phrase = dialogflow.Intent.TrainingPhrase(parts=[part])
        training_phrases.append(training_phrase)

    text = dialogflow.Intent.Message.Text(text=message_texts)
    message = dialogflow.Intent.Message(text=text)

    intent = dialogflow.Intent(
        display_name=display_name, training_phrases=training_phrases, messages=[message]
    )

    response = intents_client.create_intent(
        request={"parent": parent, "intent": intent}
    )

    print(f"Intent created: {response}")


def main():
    env = Env()
    env.read_env()
    project_id = env.str('DIALOGFLOW_PROJECT_ID')
    with open('questions.json', 'r') as file:
        questions = json.load(file)
    for question in questions:
        try:
            create_intent(
                project_id=project_id,
                display_name=question,
                training_phrases_parts=questions.get(question)['questions'],
                message_texts=[questions.get(question)['answer']]
            )
            time.sleep(1)
        except Exception as ex:
            print(ex)
            continue


if __name__ == '__main__':
    main()
