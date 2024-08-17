import os
import random

from pygame import mixer


class SoundMaker:
    def __init__(self,
                 source_dir: str) -> None:
        # Paths
        self.sounds_dir = os.path.join(source_dir, "sounds")
        self.music_dir = os.path.join(self.sounds_dir, "music")
        self.effects_dir = os.path.join(self.sounds_dir, "effects")

        # Init mixer
        mixer.init()

        # Effect types
        self.effect_types = ["tick", "answer"]
        self.effect_played = [False, False]

        # Effects
        self.create_effects()

        # Music
        self.music_listdir = os.listdir(self.music_dir)
        self.music_path = random.choice(self.music_listdir)
        self.music_played = False

    def create_effects(self) -> None:
        self.right_answer_sound = mixer.Sound(
            os.path.join(self.effects_dir, "right_answer.wav"))
        self.ticking_sound = mixer.Sound(
            os.path.join(self.effects_dir, "ticking.mp3"))

        self.effects_ch = mixer.Channel(0)

    def update_sounds(self) -> None:
        # Change effect played flag
        self.effect_played = [
            False for _ in range(len(self.effect_played))]

        # Change music played flag and choose new music file
        self.music_played = False
        self.music_path = random.choice(self.music_listdir)

    def make_effect(self, effect_type: str) -> None:
        assert effect_type in self.effect_types, "Effect type should be one of ['tick', 'answer']."

        if self.effect_played[self.effect_types.index('answer')] is False and effect_type == "answer":
            self.effects_ch.play(self.right_answer_sound)
            self.effect_played[self.effect_types.index('answer')] = True

        elif self.effect_played[self.effect_types.index('tick')] is False and effect_type == "tick":
            self.effects_ch.play(self.ticking_sound, loops=-1)
            self.effect_played[self.effect_types.index('tick')] = True

    def play_music(self, volume: float = 0.7) -> None:
        if self.music_played is False:
            mixer.music.load(os.path.join(
                self.music_dir, self.music_path))
            mixer.music.set_volume(volume)
            mixer.music.play(-1)
            self.music_played = True
