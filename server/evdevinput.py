keyCodeMap = {
    2: '1',
    3: '2',
    4: '3',
    5: '4',
    6: '5',
    7: '6',
    8: '7',
    9: '8',
    10: '9',
    11: '0',
    12: '-',
    13: '=',
    14: 'BACKSPACE',
    15: '\t',
    16: 'Q',
    17: 'W',
    18: 'E',
    19: 'R',
    20: 'T',
    21: 'Y',
    22: 'U',
    23: 'I',
    24: 'O',
    25: 'P',
    26: '{',
    27: '}',
    28: 'ENTER',
    29: 'LEFTCTRL',
    30: 'A',
    31: 'S',
    32: 'D',
    33: 'F',
    34: 'G',
    35: 'H',
    36: 'J',
    37: 'K',
    38: 'L',
    39: ';',
    40: '\'',
    41: '`',
    42: '',
    43: 'BACKSLASH',
    44: 'Z',
    45: 'X',
    46: 'C',
    47: 'V',
    48: 'B',
    49: 'N',
    50: 'M',
    51: ',',
    52: '.',
    53: '/',
    54: 'RIGHTSHIFT',
    55: 'KPASTERISK',
    56: 'LEFTALT',
    57: ' ',
}

from evdev import *

def getDeviceByName(name):
    devices = map(InputDevice, list_devices())
    for dev in devices:
        if dev.name == name:
            return dev

    return None

dev = getDeviceByName("Mag-Tek USB Swipe Reader")
def getInputLine():
    dev.grab()
    ret = ""
    for event in dev.read_loop():
        if event.type == ecodes.EV_KEY and event.value == 1:
            if event.code == 28:
                dev.ungrab()
                return ret;
            else:
                ret += keyCodeMap[event.code]
    dev.ungrab()
