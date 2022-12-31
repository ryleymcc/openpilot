import copy

from selfdrive.car.mazda.values import GEN1, Buttons


def create_steering_control(packer, car_fingerprint, frame, apply_steer, lkas):

  tmp = apply_steer + 2048

  lo = tmp & 0xFF
  hi = tmp >> 8

  # copy values from camera
  b1 = int(lkas["BIT_1"])
  er1 = int(lkas["ERR_BIT_1"])
  lnv = 0
  ldw = 0
  er2 = int(lkas["ERR_BIT_2"])

  steering_angle = 0
  b2 = 0

  tmp = steering_angle + 2048
  ahi = tmp >> 10
  amd = (tmp & 0x3FF) >> 2
  amd = (amd >> 4) | (( amd & 0xF) << 4)
  alo = (tmp & 0x3) << 2

  ctr = frame % 16
  # bytes:     [    1  ] [ 2 ] [             3               ]  [           4         ]
  csum = 249 - ctr - hi - lo - (lnv << 3) - er1 - (ldw << 7) - ( er2 << 4) - (b1 << 5)

  # bytes      [ 5 ] [ 6 ] [    7   ]
  csum = csum - ahi - amd - alo - b2

  if ahi == 1:
    csum = csum + 15

  if csum < 0:
    if csum < -256:
      csum = csum + 512
    else:
      csum = csum + 256

  csum = csum % 256

  if car_fingerprint in GEN1:
    values = {
      "LKAS_REQUEST": apply_steer,
      "CTR": ctr,
      "ERR_BIT_1": er1,
      "LINE_NOT_VISIBLE" : lnv,
      "LDW": ldw,
      "BIT_1": b1,
      "ERR_BIT_2": er2,
      "STEERING_ANGLE": steering_angle,
      "ANGLE_ENABLED": b2,
      "CHKSUM": csum
    }

  return packer.make_can_msg("CAM_LKAS", 0, values)

def create_ti_steering_control(packer, car_fingerprint, frame, apply_steer):

  key = 3294744160
  chksum = apply_steer

  if car_fingerprint in GEN1:
    values = {
        "LKAS_REQUEST"     : apply_steer,
        "CHKSUM"           : chksum,
        "KEY"              : key
     }
  # TODO
  # 1. Add new CAR values for MDARS Mazdas so that we can change the rate of the message. This will take some work.
  # 2. Listen for reply's on both CAN buses if not MDARS version of
  # Mazda (2021+ or m3 2019+) and warn the user if there is a bad connection
  # but do not cause disengagment

  # Write to both busses for *future* redundancy, but we only check bus 1 for a response in carstate and safey_mazda.h for now.
  # if (frame % 2 == 0):
  #  commands.append(packer.make_can_msg("CAM_LKAS2", 0, values))

  return packer.make_can_msg("CAM_LKAS2", 1, values)



def create_alert_command(packer, cam_msg: dict, ldw: bool, steer_required: bool):
  values = copy.copy(cam_msg)
  values.update({
    # TODO: what's the difference between all these? do we need to send all?
    "HANDS_WARN_3_BITS": 0b111 if steer_required else 0,
    "HANDS_ON_STEER_WARN": steer_required,
    "HANDS_ON_STEER_WARN_2": steer_required,

    # TODO: right lane works, left doesn't
    # TODO: need to do something about L/R
    "LDW_WARN_LL": 0,
    "LDW_WARN_RL": 0,
  })
  return packer.make_can_msg("CAM_LANEINFO", 0, values)


