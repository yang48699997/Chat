import time


class Snowflake:
    def __init__(self, data_center_id, machine_id, twepoch=1609459200000):
        self.twepoch = twepoch
        self.data_center_id = data_center_id
        self.machine_id = machine_id
        self.sequence = 0
        self.last_timestamp = -1

        self.data_center_id_bits = 5
        self.machine_id_bits = 5
        self.sequence_bits = 12

        self.max_data_center_id = (1 << self.data_center_id_bits) - 1
        self.max_machine_id = (1 << self.machine_id_bits) - 1

        self.data_center_id_shift = self.sequence_bits + self.machine_id_bits
        self.machine_id_shift = self.sequence_bits
        self.timestamp_left_shift = self.sequence_bits + self.machine_id_bits + self.data_center_id_bits
        self.sequence_mask = (1 << self.sequence_bits) - 1

        if self.data_center_id > self.max_data_center_id or self.data_center_id < 0:
            raise ValueError("Data center ID out of range喵")
        if self.machine_id > self.max_machine_id or self.machine_id < 0:
            raise ValueError("Machine ID out of range喵")

    def _current_timestamp(self):
        return int(time.time() * 1000)

    def _wait_for_next_millis(self, last_timestamp):
        timestamp = self._current_timestamp()
        while timestamp <= last_timestamp:
            timestamp = self._current_timestamp()
        return timestamp

    def next_id(self):
        timestamp = self._current_timestamp()

        if timestamp < self.last_timestamp:
            raise Exception("Clock moved backwards喵")

        if timestamp == self.last_timestamp:
            self.sequence = (self.sequence + 1) & self.sequence_mask
            if self.sequence == 0:
                timestamp = self._wait_for_next_millis(self.last_timestamp)
        else:
            self.sequence = 0

        self.last_timestamp = timestamp
        snowflake_id = ((timestamp - self.twepoch) << self.timestamp_left_shift) | \
                       (self.data_center_id << self.data_center_id_shift) | \
                       (self.machine_id << self.machine_id_shift) | \
                       self.sequence
        return snowflake_id


if __name__ == "__main__":
    snowflake = Snowflake(data_center_id=1, machine_id=1)
    for _ in range(10):
        print(snowflake.next_id())
