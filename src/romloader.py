class ROMLoader:
    def __init__(self, file_path, size):
        self.file_path = file_path
        self.size = size
    
    def load(self):
        with open(self.file_path, 'rb') as f:
            data = f.read()
        
        # Pad the data with 0s to the desired size
        data = bytearray(data)
        data.extend(bytearray(self.size - len(data)))
        return data