def create_button_cmd(packer, car_fingerprint, counter, button):

  can = int(button == Buttons.CANCEL)
  res = int(button == Buttons.RESUME)

  if car_fingerprint in GEN1:
    values = {
      "CAN_OFF": can,
      "CAN_OFF_INV": (can + 1) % 2,

      "SET_P": 0,
      "SET_P_INV": 1,

      "RES": res,
      "RES_INV": (res + 1) % 2,

      "SET_M": 0,
      "SET_M_INV": 1,

      "DISTANCE_LESS": 0,
      "DISTANCE_LESS_INV": 1,

      "DISTANCE_MORE": 0,
      "DISTANCE_MORE_INV": 1,

      "MODE_X": 0,
      "MODE_X_INV": 1,

      "MODE_Y": 0,
      "MODE_Y_INV": 1,

      "BIT1": 1,
      "BIT2": 1,
      "BIT3": 1,
      "CTR": (counter + 1) % 16,
    }

    return packer.make_can_msg("CRZ_BTNS", 0, values)
  
def create_radar_command(packer, car_fingerprint, frame, CC, CS):
  accel = 0
  ret = []
  
  if CC.longActive: # this is set true in longcontrol.py
    accel = CC.actuators.accel * 1170
    accel = accel if accel < 1000 else 1000
  else:
    accel = int(CS.cp_cam.vl["CRZ_INFO"]["ACCEL_CMD"])

  if car_fingerprint in GEN1:
    values_21B = {
        "ACC_ACTIVE"        : int(CC.longActive),
        "ACC_SET_ALLOWED"   : int(bool(int(CS.cp.vl["GEAR"]["GEAR"]) & 4)), # we can set ACC_SET_ALLOWED bit when in drive. Allows crz to be set from 1kmh.
        "CRZ_ENDED"         : 0, # this should keep acc on down to 5km/h on my 2018 M3
        "ACCEL_CMD"         : accel,
        "STATIC_1"          : int(CS.cp_cam.vl["CRZ_INFO"]["STATIC_1"]), #0x7FF,
        "STATUS"            : int(CS.cp_cam.vl["CRZ_INFO"]["STATUS"]),    #1
        "MYSTERY_BIT"       : int(CS.cp_cam.vl["CRZ_INFO"]["MYSTERY_BIT"]),
        "CTR1"              : int(CS.cp_cam.vl["CRZ_INFO"]["CTR1"])
    }

    values_21C = {
        "CRZ_ACTIVE"       : int(CC.longActive),
        "CRZ_AVAILABLE"    : int(CS.cp_cam.vl["CRZ_CTRL"]["CRZ_AVAILABLE"]),
        "DISTANCE_SETTING" : int(CS.cp_cam.vl["CRZ_CTRL"]["DISTANCE_SETTING"]),
        "ACC_ACTIVE_2"     : int(CC.longActive),
        "DISABLE_TIMER_1"  : 0,
        "DISABLE_TIMER_2"  : 0,
        "NEW_SIGNAL_1"     : int(CS.cp_cam.vl["CRZ_CTRL"]["NEW_SIGNAL_1"]),
        "NEW_SIGNAL_2"     : int(CS.cp_cam.vl["CRZ_CTRL"]["NEW_SIGNAL_2"]),
        "NEW_SIGNAL_3"     : int(CS.cp_cam.vl["CRZ_CTRL"]["NEW_SIGNAL_3"]),
        "NEW_SIGNAL_4"     : int(CS.cp_cam.vl["CRZ_CTRL"]["NEW_SIGNAL_4"]),
        "NEW_SIGNAL_5"     : int(CS.cp_cam.vl["CRZ_CTRL"]["NEW_SIGNAL_5"]),
        "NEW_SIGNAL_6"     : int(CS.cp_cam.vl["CRZ_CTRL"]["NEW_SIGNAL_6"]),
    }

    ret.append(packer.make_can_msg("CRZ_INFO", 0, values_21B))
    ret.append(packer.make_can_msg("CRZ_CTRL", 0, values_21C))
 
    if (frame % 10 == 0):
      for addr in range(361,367):
        addr_name = f"RADAR_{addr}"
        msg = CS.cp_cam.vl[addr_name]
        values = {
          "MSGS_1" : int(msg["MSGS_1"]),
          "MSGS_2" : int(msg["MSGS_2"]),
          "CTR"    : int(msg["CTR"])
        } 
        ret.append(packer.make_can_msg(addr_name, 0, values))
    
  return ret
