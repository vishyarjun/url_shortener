from typing import Union

from fastapi import FastAPI, Request, HTTPException, Form, status
from fastapi.responses import RedirectResponse,JSONResponse
from fastapi.exceptions import RequestValidationError
from models import URL
from hashing import URLHash

app = FastAPI()
url_hash = URLHash()

@app.exception_handler(RequestValidationError)
async def validation_exception_handler(request: Request, exc: RequestValidationError):
    # Get the original 'detail' list of errors
    details = exc.errors()[0]
    print(details)
    if details['msg']=='field required':   
        return JSONResponse(
                status_code=status.HTTP_400_BAD_REQUEST,
                content=f"Missing field: {details['loc'][1]} ",
            )
    return JSONResponse(
                status_code=status.HTTP_400_BAD_REQUEST,
                content=details['msg'],
            )

@app.post("/shorten")
def shorten_a_url(request: Request,url: URL = None):
    print(url)
    url = url.url
    encode = url_hash.generate_hash(url)
    output = {"key":encode,"long_url": url,"short_url": f'{str(request.base_url)}{encode}'}
    return output

@app.get("/{hsh}")
def redirect_url(hsh:str):
    url = url_hash.get_url_from_hash(hsh)
    if url:
        return RedirectResponse(url)
    return "not a valid URL."


@app.delete("/{hsh}")
def remove_mapping(hsh:str):
    
    url_hash.remove_hash_db_cache(hsh)

    return "mapping removed."