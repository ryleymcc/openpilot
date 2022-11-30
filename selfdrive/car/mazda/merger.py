from dataclasses import dataclass
from enum import Enum
from typing import Dict, List, Union

from selfdrive.car import dbc_dict
from selfdrive.car.docs_definitions import CarInfo, Harness
from cereal import car
Ecu = car.CarParams.Ecu

class CAR:
  CX3 = "MAZDA CX-3"
  CX5 = "MAZDA CX-5"
  CX9 = "MAZDA CX-9"
  MAZDA3 = "MAZDA 3"
  MAZDA6 = "MAZDA 6"
  CX9_2021 = "MAZDA CX-9 2021"
  CX5_2022 = "MAZDA CX-5 2022"
  CX3 = "MAZDA CX-3"
  CX5 = "MAZDA CX-5"
  CX9 = "MAZDA CX-9"
  MAZDA3 = "MAZDA 3"
  MAZDA6 = "MAZDA 6"
  CX9_2021 = "MAZDA CX-9 2021"
  CX5_2022 = "MAZDA CX-5 2022"
  MAZDA3_2019 = "MAZDA 3 2019"


FW_VERSIONS_old = {
  CAR.CX5_2022 : {
    (Ecu.eps, 0x730, None): [
      b'KSD5-3210X-C-00\x00\x00\x00\x00\x00\x00\x00\x00\x00',
    ],
    (Ecu.engine, 0x7e0, None): [
      b'PX2G-188K2-H\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00',
      b'PX2H-188K2-H\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00',
      b'SH54-188K2-D\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00',
      b'PXFG-188K2-C\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00',
    ],
    (Ecu.fwdRadar, 0x764, None): [
      b'K131-67XK2-F\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00',
    ],
    (Ecu.esp, 0x760, None): [
      b'KSD5-437K2-A\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00',
    ],
    (Ecu.fwdCamera, 0x706, None): [
      b'GSH7-67XK2-S\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00',
    ],
    (Ecu.transmission, 0x7e1, None): [
      b'PYB2-21PS1-H\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00',
      b'SH51-21PS1-C\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00',
      b'PXFG-21PS1-A\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00',
    ],
  },
}

FW_VERSIONS_old = {
    CAR.CX5_2022 : {
        (Ecu.eps, 0x730, None): [
        b'KSD5-3210X-C-00\x00\x00\x00\x00\x00\x00\x00\x00\x00',
        ],
        (Ecu.engine, 0x7e0, None): [
        b'PX2G-188K2-H\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00',
        ],
        (Ecu.fwdRadar, 0x764, None): [
        b'K131-67XK2-F\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00',
        ],
        (Ecu.esp, 0x760, None): [
        b'KSD5-437K2-A\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00',
        ],
        (Ecu.fwdCamera, 0x706, None): [
        b'GSH7-67XK2-S\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00',
        ],
        (Ecu.transmission, 0x7e1, None): [
        b'PYB2-21PS1-H\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00',
        ],
  },
}

def main():
    #print the FW_VERSIONS_old values
    print(FW_VERSIONS_old)