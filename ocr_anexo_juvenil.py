"""OCR auxiliar: el PDF escaneado oficial sigue siendo la fuente de autoridad."""
from pathlib import Path
import fitz,json,time
import numpy as np
from rapidocr_onnxruntime import RapidOCR
ROOT=Path(__file__).resolve().parent
path=ROOT/'biblioteca/2026/referencias/Codigo-Procesal-Penal-Juvenil-2026.pdf'
out=path.with_name(path.stem+'-OCR.txt')
images=path.parent/'juvenil-paginas'; images.mkdir(exist_ok=True)
engine=RapidOCR()
doc=fitz.open(path); pages=[]
for i,page in enumerate(doc):
    image=page.get_pixmap(matrix=fitz.Matrix(1.8,1.8),alpha=False)
    png=images/f'p{i+1:02d}.png'; image.save(png)
    array=np.frombuffer(image.samples,dtype=np.uint8).reshape(image.height,image.width,3)
    results,_=engine(array)
    text='\n'.join(r[1] for r in (results or []))
    pages.append(f'=== PÁGINA PDF {i+1} (OCR AUXILIAR; CONTRASTAR ORIGINAL) ===\n'+text)
    out.write_text('\n\n'.join(pages),encoding='utf-8')
    print(f'OCR {i+1}/{len(doc)}: {len(text)} caracteres',flush=True)
