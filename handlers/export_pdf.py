from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas
from reportlab.lib.units import inch
from reportlab.lib import colors
import os
from textwrap import wrap

def draw_wrapped_text(c, text, x, y, max_width, line_height):
    for line in wrap(text, width=95):
        c.drawString(x, y, line)
        y -= line_height
        if y < 1 * inch:
            c.showPage()
            y = 10.5 * inch
    return y

def export_chat_to_pdf(chat_history, filename="InsightPilot_Report.pdf"):
    c = canvas.Canvas(filename, pagesize=letter)
    width, height = letter
    y = height - inch

    c.setFont("Helvetica-Bold", 16)
    c.drawString(1 * inch, y, "📊 InsightPilot Session Report")
    y -= 0.5 * inch

    for entry in chat_history:
        question = entry["question"]
        answer = entry["answer"]
        code = entry.get("code")
        result = entry.get("result")
        plot_path = entry.get("plot")

        c.setFont("Helvetica-Bold", 12)
        y = draw_wrapped_text(c, f"🧑 You: {question}", 1 * inch, y, width - 1.5 * inch, 14)

        c.setFont("Helvetica", 11)
        y = draw_wrapped_text(c, f"🤖 InsightPilot: {answer}", 1.2 * inch, y, width - 1.5 * inch, 13)

        if result:
            y -= 0.1 * inch
            c.setFont("Helvetica-Bold", 11)
            y = draw_wrapped_text(c, f"📈 Result: {result}", 1.2 * inch, y, width - 1.5 * inch, 13)

        if code:
            y -= 0.1 * inch
            c.setFont("Courier-Bold", 10)
            y = draw_wrapped_text(c, "📜 Code:", 1 * inch, y, width - 1.5 * inch, 14)

            c.setFont("Courier", 9)
            for line in code.splitlines():
                y = draw_wrapped_text(c, line.strip(), 1.2 * inch, y, width - 1.5 * inch, 11)

        if plot_path and os.path.exists(plot_path):
            try:
                c.drawImage(plot_path, 1.2 * inch, y - 3 * inch, width=4.5 * inch, preserveAspectRatio=True, mask='auto')
                y -= 3.5 * inch
            except Exception:
                pass

        y -= 0.3 * inch
        if y < 1 * inch:
            c.showPage()
            y = height - inch

    c.save()
    return filename
