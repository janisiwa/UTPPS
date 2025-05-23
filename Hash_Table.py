"""Creates a hash map to store package ids and all package components.
Uses direct addressing and self-adjusts if grows to more than 70% capacity
"""
class Hash_Table:
    def __init__(self):
        """Initializes the Hash_Table

 with a fixed capacity and empty backing array."""
        #prime number larger than expected amount of packages
        self.capacity = 61
        #empty backing array
        self.map = [None]* self.capacity
        #length of backing array
        self.size = 0

        #for resizing the array
        self.new_map = None
        self.new_capacity = None

    def _get_hash(self, key):
        """Computes the hash for a given key.

        Args:
            key (int): The package ID key to hash.

        Returns:
            int or None: The hashed index if key is within capacity, else None.
        """
        #hash function for future use if decided to no longer direct address
        if key > self.capacity:
            return None
        else:
            return key % self.capacity

    #insert function using package ID - Requirement A
    def add(self, key, value):
        """Adds or updates a key-value pair in the Hash_Table

.

        Automatically resizes the backing array if the load factor exceeds 0.7.

        Args:
            key (int): The package ID key.
            value (any): The package components or value associated with the key.

        Returns:
            bool: True if the key-value pair is added or updated successfully.
        """
        # check for load capacity
        if self.size / self.capacity > 0.70:
            self.resize_backing_array()

        #hash based on the input key
        key_hash = self._get_hash(key)
        #key pair to be stored as the value in the list
        key_value = [key, value]

        if self.map[key_hash] is None:
            #there are no existing keys in that index
            self.map[key_hash] = key_value
            self.size += 1
            return True
        else:
            #update the value only
            value_pair = self.map[key_hash]
            if value_pair[0] == key:
                value_pair[1] = value
            self.size += 1
            return True

    def resize_backing_array(self):
        """Doubles the size of the backing array and rehashes all existing key-value pairs."""
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
                value_pair = self.map[index]
                new_index = self._get_hash(value_pair[0])
                self.new_map[new_index] = value_pair

        #replace with larger array
        self.map = self.new_map

        #release temporary array
        self.new_map = None
        self.new_capacity = None

    def remove(self, key):
        """Removes the key-value pair associated with the given key.

        Args:
            key (int): The package ID key to remove.

        Returns:
            bool: True if the key was found and removed, False if key was not found.
        """
        # hash based on the input key
        key_hash = self._get_hash(key)

        if self.map[key_hash] is None:
            # there are no existing keys in that index
            return False
        else:
            # delete key pair
            self.map[key_hash] = None
            return True

    #look-up function using package ID to return package - Requirement B
    def get(self, key):
        """Retrieves the value associated with the given key.

        Args:
            key (int): The package ID key to look up.

        Returns:
            value or None: The value associated with the key, or None if key not found.
        """
        # hash based on the input key
        key_hash = self._get_hash(key)

        if key_hash is None or self.map[key_hash] is None:
            # there are no existing keys in that index
            return None
        else:
            # the key is found, so return it
            value_pair = self.map[key_hash]
            return value_pair[1]

    def get_all(self):
        """Returns a list of all values stored in the Hash_Table

.

        Returns:
            list: A list containing all stored values.
        """
        return_list = []
        for entry in self.map:
            if entry:
                return_list.append(entry[1])
        return return_list
