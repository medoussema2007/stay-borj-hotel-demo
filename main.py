from datetime import date, datetime, timedelta
from typing import Optional
from fastapi import FastAPI, Depends, HTTPException
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse, StreamingResponse
from pydantic import BaseModel, Field
from sqlalchemy import create_engine, String, Integer, Float, Date, DateTime, ForeignKey, select, or_, func
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, Session, sessionmaker, relationship
import csv, io

engine=create_engine('sqlite:///./borjstay.db',connect_args={'check_same_thread':False})
SessionLocal=sessionmaker(bind=engine,autoflush=False,autocommit=False)
class Base(DeclarativeBase): pass

class Guest(Base):
    __tablename__='guests'; id:Mapped[int]=mapped_column(primary_key=True)
    full_name:Mapped[str]=mapped_column(String(120),index=True); phone:Mapped[str]=mapped_column(String(30)); email:Mapped[Optional[str]]=mapped_column(String(120),nullable=True)
    nationality:Mapped[Optional[str]]=mapped_column(String(60),nullable=True); document_id:Mapped[Optional[str]]=mapped_column(String(50),nullable=True); notes:Mapped[Optional[str]]=mapped_column(String(500),nullable=True)
    created_at:Mapped[datetime]=mapped_column(DateTime,default=datetime.utcnow)
class Room(Base):
    __tablename__='rooms'; id:Mapped[int]=mapped_column(primary_key=True); number:Mapped[str]=mapped_column(String(10),unique=True,index=True)
    room_type:Mapped[str]=mapped_column(String(30)); capacity:Mapped[int]=mapped_column(Integer,default=2); price:Mapped[float]=mapped_column(Float); status:Mapped[str]=mapped_column(String(20),default='Available'); floor:Mapped[int]=mapped_column(Integer,default=1)
class Reservation(Base):
    __tablename__='reservations'; id:Mapped[int]=mapped_column(primary_key=True); guest_id:Mapped[int]=mapped_column(ForeignKey('guests.id')); room_id:Mapped[int]=mapped_column(ForeignKey('rooms.id'))
    check_in:Mapped[date]=mapped_column(Date); check_out:Mapped[date]=mapped_column(Date); adults:Mapped[int]=mapped_column(Integer,default=1); status:Mapped[str]=mapped_column(String(20),default='Reserved')
    total:Mapped[float]=mapped_column(Float,default=0); paid:Mapped[float]=mapped_column(Float,default=0); source:Mapped[str]=mapped_column(String(30),default='Direct'); created_at:Mapped[datetime]=mapped_column(DateTime,default=datetime.utcnow)
    guest:Mapped[Guest]=relationship(); room:Mapped[Room]=relationship()
class Activity(Base):
    __tablename__='activities'; id:Mapped[int]=mapped_column(primary_key=True); action:Mapped[str]=mapped_column(String(160)); detail:Mapped[str]=mapped_column(String(240)); created_at:Mapped[datetime]=mapped_column(DateTime,default=datetime.utcnow)

class GuestIn(BaseModel):
    full_name:str=Field(min_length=2,max_length=120); phone:str=Field(min_length=5,max_length=30); email:Optional[str]=None; nationality:Optional[str]=None; document_id:Optional[str]=None; notes:Optional[str]=None
class RoomIn(BaseModel):
    number:str=Field(min_length=1,max_length=10); room_type:str; capacity:int=Field(ge=1,le=10); price:float=Field(gt=0); status:str='Available'; floor:int=Field(ge=0,le=50)
class ReservationIn(BaseModel):
    guest_id:int; room_id:int; check_in:date; check_out:date; adults:int=Field(ge=1,le=10); status:str='Reserved'; paid:float=Field(ge=0,default=0); source:str='Direct'

app=FastAPI(title='BorjStay Hotel Operations',version='2.0.0')
def db_session():
    db=SessionLocal()
    try: yield db
    finally: db.close()
def log(db,action,detail): db.add(Activity(action=action,detail=detail))
def reservation_dict(r):
    return {'id':r.id,'guest_id':r.guest_id,'guest_name':r.guest.full_name,'room_id':r.room_id,'room_number':r.room.number,'check_in':r.check_in,'check_out':r.check_out,'nights':(r.check_out-r.check_in).days,'adults':r.adults,'status':r.status,'total':r.total,'paid':r.paid,'balance':max(r.total-r.paid,0),'source':r.source,'created_at':r.created_at}

