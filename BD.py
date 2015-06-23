from sqlalchemy import create_engine, ForeignKey
from sqlalchemy import Column, Date, Integer, String
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship, backref

import socket
import json
import psutil
import jsonpickle
import socket
import time

class Monitor:
    CPU_Percente=0
    Memory_used=0
    Memory_free=0
    NetUse_Bytes_send=0
    NetUse_Bytes_recv=0
    Disk_used=0
    Disk_free=0
    Disk_Bytes_read=0
    Disk_Bytes_write=0
    INTERNET_IP=0

    INTERNET_IP = socket.gethostbyname(socket.gethostname())
    Memory_values=psutil.virtual_memory()
    NetUse_Bytes_values=psutil.net_io_counters(pernic=False)
    Disk_values=psutil.disk_usage('/')
    DiskBytes_values=psutil.disk_io_counters(perdisk=False)

    def update(self):
        #percent usage cpu for last 1 second mean
        CPU=0
        for i in range(1,10):
            CPU+=psutil.cpu_percent(interval=0.1, percpu=False)
        self.CPU_Percente=CPU/10

        #percent usage memory
        self.Memory_used=self.Memory_values.used
        self.Memory_free=self.Memory_values.used

        #NetUse_Bytes
        self.NetUse_Bytes_send=self.NetUse_Bytes_values.bytes_sent
        self.NetUse_Bytes_recv=self.NetUse_Bytes_values.bytes_recv

        #DiskInfo
        self.Disk_used=self.Disk_values.used
        self.Disk_free=self.Disk_values.free

        self.Disk_Bytes_read=self.DiskBytes_values.read_bytes
        self.Disk_Bytes_write=self.DiskBytes_values.write_bytes

engine = create_engine('sqlite:///BD_Info_IPs.db', echo=True)
Base = declarative_base()

class Client(Base):
    __tablename__ = "IP"
    id = Column(Integer, primary_key=True)
    name=Column(String)
    def __init__(self, name):
        self.name = name

class InfoIPs(Base):
    __tablename__ = "infoip"
 
    id = Column(Integer, primary_key=True)
    IP_id = Column(String, ForeignKey("IP.name"))
    CPU_Percente=Column(String)
    Memory_used=Column(String)
    Memory_free=Column(String)
    NetUse_Bytes_send=Column(String)
    NetUse_Bytes_recv=Column(String)
    Disk_used=Column(String)
    Disk_free=Column(String)
    Disk_Bytes_read=Column(String)
    Disk_Bytes_write=Column(String)



    infor = relationship("Client", backref=backref("infoip", order_by=id))
 
    #----------------------------------------------------------------------
    def __init__(self, m):
         self.CPU_Percente=m.CPU_Percente
         self.Memory_used=m.Memory_used
         self.Memory_free=m.Memory_free
         self.NetUse_Bytes_send=m.NetUse_Bytes_send
         self.NetUse_Bytes_recv=m.NetUse_Bytes_recv
         self.Disk_used=m.Disk_used
         self.Disk_free=m.Disk_free
         self.Disk_Bytes_read=m.Disk_Bytes_read
         self.Disk_Bytes_write=m.Disk_Bytes_write
 
# create tables
Base.metadata.create_all(engine)
