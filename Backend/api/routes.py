from fastapi import APIRouter
import pandas as pd
import numpy as np

router = APIRouter()

@router.get("/")
def read_root():
    return {"Hello": "World"}

@router.get("/llm")
def read_csv():
    # Path to your CSV file
    csv_file_path = "data/llm2024.csv"

    try:
        # Read the CSV file using Pandas
        df = pd.read_csv(csv_file_path, encoding='latin1')

        # Replace infinite values with NaN
        df = df.replace([np.inf, -np.inf], np.nan)

        # Replace NaN values with None for JSON serialization
        data = df.where(pd.notnull(df), None).to_dict(orient="records")

    except FileNotFoundError:
        return {"error": "CSV file not found"}
    except Exception as e:
        return {"error": str(e)}

    return {"data": data}