def room_conflict(db,room_id,start,end,exclude=None):
    stmt=select(Reservation).where(Reservation.room_id==room_id,Reservation.status.in_(['Reserved','Checked in']),Reservation.check_in<end,Reservation.check_out>start)
    if exclude: stmt=stmt.where(Reservation.id!=exclude)
    return db.scalar(stmt)

@app.on_event('startup')
def startup():
    Base.metadata.create_all(engine)
    with SessionLocal() as db:
        if not db.scalar(select(func.count(Room.id))):
            db.add_all([Room(number='101',room_type='Single',capacity=1,price=110,floor=1),Room(number='102',room_type='Double',capacity=2,price=165,floor=1),Room(number='201',room_type='Suite',capacity=3,price=260,floor=2),Room(number='202',room_type='Double',capacity=2,price=175,floor=2,status='Maintenance')]); db.flush()
            g1=Guest(full_name='Amine Ben Salem',phone='+216 20 000 001',email='amine.demo@example.com',nationality='Tunisian'); g2=Guest(full_name='Sophie Martin',phone='+33 6 00 00 00 02',email='sophie.demo@example.com',nationality='French'); db.add_all([g1,g2]); db.flush()
            today=date.today(); db.add_all([Reservation(guest_id=g1.id,room_id=1,check_in=today,check_out=today+timedelta(days=2),adults=1,status='Checked in',total=220,paid=220),Reservation(guest_id=g2.id,room_id=3,check_in=today+timedelta(days=3),check_out=today+timedelta(days=6),adults=2,status='Reserved',total=780,paid=300,source='Website')]); log(db,'Demo workspace created','Fictional records were added for portfolio presentation.'); db.commit()

@app.get('/api/dashboard')
def dashboard(db:Session=Depends(db_session)):
    today=date.today(); rooms=db.scalar(select(func.count(Room.id))) or 0; available=db.scalar(select(func.count(Room.id)).where(Room.status=='Available')) or 0
    active=db.scalars(select(Reservation).where(Reservation.status.in_(['Reserved','Checked in']))).all(); arrivals=sum(r.check_in==today for r in active); departures=sum(r.check_out==today for r in active)
    occupied=sum(r.status=='Checked in' for r in active); revenue=db.scalar(select(func.sum(Reservation.paid))) or 0; pending=sum(max(r.total-r.paid,0) for r in db.scalars(select(Reservation)).all())
    activities=db.scalars(select(Activity).order_by(Activity.created_at.desc()).limit(6)).all()
    return {'rooms':rooms,'available':available,'occupied':occupied,'occupancy':round(occupied/rooms*100) if rooms else 0,'arrivals':arrivals,'departures':departures,'revenue':revenue,'pending':pending,'activities':[{'action':a.action,'detail':a.detail,'created_at':a.created_at} for a in activities]}

@app.get('/api/guests')
def guests(q:str='',db:Session=Depends(db_session)):
    stmt=select(Guest).order_by(Guest.created_at.desc())
    if q: term=f'%{q}%'; stmt=stmt.where(or_(Guest.full_name.ilike(term),Guest.phone.ilike(term),Guest.email.ilike(term)))
    return db.scalars(stmt).all()
@app.post('/api/guests',status_code=201)
def add_guest(data:GuestIn,db:Session=Depends(db_session)):
    g=Guest(**data.model_dump()); db.add(g); log(db,'Guest added',data.full_name); db.commit(); db.refresh(g); return g
@app.put('/api/guests/{id}')
def edit_guest(id:int,data:GuestIn,db:Session=Depends(db_session)):
    g=db.get(Guest,id)
    if not g: raise HTTPException(404,'Guest not found')
    for k,v in data.model_dump().items(): setattr(g,k,v)
    log(db,'Guest updated',g.full_name); db.commit(); db.refresh(g); return g
@app.delete('/api/guests/{id}',status_code=204)
def delete_guest(id:int,db:Session=Depends(db_session)):
    g=db.get(Guest,id)
    if not g: raise HTTPException(404,'Guest not found')
    if db.scalar(select(Reservation).where(Reservation.guest_id==id)): raise HTTPException(409,'Guest has reservation history and cannot be deleted')
    db.delete(g); db.commit()

@app.get('/api/rooms')
def rooms(db:Session=Depends(db_session)): return db.scalars(select(Room).order_by(Room.number)).all()
@app.post('/api/rooms',status_code=201)
def add_room(data:RoomIn,db:Session=Depends(db_session)):
    if db.scalar(select(Room).where(Room.number==data.number)): raise HTTPException(409,'Room number already exists')
    r=Room(**data.model_dump()); db.add(r); log(db,'Room added',f'Room {r.number}'); db.commit(); db.refresh(r); return r
