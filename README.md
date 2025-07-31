# 🧠 InsightGPT – Talk to Your Data

Ever wished your dataset could just answer your questions directly?

*InsightGPT* is a chat-based data analyst that lets you upload a CSV and ask questions in plain English — and get back real Python code, charts, and explanations. It’s like having a junior data scientist who never sleeps.

---

## ⚡ What It Actually Does

* Upload a dataset (CSV)

* Ask questions like:

  > “How many houses have 3 bedrooms and a driveway?”
  > “Can you plot the correlation between sales and discount?”

* InsightGPT uses *OpenAI’s GPT-3.5* to write Python code, runs it securely, shows you:

  * 📈 *Charts* (Matplotlib / Seaborn)
  * 📊 *Results*
  * 🧠 *Natural language explanation*

* Export the full chat (with code + charts) as a *PDF report* ✨

* Auto-deployment with GitHub Actions + Docker + AWS EC2 🚀

* Real-time system monitoring via CloudWatch 📡

* Supports cost alarms (e.g., notify if usage > \$1) 💸

And if your question is outside the dataset? InsightGPT switches to a *RAG (Retrieval-Augmented Generation)* mode with domain-specific context.

---

## 🧠 Why I Built This

Most data assistants today are either too rigid or too generic. I wanted to build something that:

* Understands your dataset dynamically
* Feels like a real conversation
* Is beginner-friendly but production-scalable
* Combines the best of GPT + real Python execution
* Deploys cleanly with automated CI/CD flows

---

## 🧱 Tech Stack

* *Frontend*: Streamlit
* *LLM*: OpenAI GPT-3.5
* *RAG Framework*: LangChain + FAISS
* *Plotting*: Matplotlib, Seaborn, Plotly
* *PDF Reports*: ReportLab
* *Data Ops*: Pandas, NumPy
* *Deployment*: Docker + EC2
* *Monitoring*: CloudWatch
* *CI/CD*: GitHub Actions

---

## 🚀 How to Run It Locally

1. Clone the repo:

```bash
git clone https://github.com/kshownish/InsightGPT.git
cd InsightGPT
```

2. Install the dependencies:

```bash
pip install -r requirements.txt
```

3. Add your OpenAI API key to a .env file:

```env
OPENAI_API_KEY=sk-xxxxxxxxxxxx
```

4. Launch the app:

```bash
streamlit run app.py
```

---

## 🔍 Features at a Glance

| Feature                | Description                                            |
| ---------------------- | ------------------------------------------------------ |
| 💬 Natural Language QA | Ask anything about your dataset                        |
| 🧠 GPT-Generated Code  | View the actual code generated behind the scenes       |
| 📊 Charts & Stats      | Scatterplots, histograms, correlation heatmaps, etc.   |
| 📄 PDF Export          | Save the full chat history with code + plots           |
| 🧠 RAG Mode            | Handles general domain questions using FAISS+LangChain |
| 🧵 Domain Toggle       | Switch between Finance, Healthcare, General contexts   |
| 🐳 Dockerized App      | Easily deployable via container                        |
| 🚀 GitHub CI/CD        | Push-to-deploy setup using GitHub Actions              |
| 📡 CloudWatch Monitor  | System metrics visible in AWS dashboard                |
| 🚨 Cost Alarm Setup    | Get notified if billing exceeds \$1                    |

---

## 🥪 Demo Prompt Ideas

* “Show me the average price by location”
* “Are bathrooms and price correlated?”
* “Plot the distribution of sales across regions”
* “What is standard deviation and why does it matter?” (RAG mode)

---

## 🌐 Structure

```
InsightGPT/
├── app.py                  # Main Streamlit app
├── requirements.txt
├── .gitignore
├── .dockerignore
├── Dockerfile              # Docker instructions
├── .github/workflows       # GitHub Actions YAML
│   └── deploy.yml          # CI/CD pipeline
├── rag_knowledge/          # Domain-specific knowledge (RAG fallback)
├── handlers/               # Modular logic handlers
│   ├── csv_handler.py
│   ├── followup_handler.py
│   ├── rag_handler.py
│   └── export_pdf.py
```

---

## ✅ Future Enhancements

* 🔐 User Authentication (guest vs registered sessions)
* ☁ Deployment via ECS/Fargate
* 📆 Session storage in S3
* 🧠 Memory-based follow-ups
* 🔄 Better PDF theming & branding

---

## 🤝 Let’s Connect

This project is proudly built by **Kshownish Parachikapu**.

📧 Email me: [kshownishparachikapu@gmail.com](mailto:kshownishparachikapu@gmail.com)
🔗 Connect on LinkedIn: [LinkedIn](https://linkedin.com/in/kshownish-parachikapu-bb1b16214)

---

## 📄 License

MIT – Free to use, modify, and share.
