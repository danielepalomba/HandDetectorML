import pandas as pd

def add_column_result(input_file, output_file):
    df = pd.read_csv(input_file)

    '''
    df['result'] = 1 Scissor
    df['result'] = 2 Paper
    df['result'] = 3 Rock
    df['result'] = 4 ErrorHandling
    '''

    df.to_csv(output_file, index=False)

# Example
input_file = 'input.csv'
output_file = 'output.csv'

add_column_result(input_file, output_file)
