from typing import Tuple, List

import os
import random

import pygame


class Mention:
    def __init__(self,
                 screen_size: Tuple[int, int],
                 font_dir: str,
                 text: str = '@livequizmaster',
                 position: str = 'horizontal',
                 color: Tuple[int, int, int] = (220, 220, 220),
                 font_name: str = "Zain-Regular.ttf",
                 font_size: str = 26) -> None:
        # Screen
        self.width, self.height = screen_size

        # Init text, color
        self.text = text
        self.color = color

        # Create font
        self.font = pygame.font.Font(
            os.path.join(font_dir, font_name), font_size)

        # Setup surface
        self.setup_surface(position=position)

    def setup_surface(self, position: str) -> None:
        assert position in [
            'vertical', 'horizontal'], "Position must be one of ['vertical', 'horizontal']."

        # Create surface
        self.surface = self.font.render(self.text, True, self.color)
        self.surface.set_alpha(150)

        # Set coordinates of text
        if position == "horizontal":
            self.rect = self.surface.get_rect(
                center=(self.width * 0.76, self.height * 0.97))
        else:
            self.surface = pygame.transform.rotate(self.surface, 90)
            self.rect = self.surface.get_rect(
                center=(self.width * 0.95, self.height * 0.87))

    def render(self, screen: pygame.Surface) -> None:
        screen.blit(self.surface, self.rect)


class Background:
    def __init__(self,
                 source_dir: str,
                 screen_size: Tuple[int, int],
                 shape_size: int = 50,
                 padding: int = 20) -> None:

        # Paths
        self.icons_dir = os.path.join(source_dir, 'icons')
        self.icons_listdir = os.listdir(self.icons_dir)

        # Screen
        self.screen_width, self.screen_height = screen_size
        self.surface = pygame.Surface(screen_size)

        # Colors
        self.colors = ((255, 190, 11), (251, 86, 7),
                       (255, 0, 110), (131, 56, 236), (58, 134, 255))
        self.color_index = 0

        # Shapes
        self.shapes: List[Shape] = []
        self.shape_size = shape_size
        self.padding = padding
        self.create_shapes()

    def load_image(self) -> pygame.Surface:
        image = pygame.image.load(os.path.join(
            self.icons_dir, random.choice(self.icons_listdir))).convert_alpha()
        image = pygame.transform.scale(
            image, (self.shape_size, self.shape_size))

        return image

    def create_shapes(self, even_rows: int = 5, columns: int = 4) -> None:

        # Load icon for shape and preprocess it
        shape_image = self.load_image()

        # Find available space and interval
        available_space_x = self.screen_width - 2 * self.padding
        available_space_y = self.screen_height - 2 * self.padding

        shape_interval_x = available_space_x / (columns - 1)
        shape_interval_y = (available_space_y - even_rows *
                            self.shape_size) / (even_rows - 1)

        # Iterate through cols and rows and calculate positions
        for col in range(columns):
            rows = even_rows if col % 2 == 0 else even_rows - 1
            for row in range(rows):
                y = self.padding + (row if col % 2 == 0 else row + 0.5) * \
                    (self.shape_size + shape_interval_y)
                x = self.padding + col * shape_interval_x - self.shape_size  # Start offscreen

                # Create shapes
                shape = Shape(x=x,
                              y=y,
                              base_image=shape_image,
                              base_color=self.colors[self.color_index % len(
                                  self.colors)],
                              size=self.shape_size)
                self.shapes.append(shape)

    def render(self, screen: pygame.Surface) -> None:
        self.surface.fill(self.colors[self.color_index % len(self.colors)])

        for shape in self.shapes:
            shape.move(self.screen_width)
            shape.draw(self.surface)

        screen.blit(self.surface, (0, 0))

    def update_color(self) -> None:
        self.color_index += 1

        shape_image = self.load_image()

        for shape in self.shapes:
            shape.color = self.colors[self.color_index % len(self.colors)]
            shape.image = shape_image


class Shape:
    def __init__(self,
                 x: int,
                 y: int,
                 base_image: pygame.Surface,
                 base_color: Tuple[int, int, int],
                 size: int,
                 speed: float = 2) -> None:

        # Coordinates
        self.x = x
        self.y = y

        # Image icon
        self.base_image = base_image
        self.__image = None

        # Color
        self.base_color = base_color
        self.__color = None

        # Size and speed
        self.size = size
        self.speed = speed

    @property
    def color(self) -> Tuple[int, int, int]:
        if self.__color is None:
            self.__color = self.increase_brightness(self.base_color)

        return self.__color

    @color.setter
    def color(self, value: Tuple[int, int, int]) -> None:
        self.__color = self.increase_brightness(value)

    @property
    def image(self):
        if self.__image is None:
            self.__image = self.update_image_color(self.base_image, self.color)

        return self.__image

    @image.setter
    def image(self, value) -> None:
        self.__image = self.update_image_color(value, self.color)

    @staticmethod
    def update_image_color(image: pygame.Surface,
                           color: Tuple[int, int, int]) -> pygame.Surface:
        # Get the size of the image
        width, height = image.get_size()

        # Create a new surface with the same size
        new_image = pygame.Surface((width, height), pygame.SRCALPHA, 32)

        # Get pixel array
        for x in range(width):
            for y in range(height):
                # Get the color of the pixel
                pixel = image.get_at((x, y))

                # If the pixel is not transparent
                if pixel.a != 0:
                    # Change the pixel to the new color while keeping the alpha
                    new_image.set_at(
                        (x, y), (*color, pixel.a))
                else:
                    # Keep the pixel transparent
                    new_image.set_at((x, y), pixel)

        return new_image

    @staticmethod
    def increase_brightness(color: Tuple[int, int, int],
                            factor: float = 1.2) -> Tuple[int, int, int]:
        return tuple(min(255, int(c * factor)) for c in color)

    def move(self, width: int) -> None:
        self.x += self.speed
        if self.x > width:
            self.x = -self.size

    def draw(self, surface: pygame.Surface) -> None:
        surface.blit(self.image, (self.x, self.y))
