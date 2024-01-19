## Long-form-Table-QA
The data and code for the paper TAPERA: A Modular Framework for Long-form Table Question Answering

<p align="center">
<img src="figures/overview.png" width="80%">
</p>

## Long-form-Table-QA Outputs
We tested our model on the QTSumm and FeTaQA datasets, and the specific results can be observed in outputs

The output is provided in json format and contains the following attributes:

```
{
        "example_id": [string] The question id,
        "question": [string] The question text,
        "Devided Question 0": [string] The first devided question text,
        "function 0's 0 generation": [python sctipt] Generated executable python function to the first devided question,
        "deivdied results 0": [string] The result of python function execution,
        "deivdied long results 0": [string] The long-form answer to the first devided question,
        "Devided Question 1": [string] The second devided question text,
        "function 1's 0 generation": [python sctipt] Generated executable python function to the second devided question,
        "deivdied results 1": [string] The result of python function execution,
        "deivdied long results 1": [string] The long-form answer to the second devided question,
        "prediction": [string] The long-form answer to the question
    },
```

## Experiments
### Environment Setup
The code is tested on the following environment:
- python 3.9.12
- run `pip install -r requirements.txt` to install all the required packages

## User test

### User test interface

This user test is based on the Turke platform. The html file used for the test is user_test_interface.html. Examples of input tests are given in user_test/input_csv_examples.

After deploying the turkle platform, upload the relevant html files and test csv files

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