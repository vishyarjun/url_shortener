from pydantic import BaseModel, HttpUrl, validator

class URL(BaseModel):
    url: HttpUrl