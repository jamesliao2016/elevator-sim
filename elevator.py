from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Integer, String, Boolean, ForeignKey
from sqlalchemy.orm import relationship, backref
from sqlalchemy.orm import sessionmaker
from queue import Queue
import random
import re

order = Queue()
coordinates = []
stops = []

engine = create_engine('sqlite:///:memory:', echo=False)
Base = declarative_base()

class Floor(Base):
    __tablename__ = 'floor'

    id = Column(Integer, primary_key=True, autoincrement=True)
    probability = Column(Integer)
    density = Column(Integer)

    def __repr__(self):
        return 'Floor: %i' %self.id

class Passenger(Base):
    __tablename__ = 'passenger'

    id = Column(Integer, primary_key=True, autoincrement=True)

    origin_floor_id = Column(Integer, ForeignKey("floor.id"))
    destination_floor_id = Column(Integer, ForeignKey("floor.id"))

    origin_floor = relationship("Floor", foreign_keys=[origin_floor_id])
    destination_floor = relationship("Floor", foreign_keys=[destination_floor_id])
    start = Column(Integer, default=0)
    stop = Column(Integer, default=0)
    waiting_time = Column(Integer, default=0)
    direction = Column(String)
    in_elevator = Column(Boolean, default=False)
    finished = Column(Boolean, default=False)

    def __repr__(self):
        return 'Passenger: %s' %self.direction


class Elevator(Base):
    __tablename__ = 'elevator'

    id = Column(Integer, primary_key=True, autoincrement=True)
    direction = Column(String, default='UP')

    floor = Column(Integer, default=1)
    clock = Column(Integer, default=0)
    max_passengers = Column(Integer)
    speed = Column(Integer, default=3)
    stopped = Column(Boolean, default=True)
    status = Column(Integer, default=0)

    def move(self):
        self.clock += 1
        print '%6i       %7s        %8i    %8s    ' %(self.clock, 'M', self.floor, self.direction) , stops_to_string(stops) , '    ' , order.all()

        self.clock += 1
        print '%6i       %7s        %8i    %8s    ' %(self.clock, 'M', self.floor, self.direction) , stops_to_string(stops) , '    ' , order.all()

        self.clock += 1
        print '%6i       %7s        %8i    %8s    ' %(self.clock, 'M', self.floor, self.direction) , stops_to_string(stops) , '    ' , order.all()
        for passenger in session.query(Passenger).filter(Passenger.finished==False and Passenger.in_elevator==False):
            passenger.waiting_time += 3
        if elevator.direction == 'UP':
            self.floor += 1
        elif elevator.direction == 'DOWN':
            self.floor -= 1


    def move_to(self, floor):
        time = 0
        if self.floor < floor:
            while self.floor != floor:
                self.floor += 1
                time += self.speed
                for i in range(0, self.speed):
                    self.clock += 1
                    print '%6i       %7s        %8i    %8s    ' %(self.clock, 'MT', self.floor, self.direction) , stops_to_string(stops) , '    ' , order.all()
        elif self.floor > floor:
            while self.floor != floor:
                self.floor -= 1
                time += self.speed
                for i in range(0, self.speed):
                    self.clock += 1
                    print '%6i       %7s        %8i    %8s    ' %(self.clock, 'MT', self.floor, self.direction) , stops_to_string(stops) , '    ' , order.all()
        for passenger in session.query(Passenger).filter(Passenger.finished==False and Passenger.in_elevator==False):
            passenger.waiting_time += 3
        return self.floor, time

    def change_direction(self):
        if elevator.direction == 'UP':
            elevator.direction = 'DOWN'
        elif elevator.direction == 'DOWN':
            elevator.direction = 'UP'

    def tick(self):
        elevator.clock += 1
        print '%6i       %7s        %8i    %8s    ' %(self.clock, 'N', self.floor, self.direction) , stops_to_string(stops) , '    ' , order.all()



Session = sessionmaker(bind=engine)
Base.metadata.create_all(engine)
session = Session()
a = Floor(id=1, probability=10, density = 6)
b = Floor(id=2, probability=3, density = 2)
c = Floor(id=3, probability=3, density = 2)
d = Floor(id=4, probability=3, density = 2)
e = Floor(id=5, probability=3, density = 2)
f = Floor(id=6, probability=3, density = 2)
elevator_object = Elevator()
session.add_all([a,b,c,d,e,f])
session.add(elevator_object)
# psg = Passenger(current_floor_id=1, destination_floor_id=1, waiting_time=0, direction='UP', waiting=True)
# session.add(psg)
session.commit()
session.flush()



def load_unload_passengers(floor):
    if floor in stops:
        if session.query(Passenger).filter(Passenger.origin_floor_id):
            pass
