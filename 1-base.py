"""
Funcionalidad básica (5 puntos):
generar y guardar un nuevo vídeo con las regiones seleccionadas
dibujadas sobre los frames del vídeo original.
"""

import cv2
import numpy as np
from cv2.typing import MatLike

WINDOW_NAME = "DOG WINDOW"
RED = (0, 0, 255)
GREEN = (0, 255, 0)
BLACK = (0, 0, 0)

PREVIOUS_FRAME_KEYS = (2424832, 65361, 63234)
NEXT_FRAME_KEYS = (2555904, 65363, 63235)
QUIT_KEYS = (ord("q"), ord("Q"))

Point = tuple[int, int]
Box = tuple[Point, Point]


def main():
    print(45 * "=")
    print("1-base.py")
    print(45 * "=")

    video = cv2.VideoCapture("dog.mp4")
    frame_number = 1

    frame = read_frame(video, frame_number)
    total_frames = int(video.get(cv2.CAP_PROP_FRAME_COUNT))

    click_points: list[Point] = []
    frame_box_map: dict[int, Box] = {}

    cv2.namedWindow(WINDOW_NAME)
    cv2.setMouseCallback(
        window_name=WINDOW_NAME, on_mouse=add_click_point, param=click_points
    )

    while True:
        preview = frame.copy()

        # draw click points
        for point in click_points:
            cv2.circle(preview, point, 4, RED, -1)

        # draw current box assign to the frame
        if frame_number in frame_box_map:
            draw_box(preview, *frame_box_map[frame_number])

        draw_frame_number(preview, frame_number, total_frames)
        draw_menu(preview)

        # show frame with updates
        cv2.imshow(WINDOW_NAME, preview)

        key = cv2.waitKeyEx(20)

        if len(click_points) >= 2:
            frame_box_map[frame_number] = (click_points[0], click_points[1])
            click_points.clear()

        if key in QUIT_KEYS:
            break

        if key in PREVIOUS_FRAME_KEYS or key in NEXT_FRAME_KEYS:
            step = 1 if key in NEXT_FRAME_KEYS else -1
            new_frame = read_frame(video, frame_number + step)

            if new_frame is not None:
                frame = new_frame
                frame_number += step
                click_points.clear()

    cv2.destroyAllWindows()
    video.release()


def draw_box(frame: np.ndarray, pt1: Point, pt2: Point) -> None:
    x1, y1 = pt1
    x2, y2 = pt2

    p1 = (x1, y1)
    p2 = (x2, y1)
    p3 = (x2, y2)
    p4 = (x1, y2)

    lines = [[p1, p2], [p2, p3], [p3, p4], [p4, p1]]

    for line in lines:
        cv2.line(frame, *line, GREEN)


def draw_frame_number(frame: MatLike, frame_number: int, total_frames: int):
    draw_text_panel(frame, (f"Frame: {frame_number} / {total_frames}",))


def draw_menu(frame: MatLike) -> None:
    MENU_LINES = (
        "<- / ->: Frame anterior / siguiente",
        "Click izq: Etiquetar",
        "Q: Guardar y salir",
    )
    draw_text_panel(frame, MENU_LINES, align_right=True)


def draw_text_panel(
    frame: MatLike, lines: tuple[str, ...], align_right: bool = False
) -> None:

    LINE_GAP = 6
    FONT_FACE = cv2.FONT_HERSHEY_SIMPLEX
    FONT_SCALE = 0.4
    THICKNESS = 1
    MARGIN = 8
    PADDING = 5

    sizes = [cv2.getTextSize(line, FONT_FACE, FONT_SCALE, THICKNESS) for line in lines]

    text_width = max(width for (width, _), _ in sizes)

    (_, text_height), baseline = sizes[0]
    line_height = text_height + baseline + LINE_GAP

    panel_width = text_width + 2 * PADDING
    panel_height = len(lines) * line_height - LINE_GAP + 2 * PADDING

    x = frame.shape[1] - panel_width - MARGIN if align_right else MARGIN
    y = MARGIN

    cv2.rectangle(frame, (x, y), (x + panel_width, y + panel_height), BLACK, -1)

    for i, line in enumerate(lines):
        cv2.putText(
            img=frame,
            text=line,
            org=(x + PADDING, y + PADDING + text_height + i * line_height),
            fontFace=FONT_FACE,
            fontScale=FONT_SCALE,
            color=GREEN,
            thickness=THICKNESS,
            lineType=cv2.LINE_AA,
        )


def add_click_point(event: int, x: int, y: int, flags: int, param: list[Point]) -> None:
    if event == cv2.EVENT_LBUTTONDOWN:
        param.append((x, y))


def read_frame(video: cv2.VideoCapture, frame_number: int) -> MatLike:
    if frame_number < 1:
        return None

    video.set(cv2.CAP_PROP_POS_FRAMES, frame_number - 1)
    _success, frame = video.read()
    return frame if _success else None


main()
