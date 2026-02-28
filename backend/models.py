from pydantic import BaseModel
from typing import List, Optional

class OrderItem(BaseModel):
    menu_item_id: int
    quantity: int

class PlaceOrder(BaseModel):
    customer_id: int
    restaurant_id: int
    items: List[OrderItem]

class CustomerCreate(BaseModel):
    name: str
    email: str
    phone: Optional[str] = None
    address: Optional[str] = None

class SignupModel(BaseModel):
    name: str
    email: str
    phone: Optional[str] = None
    address: Optional[str] = None
    password: str

class LoginModel(BaseModel):
    email: str
    password: str