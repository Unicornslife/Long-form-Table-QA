# -*- coding: utf-8 -*-

import openai
import config
import os
import requests


def get_completion(prompt_system, prompt_user, message_append=None):
    openai.api_key = config.api_key
    openai.api_base = config.organization
    engine = config.model_current
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


def chat_completion_request(messages, functions=None): 
    openai.api_key = config.api_key
    openai.api_base = config.organization
    engine = config.model_current
    try:
        response = openai.ChatCompletion.create(
        model = engine,
        messages= messages,
        temperature=1, 
        functions = functions,
        function_call="auto",
    )
        return response
    except Exception as e:
        print("2",e)
        print("retrying due to an error......")