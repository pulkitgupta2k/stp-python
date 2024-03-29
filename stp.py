from heapq import heappush, heappop

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
                    (router.priority == self.root_bridge.priority and router.mac_addr < self.root_bridge.mac_addr):
                self.root_bridge = router

    def run_stp(self):
        self.calculate_root()
        rem_bridges = self.routers.copy()
        rem_bridges.remove(self.root_bridge)

        priority_q = []
        for int_no, interface in self.root_bridge.interfaces.items():
            if interface.neighbour():
                interface.status = 1 # designated port
                heappush(priority_q, (f"{interface.wire.cost}.{int_no}", interface.neighbour()))

        while rem_bridges and priority_q:
            prev_cost, interface = heappop(priority_q)
            prev_cost = int(prev_cost.split(".")[0])
            if interface.router not in rem_bridges:
                continue
            interface.status = 2 # root port
            for int_no, next_interface in interface.router.interfaces.items():
                if next_interface.neighbour():
                    heappush(priority_q, (f"{next_interface.wire.cost + prev_cost}.{int_no}", next_interface.neighbour()))
            rem_bridges.remove(interface.router)
    
    def display(self):
        for router in self.routers:
            router.display()

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
            self.status = 0 # 0: blocked ; 1: designated port ; 2: root port
            self.router = router

        def connect(self, wire):
            self.wire = wire

        def neighbour(self):
            if not self.wire or not self.wire.int_1 or not self.wire.int_2:
                print("No wire connected.")
                return None

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
        print(self.mac_addr)
        for key, value in self.interfaces.items():
            print(f"{key}:{value.status}")
        print()

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
    R0 = Router(interfaces={0, 1}, mac_addr="00.00.00.00.00.00", priority=4096)
    R1 = Router(interfaces={0, 1}, mac_addr="00.00.00.00.00.01", priority=8192)
    R2 = Router(interfaces={0, 1}, mac_addr="00.00.00.00.00.02", priority=8192)
    R3 = Router(interfaces={0, 1}, mac_addr="00.00.00.00.00.03", priority=8192)

    topology.add_router(R0)
    topology.add_router(R1)
    topology.add_router(R2)
    topology.add_router(R3)

    w0 = Wire(cost=19)
    w1 = Wire(cost=1)
    w2 = Wire(cost=19)
    w3 = Wire(cost=19)

    w0.connect_to_int(R0.interfaces[0])
    w0.connect_to_int(R1.interfaces[0])

    w1.connect_to_int(R0.interfaces[1])
    w1.connect_to_int(R2.interfaces[0])

    w2.connect_to_int(R1.interfaces[1])
    w2.connect_to_int(R3.interfaces[0])

    w3.connect_to_int(R2.interfaces[1])
    w3.connect_to_int(R3.interfaces[1])

    
    topology.run_stp()
    topology.display()
