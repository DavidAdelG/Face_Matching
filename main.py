from fastapi import FastAPI, File, UploadFile, Body, Form, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from pathlib import Path
import shutil
import os
import base64
from PIL import Image
from opencv.fr import FR
from opencv.fr.persons.schemas import PersonBase
from opencv.fr.search.schemas import VerificationRequest, SearchRequest, SearchMode

app = FastAPI()

# Allow all origins
origins = ["*"]

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"]
)

# Retrieve environment variables
BACKEND_URL = os.getenv("BACKEND_URL")
DEVELOPER_KEY = os.getenv("DEVELOPER_KEY")

# Initialize the SDK
sdk = FR(BACKEND_URL, DEVELOPER_KEY)

@app.head("/", include_in_schema=False)
def root():
    return {"E-Tourism": "Team 29"}

@app.get("/", include_in_schema=False)
def read_root():
    return {"E-Tourism": "Team 29"}

class MPerson(BaseModel):
    id: str

class Person(BaseModel):
    name: str

def save_uploaded_image(image_file: UploadFile, filename: str) -> Path:
    if not image_file.content_type.lower().endswith(("jpg", "jpeg", "png")):
        raise HTTPException(status_code=400, detail="Unsupported image format. Please upload JPG, JPEG, or PNG images.")
    
    image_path = Path("face_images") / filename
    image_path.parent.mkdir(parents=True, exist_ok=True)
    
    with open(image_path, "wb") as buffer:
        shutil.copyfileobj(image_file.file, buffer)
    
    return image_path

def save_base64_image(base64_str: str, filename: str) -> Path:
    try:
        image_data = base64.b64decode(base64_str.split(',')[1])
        
        image_path = Path("face_images") / filename
        image_path.parent.mkdir(parents=True, exist_ok=True)
        
        with open(image_path, "wb") as buffer:
            buffer.write(image_data)
        
        with Image.open(image_path) as img:
            img.verify()
        
        return image_path
    except Exception as e:
        raise HTTPException(status_code=400, detail=f"Invalid base64 image format. {str(e)}") from e

def parse_error_message(error_message: str):
    try:
        # Example error message: "(400, 'ERR_NO_FACES_FOUND', 'Could not obtain at least one face from the supplied image(s)')"
        parts = error_message.strip('()').split(', ', 2)
        status_code = int(parts[0])
        error_code = parts[1].strip("'")
        detail = parts[2].strip("'")
        return status_code, f"{error_code}: {detail}"
    except Exception as e:
        return 400, f"An unknown error occurred. Error: {str(e)}"

@app.get("/list")
def list_person():
    try:
        persons = str(sdk.persons.list())
        return persons
    except Exception as e:
        status_code, detail = parse_error_message(str(e))
        raise HTTPException(status_code=status_code, detail=detail)

@app.post("/add-person")
async def add_person(person_name: str = Form(...), image_file: UploadFile = File(...)):
    try:
        image_path = save_uploaded_image(image_file, f"{person_name}_{os.urandom(8).hex()}.{image_file.content_type.lower().split('/')[-1]}")
        
        search_object = SearchRequest([os.path.relpath(image_path, os.getcwd())], min_score=0.7, search_mode=SearchMode.FAST)
        results = sdk.search.search(search_object)
        
        if results:
            return {
                "message": "FaceID obtained Successfully",
                "ID": results[0].person.id,
                "Name": results[0].person.name,
            }
        
        Iperson = PersonBase([os.path.relpath(image_path, os.getcwd())], name=person_name)
        my_person = sdk.persons.create(Iperson)
        
        return {
            "message": "added successfully",
            "ID": my_person.id
        }
    except Exception as e:
        status_code, detail = parse_error_message(str(e))
        raise HTTPException(status_code=status_code, detail=detail)

