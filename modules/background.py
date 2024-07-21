from typing import Tuple
import os
import pygame


class Background:
    def __init__(self,
                 screen_size: Tuple[int, int],
                 shape_size: int = 50,
                 padding: int = 20) -> None:
        self.screen_width, self.screen_height = screen_size
        self.surface = pygame.Surface(screen_size)
        self.colors = ((255, 190, 11), (251, 86, 7),
                       (255, 0, 110), (131, 56, 236), (58, 134, 255))
        self.color_index = 0
        self.shapes: List[Shape] = []
        self.shape_size = shape_size
        self.padding = padding
        self.create_shapes()

    def create_shapes(self, even_rows: int = 5, columns: int = 4) -> None:
        self.shapes.clear()
        available_space_x = self.screen_width - 2 * self.padding
        available_space_y = self.screen_height - 2 * self.padding

        shape_interval_x = available_space_x / (columns - 1)
        shape_interval_y = (available_space_y - even_rows *
                            self.shape_size) / (even_rows - 1)

        for col in range(columns):
            rows = even_rows if col % 2 == 0 else even_rows - 1
            for row in range(rows):
                y = self.padding + (row if col % 2 == 0 else row + 0.5) * \
                    (self.shape_size + shape_interval_y)
                x = self.padding + col * shape_interval_x - self.shape_size  # Start offscreen

                shape = Shape(x, y, self.colors[self.color_index % len(
                    self.colors)], self.shape_size)
                self.shapes.append(shape)

    def render(self, screen: pygame.Surface, fps: int) -> None:
        self.surface.fill(self.colors[self.color_index % len(self.colors)])

        for shape in self.shapes:
            shape.move(self.screen_width)
            shape.draw(self.surface)

        screen.blit(self.surface, (0, 0))
        pygame.display.flip()
        pygame.time.Clock().tick(fps)

    def update_color(self) -> None:
        self.color_index += 1

        for shape in self.shapes:
            shape.color = shape.increase_brightness(
                color=self.colors[self.color_index % len(self.colors)])


class Shape:
    def __init__(self, x: int, y: int, base_color: Tuple[int, int, int], size: int, speed: float = 3) -> None:
        self.x = x
        self.y = y
        self.base_color = base_color
        self.__color = None
        self.size = size
        self.speed = speed
        self.image = pygame.image.load(os.path.join(
            'source', 'search.png')).convert_alpha()
        self.image = pygame.transform.scale(self.image, (size, size))
        self.update_image_color()

    @property
    def color(self) -> Tuple[int, int, int]:
        if self.__color is None:
            self.__color = self.increase_brightness(self.base_color)

        return self.__color

    @color.setter
    def color(self, value: Tuple[int, int, int]) -> None:
        self.__color = self.increase_brightness(value)
        self.update_image_color()

    def update_image_color(self):
        # Get the size of the image
        width, height = self.image.get_size()

        # Create a new surface with the same size
        new_image = pygame.Surface((width, height), pygame.SRCALPHA, 32)

        # Get pixel array
        for x in range(width):
            for y in range(height):
                # Get the color of the pixel
                pixel = self.image.get_at((x, y))

                # If the pixel is not transparent
                if pixel.a != 0:
                    # Change the pixel to the new color while keeping the alpha
                    new_image.set_at(
                        (x, y), (*self.color, pixel.a))
                else:
                    # Keep the pixel transparent
                    new_image.set_at((x, y), pixel)

        self.image = new_image

    @staticmethod
    def increase_brightness(color: Tuple[int, int, int],
                            factor: float = 1.1) -> Tuple[int, int, int]:
        return tuple(min(255, int(c * factor)) for c in color)

    def move(self, width: int) -> None:
        self.x += self.speed
        if self.x > width:
            self.x = -self.size

    def draw(self, surface: pygame.Surface) -> None:
        surface.blit(self.image, (self.x, self.y))
