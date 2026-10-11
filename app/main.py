import os
import frontmatter
import markdown
from flask import Flask, render_template

app = Flask(__name__)

def load_markdown_entries():
    entries = []
    content_dir = "content"
    if not os.path.exists(content_dir):
        return entries
    
    for filename in os.listdir(content_dir):
        if filename.endswith(".md"):
            filepath = os.path.join(content_dir, filename)
            with open(filepath, "r", encoding="utf-8") as f:
                post = frontmatter.load(f)
                html_content = markdown.markdown(post.content)
                entries.append({
                    "title": post.metadata.get("title", "Untitled"),
                    "date": post.metadata.get("date", ""),
                    "category": post.metadata.get("category", "General"),
                    "content": html_content
                })
    
    entries.sort(key=lambda x: x["date"], reverse=True)
    return entries

@app.route('/')
def home():
    entries = load_markdown_entries()
    return render_template('index.html', entries=entries)

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=int(os.environ.get("PORT", 8080)))
