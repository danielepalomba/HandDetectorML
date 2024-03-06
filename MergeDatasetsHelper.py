import pandas as pd


def unifica_csv(file1, file2, file3, output_file):
    # Carica i file CSV in DataFrame
    df1 = pd.read_csv(file1)
    df2 = pd.read_csv(file2)
    df3 = pd.read_csv(file3)

    # Verifica che i DataFrame abbiano le stesse colonne
    if not all(df.columns.equals(df1.columns) for df in [df2, df3]):
        raise ValueError("I file CSV devono avere le stesse colonne")

    # Copia i nomi delle colonne solo una volta
    colonne = list(df1.columns)

    # Unisce i DataFrame
    df_unificato = pd.concat([df1, df2, df3], ignore_index=True)

    # Scrive il DataFrame unificato in un nuovo file CSV
    df_unificato.to_csv(output_file, index=False)


if __name__ == "__main__":
    file1 = "forbice-def.csv"
    file2 = "sasso-def.csv"
    file3 = "carta-def.csv"
    output_file = "dataset.csv"

    unifica_csv(file1, file2, file3, output_file)
