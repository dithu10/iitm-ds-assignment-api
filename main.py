from fastapi import FastAPI, UploadFile, File, Form
import pandas as pd
import zipfile
import io
import os

app = FastAPI()

@app.post("/api/")
async def answer_question(question: str = Form(...), file: UploadFile = File(None)):
    if "CSV file inside" in question.lower() and file:
        # Handle ZIP file processing
        with zipfile.ZipFile(io.BytesIO(await file.read()), "r") as zip_ref:
            zip_ref.extractall("extracted_files")

        # Find the extracted CSV file
        extracted_files = os.listdir("extracted_files")
        csv_file = [f for f in extracted_files if f.endswith(".csv")]

        if csv_file:
            df = pd.read_csv(f"extracted_files/{csv_file[0]}")
            if "answer" in df.columns:
                return {"answer": str(df["answer"].iloc[0])}
            return {"answer": "No 'answer' column found in CSV"}

    # Default response for text-based questions
    return {"answer": "This is a placeholder. LLM-based answering can be added."}
