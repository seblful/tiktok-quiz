import os

from pygame import mixer


class SoundMaker:
    def __init__(self,
                 source_dir: str) -> None:
        # Paths
        self.sounds_dir = os.path.join(source_dir, "sounds")
        self.background_dir = os.path.join(self.sounds_dir, "background")
        self.effects_dir = os.path.join(self.sounds_dir, "effects")

        # Init mixer
        mixer.init()

        # Sound types
        self.effect_types = ["tick", "answer"]
        self.effect_played = [False, False]

        # Effects
        self.create_effects()

    def create_effects(self):
        self.right_answer_sound = mixer.Sound(
            os.path.join(self.effects_dir, "right_answer.wav"))
        self.ticking_sound = mixer.Sound(
            os.path.join(self.effects_dir, "ticking.mp3"))

        self.effects_ch = mixer.Channel(0)

    def make_effect(self, effect_type: str) -> None:
        assert effect_type in self.effect_types, "Effect type should be one of ['tick', 'answer']."

        if self.effect_played[self.effect_types.index('answer')] is False and effect_type == "answer":
            self.effects_ch.play(self.right_answer_sound)
            self.effect_played[self.effect_types.index('answer')] = True

        elif self.effect_played[self.effect_types.index('tick')] is False and effect_type == "tick":
            self.effects_ch.play(self.ticking_sound)
            self.effect_played[self.effect_types.index('tick')] = True

    def play_music(self) -> None:
        pass
