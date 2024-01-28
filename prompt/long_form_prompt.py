# -*- coding: utf-8 -*-


from utils.openai_utils import *
import re


def function_generator(question_prompt,table_prompt,table_name):
    prompt_system = f"""
        You are an expert in executable python program generation. The user will give you a table and a related question.
    """

    prompt_user= f"""
        Upon receiving a table and a related question, your task is to develop a single, executable Python script suited to process the table data and provide an answer. The script should be designed to analyze the table contents and return the answer in string format if it is directly available within the table. If the table does not contain the necessary information to answer the question, the script should be programmed to return 'None'.
        After generating a Python program script, you should check if the script contains any syntax errors. If there are syntax errors, you should SELF-DEBUG it until it's executable.
        
        Example:
        Question: Which country has won the OGAE Video Contest multiple times?
        Table_Title：OGAE Video Contest - Winners
        Table:
            "header": ["Year", "Country", "Video", "Performer", "Points", "Host city"],
            "rows": 
                ["2003", "France", "\"Fan\"", "Pascal Obispo", "122", "Turkey Istanbul"],
                ["2004", "Portugal", "\"Cavaleiro Monge\"", "Mariza", "133", "France Fontainebleau"],
                ["2005", "Ukraine", "\"I Will Forget You\"", "Svetlana Loboda", "171", "Portugal Lisbon"],
                ["2006", "Italy", "\"Contromano\"", "Nek", "106", "Turkey Izmir"],
                ["2007", "Russia", "\"LML\"", "Via Gra", "198", "Italy Florence"],
                ["2008", "Russia", "\"Potselui\"", "Via Gra", "140", "Russia Moscow"]
        Response:
            def multiple_winners_in_OGAE_contest(table):
                from collections import Counter

                # Extract the column for countries
                country_column_index = table["header"].index("City")
                countries = [row[country_column_index] for row in table["rows"]]

                # Count the victories for each country
                victory_count = Counter(countries)

                # Filter and return countries with multiple victories
                multiple_victories = [country for country, count in victory_count.items() if count > 1]
                return ', '.join(multiple_victories) if multiple_victories else None

        Now please give your answer to generate a python script to answer the original answer of the given table. Let's think step by step and follow the templates of given example.

        The following is the tables' header:'''{table_prompt}'''
        The following is the table:'''{question_prompt}'''
        The following is the table's name:'''{table_name}'''

    """
    function_response = get_completion(prompt_system, prompt_user)
    return function_response


def function_extraction(function_response):
    prompt_system = f"""
        You are a python function extraction assistant. The user will give you a python script.\
    """

    prompt_user = f"""
        Give you a paragraph about the python function, including the function body, function description,function Example usage, etc. You need to extract the function body from it. Your answer only needs to contain the extracted function(start with def), no other explanation is required, no function Example usage is requried.\
    
        Example:
        Idea:
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

        Response:
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
        
            
        Now please give your answer. Let's follow templates of examples. 
        The following is the function response:'''{function_response}'''\
    """

    function_extract_response = get_completion(prompt_system,prompt_user)
    function_extract_response = function_extract_response.replace('python', '')
    return function_extract_response

def plan_generation(question_prompt):
    prompt_user = f"""
            Give you a complex question over a table, your task is to assess the number of distinct facts the question seeks. If the question encompasses more than one fact, it necessitates deconstruction into a series of sequential sub-questions. This process involves breaking down the complexity to address each fact individually. On the other hand, if the question is focused on a single fact, your response should involve presenting the question as is, without further decomposition.
            Answer in the following format: 1. 2. 3. 4. 5.....

            Example1:
            Question: Which song earned the highest points in the Bundesvision Song Contest 2010 and how many points did it secure?

            Response: 
            1.Which song earned the highest points in the Bundesvision Song Contest 2010? 
            2.How many points did it secure?

            Example2:
            Question: Which country has won the OGAE Video Contest multiple times, and what were the corresponding years, winning songs and points scored?

            Response: 
            1.Which country has won the OGAE Video Contest multiple times?
            2.What were the corresponding years of these victories?
            3.What were the winning songs for each of these years?
            4.What were the points scored in each of these victories?


            Now please give your answer to the given question. Let's think step by step and follow templates of examples. 
            The following is the qustion:'''{question_prompt}'''\
            """
    
    prompt_system = f"""
            You are an expert plan generation assistant.
            """
    questions = get_completion(prompt_system,prompt_user)
    questions = questions.replace("The answer should be: \n", "")
    questions = questions.replace("The answer should be:", "")
    if '\n' in questions:
        lines = questions.split('\n')
    else:
        lines = re.split(r'\d+\.\s*', questions)


    questions_list = [line.strip() for line in lines if line.strip()]


    return questions_list

