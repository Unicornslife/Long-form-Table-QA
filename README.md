## Long-form-Table-QA
The data and code for the paper TAPERA: A Modular Framework for Long-form Table Question Answering

<p align="center">
<img src="figures/overview.png" width="80%">
</p>

## Long-form-Table-QA Outputs
We tested our model using the QTSumm and FeTaQA datasets. The specific outcomes of these tests are available in the output files.

### Output File Format

The output is provided in json format, and contains the following attributes:

```
{
        "example_id": [string] The question id,
        "question": [string] The question text,
        "Devided Question 0": [string] Text of the first divided question,
        "function 0's 0 generation": [python sctipt] Generated executable python function to the first devided question,
        "deivdied results 0": [string] The result of python function execution,
        "deivdied long results 0": [string] The long-form answer to the first devided question,
        "Devided Question 1": [string] Text of the second divided question,
        "function 1's 0 generation": [python sctipt] Generated executable python function to the second devided question,
        "deivdied results 1": [string] The result of python function execution,
        "deivdied long results 1": [string] The long-form answer to the second devided question,
        ....
        "prediction": [string] The long-form answer to the question
    },

```

## Experiments
### Environment Setup
The code is tested on the following environment:
- python 3.9.12
- run `pip install -r requirements.txt` to install all the required packages

### How to Run

Once you have Python set up, you can execute the script with the following command:

```
python run_llm.py --api_key [input your OpenAI API key] --base_url [input your OpenAI base URL]
```

#### Arguments Explanation

1. `--model`: Specifies the model you want to use. Default is "gpt-3.5-turbo-1106".
2. `--start_num`: The starting number for processing the data. Default is 0.
3. `--end_num`: The ending number for processing the data. Default is 1000.
4. `--dataset_name`: The name of the dataset you are using. Default is "yale-nlp/QTSumm".
5. `--split_name`: The split of the dataset to be used (e.g., "train", "test"). Default is "test".
6. `--api_key`: Your OpenAI API key. This is required to authenticate your requests.
7. `--base_url`: The base URL for the OpenAI API.
8. `--output_path`: The file path where you want to save the output. Default is "output.json".

### Additional Notes

- replace `[input your OpenAI API key]` and `[input your OpenAI base URL]` with your actual API key and base URL.
- You can customize the script by setting different models, datasets, data splits, and output paths as per your needs.
- If you choose to use different datasets for computation, be aware that it may be necessary to adjust the code according to the structure of the selected dataset. Different datasets may have various formats and requirements, so please ensure that your code can properly handle the specific format of the dataset you select.

## User test

### User Test Interface Description

This section outlines the process and components involved in conducting user testing through the Turkle platform. 

- The primary file for the test interface is named `user_test_interface.html`.
- Within the directory `user_test/input_csv_examples`, we provide a range of CSV files.

### Deployment and Execution

- After setting up the Turkle platform, the next step involves uploading the relevant HTML files and test CSV files.
- Once uploaded, the platform is ready to host user testing sessions, ensuring an efficient testing cycle.

## Contact
For any issues or questions, kindly email us at: Yilun Zhao (yilun.zhao@yale.edu).

## Citation

If you use this in your work, please kindly cite the paper:

```
@misc{zhao2023Long-form-Table-QA,
      title={TAPERA: A Modular Framework for Long-form Table Question Answering}, 
      year={2023},
}
```