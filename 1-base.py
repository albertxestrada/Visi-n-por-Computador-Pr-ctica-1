"""
Funcionalidad básica (5 puntos):
generar y guardar un nuevo vídeo con las regiones seleccionadas
dibujadas sobre los frames del vídeo original.
"""

import os

import cv2

WINDOW_NAME = "DOG WINDOW"
RED = (0, 0, 255)
GREEN = (0, 255, 0)

PREVIOUS_FRAME_KEYS = (2424832, 65361, 63234)
NEXT_FRAME_KEYS = (2555904, 65363, 63235)
QUIT_KEYS = (ord("q"), ord("Q"))
DISCARD_KEYS = (27,)  # Esc
UNDO_KEYS = (ord("z"), ord("Z"))
PAUSE_KEYS = (ord(" "),)
OUTPUT_PATH = "./outputs/1-base.mp4"


def draw_box(frame, pt1, pt2):
    x1, y1 = pt1
    x2, y2 = pt2

    p1 = (x1, y1)
    p2 = (x2, y1)
    p3 = (x2, y2)
    p4 = (x1, y2)

    lines = [[p1, p2], [p2, p3], [p3, p4], [p4, p1]]

    for line in lines:
        cv2.line(frame, *line, GREEN)


def draw_frame_number(frame, frame_number, total_frames, paused):
    status = "Pausado" if paused else "Reproduciendo"

    TEXTS = [f"Frame: {frame_number} / {total_frames}", status]

    draw_text(frame, TEXTS, x=10)


def draw_menu(frame):

    width = frame.shape[1]
    RIGHT_MARGIN = 240

    TEXTS = [
        "Espacio: Pausar / reproducir",
        "<- / ->: Frame anterior / siguiente",
        "Click izq: Etiquetar",
        "Q: Guardar y salir",
        "Esc: Salir sin guardar",
        "Z: Deshacer",
    ]
    draw_text(frame, TEXTS, x=width - RIGHT_MARGIN)


def draw_text(frame, texts, x):

    INITIAL_TOP_MARGIN = 20
    LINE_HEIGHT = 18

    for i, text in enumerate(texts):
        org_x = x
        org_y = INITIAL_TOP_MARGIN + i * LINE_HEIGHT

        cv2.putText(
            img=frame,
            text=text,
            org=(org_x, org_y),
            fontFace=cv2.FONT_HERSHEY_SIMPLEX,
            fontScale=0.4,
            color=GREEN,
            thickness=1,
        )


def add_click_point(event, x, y, flags, param):
    if event == cv2.EVENT_LBUTTONDOWN:
        param.append((x, y))


def read_frame(video, frame_number):
    if frame_number < 1:
        return None

    video.set(cv2.CAP_PROP_POS_FRAMES, frame_number - 1)
    _success, frame = video.read()
    return frame if _success else None


def save_labeled_video(video, frame_box_map):
    width = int(video.get(cv2.CAP_PROP_FRAME_WIDTH))
    height = int(video.get(cv2.CAP_PROP_FRAME_HEIGHT))
    fps = video.get(cv2.CAP_PROP_FPS) or 30

    os.makedirs(os.path.dirname(OUTPUT_PATH), exist_ok=True)

    writer = cv2.VideoWriter(
        OUTPUT_PATH, cv2.VideoWriter_fourcc(*"mp4v"), fps, (width, height)
    )

    # Back to the start, then read in order: faster than jumping to each frame.
    video.set(cv2.CAP_PROP_POS_FRAMES, 0)
    frame_number = 1
    success, frame = video.read()

    while success:
        for box in frame_box_map.get(frame_number, []):
            draw_box(frame, *box)

        writer.write(frame)

        frame_number += 1
        success, frame = video.read()

    writer.release()

    print(f"Saved {OUTPUT_PATH} ({len(frame_box_map)} frames labeled)")


def main():
    print(45 * "=")
    print("1-base.py")
    print(45 * "=")

    video = cv2.VideoCapture("dog.mp4")
    frame_number = 1

    paused = True
    frame_delay = int(1000 / (video.get(cv2.CAP_PROP_FPS) or 30))

    frame = read_frame(video, frame_number)
    total_frames = int(video.get(cv2.CAP_PROP_FRAME_COUNT))

    click_points = []
    frame_box_map = {}

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
        for box in frame_box_map.get(frame_number, []):
            draw_box(preview, *box)

        draw_frame_number(preview, frame_number, total_frames, paused)
        draw_menu(preview)

        # show frame with updates
        cv2.imshow(WINDOW_NAME, preview)

        key = cv2.waitKeyEx(frame_delay)

        if key in PAUSE_KEYS:
            paused = not paused

        step = 0

        if key in PREVIOUS_FRAME_KEYS or key in NEXT_FRAME_KEYS:
            step = 1 if key in NEXT_FRAME_KEYS else -1
            paused = True
        elif not paused:
            step = 1

        if step != 0:
            new_frame = read_frame(video, frame_number + step)

            if new_frame is not None:
                frame = new_frame
                frame_number += step
                click_points.clear()
            else:
                # At the first or last frame there is nowhere to go: stay put.
                paused = True

                step = 0

        if len(click_points) >= 2:
            box = (click_points[0], click_points[1])
            frame_box_map.setdefault(frame_number, []).append(box)
            click_points.clear()

        if key in UNDO_KEYS and frame_box_map.get(frame_number):
            frame_box_map[frame_number].pop()

        if key in QUIT_KEYS or key in DISCARD_KEYS:
            break

    cv2.destroyAllWindows()

    if key in QUIT_KEYS:
        save_labeled_video(video, frame_box_map)
    else:
        print("Exited without saving")

    video.release()


main()