def ask_GPT_diectly(question_prompt,table_prompt):
        prompt_system = f"""
            You are an expert in answering questions directly according to the given table.
        """
        prompt_user = f"""
            Answer the question acording to the given table. Give your answer directly, no other words.
            
            Example:
            Qustion: Which team is the first?
            Table: 
                'header': ['Rank', 'Cyclist', 'Team', 'Time', 'UCI ProTour','Points']
                'rows': [['1','Alejandro Valverde(ESP)',"Caisse d'Epargne",'5h 29' 10"','40']
            
            Response:
                Caisse d'Epargne

            Now please give your answer to the given question. Let's follow templates of examples.
            The following is the qustion:'''{question_prompt}'''\
            The following is the table:'''{table_prompt}'''\
            
        """

        results = get_completion(prompt_system,prompt_user)
        print("directly results:",results)
        return results

def generate_long_answer(question_prompt,result_list):
    prompt_user = f"""
            Given a question and a list of relevant facts, each containing part of the information needed to answer the question, your task is to synthesize these facts into a coherent, long sentence that fully addresses the question. The goal is to integrate the individual pieces of information from the list seamlessly, creating a comprehensive response that encapsulates all aspects of the question in a clear and concise manner.

            Example:
            Question: Which country has won the OGAE Video Contest multiple times, and what were the corresponding years, winning songs and points scored?

            Fact List:
            [1. Russia, France, and Belgium have each won the OGAE Video Contest multiple times.
            2. Russia won the contest in 2007, 2008, and 2009, France in 2003, 2011, and 2014, and Belgium in 2013 and 2017. 
            3. Russia's winning songs were “LML” in 2007, “Potselui” in 2008, and “Karma” in 2009; France’s were “Fan” in 2003, “Lonely Lisa” in 2011, and “Tourner dans le vide” in 2014; Belgium’s were “Papaoutai” in 2013 and “Mud Blood” in 2017. 
            4. Russia scored 198 points in 2007, 140 points in 2008, and 142 points in 2009; France scored 122 points in 2003, 96 points in 2011, and 141 points in 2014; Belgium scored 144 points in 2013 and 184 points in 2017.]

            Response:
            Russia, France, and Belgium have each won the OGAE Video Contest multiple times. Specifically, Russia triumphed in 2007 with "LML" scoring 198 points, in 2008 with "Potselui" scoring 140 points, and in 2009 with "Karma" scoring 142 points. France secured victories in 2003 with "Fan" scoring 122 points, in 2011 with "Lonely Lisa" scoring 96 points, and in 2014 with "Tourner dans le vide" scoring 141 points. Belgium won in 2013 with "Papaoutai" scoring 144 points and again in 2017 with "Mud Blood" scoring 184 points.

            Now please give your answer to generate a final answer integrating sub-answers.Let's follow templates of examples. 

            The following is the qustion:'''{question_prompt}'''\
            The following is the several elements in a list:'''{result_list}'''
            """
    prompt_system = f"""
            You are an expert in extracting complex information and integrating sub-answers.
            """
    
    long_answer = get_completion(prompt_system,prompt_user)
    print("predict_answer:",long_answer)
    return long_answer

