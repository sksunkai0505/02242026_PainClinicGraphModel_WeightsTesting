from resourceWeightsUtilities import *

clean_df = preprocess_remove_pre_monday_and_weekends(
    input_filepath="WeightDataTemplate.csv",
    output_filepath="WeightDataTemplate_Cleaned.csv",
    date_column="Date"   # change if your column name differs
    )
print("8-----clean_df: {0}".format(clean_df))