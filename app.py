<<<<<<< HEAD
import os
from __init__ import create_app

app = create_app()

if __name__ == "__main__":
    # Hugging Face Spaces secara mutlak mewajibkan port 7860 dan host 0.0.0.0
    port = int(os.environ.get("PORT", 7860))
=======
import os
from __init__ import create_app

app = create_app()

if __name__ == "__main__":
    # Hugging Face Spaces secara mutlak mewajibkan port 7860 dan host 0.0.0.0
    port = int(os.environ.get("PORT", 7860))
>>>>>>> b73cd00b7e0ae6d1410a1de57b403e897908a1fa
    app.run(host="0.0.0.0", port=port)