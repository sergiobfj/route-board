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

@router.get("/display")
def get_display(session: Session = Depends(get_session)):

    statement = select(Route).where(Route.status == "in_progress").order_by(Route.created_at)
    in_progress = session.exec(statement).first()

    if in_progress:
        stops = session.exec(select(RouteStop).where(RouteStop.route_id == in_progress.id)).all()
        
        stops_with_items = []
        for stop in stops:
            items = session.exec(select(RouteItem).where(RouteItem.stop_id == stop.id)).all()
            stops_with_items.append({
                "city": stop.city,
                "items": items
            })
        
        in_progress_data = {
            "id": in_progress.id,
            "name": in_progress.name,
            "stops": stops_with_items
        }
    else:
        in_progress_data = None


    statement = select(Route).where(Route.status == "waiting").order_by(Route.created_at)
    waiting = session.exec(statement).first()

    if waiting:
        stops = session.exec(select(RouteStop).where(RouteStop.route_id == waiting.id)).all()

        stops_with_items = []
        for stop in stops:
            items = session.exec(select(RouteItem).where(RouteItem.stop_id == stop.id)).all()
            stops_with_items.append ({
                "city": stop.city,
                "items": items
            })
            
        waiting_data = {
            "id": waiting.id,
            "name": waiting.name,
            "driver_name": waiting.driver_name,
            "truck_plate": waiting.truck_plate,
            "stops": stops_with_items
        }

    else:
        waiting_data = None

    
    return {
        "in_progress": in_progress_data,
        "next": waiting_data
    }

            