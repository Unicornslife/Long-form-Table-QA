# -*- coding: utf-8 -*-
import json
import openai
import ast
import argparse
import random
from utils.openai_utils import *
from prompt.long_form_prompt import *
from datasets import load_dataset

model_current = "None"
api_key = "None"
organization = "None"


def extract_function_info(function_str):
    module = ast.parse(function_str)
    function_definition = module.body[0]  
    function_name = function_definition.name
    function_args = [arg.arg for arg in function_definition.args.args]
    if 'table' in function_args:
        function_args.remove('table')

    properties = {
    arg: {
        "type": "string",
        "description": "the thing user wants to query,maybe a person's name, a city's name, etc.",
    }
    for arg in function_args
    }

    required = list(properties.keys())

    p = {
        "name": function_name,
        "description": "Use this function to answer user's questions.",
        "parameters": {
            "type": "object",
            "properties": properties,
            "required": required,
        },
    }
    function = []
    function.append(p)
    return function,function_name,function_args



def create_function_from_string(function_string):
    exec(function_string)
    return locals()[function_string.split()[1].split('(')[0]]

def execute_function_call(message,table_prompt,function_name,function_extract_response,function_args):
    if message.get("function_call"):
        if message["function_call"]["name"] == function_name:
            arguments = json.loads(message["function_call"]["arguments"])
            function_ref = create_function_from_string(function_extract_response)
            args = [table_prompt] + [arguments[function_args[i]] for i in range(len(arguments))]
            result = function_ref(*args)
        else:
            result = f"Error: function {message['function_call']['name']} does not exist"

        return result
    

def self_debugging_in(assistant_message_1,table_prompt,function_name,function_extract_response,function_args,question_prompt,cur_output,j,time):
    i = 0
    try: 
        flag = 0
        Feedback = "the python script is correct, nothing to fix."
        results = execute_function_call(assistant_message_1,table_prompt,function_name,function_extract_response,function_args)
    except Exception as e:
        Feedback = e
        flag = 1
        print("1",e)

    while(flag == 1 and i < 5):
        i = i + 1
        function_extract_response = self_debugging(function_extract_response,Feedback,function_args,table_prompt)
        try:
            flag = 0
            Feedback = "the python script is correct, nothing to fix."
            results = execute_function_call(assistant_message_1,table_prompt,function_name,function_extract_response,function_args)
            print("fixed")
        except Exception as e:
            Feedback = e
            flag = 1

    # print(function_extract_response)
    cur_output[f"function {j}'s {time} generation"] = function_extract_response
    
    if(i == 5):
        results = ask_GPT_diectly(question_prompt,table_prompt)

        
    return results


def function_call_generator(question_prompt,table_prompt,function_extract_response,function,function_name,function_args,cur_output,i,time):
    messages = []
    messages.append({"role": "user", "content": question_prompt})

    chat_response = chat_completion_request(messages, functions=function)
    assistant_message_1 = chat_response["choices"][0]["message"]
    assistant_message_1["content"] = "None"
    messages.append(assistant_message_1)

    results = self_debugging_in(assistant_message_1,table_prompt,function_name,function_extract_response,function_args,question_prompt,cur_output,i,time)
    if results == None or results == "None":
        print("can not find answer!")
        results = ask_GPT_diectly(question_prompt,table_prompt)
    print(f"results: {results}")

    return assistant_message_1,messages,results

def sentence_generator(assistant_message_1, messages,results,question_prompt,function):
    try:
        if results !='':
            messages.append({"role": "function", "name": assistant_message_1["function_call"]["name"], "content": results})
            chat_response = chat_completion_request(
                messages, functions=function
            )
            assistant_message_2 = chat_response["choices"][0]["message"]
            long_answer = assistant_message_2["content"]
            print("success")
    except Exception:
       long_answer = sentence_generator_prompt(question_prompt,results)
    
    print(long_answer)
    return long_answer

def process_question(question, table_prompt, table_name, results_list, cur_output, j, renewed_table):
    Devided_result_list = []
    question_prompt = question if not results_list else combine_question(question, results_list)
    print(f"Devided Question: {question_prompt}")
    cur_output[f"Devided Question {j}"] = question_prompt
    table_input = table_prompt if not results_list else check_coherent_table(table_prompt,renewed_table,question_prompt,cur_output)
    loop_range = 3

    for time in range(loop_range):
        function_response = function_generator(question_prompt, table_input, table_name)
        function_extract_response = function_extraction(function_response)
        function, function_name, function_args = extract_function_info(function_extract_response)
        assistant_message_1, messages, results = function_call_generator(question_prompt, table_input, function_extract_response, function, function_name, function_args, cur_output, j, time)
        Devided_result_list.append(results)

    final_divide_answer = final_answer_generator(question_prompt, Devided_result_list, table_input)
    print("final_answer:", final_divide_answer)
    cur_output[f"Devided results {j}"] = final_divide_answer
    sentence = sentence_generator(assistant_message_1, messages, final_divide_answer, question_prompt, function)
    cur_output[f"Devided long results {j}"] = sentence
    results_list.append(sentence)

    # Updating the table based on the sentence
    if len(results_list) == 1:
        renewed_table = update_table(table_prompt, sentence)

    return renewed_table, results_list

def get_table_answer(test_data,start_num, end_num):
    output_dict = []
    if model_current == "gpt-35-turbo":
        list_num = range(start_num, end_num)
    else:
        list_num = random.sample(range(start_num, end_num), 5)
    
    for i in list_num:
        try:
            questions = test_data[i]["question"]
            questions_list = question_devide(questions)
            table_prompt = test_data[i]["table"]
            ground_outputs = test_data[i]["response"]
            table_name = test_data[i]["table_title"]
            example_id = test_data[i]["example_id"]
            print(f"Question {i}: {questions}")
            results_list = []
            renewed_table = table_prompt
            cur_output = {"example_id": example_id, "question": questions}
            j = 0
            for question in questions_list:
                renewed_table, results_list = process_question(question, table_prompt, table_name, results_list, cur_output, j, renewed_table)
                j += 1

            long_answer = generate_long_answer(questions,results_list)
            print("ground_answer:",ground_outputs)
            cur_output["predict_long_answer"] = long_answer
            output_dict.append(cur_output)

        except Exception:
            cur_output = {"example_id": example_id, "question": questions, "predict_long_answer": "error"}
            output_dict.append(cur_output)
        
    return output_dict



if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--model", type=str, default="gpt-35-turbo")
    parser.add_argument("--start_num", type=int, default=0)
    parser.add_argument("--end_num", type=int, default=1000)
    parser.add_argument("--dataset_name", type=str, default="yale-nlp/QTSumm")
    parser.add_argument("--split_name", type=str, default="test")
    parser.add_argument("--api_key", type=str)
    parser.add_argument("--organization", type=str)
    args = parser.parse_args()
    model_current = args.model
    api_key = args.api_key
    organization = args.organization
    test_data = load_dataset(args.dataset_name, split=args.split_name)
    data = []
    data = get_table_answer(test_data, args.start_num, args.end_num)

    with open(f"{args.dataset_name}_{args.split_name}_{model_current}_output.json", "w") as f:
        json.dump(data, f, indent=4)
