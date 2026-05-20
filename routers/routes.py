from fastapi import APIRouter, Depends, File, UploadFile
from sqlmodel import Session, select
from models import Route, RouteStop, RouteItem, RouteCreate
from database import get_session

router = APIRouter()

@router.post("/routes")
def route_create(route: RouteCreate, session: Session = Depends(get_session)):

    db_route = Route(name=route.name)
    session.add(db_route)
    session.commit()
    session.refresh(db_route)

    for stop in route.stops:
        db_stop = RouteStop(city=stop.city, route_id=db_route.id)
        session.add(db_stop)
        session.commit()
        session.refresh(db_stop)

        for item in stop.items:
            db_item = RouteItem(
                module_qty=item.module_qty,
                module_brand=item.module_brand,
                inverter_qty=item.inverter_qty,
                inverter_brand=item.inverter_brand,
                stop_id=db_stop.id
            )
            session.add(db_item)

    session.commit()
    return db_route
