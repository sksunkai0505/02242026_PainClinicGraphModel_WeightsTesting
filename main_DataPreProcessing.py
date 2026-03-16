from resourceWeightsUtilities import *


if __name__ == "__main__":
    logistic_file = "PredictionsRaw/LLM_LOGISTIC_OR_noleak_Predicted_Probability_2024-03-01.csv"
    template_file = "WeightDataTemplate.csv"
    output_file = "WeightDataTemplate_updated.csv"

    update_weight_template(logistic_file, template_file, output_file)

    clean_df = preprocess_remove_pre_monday_and_weekends(
    input_filepath="WeightDataTemplate_updated.csv",
    output_filepath="WeightDataTemplate_Cleaned.csv",
    date_column="Date"   # change if your column name differs
    )
    print("8-----clean_df: {0}".format(clean_df))