from fastapi import FastAPI
from pydantic import BaseModel

app = FastAPI()

# курсы относительно USD
kursy = {
    "USD": 1.0,
    "EUR": 0.92,
    "RUB": 89.0,
    "GBP": 0.79,
    "JPY": 155.0,
    "CNY": 7.25
}

class ReqData(BaseModel):
    amount: float
    from_curr: str
    to_curr: str

@app.post("/convert")
def convert(req: ReqData):
    if req.amount < 0:
        return {"error": "сумма не может быть отрицательной"}, 400
        
    valid = ["USD", "EUR", "RUB", "GBP", "JPY", "CNY"]
    if req.from_curr not in valid or req.to_curr not in valid:
        return {"error": "валюта не поддерживается"}, 400
        
    # считаем через USD
    usd_part = req.amount / kursy[req.from_curr]
    final = usd_part * kursy[req.to_curr]
    rate = kursy[req.to_curr] / kursy[req.from_curr]
    
    return {
        "message": f"{req.amount} {req.from_curr} = {round(final, 2)} {req.to_curr}",
        "result": round(final, 2),
        "rate": round(rate, 4)
    }

@app.get("/currencies")
def show_all():
    return kursy