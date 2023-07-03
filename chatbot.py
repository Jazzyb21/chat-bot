import os
import openai
import panel as pn  # GUI
pn.extension()
from dotenv import load_dotenv, find_dotenv
_ = load_dotenv(find_dotenv()) # read local .env file

openai.api_key  = os.getenv('OPENAI_API_KEY')

def get_completion(prompt, model="gpt-3.5-turbo"):
    messages = [{"role": "user", "content": prompt}]
    response = openai.ChatCompletion.create(
        model=model,
        messages=messages,
        temperature=0, # this is the degree of randomness of the model's output
    )
    return response.choices[0].message["content"]

def get_completion_from_messages(messages, model="gpt-3.5-turbo", temperature=0):
    response = openai.ChatCompletion.create(
        model=model,
        messages=messages,
        temperature=temperature, # this is the degree of randomness of the model's output
    )
#     print(str(response.choices[0].message))
    return response.choices[0].message["content"]

def collect_messages(_):
    prompt = inp.value_input
    inp.value = ''
    context.append({'role':'user', 'content':f"{prompt}"})
    response = get_completion_from_messages(context) 
    context.append({'role':'assistant', 'content':f"{response}"})
    panels.append(
        pn.Row('User:', pn.pane.Markdown(prompt, width=600)))
    panels.append(
        pn.Row('Assistant:', pn.pane.Markdown(response, width=600, style={'background-color': '#F6F6F6'})))
 
    return pn.Column(*panels)

panels = [] # collect display 

context = [ {'role':'system', 'content':"""
You are a assistant, an automated service explain and answer questions about the Supplemental Nutrition Assistance Program (SNAP) for a specified state. \
You first greet the person needing help in a friendly, inviting tone, \
then ask them what state they are located in, \
and  ask what they need help with. \
You wait and summarize their question to answer \
Ask the person if they need help with anything else \
Only answer questions related to SNAP, food stamps, food pantries, hunger, WIC,  or food insecurity \
Make sure to clarify all questions and be kind and inviting \
Make sure to have clear, concise answers that are easy and quick to read and link any webites or relevant information \
"""} ]  # accumulate messages


inp = pn.widgets.TextInput(value="Hi", placeholder='Enter text here…')
button_conversation = pn.widgets.Button(name="Chat!")

interactive_conversation = pn.bind(collect_messages, button_conversation)

dashboard = pn.Column(
    inp,
    pn.Row(button_conversation),
    pn.panel(interactive_conversation, loading_indicator=True, height=300),
)

dashboard


messages =  context.copy()

response = get_completion_from_messages(messages, temperature=0)
print(response)

dashboard.show()