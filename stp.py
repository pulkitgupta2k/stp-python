import heapq

class Topology:
    def __init__(self):
        self.root_bridge = None
        self.routers = set()

    def add_router(self, router):
        self.routers.add(router)

    def remove_router(self, router):
        self.routers.remove(router)

    def calculate_root(self):
        for router in self.routers:
            if self.root_bridge == None:
                self.root_bridge = router
                continue

            if (router.priority < self.root_bridge.priority) or \
                    (router.priority == self.root_bridge.priority and router.mac_addr > self.root_bridge.mac_addr):
                self.root_bridge = router

    def run_stp(self):
        self.calculate_root()
        rem_bridges = self.routers
        rem_bridges.remove(self.root_bridge)

        # priority_q = []
        # heappush(priority_q, (f"{self.root_bridge.}"))

class Router:
    def __init__(self, interfaces={}, mac_addr="00.00.00.00.00.00", priority=32768):
        self._id = id(self)
        self.interfaces = {}
        for interface in interfaces:
            self.add_interface(interface)
        self.mac_addr = mac_addr
        self.priority = priority

    class Interface:
        def __init__(self, router):
            self._id = id(self)
            self.wire = None
            self.status = 0
            self.router = router

        def connect(self, wire):
            self.wire = wire

        def neighbour(self):
            if not self.wire or not self.wire.int_1 or not self.wire.int_2:
                print("No wire connected.")
                return

            if self.wire.int_1 == self:
                return self.wire.int_2

            if self.wire.int_2 == self:
                return self.wire.int_1

    def add_interface(self, int_no):
        if int_no in self.interfaces:
            print(f"{int_no} is already an interface")
            return
        self.interfaces[int_no] = self.Interface(self)

    def display(self):
        print(self._id)
        # for key, value in self.interfaces.items():
        #     print(key, value.wire)

class Wire:
    def __init__(self, cost=19, int_1=None, int_2=None):
        self._id = id(self)
        self.cost = cost
        self.int_1 = int_1
        self.int_2 = int_2

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
        print(self.int_1.router._id)
        print(self.int_2.router._id)

if __name__ == "__main__":
    topology = Topology()
    R1 = Router(interfaces={1, 2, 3}, mac_addr="00.00.00.00.00.01", priority=4096)
    R2 = Router(interfaces={1, 2, 3}, mac_addr="00.00.00.00.00.02", priority=8192)

    R1.display()
    R2.display()

    topology.add_router(R1)
    topology.add_router(R2)

    w1 = Wire()
    w2 = Wire()

    w1.connect_to_int(R1.interfaces[1])
    w1.connect_to_int(R2.interfaces[1])

    w1.display()    
