import pandas as pd
import os

def generate_dbt_from_excel(file_path: str, output_dir: str = "dbt_models") -> str:
    df = pd.read_excel(file_path, sheet_name=0, engine="openpyxl")
    mapped_df = df[df["Overall Mapping Status"] == "Mapped"]

    target_table = mapped_df["Target Entity"].iloc[0]
    base_table = mapped_df["Source Entity"].iloc[0]

    sql_lines = ["SELECT"]
    for _, row in mapped_df.iterrows():
        transformation = row["ETL Transformation logic"]
        source_entity = row["Source Entity"]
        source_attribute = row["Source Attribute"]
        target_attribute = row["Target Attribute"]

        if pd.notna(transformation) and transformation.strip() != "":
            sql_line = f"    {transformation} AS {target_attribute}"
        else:
            sql_line = f"    {source_entity}.{source_attribute} AS {target_attribute}"
        sql_lines.append(sql_line + ",")

    sql_lines[-1] = sql_lines[-1].rstrip(",")
    sql_lines.append(f"FROM {base_table}")

    for join in mapped_df["Mapping joins"].dropna().unique():
        if "=" in join:
            right_table = join.split("=")[1].strip().split(".")[0]
            sql_lines.append(f"JOIN {right_table} ON {join}")

    sql_content = "
".join(sql_lines)

    schema_lines = [
        "version: 2",
        "",
        "models:",
        f"  - name: {target_table}",
        f"    description: "Auto-generated DBT model for {target_table}"",
        "    columns:"
    ]

    for _, row in mapped_df.iterrows():
        target_attribute = row["Target Attribute"]
        remarks = row["Remarks"] if pd.notna(row["Remarks"]) else "Auto-generated column"
        schema_lines.append(f"      - name: {target_attribute}")
        schema_lines.append(f"        description: "{remarks}"")
        schema_lines.append(f"        tests:")
        schema_lines.append(f"          - not_null")

    os.makedirs(output_dir, exist_ok=True)
    with open(os.path.join(output_dir, f"{target_table}.sql"), "w") as f:
        f.write(sql_content)
    with open(os.path.join(output_dir, "schema.yml"), "w") as f:
        f.write("
".join(schema_lines))

    return f"Generated: {output_dir}/{target_table}.sql, {output_dir}/schema.yml"
