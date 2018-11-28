import umsgpack


class SampleSerialization:
    def __init__(self, path):
        super().__init__()
        self._fileobj = open(path, mode='bw')

    def save(self, data):
        umsgpack.dump(data, self._fileobj)

    def close(self):
        self._fileobj.close()