@app.post("/add-personBase64")
async def add_person_base64(person_name: str = Form(...), image_base64: str = Body(...)):
    try:
        image_path = save_base64_image(image_base64, f"{person_name}_{os.urandom(8).hex()}.jpg")
        
        search_object = SearchRequest([os.path.relpath(image_path, os.getcwd())], min_score=0.7, search_mode=SearchMode.FAST)
        results = sdk.search.search(search_object)
        
        if results:
            return {
                "message": "FaceID obtained Successfully",
                "ID": results[0].person.id,
                "Name": results[0].person.name,
            }
        
        Iperson = PersonBase([os.path.relpath(image_path, os.getcwd())], name=person_name)
        my_person = sdk.persons.create(Iperson)
        
        return {
            "message": "added successfully",
            "ID": my_person.id
        }
    except Exception as e:
        status_code, detail = parse_error_message(str(e))
        raise HTTPException(status_code=status_code, detail=detail)

@app.post("/face-matching")
async def face_matching(person_id: str = Form(...), image_file: UploadFile = File(...)):
    try:
        image_path = save_uploaded_image(image_file, f"{os.urandom(8).hex()}.{image_file.content_type.lower().split('/')[-1]}")
        
        search_object = SearchRequest([image_path], min_score=0.7, search_mode=SearchMode.FAST)
        results = sdk.search.search(search_object)
        if not results:
            return {"error": "You are matching two different persons."}
        
        if person_id == results[0].person.id:
            verify_object = VerificationRequest(person_id, [str(image_path)])
            results = sdk.search.verify(verify_object)
        
        if results.person._collections:
            collection = str(results.person._collections[0])
            is_reserved = "Reserved" in collection
        else:
            is_reserved = None
        
        return {
            "message": "Done!",
            "Name": results.person._name,
            "isReserved": is_reserved,
            "score": "{:.2f}%".format(results.score * 100)
        }
    except Exception as e:
        status_code, detail = parse_error_message(str(e))
        raise HTTPException(status_code=status_code, detail=detail)

@app.post("/face-matchingBase64")
async def face_matching_base64(person_id: str = Form(...), image_base64: str = Body(...)):
    try:
        image_path = save_base64_image(image_base64, f"{os.urandom(8).hex()}.jpg")
        
        search_object = SearchRequest([image_path], min_score=0.7, search_mode=SearchMode.FAST)
        results = sdk.search.search(search_object)
        if not results:
            return {"error": "You are matching two different persons."}
        
        if person_id == results[0].person.id:
            verify_object = VerificationRequest(person_id, [str(image_path)])
            results = sdk.search.verify(verify_object)
        
        if results.person._collections:
            collection = str(results.person._collections[0])
            is_reserved = "Reserved" in collection
        else:
            is_reserved = None
        
        return {
            "message": "Done!",
            "Name": results.person._name,
            "isReserved": is_reserved,
            "score": "{:.2f}%".format(results.score * 100)
        }
    except Exception as e:
        status_code, detail = parse_error_message(str(e))
        raise HTTPException(status_code=status_code, detail=detail)

@app.post("/search-by-image")
async def search_by_image(image_file: UploadFile = File(...)):
    try:
        image_path = save_uploaded_image(image_file, f"{os.urandom(8).hex()}.{image_file.content_type.lower().split('/')[-1]}")
        
        search_object = SearchRequest([image_path], min_score=0.7, search_mode=SearchMode.FAST)
        results = sdk.search.search(search_object)
        
        if not results:
            return {"message": "No person found in the image."}
        
        return {
            "person_id": results[0].person.id,
            "person_name": results[0].person.name,
            "score": "{:.2f}%".format(results[0].score * 100)
        }
    except Exception as e:
        status_code, detail = parse_error_message(str(e))
        raise HTTPException(status_code=status_code, detail=detail)

