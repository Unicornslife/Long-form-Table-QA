# -*- coding: utf-8 -*-


from utils.openai_utils import *
import re
import json
import openai
import requests
import ast

def function_generator(question_prompt,table_prompt,table_name):
    prompt_system = f"""
    you are a python script generator. The user will give you a question and a table.\
    You need to generate only one python script that can be executed over the table to get answer.\
    You should give me your idea about how to generate python function and generate the python script according to the table based on your idea\
    Your answer only needs to contain the function(start with def) and the idea, no other words.\
    
    The first parameter should be the table.\
    If you need other parameters, they should be formed according to the question.\

    Note if the answer is in the table, please return the answer.\
    the return value should be in string format.\
    If the answer is not in the table, please return None.\
    
    for example:\
    The following is the qustion:'''which country had the most cyclists finish within the top 10?'''\
    The following is the table:''' \
    'header': ['Rank', 'Cyclist', 'Team', 'Time', 'UCI ProTour','Points']\
    'rows': [['1','Alejandro Valverde(ESP)',"Caisse d'Epargne",'5h 29' 10"','40'],
    '''\
    
    Your anwser should be:
    The following is the idea:\
    1.Clarify the Question:
    Firstly, we need to define the problem: from the provided data, which country has the highest number of cyclists finishing in the top 10?

    2.Understand Data Structure:
    Observing the structure of the given data, we noticed that each 'Cyclist' string contains a country code positioned between parentheses. Our task, then, is to extract this country code from these strings.

    3.Data Extraction:
    We can use string methods to extract the country code following the cyclist's name. Specifically, we utilize strip('()') to remove the parentheses.

    4.Counting Cyclists per Country:
    Without using Counter, we can manually tally the occurrences using a dictionary named country_counts. For each country code extracted in the previous step, if it's already in the dictionary, we increment its count; if not, we add it to the dictionary with a count of 1.

    5.Determine the Most Common Country:
    Using the max function and the key argument, we can identify the country with the most cyclists from the country_counts dictionary.

    6.Return the Result:
    The function ultimately returns the country code with the highest count of cyclists.

    The following is the python script:\
    def top_country(table):
        countries = [row[1].strip('()') for row in table['rows']]
        country_counts = []
        for country in countries:
            if country in country_counts:
                country_counts[country] += 1
            else:
                country_counts[country] = 1
        most_common_country = max(country_counts, key=country_counts.get)
        return most_common_country \
    
    """

    prompt_user= f"""
    The following is the tables' header:'''{table_prompt}'''\
    The following is the table:'''{question_prompt}'''\
    The following is the table's name:'''{table_name}'''\
    
    """
    function_response = get_completion(prompt_system, prompt_user)
    return function_response


def ask_GPT_diectly(question_prompt,table_prompt):
        prompt_system_2 = f"""
        Answer the question acording to the given table.\
        Give your answer directly, no other words.\
        
        For example:\
        The following is the qustion:'''which team is the first'''\
        The following is the table:''' \
        'header': ['Rank', 'Cyclist', 'Team', 'Time', 'UCI ProTour','Points']\
        'rows': [['1','Alejandro Valverde(ESP)',"Caisse d'Epargne",'5h 29' 10"','40'],'''\
        
        Your anwser should be:
        '''Caisse d'Epargne'''\
        """
        

        prompt_user_2 = f"""
        The following is the qustion:'''{question_prompt}'''\
        The following is the table:'''{table_prompt}'''\
        
        """

        results = get_completion(prompt_system_2,prompt_user_2)
        print("directly results:",results)
        return results

