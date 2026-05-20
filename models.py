from sqlmodel import SQLModel, Field
from datetime import datetime

class Route(SQLModel, table=True):
    id: int | None = Field(default=None, primary_key=True)
    name: str
    status: str = Field(default="waiting")
    created_at: datetime = Field(default_factory=datetime.utcnow)

class RouteStop(SQLModel, table=True):
    id: int | None = Field(default= None, primary_key= True)
    city: str
    route_id: int = Field(foreign_key="route.id")

class RouteItem(SQLModel, table=True):
    id: int | None = Field(default= None, primary_key=True)
    module_qty: int
    module_brand: str
    inverter_qty: int
    inverter_brand: str
    stop_id: int = Field(foreign_key="routestop.id")

class RouteItemCreate(SQLModel):
    module_qty: int
    module_brand: str
    inverter_qty: int
    inverter_brand: str

class RouteStopCreate(SQLModel):
    city: str
    items: list[RouteItemCreate]

class RouteCreate(SQLModel):
    name: str
    stops: list[RouteStopCreate]