def generate_passengers(sec):
    p = []
    count = 0
    tmp_list = []
    for t in range(0, sec):
        for passenger in session.query(Passenger).filter(Passenger.finished==False and Passenger.in_elevator==False):
            passenger.waiting_time += 1
        f_l = (session.query(Floor).all())
        for floor in sorted(f_l, key=lambda *args: random.random()) :
            z = 0
            for x in range(0,floor.density - 1):
                y = random.randint(0,99)
                if y <= floor.probability:
                    c_f = floor.id
                    d_f = 0
                    while d_f == 0:
                        tmp = random.randint(1,6)
                        if tmp != c_f:
                            d_f = tmp
                    if c_f < d_f:
                        direction = 'UP'
                    elif c_f > d_f:
                        direction = 'DOWN'
                    tmp = Passenger(origin_floor_id = c_f, destination_floor_id=d_f, direction=direction, waiting_time=0, start=elevator.clock, in_elevator=False)
                    session.add(tmp)
                    session.commit()
                    d = 'D' if direction == 'DOWN' else 'U'
                    if not order.has('%i%s' %(c_f,d)):
                        order.enqueue('%i%s' %(c_f,d))
                    # stops.append(d_f)
                    order.coordinate(c_f, d_f)
                    z = z + 1
                    count = count + 1
            p.append(z)
    return p, count

elevator = session.query(Elevator).all()[0]

def get_stops(stops=[]):
    for passenger in session.query(Passenger).filter_by(in_elevator=True, finished=False):
        if passenger.destination_floor_id not in stops:
            stops.append(passenger.destination_floor_id)
    if elevator.direction == 'DOWN':
        rev = True
    else:
        rev = False
    stops.sort(reverse=rev)
    return stops

def stops_to_string(stops):
    string = '|'
    for i in range(0,6):
        try:
            s = stops[i]
            string += ' %i |' %s
        except:
            string += ' - |'
    return string

def clean_coordinates():
    for passenger in session.query(Passenger).filter_by(finished=True):
        order.rem_coordinate(passenger.origin_floor_id, passenger.destination_floor_id)

elevator.clock = 0
while elevator.clock <= 120:
    stops = []
    elevator.tick()
    b, count = generate_passengers(1)
    if order.size() > 0:
        n_r = order.get_next()
        r_f = int(n_r[0])
        print '-------------------------------------------------------------------------------------------'
        print order.all()
        print 'Next request : %s --> From Floor %i going %s' %(n_r, r_f, 'UP' if n_r[1] == 'U' else 'DOWN')
        clean_coordinates()
        print order.get_coordinates()

        next_request = order.dequeue()
        request_floor = int(next_request[0])
        elevator.direction = 'UP' if next_request[1] == 'U' else 'DOWN'
        print '-------------------------------------------------------------------------------------------'
        print ' Timer        Section        Elevator    Elevator    Next                          Next in '
        print ' (secs)       (A,B,C)         Floor       Going      Stops                          Queue  '
        print ' ------       -------        --------    --------    --------------------------   ---------'
        current, time = elevator.move_to(request_floor)
        clean_coordinates()
        for passenger in session.query(Passenger).filter_by(origin_floor_id = request_floor,direction = elevator.direction):
            passenger.in_elevator = True
        b, c = generate_passengers(time)
        stops = get_stops()
        # print '%6i       %7s        %8i    %8s    ' %(elevator.clock, 'A', elevator.floor, elevator.direction) , stops_to_string(stops) , '    ' , order.all()
        while len(stops) != 0:
            elevator.move()
            clean_coordinates()
            if elevator.floor in stops:
                clean_coordinates()
                stops.remove(elevator.floor)
                # print 'B', stops, elevator.direction, elevator.floor, order.all()
                # print '%6i       %7s        %8i    %8s    ' %(elevator.clock, 'B', elevator.floor, elevator.direction) , stops_to_string(stops) , '    ' , order.all()
                for passenger in session.query(Passenger).filter_by(destination_floor_id = elevator.floor):
                    passenger.finished = True
                    passenger.stop = passenger.start + passenger.waiting_time - 2
                for passenger in session.query(Passenger).filter_by(origin_floor_id = elevator.floor, direction = elevator.direction):
                    passenger.in_elevator = True
                    if order.has('%i%s' %(passenger.origin_floor_id,passenger.direction[0])):
                        order.remove('%i%s' %(passenger.origin_floor_id,passenger.direction[0]))
                stops = get_stops(stops)
                # print 'C', stops, elevator.direction, elevator.floor, order.all()
                # print '%6i       %7s        %8i    %8s    ' %(elevator.clock, 'C', elevator.floor, elevator.direction) , stops_to_string(stops) , '    ' , order.all()





for passenger in session.query(Passenger).filter_by(finished=True):
    print passenger.origin_floor, passenger.destination_floor, passenger.waiting_time, (passenger.start, passenger.stop)