def function_extraction(function_response):
    prompt_system = f"""
    Give you a paragraph about the python function, including the function body, function description,function Example usage, etc.\
    You need to extract the function body from it.\
    Your answer only needs to contain the extracted function(start with def), no other explanation is required, no function Example usage is requried.\
    
    for example:\
    The following is the idea:\
    1.Clarify the Question:
    Firstly, we need to define the problem: from the provided data, which country has the highest number of cyclists finishing in the top 10?

    2.Understand Data Structure:
    Observing the structure of the given data, we noticed that each 'Cyclist' string contains a country code positioned between parentheses. Our task, then, is to extract this country code from these strings.

    3.Data Extraction:
    We can use string methods to extract the country code following the cyclist's name. Specifically, we utilize strip('()') to remove the parentheses.

    4.Counting Cyclists per Country:
    Without using Counter, we can manually tally the occurrences using a dictionary named country_counts. For each country code extracted in the previous step, if it's already in the dictionary, we increment its count; if not, we add it to the dictionary with a count of 1.

    5.Determine the Most Common Country:
    Using the max function and the key argument, we can identify the country with the most cyclists from the country_counts dictionary.

    6.Return the Result:
    The function ultimately returns the country code with the highest count of cyclists.

    The following is the python script:\
    def top_country(table):
        countries = [row[1].strip('()') for row in table['rows']]
        country_counts = []
        for country in countries:
            if country in country_counts:
                country_counts[country] += 1
            else:
                country_counts[country] = 1
        most_common_country = max(country_counts, key=country_counts.get)
        return most_common_country \
    '''\

    your answer should be:\
    def top_country(table):
        countries = [row[1].strip('()') for row in table['rows']]
        country_counts = []
        for country in countries:
            if country in country_counts:
                country_counts[country] += 1
            else:
                country_counts[country] = 1
        most_common_country = max(country_counts, key=country_counts.get)
        return most_common_country \
    
    """

    prompt_user = f"""
    The following is the tables' header:'''{function_response}'''\
    Extract the function body from the paragraph.\
    """

    function_extract_response = get_completion(prompt_system,prompt_user)
    function_extract_response = function_extract_response.replace('python', '')
    return function_extract_response

def question_devide(question_prompt):
    prompt_user = f"""
            The following is the qustion:'''{question_prompt}'''\
            """
    prompt_system = f"""
            Give you a mult-question, you need to check how many facts does this question ask.\
            if this question asks more than one fact, you need to divide this question into several questions.\
            if this question asks one fact, you need to give this question directly.\

            Give your answer directly, no other words.\
            Answer in the following format: 1. 2. 3. 4. 5.....\
            
            for example:\
            The following is the qustion:'''Which song earned the highest points in the Bundesvision Song Contest 2010 and how many points did it secure?'''\
            
            The answer should be: 
            '''1. Which song earned the highest points in the Bundesvision Song Contest 2010? 
            2. how many points did it secure?'''\

            """
    questions = get_completion(prompt_system,prompt_user)
    questions = questions.replace("The answer should be: \n", "")
    questions = questions.replace("The answer should be:", "")
    if '\n' in questions:
        lines = questions.split('\n')
    else:
        lines = re.split(r'\d+\.\s*', questions)


    questions_list = [line.strip() for line in lines if line.strip()]
    # questions_list = [re.sub(r'^\d+\.\s*', '', q) for q in cleaned_lines]


    return questions_list


def generate_long_answer(question_prompt,result_list):
    prompt_user = f"""
            The following is the qustion:'''{question_prompt}'''\
            The following is the list:'''{result_list}'''
            """
    prompt_system = f"""
            Give you a question and the several facts in the list.\
            the several facts in the list includes the answers to the question.\
            You combine these facts to answer the question in a long sentence answer.\
            Give your answer directly, no other words\
            
            for example:\
            The following is the qustion:'''Which song earned the highest points in the Bundesvision Song Contest 2010 and how many points did it secure?'''\
            The following is the several facts:'''
            ["Unter deiner Flagge" is the song that earned the highest points in the Bundesvision Song Contest in 2010.,
            The song 'Unter deiner Flagge' secured 164 points in the Bundesvision Song Contest in 2010.]

            The answer should be:
            '''the song 'Unter deiner Flagge' secured 164 points in the Bundesvision Song Contest in 2010.'''\
            """
    
    long_answer = get_completion(prompt_system,prompt_user)
    print("predict_answer:",long_answer)
    return long_answer

def combine_question(question_prompt,result_list):
    prompt_user = f"""
            The following is the qustion:'''{question_prompt}'''\
            The following is the several facts:'''{result_list}'''
            """
    prompt_system = f"""
            Give you a question and the several facts to this question.\
            You should combine the several facts into this question.\
            If the several facts needn't be combined into the question, you should give the question without chaning in your reply.\
            Give your answer directly, no other words should be added\
            
            for example:\
            The following is the qustion: '''when did the current ruler of Wogodogo begin their rule?'''
            The following is the several facts: ''' the current ruler of Wogodogo is Peter.'''

            The answer should be: '''when did the current ruler of Wogodogo 'Peter' begin their rule?'''

            """
    
    combined_qusetion = get_completion(prompt_system,prompt_user)

    return combined_qusetion