@app.post("/search-by-imageBase64")
async def search_by_image_base64(image_base64: str = Body(...)):
    try:
        image_path = save_base64_image(image_base64, f"{os.urandom(8).hex()}.jpg")
        
        search_object = SearchRequest([image_path], min_score=0.7, search_mode=SearchMode.FAST)
        results = sdk.search.search(search_object)
        
        if not results:
            return {"message": "No person found in the image."}
        
        return {
            "person_id": results[0].person.id,
            "person_name": results[0].person.name,
            "score": "{:.2f}%".format(results[0].score * 100)
        }
    except Exception as e:
        status_code, detail = parse_error_message(str(e))
        raise HTTPException(status_code=status_code, detail=detail)

@app.post("/historical-by-image")
async def search_by_image_historical(image_file: UploadFile = File(...)):
    try:
        image_path = save_uploaded_image(image_file, f"{os.urandom(8).hex()}.{image_file.content_type.lower().split('/')[-1]}")
        
        search_object = SearchRequest([image_path], min_score=0.7, search_mode=SearchMode.FAST, collection_ids=[HISTORICAL_COLLECTION_ID])
        results = sdk.search.search(search_object)
        
        if not results:
            return {"message": "No person found in the image within the historical collection."}
        
        return {
            "1st_person": results[0].person.name,
            "1st_score": "{:.2f}%".format(results[0].score * 100),
            "2nd_person": results[1].person.name,
            "2nd_score": "{:.2f}%".format(results[1].score * 100),
            "3rd_person": results[2].person.name,
            "3rd_score": "{:.2f}%".format(results[2].score * 100)
        }
    except Exception as e:
        status_code, detail = parse_error_message(str(e))
        raise HTTPException(status_code=status_code, detail=detail)

@app.post("/historical-by-image-base64")
async def search_by_image_base64_historical(image_base64: str = Body(...)):
    try:
        image_path = save_base64_image(image_base64, f"{os.urandom(8).hex()}.jpg")
        
        search_object = SearchRequest([image_path], min_score=0.7, search_mode=SearchMode.FAST, collection_ids=[HISTORICAL_COLLECTION_ID])
        results = sdk.search.search(search_object)
        
        if not results:
            return {"message": "No person found in the image within the historical collection."}
        
        return {
            "1st_person": results[0].person.name,
            "1st_score": "{:.2f}%".format(results[0].score * 100),
            "2nd_person": results[1].person.name,
            "2nd_score": "{:.2f}%".format(results[1].score * 100),
            "3rd_person": results[2].person.name,
            "3rd_score": "{:.2f}%".format(results[2].score * 100)
        }
    except Exception as e:
        status_code, detail = parse_error_message(str(e))
        raise HTTPException(status_code=status_code, detail=detail)

@app.post("/search-by-id")
def search_by_id(person_id: str = Form(...)):
    try:
        search_results = sdk.persons.get(person_id)
        
        if not search_results:
            return {"message": "No person found with the provided ID."}
        
        return {
            "Name": search_results.name,
            "isReserved": search_results.collections
        }
    except Exception as e:
        status_code, detail = parse_error_message(str(e))
        raise HTTPException(status_code=status_code, detail=detail)

@app.post("/reserve-person")
def reserve(person_id: str = Form(...)):
    try:
        id = person_id
        person = sdk.persons.get(id)
        person.collections = [sdk.collections.get("1f11ea6b-05d2-458b-846e-73df744efb64")]
        sdk.persons.update(person)
        return {
            "Person ID": id,
            "Name": person.name,
            "isReserved": sdk.collections.get("1f11ea6b-05d2-458b-846e-73df744efb64").name
        }
    except Exception as e:
        status_code, detail = parse_error_message(str(e))
        raise HTTPException(status_code=status_code, detail=detail)

@app.delete("/delete-person")
def delete_person(person_id: str = Form(...)):
    try:
        sdk.persons.delete(person_id)
        return {"message": "Person deleted successfully."}
    except Exception as e:
        status_code, detail = parse_error_message(str(e))
        raise HTTPException(status_code=status_code, detail=detail)