def combine_question(question_prompt,result_list,j):
    prompt_user = f"""
            Give you a processing plan and the answers to previous sub-questions. Your task is to refine the current plan given to you and generate a revised plan. If you believe the plan is finalized or it is comprehensive enough to answer the given complex question, please stop revising and return the plan directly.

            Example:
            Plan: 1.What were the corresponding years of these victories? 2. What were the winning songs for each of these years? 3. What were the points scored in each of these victories?
            Sub-question answers: Russia, France, and Belgium have each won the OGAE Video Contest multiple times

            Response:
            1.For Russia, France, and Belgium, who have each won the OGAE Video Contest multiple times, what were the corresponding years of these victories?
            2.What were the winning songs for each year that Russia, France, and Belgium won the OGAE Video Contest, considering they have each won multiple times?
            3.What were the points scored by Russia, France, and Belgium in each of their multiple victories at the OGAE Video Contest?

            Now please give your answer to the given question. Let's think step by step and follow templates of examples. 

            The following is the qustion:'''{question_prompt}'''
            The following is the several facts:'''{result_list}'''
            """
    prompt_system = f"""
            You are an expert in iterative plan refinement.
            """
    
    combined_question = get_completion(prompt_system,prompt_user)
    sentences = combined_question.strip().split('\n')

    if j < len(sentences) and j >= 0:
        selected_question =  sentences[j].strip()
    else:
        selected_question =  question_prompt

    return selected_question 


def final_answer_generator(question_prompt,Devided_result_list,table_prompt):
    direct_answer = ask_GPT_diectly(question_prompt,table_prompt)
    Devided_result_list.append(direct_answer)
    prompt_user = f"""
            Give you a list containing some elements.You should choose the element that appears most frequently in the list.You should notice that some elements have the same meaning but they are expressed in different ways and you should recoginze them.
            Give your answer directly, no other words should be included.If these elements' meanings are all different from each other, please type '''can't find'''
            
            Example:
            Question: When did the Wogodogo begin his rule?
            Facts:
            [['Totals', 'Kim Barnes Arico', 'Sue Guevara'], 'Totals, Kim Barnes Arico, Sue Guevara', 'Carmel Borders, Gloria Soluk, Bud VanDeWege', 'Gloria Soluk, Bud VanDeWege, Sue Guevara']
            
            Response:
            ['Totals', 'Kim Barnes Arico', 'Sue Guevara']

            Now please give your answer to generate a final answer. Let's think step by step and follow templates of examples.
            The following is the qustion:'''{question_prompt}'''
            The following is the several elements in a list:'''{Devided_result_list}'''
            """
    prompt_system = f"""
            You are an expert in choosing the most frequent element in a list.\
            """
    
    final_answer = get_completion(prompt_system,prompt_user)

    if ("can't find" in final_answer):
        return Devided_result_list[0]
    
    if len(final_answer)/len(Devided_result_list[0])<0.8 and len(final_answer)/len(Devided_result_list[1])<0.8 and len(final_answer)/len(Devided_result_list[2])<0.8:
        return Devided_result_list[0]
    
    return final_answer


