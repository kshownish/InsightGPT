import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import io
import os
import re
import contextlib
from openai import OpenAI
from dotenv import load_dotenv

load_dotenv()
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

def summarize_dataframe(df, max_rows=5):
    summary = f"Shape: {df.shape}\n\n"
    summary += "Columns:\n"
    for col in df.columns:
        summary += f"- {col} ({df[col].dtype}) | Nulls: {df[col].isnull().sum()}\n"
    summary += "\nSample Preview:\n"
    summary += str(df.head(max_rows)) + "\n\n"
    summary += "Stats:\n"
    summary += str(df.describe(include='number')) + "\n"
    return summary

def generate_code_from_gpt(summary, question, domain="General"):
    domain_hint = {
        "General": "",
        "Finance": "You are analyzing financial data like revenue, sales, expenses.",
        "Healthcare": "You are analyzing patient records or medical data."
    }

    prompt = f"""
You are a Python data analyst using pandas and seaborn/matplotlib.

You are working with a DataFrame called **df**.

Here is the dataset summary:
{summary}

Domain: {domain_hint.get(domain, "")}

Now write Python code to answer this user question:
"{question}"

Use ONLY the variable name 'df' — do not use 'data' or anything else.

Only return:
```python
<your code>
```
Use quotes around string comparisons. Do not use plt.show().
"""
    response = client.chat.completions.create(
    model="gpt-3.5-turbo",
    messages=[
        {"role": "system", "content": "You generate Python pandas/matplotlib code to analyze data."},
        {"role": "user", "content": prompt}
    ]
)

    reply = response.choices[0].message.content.strip()
    match = re.search(r"```python(.*?)```", reply, re.DOTALL)
    return match.group(1).strip() if match else reply.strip()

def execute_generated_code(code, df):
    plot_detected = any(x in code.lower() for x in ["plt.", "sns.", "df.plot"])
    image_path = None
    try:
        local_vars = {"df": df, "plt": plt, "sns": sns}
        plt.clf()  # reset plot

    # Execute the code
        with contextlib.redirect_stdout(io.StringIO()):
            exec(code, {}, local_vars)

        if plot_detected:
            image_path = f"temp_plot_{hash(code)}.png"
            plt.savefig(image_path, bbox_inches='tight')
            return "📊 Chart generated successfully.", image_path

        # Try to return the last result variable
        result_vars = [k for k in local_vars if k not in ["df", "plt", "sns"]]
        if result_vars:
            return local_vars[result_vars[-1]], None

        return "✅ Code ran successfully, but no result returned.", None

    except Exception as e:
        return f"⚠️ Error executing code: {e}\n\nGenerated code:\n{code}", None

def ask_gpt_to_explain_result(result, question, domain="General"):
    if isinstance(result, str) and "⚠️" in result:
        return result
    prompt = f"""
You're a data assistant. User asked: "{question}"
Here is the result: {result}

Explain what this result means. Domain: {domain}.
Be clear, brief, and use plain English.
"""
    response = client.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=[
            {"role": "system", "content": "Explain data results in user-friendly language."},
            {"role": "user", "content": prompt}
        ]
    )

    return response.choices[0].message.content.strip()
