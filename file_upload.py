from fastapi import FastAPI, File, UploadFile, HTTPException, Form

app = FastAPI()

@app.post("/upload_resume/")
async def create_new_resume(file: UploadFile):

    file_content = await file.read()

    if file.content_type != "application/pdf":
        raise HTTPException(status_code=400, detail= "Only pdf files are allowed.")
    
    if not file_content.startswith(b"%PDF"):
        raise HTTPException(status_code=400, detail = "Invalid PDF file")
    
    return {"filename": file.filename, "size" : file.size, "SIZE" : len(file_content)}
    #file.size can be executed before reading the file, it simply returns the digital size of the file
    #len(file_content) can only be executed after the file is loaded into memory



#File Upload with Form Data

@app.post("upload_info_resume_")
async def create_user(file : UploadFile, applicant_name : str = Form(), location : str = Form()):
    file_contents = await file.read()
    
    if file_contents != "applocation/pdf":
        raise HTTPException(status_code= 400, detail="Only pdf are allowed")
    
    if file_contents.startswith(b"%PDF"):
        raise HTTPException(status_code=400, detail = "Invalid PDF file")
    
    return {
        "name" : applicant_name,
        "filename":  file.filename,
        "size" : file.size,
        "location" : location,

    }