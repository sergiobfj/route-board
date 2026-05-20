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

@router.get("/routes")
def list_routes(session: Session = Depends(get_session)):

    routes = session.exec(select(Route)).all()

    result = []

    for route in routes:
        stops = session.exec(select(RouteStop).where(RouteStop.route_id == route.id)).all()

        stops_with_items = []
        for stop in stops:
            items = session.exec(select(RouteItem).where(RouteItem.stop_id == stop.id)).all()
            stops_with_items.append ({
                "city": stop.city,
                "items": items
            })

        result.append({
            "id": route.id,
            "name": route.name,
            "status": route.status,
            "stops": stops_with_items
        })

    return result

@router.patch("/routes/{id}")
def update_route(id: int, status: str, session: Session = Depends(get_session)):

    route = session.get(Route, id)
    route.status = status

    session.add(route)
    session.commit()
    session.refresh(route)
    

    return route



