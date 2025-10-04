# DBT Model Generator Agent

This project uses LangChain to create an agent that dynamically generates DBT model SQL and schema.yml files from an Excel-based Source-to-Target (S2T) mapping.

## Features

- Parses Excel S2T mapping file
- Dynamically builds SQL transformation logic (no templating)
- Generates `schema.yml` with column metadata and tests
- Uses LangChain agent with tool integration
- Supports aggregation, joins, and transformation logic from mapping

## Project Structure

dbt_agent/
├── main.py                  # LangChain agent entry point
├── tools/
│   └── dbt_generator.py     # Core logic to parse Excel and generate DBT files
├── dbt_models/              # Output folder for generated SQL and YAML
└── CTMS_S2T_Detailed_Mapping.xlsx  # Sample input file

## Setup Instructions

1. Clone the repository
2. Create a virtual environment
3. Install dependencies
4. Run the agent

## Requirements

- Python 3.8+
- pandas
- openpyxl
- langchain
- openai

## License

MIT License
