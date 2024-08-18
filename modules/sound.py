import os
import random

from pygame import mixer
import edge_tts


class SoundMaker:
    def __init__(self,
                 source_dir: str) -> None:
        # Paths
        self.sounds_dir = os.path.join(source_dir, "sounds")
        self.music_dir = os.path.join(self.sounds_dir, "music")
        self.effects_dir = os.path.join(self.sounds_dir, "effects")

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

    def make_effect(self, effect_type: str) -> None:
        assert effect_type in self.effect_types, "Effect type should be one of ['tick', 'answer']."

        if self.effect_played[self.effect_types.index('answer')] is False and effect_type == "answer":
            self.effects_ch.play(self.right_answer_sound)
            self.effect_played[self.effect_types.index('answer')] = True

        elif self.effect_played[self.effect_types.index('tick')] is False and effect_type == "tick":
            self.effects_ch.play(self.ticking_sound, loops=-1)
            self.effect_played[self.effect_types.index('tick')] = True

    def play_music(self, volume: float = 0.4) -> None:
        if self.music_played is False:
            mixer.music.load(os.path.join(
                self.music_dir, self.music_path))
            mixer.music.set_volume(volume)
            mixer.music.play(-1)
            self.music_played = True

    def update_sounds(self) -> None:
        # Change effect played flag
        self.effect_played = [
            False for _ in range(len(self.effect_played))]

        # Change music played flag and choose new music file
        self.music_played = False
        self.music_path = random.choice(self.music_listdir)


class VoiceMaker:
    def __init__(self, source_dir: str) -> None:
        # Paths
        self.sounds_dir = os.path.join(source_dir, "sounds")
        self.voice_dir = os.path.join(self.sounds_dir, "voices")

        self.q_and_a_path = os.path.join(self.voice_dir, "q_and_a.mp3")
        self.right_answer_path = os.path.join(
            self.voice_dir, "right_answer.mp3")

        # Voice
        self.voice = "en-US-AriaNeural"
        self.voice_types = ["q_and_a", "right_answer"]
        self.text_created = [False, False]
        self.voice_played = [False, False]
        self.create_channel()

    def create_channel(self) -> None:
        self.voice_ch = mixer.Channel(1)

    def create_voice(self, voice_type: str, *args) -> None:
        # Retrieve text from question and answers
        if self.text_created[self.voice_types.index('q_and_a')] is False and voice_type == "q_and_a":
            # Retrieve question and answers
            question, answers = args
            answers = answers.copy()

            # Create text
            text = question + "\n" + "\n".join(answers)

            # Create voice
            communicate = edge_tts.Communicate(text, self.voice, rate="-10%")
            communicate.stream_sync()
            communicate.save_sync(self.q_and_a_path)

            # Change flag
            self.text_created[self.voice_types.index('q_and_a')] = True

        elif self.text_created[self.voice_types.index('right_answer')] is False and voice_type == "right_answer":
            text = args[0]
            # Create voice
            communicate = edge_tts.Communicate(text, self.voice)
            communicate.stream_sync()
            communicate.save_sync(self.right_answer_path)

            # Change flag
            self.text_created[self.voice_types.index('right_answer')] = True

    def make_voice(self, voice_type: str, *args, volume=1) -> None:
        assert voice_type in self.voice_types, "Voice type should be one of ['q_and_a', 'right_answer']."

        # Create voice file
        self.create_voice(voice_type, *args)

        # Play voice file
        if self.voice_played[self.voice_types.index('q_and_a')] is False and voice_type == "q_and_a":
            q_and_a_sound = mixer.Sound(self.q_and_a_path)
            self.voice_ch.play(q_and_a_sound)
            self.voice_played[self.voice_types.index('q_and_a')] = True

        elif self.voice_played[self.voice_types.index('right_answer')] is False and voice_type == "right_answer":
            right_answer_sound = mixer.Sound(self.right_answer_path)
            self.voice_ch.play(right_answer_sound)
            self.voice_played[self.voice_types.index('right_answer')] = True

    def update_voices(self):
        self.text_created = [
            False for _ in range(len(self.text_created))]
        self.voice_played = [
            False for _ in range(len(self.voice_played))]
