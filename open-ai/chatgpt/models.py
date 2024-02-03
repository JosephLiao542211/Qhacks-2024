import os
import openai
from dotenv import load_dotenv

model = "gpt-3.5-turbo"

load_dotenv()
mood_conversation_history =[]
api_key = os.environ.get('.env')
client = openai.OpenAI(api_key=api_key)

def mood_detection_model(user_r):
    mood_model = client.chat.completions.create(
        model=model,
        messages=[
        {"role": "system", "content": "You are a higly attuned and emotionally receptive empath to children. \
        You categorize all the responses that are inputted to you as either 'happy' or 'sad'. \
        All the responses inputted towards you are children in one of the two emotionally states mentioned above \
        recounting their day. \
        You respond with either 'happy' or 'sad' depending on what mood you believe the child is feeling about their day.\
        If the string 'DO_NOT_REPLY' is found at the end of any prompts or chat history, reply only with the string 'no_response'. \
            "},
        {"role": "user", "content": user_r}
        ]
    )
    if not (mood_model.choices[0].message.content == "happy" or mood_model.choices[0].message.content == "sad"):
        raise ValueError("The model's response is not 'happy' or 'sad'.")
    mood_conversation_history.append({"role": "user", "content": user_r})
    mood_conversation_history.append({"role": "assistant", "content": mood_model.choices[0].message.content})
    return mood_model.choices[0].message.content, [mood_conversation_history, user_r]

def first_follow_up_q(model, prev_conversation_history):
    new_conversation_history = []
    new_conversation_history += prev_conversation_history
    new_conversation_history.append({"role": "system", "content":
                            "You are a super enthusiastic and positive journalling assistant talking to a child. \
                            You are also extremely concise and endearing with your responses, limiting them to \
                            two sentences or less. \
                            You ask follow up questions about the children you are talking to's day and in particular, \
                            how certain events made a child feel and what lead to certain events happening if you deem \
                            those events were within their control.\
                            "})

    new_conversation_history.append({"role": "user", "content": "Now that I have told you about my day, specifically my last response, \
                                present me with a response \
                                that asks me how I felt about the events that happened today or why I think a specific event \
                                that was within my control occured. \
                                "})
    # Send the entire conversation history to the model
    response = client.chat.completions.create(
    model=model,
    messages=new_conversation_history
    )
    # Extract the assistant's reply from the response
    assistant_reply = response.choices[0].message.content

    return assistant_reply

def second_follow_up_q(model, prev_conversation_history):
    new_conversation_history = []
    new_conversation_history += prev_conversation_history
    new_conversation_history.append({"role": "system", "content":
                "You are still a super enthusiastic, positive, concise, and endearing journalling assistant talking to a child. \
                You are also still limiting your responses to two sentences or less. \
                Ask a follow up question to the last prompt the user entered and make sure that your question does \
                not relate to any previous questions you asked the user.\
                "})
    # Send the entire conversation history to the model
    response = client.chat.completions.create(
    model=model,
    messages=new_conversation_history
    )
    # Extract the assistant's reply from the response
    assistant_reply = response.choices[0].message.content

    return assistant_reply

def r_second_follow_up_q(model, prev_conversation_history):
    new_conversation_history = []
    new_conversation_history += prev_conversation_history
    new_conversation_history.append({"role": "system", "content":
                "You are still a super enthusiastic, positive, concise, and endearing journalling assistant talking to a child. \
                You are limiting your responses to one sentence. \
                Give a positive and endearing response to the user's most recent prompt .\
                "})
    # Send the entire conversation history to the model
    response = client.chat.completions.create(
    model=model,
    messages=new_conversation_history
    )
    # Extract the assistant's reply from the response
    assistant_reply = response.choices[0].message.content

    return assistant_reply

