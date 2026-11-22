import io
import edge_tts
from fastapi import FastAPI, Query, Response

app = FastAPI()

@app.get("/")
async def health():
    return {"status": "ok"}

@app.get("/tts")
async def tts(text: str = Query(...), gender: str = Query("male")):
    voice = "km-KH-SreymomNeural" if "female" in gender.lower() else "km-KH-PisethNeural"
    communicate = edge_tts.Communicate(text, voice)
    buf = io.BytesIO()
    async for chunk in communicate.stream():
        if chunk["type"] == "audio":
            buf.write(chunk["data"])
    return Response(content=buf.getvalue(), media_type="audio/mpeg")
