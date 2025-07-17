import easyocr
import numpy as np
from PIL import Image
import io

class OCRHandler:
    def __init__(self):
        # only load once, CPU fallback
        self.reader = easyocr.Reader(["en"], gpu=False)

    async def extract_text(self, image_bytes: bytes) -> str:
        try:
            img = Image.open(io.BytesIO(image_bytes)).convert("RGB")
            arr = np.array(img)
            results = self.reader.readtext(arr)
            texts = [t for (_, t, p) in results if p > 0.5]
            if not texts:
                return "No text could be extracted from the image."
            return " ".join(texts)
        except Exception as e:
            print(f"[OCRHandler] error: {e}")
            return f"Error processing image: {e}"