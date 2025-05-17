class Truck:
    #
    __truck_id=set()

    def __init__(self, truck_id:'int',package_max:'int',driver=''):
        # ensure unique id
        if truck_id in Truck.__truck_id:
            raise ValueError(f"Truck with ID {truck_id} already exists.", truck_id)

        self.id = truck_id
        self.driver=driver
        self.status='at hub'
        self.packages_not_delivered =None
        self.departure_time=None
        self.return_time=None
        self.trip_distance=None
        self.package_maximum=package_max
        self.route=None

    def get_trucks_count(self):
        return len(Truck.__truck_id)