@app.put('/api/rooms/{id}')
def edit_room(id:int,data:RoomIn,db:Session=Depends(db_session)):
    r=db.get(Room,id)
    if not r: raise HTTPException(404,'Room not found')
    duplicate=db.scalar(select(Room).where(Room.number==data.number,Room.id!=id))
    if duplicate: raise HTTPException(409,'Room number already exists')
    for k,v in data.model_dump().items(): setattr(r,k,v)
    log(db,'Room updated',f'Room {r.number}'); db.commit(); db.refresh(r); return r

@app.get('/api/reservations')
def reservations(status:str='',db:Session=Depends(db_session)):
    stmt=select(Reservation).order_by(Reservation.check_in.desc())
    if status: stmt=stmt.where(Reservation.status==status)
    return [reservation_dict(r) for r in db.scalars(stmt).all()]
@app.post('/api/reservations',status_code=201)
def add_reservation(data:ReservationIn,db:Session=Depends(db_session)):
    if data.check_out<=data.check_in: raise HTTPException(400,'Check-out must be after check-in')
    room=db.get(Room,data.room_id); guest=db.get(Guest,data.guest_id)
    if not room or not guest: raise HTTPException(404,'Guest or room not found')
    if room.status=='Maintenance': raise HTTPException(409,'Room is under maintenance')
    if data.adults>room.capacity: raise HTTPException(400,'Guest count exceeds room capacity')
    if room_conflict(db,data.room_id,data.check_in,data.check_out): raise HTTPException(409,'Room is not available for these dates')
    total=(data.check_out-data.check_in).days*room.price; r=Reservation(**data.model_dump(),total=total); db.add(r); log(db,'Reservation created',f'{guest.full_name} · Room {room.number}'); db.commit(); db.refresh(r); return reservation_dict(r)
@app.put('/api/reservations/{id}/status')
def change_status(id:int,payload:dict,db:Session=Depends(db_session)):
    r=db.get(Reservation,id)
    if not r: raise HTTPException(404,'Reservation not found')
    status=payload.get('status'); allowed=['Reserved','Checked in','Checked out','Cancelled']
    if status not in allowed: raise HTTPException(400,'Invalid status')
    r.status=status; r.room.status='Occupied' if status=='Checked in' else ('Available' if r.room.status!='Maintenance' else r.room.status); log(db,'Reservation status changed',f'Room {r.room.number} · {status}'); db.commit(); return reservation_dict(r)
@app.put('/api/reservations/{id}/payment')
def payment(id:int,payload:dict,db:Session=Depends(db_session)):
    r=db.get(Reservation,id)
    if not r: raise HTTPException(404,'Reservation not found')
    amount=float(payload.get('amount',0))
    if amount<=0 or r.paid+amount>r.total: raise HTTPException(400,'Invalid payment amount')
    r.paid+=amount; log(db,'Payment recorded',f'{amount:.2f} TND · Room {r.room.number}'); db.commit(); return reservation_dict(r)

@app.get('/api/reports')
def reports(db:Session=Depends(db_session)):
    rs=db.scalars(select(Reservation)).all(); total=sum(r.total for r in rs); collected=sum(r.paid for r in rs)
    by_source={}; by_status={}
    for r in rs: by_source[r.source]=by_source.get(r.source,0)+1; by_status[r.status]=by_status.get(r.status,0)+1
    return {'bookings':len(rs),'booked_revenue':total,'collected':collected,'outstanding':total-collected,'by_source':by_source,'by_status':by_status}
@app.get('/api/export/reservations.csv')
def export_csv(db:Session=Depends(db_session)):
    output=io.StringIO(); w=csv.writer(output); w.writerow(['Guest','Room','Check-in','Check-out','Status','Total TND','Paid TND','Source'])
    for r in db.scalars(select(Reservation)).all(): w.writerow([r.guest.full_name,r.room.number,r.check_in,r.check_out,r.status,r.total,r.paid,r.source])
    return StreamingResponse(iter([output.getvalue()]),media_type='text/csv',headers={'Content-Disposition':'attachment; filename=borjstay-reservations.csv'})

app.mount('/static',StaticFiles(directory='static'),name='static')
@app.get('/')
def home(): return FileResponse('static/index.html')
