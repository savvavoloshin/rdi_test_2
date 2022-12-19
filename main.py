from fastapi import FastAPI, File, UploadFile

import filetype
import soundfile as sf
import io

app = FastAPI()

@app.post("/files/")
async def create_file(file: bytes = File()):

    def readWavHeader(file):
        bitsPerSample = file[34]
        audioFormat = file[20]
        return {"bitsPerSample": bitsPerSample, "audioFormat": audioFormat}
    
    def wavDuration(file):        
        f = sf.SoundFile(file=io.BytesIO(file))
        return (f.frames / f.samplerate)

    kind = filetype.guess(file)

    filetype_info = {"extension": None, "MIME type": None, "isValid": False, "errors": []}
    duration = None

    if kind:
        filetype_info["extension"] = kind.extension
        filetype_info["MIME type"] = kind.mime
        
        if (kind.extension == 'wav'):
            wavHeaderParams = readWavHeader(file)
            duration = wavDuration(file)

            # wav should be signed int16 and to be not more than 10 seconds length
            if (wavHeaderParams["bitsPerSample"] == 16):
                if (wavHeaderParams["audioFormat"] == 1):
                    if (duration <= 10.0):
                        filetype_info["isValid"] = True

            if (wavHeaderParams["bitsPerSample"] != 16):
                filetype_info["errors"].append("BitsPerSample should be 16")
            if (wavHeaderParams["audioFormat"] != 1):
                filetype_info["errors"].append("Wav is not PCM")
            if (wavDuration(file) > 10.0):
                filetype_info["errors"].append("Duration is too long, > 10 sec...")

        else:
            filetype_info["errors"].append("file format should be wav")
    else:
        filetype_info["errors"].append("file format error")

    return {"file_size": len(file), "filetype_info": filetype_info}