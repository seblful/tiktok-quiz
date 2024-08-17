import os


class SoundMaker:
    def __init__(self,
                 source_dir: str) -> None:
        # Paths
        self.sounds_dir = os.path.join(source_dir, "sounds")
        self.background_dir = os.path.join(self.sounds_dir, "background")
        self.effects_dir = os.path.join(self.sounds_dir, "effects")
