# -*- coding: utf-8 -*-

import openai
import os
import requests
from run_llm import model_current, api_key, organization

openai.api_key = api_key
openai.organization = organization


def get_completion(prompt_system, prompt_user, message_append=None):
    engine = model_current
    messages = [{"role": "system", "content": prompt_system}
                ,{"role": "user", "content": prompt_user}]
    if message_append is not None:
        messages = messages + message_append

    try:
        response = openai.ChatCompletion.create(
            model=engine,
            messages=messages,
            temperature=1
        )
        return response["choices"][0]["message"]["content"]
    except Exception as e:
        print("1",e)
        print("retrying due to an error......")

    
def chat_completion_request(messages, functions=None, function_call=None, model="gpt-4"):
    headers = {
        "Content-Type": "application/json",
        "Authorization": "Bearer " + openai.api_key,
        "openai-organization": openai.organization,
    }
    json_data = {"model": model, "messages": messages}
    if functions is not None:
        json_data.update({"functions": functions})
    if function_call is not None:
        json_data.update({"function_call": function_call})
    try:
        response = requests.post(
            "https://api.openai.com/v1/chat/completions",
            headers=headers,
            json=json_data,
        )
        return response
    except Exception as e:
        print("Unable to generate ChatCompletion response")
        print(f"Exception: {e}")
        return e