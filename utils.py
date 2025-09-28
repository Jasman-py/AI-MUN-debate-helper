import datetime
import pdfkit
import os


def export_transcript_to_text(topic, transcript, filename=None):
    if filename is None:
        timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M")
        filename = f"argumind_transcript_{timestamp}.txt"
    with open(filename, "w", encoding="utf-8") as f:
        f.write(f"Topic: {topic}\n\n")
        f.write(transcript)
    return os.path.abspath(filename)

def export_transcript_to_pdf(html_content, filename=None):
    # requires wkhtmltopdf installed on system
    if filename is None:
        filename = "argumind_debate_transcript.pdf"
    pdfkit.from_string(html_content, filename)
    return os.path.abspath(filename)

def simple_fallacy_guessing(text):
    """
    Lightweight heuristic: looks for common fallacy words - not rigorous.
    Use LLM-based fallacy detection for production.
    """
    suspects = []
    fallacy_triggers = {
        "ad hominem": ["you're", "they are stupid", "you are", "character"],
        "appeal to emotion": ["feel", "heart", "think about"],
        "slippery slope": ["will lead to", "end up causing"],
    }
    lower = text.lower()
    for name, triggers in fallacy_triggers.items():
        if any(t in lower for t in triggers):
            suspects.append(name)
    return suspects