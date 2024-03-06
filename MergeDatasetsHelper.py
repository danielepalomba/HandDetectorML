import pandas as pd


def unify_csv(file1, file2, output_file):

    df1 = pd.read_csv(file1)
    df2 = pd.read_csv(file2)

    # verify that the DataFrames have the same columns
    if not all(df.columns.equals(df1.columns) for df in [df2]):
        raise ValueError("I file CSV devono avere le stesse colonne")

    colonne = list(df1.columns)

    # unify dataframes
    df_unificato = pd.concat([df1, df2], ignore_index=True)

    # write
    df_unificato.to_csv(output_file, index=False)


if __name__ == "__main__":
    file1 = "file1.csv"
    file2 = "file2.csv"
    output_file = "output.csv"

    unify_csv(file1, file2, output_file)
