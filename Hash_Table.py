"""Creates a hash map to store package ids and all package components.
Uses direct addressing for under 61 packages
"""
class Hash_Table:
    def __init__(self):
        #prime number larger than expected amount of packages
        self.capacity = 4
        #empty backing array
        self.map = [None]* self.capacity
        #length of backing array
        self.size = 0

        #for resizing the array
        self.new_map = None
        self.new_capacity = None

    def _get_hash(self, key):
        #hash function for future use if decided to no longer direct address
        return key % self.capacity

    def add(self,key,value):
        # check for load capacity
        if self.size / self.capacity > 0.70:
            self.resize_backing_array()

        #hash based on the input key
        key_hash = self._get_hash(key)
        #key pair to be stored as the value in the list
        key_value = [key,value]

        if self.map[key_hash] is None:
            #there are no existing keys in that index
            self.map[key_hash] = list([key_value])
            self.size += 1
            return True
        else:
            #look through the list of existing key pairs
            for value_pair in self.map[key_hash]:
                if value_pair[0] == key:
                    #the key is found, so update the value of the existing key pair
                    value_pair[1]=value
                    return True
            #the key is not found, so add the new key pair to the list
            self.map[key_hash].append(key_value)
            self.size += 1
            return True




    def resize_backing_array(self):
        # double the existing size
        self.new_capacity = self.capacity * 2
        # empty backing array
        self.new_map = [None] * self.capacity
        #set new capacity for hashing function
        old_capacity = self.capacity
        self.capacity = self.new_capacity

        #copy from old array to new array
        for index in range(old_capacity):
            #copy only the existing data elements
            if self.map[index] is not None:
                #if the current element contains a list of key value pairs
                for key, value in self.map[index]:
                    #add the key pair as new list or append to existing list
                    new_index = self._get_hash(key)
                    if self.new_map[new_index] is None:
                        self.new_map[new_index] = list([key, value])
                    else:
                        self.new_map[new_index].append((key, value))


        #replace with larger array
        self.map = self.new_map


        #release temporary array
        self.new_map= None
        self.new_capacity = None

    def remove(self,key):
        # hash based on the input key
        key_hash = self._get_hash(key)

        if self.map[key_hash] is None:
            # there are no existing keys in that index
            return False
        else:
            # look through the list of existing key pairs
            for index, value_pair in enumerate(self.map[key_hash]):
                if self.map[key_hash][index][0]==key:
                    self.map[key_hash].pop(index)
                    return True

    def get(self,key):
        # hash based on the input key
        key_hash = self._get_hash(key)

        if self.map[key_hash] is None:
            # there are no existing keys in that index
            return None
        else:
            # look through the list of existing key pairs
            for value_pair in self.map[key_hash]:
                if value_pair[0] == key:
                    # the key is found, so return it
                    return value_pair[1]

