"""
Tools for working with spritesheets and visualizing frame layouts
"""

import pygame
from typing import Tuple, Optional
from pathlib import Path


def visualize_spritesheet(
    image_path: str,
    frame_size: Tuple[int, int],
    output_path: Optional[str] = None,
    grid_color: Tuple[int, int, int] = (0, 255, 0),
    text_color: Tuple[int, int, int] = (255, 255, 255),
    text_bg_color: Tuple[int, int, int] = (0, 0, 0),
    font_size: int = 20,
) -> str:
    """
    Create a visualization of a spritesheet with frame numbers and grid overlay.
    """
    # Initialize pygame if not already done
    if not pygame.get_init():
        pygame.init()

    # Initialize display if not already done (required for font operations)
    if not pygame.display.get_init():
        pygame.display.set_mode((1, 1), pygame.HIDDEN)

    # Load the spritesheet
    original_image = pygame.image.load(image_path).convert_alpha()
    sheet_width = original_image.get_width()
    sheet_height = original_image.get_height()

    frame_width, frame_height = frame_size
    frames_per_row = sheet_width // frame_width
    frames_per_col = sheet_height // frame_height
    total_frames = frames_per_row * frames_per_col

    # Create info header height
    info_height = 60

    # Create new image with info header
    viz_width = sheet_width
    viz_height = sheet_height + info_height
    viz_image = pygame.Surface((viz_width, viz_height), pygame.SRCALPHA)
    viz_image.fill((40, 40, 40))  # Dark background for header

    # Draw info header
    font_big = pygame.font.Font(None, 24)
    font_small = pygame.font.Font(None, 18)

    # Main info
    info_text = font_big.render(
        f"Size: {sheet_width}x{sheet_height} | Frame: {frame_width}x{frame_height}",
        True,
        (255, 255, 255),
    )
    viz_image.blit(info_text, (10, 5))

    # Grid info
    grid_text = font_small.render(
        f"Grid: {frames_per_row} cols x {frames_per_col} rows = {total_frames} frames",
        True,
        (200, 200, 200),
    )
    viz_image.blit(grid_text, (10, 30))

    # Draw original spritesheet below header
    viz_image.blit(original_image, (0, info_height))

    # Create font for frame numbers
    font = pygame.font.Font(None, font_size)

    # Draw grid and frame numbers (offset by header height)
    for row in range(frames_per_col):
        for col in range(frames_per_row):
            frame_index = row * frames_per_row + col

            # Calculate frame position (offset by header)
            x = col * frame_width
            y = row * frame_height + info_height

            # Draw grid lines
            frame_rect = pygame.Rect(x, y, frame_width, frame_height)
            pygame.draw.rect(viz_image, grid_color, frame_rect, 2)

            # Draw frame number
            text_surface = font.render(str(frame_index), True, text_color)
            text_rect = text_surface.get_rect()

            # Position text in corner of frame
            text_x = x + 2
            text_y = y + 2

            # Draw text background for better readability
            bg_rect = pygame.Rect(
                text_x - 1, text_y - 1, text_rect.width + 2, text_rect.height + 2
            )
            pygame.draw.rect(viz_image, text_bg_color, bg_rect)

            # Draw the text
            viz_image.blit(text_surface, (text_x, text_y))

    # Determine output path
    if output_path is None:
        path_obj = Path(image_path)
        output_path = str(path_obj.parent / f"{path_obj.stem}_grid{path_obj.suffix}")

    # Save the visualization
    pygame.image.save(viz_image, output_path)

    print(f"Spritesheet visualization saved to: {output_path}")
    print(f"Total frames: {total_frames} ({frames_per_row}x{frames_per_col})")
    print(f"Frame size: {frame_width}x{frame_height}")

    return output_path


def create_spritesheet_from_frames(
    source_sheet_path: str,
    frame_size: Tuple[int, int],
    frame_indices: list,
    output_path: Optional[str] = None,
    frames_per_row: int = None,
) -> str:
    """
    Create a new compact spritesheet from selected frames of another spritesheet.

    Args:
        source_sheet_path: Path to the source spritesheet
        frame_size: (width, height) of each frame
        frame_indices: List of frame indices to include
        output_path: Where to save the new spritesheet (optional)
        frames_per_row: How many frames per row (auto if None)

    Returns:
        Path to the created spritesheet file
    """
    if not pygame.get_init():
        pygame.init()

    # Initialize display if not already done
    if not pygame.display.get_init():
        pygame.display.set_mode((1, 1), pygame.HIDDEN)

    # Load source spritesheet
    source_sheet = pygame.image.load(source_sheet_path).convert_alpha()
    source_width = source_sheet.get_width()
    frame_width, frame_height = frame_size
    source_frames_per_row = source_width // frame_width

    # Extract frames from source
    frames = []
    for frame_index in frame_indices:
        row = frame_index // source_frames_per_row
        col = frame_index % source_frames_per_row

        x = col * frame_width
        y = row * frame_height

        frame = pygame.Surface(frame_size, pygame.SRCALPHA)
        frame.blit(source_sheet, (0, 0), pygame.Rect(x, y, frame_width, frame_height))
        frames.append(frame)

    # Calculate new spritesheet dimensions
    total_frames = len(frames)
    if frames_per_row is None:
        # Auto-calculate optimal layout
        if total_frames <= 4:
            frames_per_row = total_frames
        elif total_frames <= 8:
            frames_per_row = 4
        else:
            frames_per_row = 8

    rows = (total_frames + frames_per_row - 1) // frames_per_row
    new_width = frames_per_row * frame_width
    new_height = rows * frame_height

    # Create new compact spritesheet
    new_sheet = pygame.Surface((new_width, new_height), pygame.SRCALPHA)
    new_sheet.fill((0, 0, 0, 0))  # Transparent background

    # Place frames in new sheet
    for i, frame in enumerate(frames):
        row = i // frames_per_row
        col = i % frames_per_row

        x = col * frame_width
        y = row * frame_height

        new_sheet.blit(frame, (x, y))

    # Save new spritesheet
    if output_path is None:
        path_obj = Path(source_sheet_path)
        output_path = str(path_obj.parent / f"{path_obj.stem}_custom.png")

    pygame.image.save(new_sheet, output_path)

    print(f"New spritesheet saved to: {output_path}")
    print(f"Frames: {total_frames} ({frames_per_row}x{rows})")
    print(f"Size: {new_width}x{new_height}")

    return output_path
