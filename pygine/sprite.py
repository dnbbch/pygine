"""
Core sprite functionality with animation support
"""

import pygame
import math
from typing import List, Dict, Tuple, Optional, Union
from pathlib import Path
from .animation import Animation, AnimationManager


class AnimatedSprite(pygame.sprite.Sprite):
    """
    Enhanced pygame Sprite with built-in animation, transformation, and utility methods.

    This class extends pygame.sprite.Sprite to provide easy animation management,
    sprite sheet handling, transformations, and common game object functionality.

    Args:
        image_path: Path to sprite sheet image file
        frame_size: (width, height) of each frame in pixels
        position: Initial (x, y) position. Defaults to (0, 0)

    Example:
        >>> player = AnimatedSprite("player.png", (32, 32), (100, 100))
        >>> player.add_animation("walk", [0, 1, 2, 3], fps=10)
        >>> player.play_animation("walk")
    """

    def __init__(
        self,
        image_path: Union[str, Path],
        frame_size: Tuple[int, int],
        position: Tuple[int, int] = (0, 0),
    ):
        super().__init__()

        # Core properties
        self.original_image = pygame.image.load(str(image_path)).convert_alpha()
        self.frame_size = frame_size
        self._position = list(position)

        # Calculate spritesheet dimensions
        self.sheet_width = self.original_image.get_width()
        self.sheet_height = self.original_image.get_height()
        self.frames_per_row = self.sheet_width // frame_size[0]
        self.frames_per_col = self.sheet_height // frame_size[1]
        self.total_frames = self.frames_per_row * self.frames_per_col

        # Extract all frames from spritesheet
        self.frames = self._extract_frames()

        # Animation system
        self.animation_manager = AnimationManager()
        self.current_frame = 0

        # Transformation properties
        self.rotation = 0.0
        self.scale = 1.0
        self.flip_x = False
        self.flip_y = False
        self._mirrored = False

        # Physics properties
        self.velocity = [0.0, 0.0]
        self.acceleration = [0.0, 0.0]

        # Initialize pygame sprite properties
        self.image = self.frames[0] if self.frames else pygame.Surface(frame_size)
        self.rect = self.image.get_rect()
        self.rect.topleft = position

        # Collision properties
        self.collision_rect = self.rect.copy()
        self.collision_offset = (0, 0)

        # Custom hitbox properties
        self.custom_hitbox_size = None  # (width, height) or None for default
        self.hitbox_shape = "rect"  # "rect" or "circle"
        self.hitbox_radius = None  # for circle hitboxes

    def _extract_frames(self) -> List[pygame.Surface]:
        """Extract all individual frames from the sprite sheet."""
        frames = []
        frame_width, frame_height = self.frame_size

        for row in range(self.frames_per_col):
            for col in range(self.frames_per_row):
                x = col * frame_width
                y = row * frame_height

                frame = pygame.Surface(self.frame_size, pygame.SRCALPHA)
                frame.blit(
                    self.original_image,
                    (0, 0),
                    pygame.Rect(x, y, frame_width, frame_height),
                )
                frames.append(frame)

        return frames

    def add_animation(
        self, name: str, frames: List[int], fps: float = 10, loop: bool = True
    ) -> None:
        """
        Add a new animation to this sprite.

        Args:
            name: Unique name for the animation
            frames: List of frame indices from the sprite sheet
            fps: Animation speed in frames per second
            loop: Whether animation should loop

        Example:
            >>> sprite.add_animation("walk", [0, 1, 2, 3], fps=8)
            >>> sprite.add_animation("jump", [4, 5, 6], fps=12, loop=False)
        """
        # Validate frame indices
        valid_frames = [f for f in frames if 0 <= f < len(self.frames)]
        if len(valid_frames) != len(frames):
            invalid = [f for f in frames if f not in valid_frames]
            print(
                f"Warning: Invalid frame indices {invalid} for sprite with {len(self.frames)} frames"
            )

        animation = Animation(name, valid_frames, fps, loop)
        self.animation_manager.add_animation(animation)

    def play_animation(
        self, name: str, restart: bool = False, mirror: Optional[bool] = None
    ) -> bool:
        """
        Play a specific animation.

        Args:
            name: Name of the animation to play
            restart: Force restart if animation is already playing
            mirror: Override mirror state for this animation

        Returns:
            True if animation started successfully, False if animation not found
        """
        if mirror is not None:
            self._mirrored = mirror

        return self.animation_manager.play_animation(name, restart)

    def stop_animation(self) -> None:
        """Stop the current animation."""
        self.animation_manager.stop()

    def pause_animation(self) -> None:
        """Pause the current animation."""
        self.animation_manager.pause()

    def resume_animation(self) -> None:
        """Resume the paused animation."""
        self.animation_manager.resume()

    def is_animation_finished(self) -> bool:
        """Check if current animation has finished (for non-looping animations)."""
        return self.animation_manager.is_finished()

    def get_current_animation(self) -> Optional[str]:
        """Get the name of the currently playing animation."""
        return self.animation_manager.current_animation_name

    def get_animation_frame(self) -> int:
        """Get the current frame index within the animation."""
        return self.animation_manager.get_current_frame_index()

    def update(self, dt: float = 1 / 60) -> None:
        """
        Update the sprite's animation and physics.

        Args:
            dt: Delta time in seconds
        """
        # Update animation
        self.animation_manager.update(dt)
        current_animation = self.animation_manager.get_current_animation()

        if current_animation:
            frame_index = self.animation_manager.get_current_frame_index()
            if 0 <= frame_index < len(current_animation.frames):
                sprite_frame_index = current_animation.frames[frame_index]
                if 0 <= sprite_frame_index < len(self.frames):
                    self.current_frame = sprite_frame_index

        # Update physics
        self.velocity[0] += self.acceleration[0] * dt
        self.velocity[1] += self.acceleration[1] * dt

        self._position[0] += self.velocity[0] * dt
        self._position[1] += self.velocity[1] * dt

        # Update image with current transformations
        self._update_image()

        # Update rect position
        self.rect.center = (int(self._position[0]), int(self._position[1]))

        # Update collision rect
        self.collision_rect.center = (
            self.rect.centerx + self.collision_offset[0],
            self.rect.centery + self.collision_offset[1],
        )

    def _update_image(self) -> None:
        """Update the displayed image with current transformations."""
        if not self.frames:
            return

        # Start with current frame
        image = self.frames[self.current_frame].copy()

        # Apply scaling
        if self.scale != 1.0:
            new_size = (
                int(image.get_width() * self.scale),
                int(image.get_height() * self.scale),
            )
            image = pygame.transform.scale(image, new_size)

        # Apply flipping/mirroring
        flip_x = self.flip_x or self._mirrored
        if flip_x or self.flip_y:
            image = pygame.transform.flip(image, flip_x, self.flip_y)

        # Apply rotation
        if self.rotation != 0:
            image = pygame.transform.rotate(image, self.rotation)

        # Обновляем изображение и создаём новый rect.
        # Координаты центра установит вызывающий метод update(),
        # чтобы избежать двойного пересчёта за один кадр.
        self.image = image
        self.rect = self.image.get_rect()

    # Position and movement methods
    def set_position(self, x: float, y: float) -> None:
        """Set sprite position."""
        self._position = [float(x), float(y)]

    def get_position(self) -> Tuple[float, float]:
        """Get current sprite position."""
        return tuple(self._position)

    # --- NEW CONVENIENCE PROPERTIES -------------------------------------------------
    @property
    def x(self) -> float:
        """Horizontal center coordinate of the sprite (read-write)."""
        return self._position[0]

    @x.setter
    def x(self, value: float) -> None:
        self._position[0] = float(value)
        # Keep rect and collision rect in sync immediately
        self.rect.centerx = int(value)
        self.collision_rect.centerx = int(value) + self.collision_offset[0]

    @property
    def y(self) -> float:
        """Vertical center coordinate of the sprite (read-write)."""
        return self._position[1]

    @y.setter
    def y(self, value: float) -> None:
        self._position[1] = float(value)
        # Keep rect and collision rect in sync immediately
        self.rect.centery = int(value)
        self.collision_rect.centery = int(value) + self.collision_offset[1]

    # -------------------------------------------------------------------------------

    def move(self, dx: float, dy: float) -> None:
        """Move sprite by offset."""
        self._position[0] += dx
        self._position[1] += dy

    def move_to(self, x: float, y: float, speed: float = None) -> None:
        """Move sprite towards target position."""
        if speed is None:
            self.set_position(x, y)
        else:
            dx = x - self._position[0]
            dy = y - self._position[1]
            distance = math.sqrt(dx**2 + dy**2)

            if distance > 0:
                dx_norm = dx / distance
                dy_norm = dy / distance
                self.velocity[0] = dx_norm * speed
                self.velocity[1] = dy_norm * speed

    # Transformation methods
    def set_rotation(self, angle: float) -> None:
        """Set rotation angle in degrees."""
        self.rotation = angle % 360

    def rotate(self, angle: float) -> None:
        """Rotate by angle in degrees."""
        self.rotation = (self.rotation + angle) % 360

    def rotate_towards(self, x: float, y: float) -> None:
        """Rotate to face a specific point."""
        dx = x - self._position[0]
        dy = y - self._position[1]
        angle = math.degrees(math.atan2(-dy, dx))
        self.set_rotation(angle)

    def rotate_towards_mouse(self) -> None:
        """Rotate to face mouse cursor."""
        mouse_x, mouse_y = pygame.mouse.get_pos()
        self.rotate_towards(mouse_x, mouse_y)

    def set_scale(self, scale: float) -> None:
        """Set sprite scale (1.0 = normal size)."""
        self.scale = max(0.1, scale)  # Prevent negative or zero scale

    def set_flip(self, flip_x: bool = False, flip_y: bool = False) -> None:
        """Set sprite flipping."""
        self.flip_x = flip_x
        self.flip_y = flip_y

    def mirror(self, mirrored: bool = True) -> None:
        """Mirror sprite horizontally (useful for left/right movement)."""
        self._mirrored = mirrored

    # Collision methods
    def set_collision_rect(
        self, width: int, height: int, offset_x: int = 0, offset_y: int = 0
    ) -> None:
        """Set custom collision rectangle that works with rotation."""
        self.collision_rect = pygame.Rect(0, 0, width, height)
        self.collision_offset = (offset_x, offset_y)
        self.custom_hitbox_size = (width, height)
        self.hitbox_shape = "rect"

    def set_collision_circle(
        self, radius: float, offset_x: int = 0, offset_y: int = 0
    ) -> None:
        """Set circular collision area."""
        self.hitbox_shape = "circle"
        self.hitbox_radius = radius
        self.collision_offset = (offset_x, offset_y)
        # Still set rect for compatibility
        size = int(radius * 2)
        self.collision_rect = pygame.Rect(0, 0, size, size)

    def reset_collision_to_default(self) -> None:
        """Reset collision area to match sprite size."""
        self.custom_hitbox_size = None
        self.hitbox_shape = "rect"
        self.hitbox_radius = None
        self.collision_offset = (0, 0)

    def collides_with(self, other: "AnimatedSprite") -> bool:
        """Check collision with another sprite (supports rotation and different shapes)."""
        # Circle vs Circle collision
        if self.hitbox_shape == "circle" and other.hitbox_shape == "circle":
            return self._check_circle_collision(other)

        # Circle vs Rect collision
        if self.hitbox_shape == "circle" or other.hitbox_shape == "circle":
            return self._check_circle_rect_collision(other)

        # ALWAYS use the same corner-based collision as debug_draw shows
        return self._check_precise_rect_collision(other)

    def _check_precise_rect_collision(self, other: "AnimatedSprite") -> bool:
        """Precise rectangle collision using the exact same coordinates as debug_draw."""
        corners_a = self._get_corners()
        corners_b = other._get_corners()

        # Use SAT (Separating Axis Theorem) for precise collision
        return self._separating_axis_test(corners_a, corners_b)

    def _separating_axis_test(self, corners_a, corners_b):
        """Separating Axis Theorem test for polygon collision."""
        # Get all edges from both polygons
        all_corners = [corners_a, corners_b]

        for corners in all_corners:
            for i in range(len(corners)):
                # Get edge vector
                p1 = corners[i]
                p2 = corners[(i + 1) % len(corners)]
                edge = (p2[0] - p1[0], p2[1] - p1[1])

                # Get perpendicular (normal) vector
                normal = (-edge[1], edge[0])

                # Normalize
                length = math.sqrt(normal[0] ** 2 + normal[1] ** 2)
                if length == 0:
                    continue
                normal = (normal[0] / length, normal[1] / length)

                # Project both polygons onto this axis
                proj_a = [
                    corner[0] * normal[0] + corner[1] * normal[1]
                    for corner in corners_a
                ]
                proj_b = [
                    corner[0] * normal[0] + corner[1] * normal[1]
                    for corner in corners_b
                ]

                min_a, max_a = min(proj_a), max(proj_a)
                min_b, max_b = min(proj_b), max(proj_b)

                # Check for separation
                if max_a < min_b or max_b < min_a:
                    return False  # Separation found - no collision

        return True  # No separation found - collision detected

    def _check_obb_collision(self, other: "AnimatedSprite") -> bool:
        """DEPRECATED: Use _check_precise_rect_collision instead."""
        return self._check_precise_rect_collision(other)

    def _get_corners(self):
        """Get the four corners of the sprite's hitbox - EXACTLY what debug_draw shows."""
        # Use custom size if set, otherwise use frame size with scale
        if self.custom_hitbox_size:
            width, height = self.custom_hitbox_size
            # Custom sizes don't scale automatically
        else:
            width = self.frame_size[0] * self.scale
            height = self.frame_size[1] * self.scale

        # IMPORTANT: Use the same rounding as in update() method for consistency
        center_x = int(self._position[0]) + self.collision_offset[0]
        center_y = int(self._position[1]) + self.collision_offset[1]

        # Calculate corners relative to center
        half_w = width / 2
        half_h = height / 2

        corners = [
            (-half_w, -half_h),  # Top-left
            (half_w, -half_h),  # Top-right
            (half_w, half_h),  # Bottom-right
            (-half_w, half_h),  # Bottom-left
        ]

        # Apply rotation if needed
        if self.rotation != 0:
            # Invert angle to match pygame.transform.rotate direction
            # pygame rotates counter-clockwise with positive angles, but Y axis points down
            angle_rad = math.radians(-self.rotation)
            cos_a = math.cos(angle_rad)
            sin_a = math.sin(angle_rad)

            rotated_corners = []
            for x, y in corners:
                new_x = x * cos_a - y * sin_a
                new_y = x * sin_a + y * cos_a
                rotated_corners.append((new_x, new_y))
            corners = rotated_corners

        # Translate to world coordinates
        world_corners = [(center_x + x, center_y + y) for x, y in corners]
        return world_corners

    def _check_circle_collision(self, other: "AnimatedSprite") -> bool:
        """Check collision between two circles."""
        # Use same rounding as everywhere else
        center1 = (
            int(self._position[0]) + self.collision_offset[0],
            int(self._position[1]) + self.collision_offset[1],
        )
        center2 = (
            int(other._position[0]) + other.collision_offset[0],
            int(other._position[1]) + other.collision_offset[1],
        )

        dx = center2[0] - center1[0]
        dy = center2[1] - center1[1]
        distance = math.sqrt(dx * dx + dy * dy)

        return distance <= (self.hitbox_radius + other.hitbox_radius)

    def _check_circle_rect_collision(self, other: "AnimatedSprite") -> bool:
        """Precise collision between circle and rectangle using proper algorithm."""
        if self.hitbox_shape == "circle":
            circle_sprite = self
            rect_sprite = other
        else:
            circle_sprite = other
            rect_sprite = self

        # Get circle center with consistent rounding
        circle_center = (
            int(circle_sprite._position[0]) + circle_sprite.collision_offset[0],
            int(circle_sprite._position[1]) + circle_sprite.collision_offset[1],
        )

        # For rotated rectangles, use polygon-circle collision
        if rect_sprite.rotation != 0 or rect_sprite.custom_hitbox_size:
            return self._check_polygon_circle_collision(circle_sprite, rect_sprite)

        # Simple case: axis-aligned rectangle
        # Get rectangle bounds
        rect_width = rect_sprite.frame_size[0] * rect_sprite.scale
        rect_height = rect_sprite.frame_size[1] * rect_sprite.scale

        rect_center_x = int(rect_sprite._position[0]) + rect_sprite.collision_offset[0]
        rect_center_y = int(rect_sprite._position[1]) + rect_sprite.collision_offset[1]

        rect_left = rect_center_x - rect_width / 2
        rect_right = rect_center_x + rect_width / 2
        rect_top = rect_center_y - rect_height / 2
        rect_bottom = rect_center_y + rect_height / 2

        # Find closest point on rectangle to circle center
        closest_x = max(rect_left, min(circle_center[0], rect_right))
        closest_y = max(rect_top, min(circle_center[1], rect_bottom))

        # Calculate distance from circle center to closest point
        dx = circle_center[0] - closest_x
        dy = circle_center[1] - closest_y
        distance = math.sqrt(dx * dx + dy * dy)

        return distance <= circle_sprite.hitbox_radius

    def _check_polygon_circle_collision(
        self, circle_sprite: "AnimatedSprite", rect_sprite: "AnimatedSprite"
    ) -> bool:
        """Check collision between circle and rotated polygon using precise algorithm."""
        circle_center = (
            int(circle_sprite._position[0]) + circle_sprite.collision_offset[0],
            int(circle_sprite._position[1]) + circle_sprite.collision_offset[1],
        )

        # Get polygon corners
        polygon_corners = rect_sprite._get_corners()

        # Check if circle center is inside polygon
        inside = self._point_in_polygon(circle_center, polygon_corners)
        if inside:
            return True

        # Check distance from circle center to each edge of polygon
        for i in range(len(polygon_corners)):
            p1 = polygon_corners[i]
            p2 = polygon_corners[(i + 1) % len(polygon_corners)]

            # Distance from circle center to line segment
            distance = self._point_to_line_distance(circle_center, p1, p2)
            if distance <= circle_sprite.hitbox_radius:
                return True

        return False

    def _point_in_polygon(self, point, polygon):
        """Check if point is inside polygon using ray casting algorithm."""
        x, y = point
        n = len(polygon)
        inside = False

        p1x, p1y = polygon[0]
        for i in range(1, n + 1):
            p2x, p2y = polygon[i % n]
            if y > min(p1y, p2y):
                if y <= max(p1y, p2y):
                    if x <= max(p1x, p2x):
                        if p1y != p2y:
                            xinters = (y - p1y) * (p2x - p1x) / (p2y - p1y) + p1x
                        if p1x == p2x or x <= xinters:
                            inside = not inside
            p1x, p1y = p2x, p2y

        return inside

    def _point_to_line_distance(self, point, line_p1, line_p2):
        """Calculate minimum distance from point to line segment."""
        px, py = point
        x1, y1 = line_p1
        x2, y2 = line_p2

        # Vector from line start to line end
        line_vec = (x2 - x1, y2 - y1)
        # Vector from line start to point
        point_vec = (px - x1, py - y1)

        # Length squared of line
        line_len_sq = line_vec[0] * line_vec[0] + line_vec[1] * line_vec[1]

        if line_len_sq == 0:
            # Line is actually a point
            return math.sqrt((px - x1) * (px - x1) + (py - y1) * (py - y1))

        # Project point onto line
        dot_product = point_vec[0] * line_vec[0] + point_vec[1] * line_vec[1]
        t = max(0, min(1, dot_product / line_len_sq))

        # Find closest point on line segment
        closest_x = x1 + t * line_vec[0]
        closest_y = y1 + t * line_vec[1]

        # Distance from point to closest point on line
        dx = px - closest_x
        dy = py - closest_y
        return math.sqrt(dx * dx + dy * dy)

    def collides_with_group(self, group: pygame.sprite.Group) -> List["AnimatedSprite"]:
        """Check collision with sprite group."""
        collisions = []
        for sprite in group:
            if isinstance(sprite, AnimatedSprite) and sprite != self:
                if self.collides_with(sprite):
                    collisions.append(sprite)
        return collisions

    # Utility methods
    def distance_to(self, other: Union["AnimatedSprite", Tuple[float, float]]) -> float:
        """Calculate distance to another sprite or point using consistent positioning."""
        if isinstance(other, AnimatedSprite):
            # Use consistent positioning like in collisions
            other_pos = (int(other._position[0]), int(other._position[1]))
        else:
            other_pos = other

        # Use consistent positioning
        self_pos = (int(self._position[0]), int(self._position[1]))

        dx = other_pos[0] - self_pos[0]
        dy = other_pos[1] - self_pos[1]
        return math.sqrt(dx**2 + dy**2)

    def angle_to(self, other: Union["AnimatedSprite", Tuple[float, float]]) -> float:
        """Calculate angle to another sprite or point using consistent positioning."""
        if isinstance(other, AnimatedSprite):
            # Use consistent positioning like in collisions
            other_pos = (int(other._position[0]), int(other._position[1]))
        else:
            other_pos = other

        # Use consistent positioning
        self_pos = (int(self._position[0]), int(self._position[1]))

        dx = other_pos[0] - self_pos[0]
        dy = other_pos[1] - self_pos[1]
        return math.degrees(math.atan2(-dy, dx))

    def is_on_screen(self, screen_rect: pygame.Rect) -> bool:
        """Check if sprite is visible on screen."""
        return self.rect.colliderect(screen_rect)

    def wrap_screen(self, screen_rect: pygame.Rect) -> None:
        """Wrap sprite around screen edges."""
        if self.rect.right < 0:
            self.rect.left = screen_rect.right
        elif self.rect.left > screen_rect.right:
            self.rect.right = 0

        if self.rect.bottom < 0:
            self.rect.top = screen_rect.bottom
        elif self.rect.top > screen_rect.bottom:
            self.rect.bottom = 0

        self._position[0] = self.rect.centerx
        self._position[1] = self.rect.centery

    def debug_draw(self, screen: pygame.Surface) -> None:
        """
        Draw debug hitbox - EXACTLY the same area used for collision detection.

        Args:
            screen: Surface to draw on

        Shows:
            - Green shape: precise hitbox used for collision detection
        """
        if self.hitbox_shape == "circle":
            # Draw circle hitbox with same rounding
            center = (
                int(self._position[0]) + self.collision_offset[0],
                int(self._position[1]) + self.collision_offset[1],
            )
            radius = int(self.hitbox_radius)
            pygame.draw.circle(screen, (0, 255, 0), center, radius, 2)
        else:
            # Draw rectangular hitbox - EXACTLY the same corners used in collision
            corners = self._get_corners()
            # Convert to integers for drawing
            int_corners = [(int(x), int(y)) for x, y in corners]
            pygame.draw.polygon(screen, (0, 255, 0), int_corners, 2)

    def debug_info(self) -> Dict:
        """Get debug information about the sprite."""
        return {
            "position": self.get_position(),
            "velocity": self.velocity.copy(),
            "rotation": self.rotation,
            "scale": self.scale,
            "current_frame": self.current_frame,
            "animation": self.get_current_animation(),
            "animation_frame": self.get_animation_frame(),
            "total_frames": len(self.frames),
            "rect": (self.rect.x, self.rect.y, self.rect.width, self.rect.height),
        }