def update_table(table_prompt,results):
    prompt_system = f"""
        You are an expert in table querying.   
        """
    prompt_user = f"""
        Give you a table and the fact you should query in the table.You need query the table and tell me which rows of the table should be queried in order to find the fact.\You should return the queried rows of the table. If the answer is not in the table, you should return None.
        Give your answer in the form of list. Give your answer directly,no other words should be included.
        
        Example:
        Table:
            "header": ["Draw", "State", "Artist", "Song", "English translation", "Place", "Points"],
            "rows": [
                ["01", "Hamburg", "Selig", "\"Von Ewigkeit zu Ewigkeit\"", "From eternity to eternity", "8", "40"],
                ["02", "Rhineland-Palatinate", "Auletta", "\"Sommerdiebe\"", "Summer thieves", "14", "17"],
                ["03", "Saxony", "Blockflöte des Todes (de) & Diane Weigmann (de)", "\"Alles wird teurer\"", "Everything gets more expensive", "11", "20"],
                ["04", "Bremen", "Kleinstadthelden (de)", "\"Indie Boys\"", "—", "11", "20"],
                ["05", "Mecklenburg-Vorpommern", "Sebastian Hämer", "\"Is' schon ok\"", "It's okay", "10", "22"],
                ["06", "Lower Saxony", "Bernd Begemann & Dirk Darmstaedter (de)", "\"So geht das jede Nacht\"", "That's how it is every night", "16", "4"],
                ["07", "Brandenburg", "Das Gezeichnete Ich (de)", "\"Du, Es und Ich\"", "You, it and me", "5", "87"],
                ["08", "Schleswig-Holstein", "Stanfour", "\"Sail On\"", "—", "7", "60"],
                ["09", "Hesse", "Oceana & Leon Taylor (de)", "\"Far Away\"", "—", "13", "18"],
                ["10", "Saarland", "Mikroboy (de)", "\"Nichts ist umsonst\"", "Nothing's for free", "15", "12"],
                ["11", "Thuringia", "Norman Sinn (de) & Ryo (de)", "\"Planlos\"", "Aimless", "6", "79"],
                ["12", "Bavaria", "Blumentopf", "\"SoLaLa\"", "So-so", "4", "94"],
                ["13", "Saxony-Anhalt", "Silly", "\"Alles Rot\"", "Everything red", "2", "152"],
                ["14", "Baden-Württemberg", "Bakkushan", "\"Springwut\"", "Jump furor", "9", "39"],
                ["15", "Berlin", "Ich + Ich feat. Mohamed Mounir", "\"Yasmine\"", "—", "3", "100"],
                ["16", "North Rhine-Westphalia", "Unheilig", "\"Unter deiner Flagge\"", "Under your flag", "1", "164"]
            ]

        Facts: 
            Auletta is from Rhineland-Palatinate

        Response:
           ["02", "Rhineland-Palatinate", "Auletta", "\"Sommerdiebe\"", "Summer thieves", "14", "17"]
        
        The following is the table:'''{table_prompt}'''\
        The following is a fact:'''{results}'''
            """

    if(results == None or results == "None" or results == []):
        return table_prompt
    
    row = get_completion(prompt_system,prompt_user)
    if "None" in row or "none" in row or "NONE" in row or "[]" in row:
        return table_prompt
    
    cleaned_row = row.replace("The answer should be:", "")
    cleaned_row = cleaned_row.replace("```\n", "")

    new_table = {}
    if "header" in table_prompt:
        new_table["header"] = table_prompt["header"]

    new_table["rows"] = cleaned_row

    return new_table


def check_coherent_table(table,renewed_table,question):
    prompt_user = f"""
            You are an expert in table checking.
            """
    prompt_system = f"""
            Give you a table and the question. You need to check whether the question asked is related to the specific data in the table. The first row of the table is the header, followed by the specific data.
            If they are relevent, You should return "YES". If the answer is not in the table, you should return "NO".
            Give your answer directly,no other words should be included.
            
            Example:
            Table: [ [ "Year", "Title", "Role", "Channel" ], [ "2015", "Kuch Toh Hai Tere Mere Darmiyaan", "Sanjana Kapoor", "Star Plus" ] ]
            Question: Which year did Kuch Toh Hai Tere Mere Darmiyaan present?

            Response: YES

            Now please give your answer to check whether the question asked is related to the specific data in the table. Let's follow templates of examples.
            The following is the table:'''{renewed_table}'''
            The following is a question:'''{question}'''
        """

    
    check = get_completion(prompt_system,prompt_user)
    print(check)
    if "YES" in check or "yes" in check or "Yes" in check or "Y" in check:
        return renewed_table

    return table

def self_debugging(function_extract_response,Feedback,function_args,table_prompt):
    prompt_system = f"""
        You are an expert in python script debugging.
        """

    prompt_user = f"""
        There are some questions about the python script.You should fix the python script by given Feedback for wrong reasons. After your fixing, the python script given by you should run without error with the given table and function_args. Your answer only needs to contain the function(start with def)
        Note if the answer is in the table, please return the answer. The return value should be in string format. If the answer is not in the table, please return None.

        Now please give your answer to debug.
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
            I will give you a specific question along with its corresponding answer and your objective is to construct a comprehensive, well-structured response in a single, elongated sentence. The response should be formulated directly based on the provided answer, ensuring that it thoroughly addresses the query. 

            Example:
            Question: Which country has won the OGAE Video Contest multiple times?
            Corresponding Answer: Russia, France, and Belgium.

            Response:
            Russia, France, and Belgium have each won the OGAE Video Contest multiple times

            Now please give your answer to generate a long-form answer. Let's think step by step and follow templates of examples. 

            The following is the qustion:'''{question_prompt}'''\
            The following is the corresponding answer:'''{results}'''
            """
    prompt_system = f"""
            You are an expert in generating a long-form answer.
            """
    long_answer = get_completion(prompt_system,prompt_user)

    return long_answer