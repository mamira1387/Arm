from fastapi import FastAPI, File, UploadFile
from fastapi.responses import StreamingResponse
from typing import Dict
from io import BytesIO

app = FastAPI()

# ذخیره فریم‌ها به‌صورت درون‌حافظه‌ای
frames: Dict[str, BytesIO] = {}

@app.post("/send_frame_from_file/{stream_id}")
async def send_frame_from_file(stream_id: str, file: UploadFile = File(...)):
    content = await file.read()
    frames[stream_id] = BytesIO(content)
    return {"message": "Frame received"}

@app.get("/video_feed/{stream_id}")
async def video_feed(stream_id: str):
    async def frame_generator():
        while True:
            if stream_id in frames:
                frame = frames[stream_id].getvalue()
                yield (b"--frame\r\n"
                       b"Content-Type: image/jpeg\r\n\r\n" + frame + b"\r\n")
    return StreamingResponse(frame_generator(), media_type="multipart/x-mixed-replace; boundary=frame")
