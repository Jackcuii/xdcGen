    def __init__(self, args):
        self.args = args
    def getStr(self, port):
        print("Poorly implemented pin class")
        assert(0)

class FPGAdevice:
    name = None
    switches = None
    leds = None
    rgbs = None
    seg7 = None
    seg7en = None
    reset = None
    buttons = None
    clock = None
    allpins = None

    def __str__(self):
        return f"{self.name} FPGA device: \n with {len(self.switches)} switches, {len(self.leds)} LEDs, {len(self.rgbs)} RGB LEDs, {len(self.seg7)} 7-segment displays, {len(self.seg7en)} 7-segment display enable pins, {len(self.reset)} reset pins, and {len(self.buttons)} buttons."
    
    @classmethod
    def lookup(cls, name):
        if name in cls.allpins:
            return cls.allpins[name]
        else:
            print(f"Pin {name} not found in {cls.name}")
            assert(0)

    # To enable the syntax sugar, you need to implement the following functions
    @classmethod
    def ClockMap(cls):
        print("Poorly implemented clock map")
        assert(0)

    @classmethod
    def Seg7Map(cls):
        print("Poorly implemented 7-segment map")
        assert(0)
    
    @classmethod
    def Seg7EnMap(cls):
        print("Poorly implemented 7-segment enable map")
        assert(0)

# Add new supports here
class A7_100T_Pin(Pin):
    def getStr(self, port):
        return f"set_property -dict {{ PACKAGE_PIN {self.args}   IOSTANDARD LVCMOS33 }} [get_ports {{ {port} }}];"

package_pins1 = ["J15", "L16", "M13", "R15", "R17", "T18", "U18", "R13", "T8", "U8", "R16", "T13", "H6", "U12", "U11", "V10"]
package_pins2 = ["H17", "K15", "J13", "N14", "R18", "V17", "U17", "U16", "V16", "T15", "U14", "T16", "V15", "V14", "V12", "V11"]
package_pins3 = ["N15", "M16", "R12", "N16", "R11", "G14"]
rgb = ["LED16R", "LED16G", "LED16B", "LED17R", "LED17G", "LED17B"]
package_pins4 = ["T10", "R10", "K16", "K13", "P15", "T11", "L18", "H15"]
seg = ["CA", "CB", "CC", "CD", "CE", "CF", "CG", "DP"]
package_pins5 = ["J17", "J18", "T9", "J14", "P14", "T14", "K2", "U13"]
package_pins6 = ["N17", "M18", "P17", "M17", "P18"]
button = ["BC", "BU", "BL", "BR", "BD"]
switches = {f"SW{i}" : A7_100T_Pin(f"{package_pins1[i]}") for i in range(16)}
leds = {f"LED{i}" : A7_100T_Pin(f"{package_pins2[i]}") for i in range(16)}
rgbs = {f"{rgb[i]}" : A7_100T_Pin(f"{package_pins3[i]}") for i in range(6)}
seg7 = {f"{seg[i]}" : A7_100T_Pin(f"{package_pins4[i]}") for i in range(8)}
seg7en = {f"AN{i}" : A7_100T_Pin(f"{package_pins5[i]}") for i in range(8)}
reset = {"RST" : A7_100T_Pin("C12")}
buttons = {f"{button[i]}" : A7_100T_Pin(f"{package_pins6[i]}") for i in range(5)}
clock = {"CLK100" : A7_100T_Pin("E3")}
usb = {"PS2CLK" : A7_100T_Pin("F4"), "PS2DATA" : A7_100T_Pin("B2")

class A7_100T(FPGAdevice):
    name = "Artix-7 100T"
    # actually, you do not need to add pin infos seperately, here is to clearly show it
    allpins = {**switches, **leds, **rgbs, **seg7, **seg7en, **reset, **buttons, **clock, **usb}

    @classmethod
    def ClockMap(cls):
        return ["CLK100"]
    
    @classmethod
    def Seg7Map(cls):
        return ["CA", "CB", "CC", "CD", "CE", "CF", "CG"]

    @classmethod
    def Seg7EnMap(cls):
        return ["AN0", "AN1", "AN2", "AN3", "AN4", "AN5", "AN6", "AN7"]

# Register new devices here
SupportedDevices = [A7_100T]
    
