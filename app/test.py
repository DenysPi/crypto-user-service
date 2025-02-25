from fastapi.templating import Jinja2Templates
from fastapi import Request
templates = Jinja2Templates(directory="templates")
print(templates)

def login_page(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})

login_page('g')