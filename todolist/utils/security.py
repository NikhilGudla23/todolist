import html

def sanitize_text(text):
    """
    Sanitize plain text by escaping HTML special tags.
    Helps prevent XSS and layout breaks in Streamlit markdown rendering.
    """
    if text is None:
        return ""
    return html.escape(str(text).strip())