def final_answer_generator(question_prompt,Devided_result_list,table_prompt):
    direct_answer = ask_GPT_diectly(question_prompt,table_prompt)
    Devided_result_list.append(direct_answer)
    prompt_user = f"""
            The following is the several elements in a list:'''{Devided_result_list}'''
            """
    prompt_system = f"""
            Give you a list containing some elements.\
            You should choose the element that appears most frequently in the list.\
            You should notice that some elements have the same meaning but they are expressed in different ways and you should recoginze them.\
            Give your answer directly, no other words should be included.\
            if these elements' meanings are all different from each other, please type '''can't find'''\
            
            for example:\
            The following is the qustion: '''when did the Wogodogo begin his rule?'''\
            The following is the several answers in a list: '''[['Totals', 'Kim Barnes Arico', 'Sue Guevara'], 'Totals, Kim Barnes Arico, Sue Guevara', 'Carmel Borders, Gloria Soluk, Bud VanDeWege', 'Gloria Soluk, Bud VanDeWege, Sue Guevara']'''\

            The answer should be: '''['Totals', 'Kim Barnes Arico', 'Sue Guevara']'''\

            """
    
    final_answer = get_completion(prompt_system,prompt_user)

    if ("can't find" in final_answer):
        return Devided_result_list[0]
    
    if len(final_answer)/len(Devided_result_list[0])<0.8 and len(final_answer)/len(Devided_result_list[1])<0.8 and len(final_answer)/len(Devided_result_list[2])<0.8:
        return Devided_result_list[0]
    
    return final_answer


def update_table(table_prompt,results):
    prompt_user = f"""
            The following is the table:'''{table_prompt}'''\
            The following is a fact:'''{results}'''
            """
    prompt_system = f"""
            Give you a table and the fact you should query in the table.\
            You need query the table and tell me which rows of the table should be queried in order to find the fact.\
            You should return the queried rows of the table.\
            if the answer is not in the table, you should return None.\
            Give your answer in the form of list.\
            Give your answer directly,no other words should be included.\
            
            for example:\
            The following is the table:'''"table": 
            "header": [
                "Draw",
                "State",
                "Artist",
                "Song",
                "English translation",
                "Place",
                "Points"
            ],
            "rows": [
                [
                    "01",
                    "Hamburg",
                    "Selig",
                    "\"Von Ewigkeit zu Ewigkeit\"",
                    "From eternity to eternity",
                    "8",
                    "40"
                ],
                [
                    "02",
                    "Rhineland-Palatinate",
                    "Auletta",
                    "\"Sommerdiebe\"",
                    "Summer thieves",
                    "14",
                    "17"
                ],
                [
                    "03",
                    "Saxony",
                    "Blockfl\u00f6te des Todes (de) & Diane Weigmann (de)",
                    "\"Alles wird teurer\"",
                    "Everything gets more expensive",
                    "11",
                    "20"
                ],
                [
                    "04",
                    "Bremen",
                    "Kleinstadthelden (de)",
                    "\"Indie Boys\"",
                    "\u2014",
                    "11",
                    "20"
                ],
                [
                    "05",
                    "Mecklenburg-Vorpommern",
                    "Sebastian H\u00e4mer",
                    "\"Is' schon ok\"",
                    "It's okay",
                    "10",
                    "22"
                ],
                [
                    "06",
                    "Lower Saxony",
                    "Bernd Begemann & Dirk Darmstaedter (de)",
                    "\"So geht das jede Nacht\"",
                    "That's how it is every night",
                    "16",
                    "4"
                ],
                [
                    "07",
                    "Brandenburg",
                    "Das Gezeichnete Ich (de)",
                    "\"Du, Es und Ich\"",
                    "You, it and me",
                    "5",
                    "87"
                ],
                [
                    "08",
                    "Schleswig-Holstein",
                    "Stanfour",
                    "\"Sail On\"",
                    "\u2014",
                    "7",
                    "60"
                ],
                [
                    "09",
                    "Hesse",
                    "Oceana & Leon Taylor (de)",
                    "\"Far Away\"",
                    "\u2014",
                    "13",
                    "18"
                ],
                [
                    "10",
                    "Saarland",
                    "Mikroboy (de)",
                    "\"Nichts ist umsonst\"",
                    "Nothing's for free",
                    "15",
                    "12"
                ],
                [
                    "11",
                    "Thuringia",
                    "Norman Sinn (de) & Ryo (de)",
                    "\"Planlos\"",
                    "Aimless",
                    "6",
                    "79"
                ],
                [
                    "12",
                    "Bavaria",
                    "Blumentopf",
                    "\"SoLaLa\"",
                    "So-so",
                    "4",
                    "94"
                ],
                [
                    "13",
                    "Saxony-Anhalt",
                    "Silly",
                    "\"Alles Rot\"",
                    "Everything red",
                    "2",
                    "152"
                ],
                [
                    "14",
                    "Baden-W\u00fcrttemberg",
                    "Bakkushan",
                    "\"Springwut\"",
                    "Jump furor",
                    "9",
                    "39"
                ],
                [
                    "15",
                    "Berlin",
                    "Ich + Ich feat. Mohamed Mounir",
                    "\"Yasmine\"",
                    "\u2014",
                    "3",
                    "100"
                ],
                [
                    "16",
                    "North Rhine-Westphalia",
                    "Unheilig",
                    "\"Unter deiner Flagge\"",
                    "Under your flag",
                    "1",
                    "164"
                ]
            ]
        '''\
        The following is several facts:'''Auletta is from Rhineland-Palatinate'''

        The answer should be: '''
            [
                "02",
                "Rhineland-Palatinate",
                "Auletta",
                "\"Sommerdiebe\"",
                "Summer thieves",
                "14",
                "17"
            ]'''\

            """
    if(results == None or results == "None" or results == []):
        return table_prompt
    
    row = get_completion(prompt_system,prompt_user)
    if "None" in row or "none" in row or "NONE" in row or "[]" in row:
        return table_prompt
    
    cleaned_row = row.replace("The answer should be:", "")
    cleaned_row = cleaned_row.replace("```\n", "")

    new_table = {}
    new_table["header"] = table_prompt["header"]
    new_table["rows"] = cleaned_row

    return new_table


