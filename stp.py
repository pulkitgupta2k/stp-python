class router:
    def __init__(self):
        self._id = id(self)
        self.interfaces = {}
        self.mac_addr = "00:00:00:00:00:00"
        self.priority = 32768

    class interface:
        def __init__(self):
            self._id = id(self)
            self.wire = wire()
            self.status = 0

        def connect(self, wire):
            self.wire = wire

    def add_interface(self, int_name):
        if int_name in self.interfaces:
            print(f"{int_name} is already an interface")
            return
        self.interfaces[int_name] = self.interface()
    
    # def connect_int_to_wire(self, int_name, wire):
    #     if int_name not in self.interfaces:
    #         print(f"{int_name} is not an interface")
    #         return
    #     self.interfaces[int_name].connect(wire)


    def display(self):
        for key, value in self.interfaces.items():
            print(key, value.wire)

class wire:
    def __init__(self):
        self._id = id(self)
        self.cost = 19
        self.int_1 = None
        self.int_2 = None

    def connect_to_int(self, interface):
        if not self.int_1:
            interface.connect(self)
            self.int_1 = interface

        elif not self.int_2:
            interface.connect(self)
            self.int_2 = interface
        
        else:
            print("No free end in the wire")
            return

    def display(self):
        pass


if __name__ == "__main__":
    r1 = router()
    r2 = router()
    w1 = wire()
    r1.add_interface("Eth1")
    r2.add_interface("Eth1")

    w1.connect_to_int(r1.interfaces["Eth1"])
    w1.connect_to_int(r2.interfaces["Eth1"])

    r1.display()
    r2.display()
