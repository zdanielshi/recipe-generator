# Import libraries
import streamlit as st
import toml
import json
import random
from openai import OpenAI

# Connect to OpenAI API

# Define functions
openai_key = st.secrets["openai_api_key"]
client = OpenAI(api_key = openai_key)

## Function to load "About content"
def load_about():
  with open('about.txt', 'r') as file:
    about_text = file.read()
  return about_text

## Function to pull prompt_messages.toml
def load_toml(file_path):
  with open(file_path, "r") as file:
    return toml.load(file)

### Pull in the toml messages here
prompt_messages = load_toml("prompt_messages.toml")
recipe_prompt = prompt_messages["prompts"]["recipe_prompt"]

## Function to query OpenAI API
def get_recipe(dish, complexity, language):
  formatted_recipe_prompts = [{"role": prompt["role"], 
                             "content": prompt["content"].format(dish=dish, complexity=complexity, language=language)} 
                            for prompt in recipe_prompt if "content" in prompt]
  response = client.chat.completions.create(
    model = "gpt-3.5-turbo-1106",
    messages = formatted_recipe_prompts,
    temperature = 0,
    max_tokens = 1000,
    top_p = 1,
    frequency_penalty = 0.25,
    presence_penalty = 0
  )
  openai_response = response.choices[0].message.content

  return openai_response

# Function to get 4 random dishes
def get_random_dishes():
    with open('dishes.txt', 'r') as file:
        dishes = file.read().splitlines()
    return random.sample(dishes, 4)

# Streamlit interface

# Initialize session state for random dishes
if 'random_dishes' not in st.session_state:
    st.session_state.random_dishes = get_random_dishes()

## Complexity and language components
complexity_choices = ["Home cook", "Seasoned cook", "Professional chef"]
languages = ["English", "French", "Spanish", "German"]

## Title
st.title('Recipe Generator')

## Display About content
st.sidebar.title("About")
st.sidebar.write(load_about())

## Display dish selection
st.subheader('Select a Dish')
selected_dish = st.selectbox("Choose a Dish", st.session_state.random_dishes)

## Select complexity level
selected_complexity = st.selectbox("Select Complexity Level", complexity_choices)

## Select language
selected_language = st.selectbox("Select Language", languages)

# Button to generate recipe
if st.button("Generate Recipe"):
    recipe = get_recipe(selected_dish, selected_complexity, selected_language)
    st.write(recipe)