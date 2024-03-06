import pandas as pd

def aggiungi_colonna_result(input_file, output_file):
    df = pd.read_csv(input_file)

    #df['result'] = 1 Forbice
    # df['result'] = 2 Carta
    # df['result'] = 3 Sasso

    df.to_csv(output_file, index=False)

# Esempio di utilizzo
input_file = 'your-file.csv'
output_file = 'your-output-file.csv'

aggiungi_colonna_result(input_file, output_file)
