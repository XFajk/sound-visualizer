from time import perf_counter

class _Time:
    def __init__(self):
        self._last_frame_time = perf_counter()
        self._current_frame_time = 0.0
        self.delta_time = 0.0
        self.time = 0.0
    
    def update(self):
        self._current_frame_time = perf_counter()
        self.delta_time = self._current_frame_time - self._last_frame_time
        self._last_frame_time = self._current_frame_time
        
        self.time += self.delta_time
        
TIME = _Time()