def check_coherent_table(table,renewed_table,question,cur_output):
    prompt_user = f"""
            The following is the table:'''{renewed_table}'''\
            The following is a question:'''{question}'''
            """
    prompt_system = f"""
            Give you a table and the question.\
            You need to check whether the question asked is related to the specific data in the table\
            The first row of the table is the header, followed by the specific data.\
            If they are relevent, You should return "YES".\
            if the answer is not in the table, you should return "NO".\
            Give your answer directly,no other words should be included.\
            
            for example:\
            The following is the table:'''[ [ "Year", "Title", "Role", "Channel" ], [ "2015", "Kuch Toh Hai Tere Mere Darmiyaan", "Sanjana Kapoor", "Star Plus" ] ]\
            '''\
            The following is a question:'''which year did Kuch Toh Hai Tere Mere Darmiyaan present?'''\

            The answer should be: '''
                YES
            '''

        """

    
    check = get_completion(prompt_system,prompt_user)
    print(check)
    cur_output["check_coherent"] = check
    if "YES" in check or "yes" in check or "Yes" in check or "Y" in check:
        return renewed_table

    return table

def self_debugging(function_extract_response,Feedback,function_args,table_prompt):
    prompt_system = f"""
        there are some questions about the python script.\
        You should fix the python script by given Feedback for wrong reasons.\
        After your fixing, the python script given by you should run without error with the given table and function_args .\
        Your answer only needs to contain the function(start with def)\
        No other words.\
        Note if the answer is in the table, please return the answer.\
        the return value should be in string format.\
        If the answer is not in the table, please return None.\
        """

    prompt_user = f"""
        The following is the python script:'''{function_extract_response}'''\
        The following is the Feedback:'''{Feedback}'''\
        The following is the test function_args:'''{function_args}'''\
        The following is the test table:'''{table_prompt}'''\
        """

    function_extract_response = get_completion(prompt_system,prompt_user)
    function_extract_response = function_extract_response.replace('python', '')

    return function_extract_response

def sentence_generator_prompt(question_prompt,results):
    prompt_user = f"""
                The following is the qustion:'''{question_prompt}'''\
                The following is the answer:'''{results}'''
                """
    prompt_system = f"""
                Give you a question and the answer to this qusetion.\
                You should answer the question based on the answer in a long sentence answer.\
                Give your answer directly, no other words.\
                """
    long_answer = get_completion(prompt_system,prompt_user)

    return long_answer