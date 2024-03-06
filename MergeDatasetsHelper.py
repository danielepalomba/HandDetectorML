import pandas as pd


def unify_csv(file1, file2, file3, file4, file5, output_file):

    df1 = pd.read_csv(file1)
    df2 = pd.read_csv(file2)
    df3 = pd.read_csv(file3)
    df4 = pd.read_csv(file4)
    df5 = pd.read_csv(file5)

    # verify that the DataFrames have the same columns
    if not all(df.columns.equals(df1.columns) for df in [df2, df3, df4, df5]):
        raise ValueError("I file CSV devono avere le stesse colonne")

    colonne = list(df1.columns)

    # unify dataframes
    df_unificato = pd.concat([df1, df2, df3, df4, df5], ignore_index=True)

    # write
    df_unificato.to_csv(output_file, index=False)


if __name__ == "__main__":
    file1 = "paper-labeled.csv"
    file2 = "wrong-labeled.csv"
    file3 = "exit-labeled.csv"
    file4 = "scissor-labeled.csv"
    file5 = "rock-labeled.csv"
    output_file = "merged-dataset.csv"

    unify_csv(file1, file2, file3, file4, file5, output_file)
