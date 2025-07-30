import os
from openai import OpenAI
from dotenv import load_dotenv
import re
from followup_handler import generate_followup_answer
from csv_handler import summarize_dataframe, generate_code_from_gpt, execute_generated_code, ask_gpt_to_explain_result
from rag_handler import get_context_from_rag

load_dotenv()
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

def generate_hybrid_answer(summary, followup_question):
    """
    Combines both dataset summary and RAG context to form a hybrid response.
    """
    # 1. Get context from RAG (real_estate_knowledge.txt)
    context = get_context_from_rag(followup_question)

    # 2. Construct hybrid prompt
    prompt = f"""
You are an intelligent data assistant.

Use the dataset summary and real estate knowledge to answer the question below:

--- Dataset Summary ---
{summary}

--- Knowledge Base Context ---
{context}

--- Question ---
{followup_question}

Give a clear and data-aware answer based on both sources.
"""

    response = client.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=[
            {"role": "system", "content": "You answer real estate questions using both data and knowledge."},
            {"role": "user", "content": prompt}
        ]
    )

    return response.choices[0].message.content.strip()



def route_smart_answer(df, question):
    # Check if question is asking for code generation
    keywords = ["code", "generate code", "python code", "how to get", "what is the code", "write code"]
    if any(keyword in question.lower() for keyword in keywords):
        summary = summarize_dataframe(df)
        code = generate_code_from_gpt(summary, question)
        result = execute_generated_code(code, df)
        explanation = ask_gpt_to_explain_result(result, question)

        return f"""
```python
{code}
```
📊 Result: {result}

🧠 Insight: {explanation}
"""
    else:
        return generate_hybrid_answer(df, question)


import re
from followup_handler import generate_followup_answer
from csv_handler import summarize_dataframe, generate_code_from_gpt, execute_generated_code, ask_gpt_to_explain_result
from rag_handler import get_context_from_rag

def route_smart_answer(df, question):
    q_lower = question.lower()

    if any(word in q_lower for word in ['why', 'how', 'reason', 'advantage']):
        # Use RAG reasoning
        return generate_followup_answer(question)

    elif any(word in q_lower for word in ['how many', 'average', 'sum', 'count', 'maximum', 'minimum']):
        # Use code + CSV
        summary = summarize_dataframe(df)
        code = generate_code_from_gpt(summary, question)
        result = execute_generated_code(code, df)
        return ask_gpt_to_explain_result(result, question)

    else:
        # Default to hybrid
        from hybrid_handler import generate_hybrid_answer
        return generate_hybrid_answer(df, question)
