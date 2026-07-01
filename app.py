import os
from __init__ import create_app

app = create_app()

if __name__ == "__main__":
    # Hugging Face Spaces secara mutlak mewajibkan port 7860 dan host 0.0.0.0
    port = int(os.environ.get("PORT", 7860))
    app.run(host="0.0.0.0", port=port)