"""
Library API

Author: Sandeep Sharma
Author Email: sandeeptech8@gmail.com
"""

from fastapi import FastAPI, Depends

app = FastAPI()

@app.get("/")
async def home():
    """
    home
    """
    return {"message": "Hello world"}
