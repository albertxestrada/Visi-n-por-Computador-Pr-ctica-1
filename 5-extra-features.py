"""
Funcionalidades extra (hasta 1 punto adicional):
incorporar mejoras que faciliten el etiquetado, como seleccionar 
regiones de forma no rectangular y extraer únicamente su contenido,
deshacer el último punto seleccionado mediante una tecla, 
modificar regiones o eliminar selecciones.
"""

import os

import cv2

WINDOW_NAME = "DOG WINDOW"
RED = (0, 0, 255)
GREEN = (0, 255, 0)
YELLOW = (0, 255, 255)

PREVIOUS_FRAME_KEYS = (2424832, 65361, 63234)
NEXT_FRAME_KEYS = (2555904, 65363, 63235)
QUIT_KEYS = (ord("q"), ord("Q"))
DISCARD_KEYS = (27,)  # Esc
UNDO_KEYS = (ord("z"), ord("Z"))
PAUSE_KEYS = (ord(" "),)
CANCEL_KEYS = (ord("c"), ord("C"))
OUTPUT_PATH = "./outputs/5-extra-features.mp4"
REGIONS_OUTPUT_DIR = "./outputs/regions-5-extra-features"
CLOSE_DISTANCE_PX = 20


def draw_region(frame, points, closed, color=GREEN):
    for p1, p2 in zip(points, points[1:]):
        cv2.line(frame, p1, p2, color, thickness=2, lineType=cv2.LINE_AA)

    if closed and len(points) > 2:
        cv2.line(frame, points[-1], points[0], color, thickness=2, lineType=cv2.LINE_AA)


def is_close_to_first_point(points, x, y):
    first_x, first_y = points[0]
    # if the distance between two points is less than or equal to 15 pixels, consider it as closing the region
    # distance of two points formula: d = sqrt((x - first_x)^2 + (y - first_y)^2)
    return (x - first_x) ** 2 + (y - first_y) ** 2 <= CLOSE_DISTANCE_PX**2


def get_inherited_regions(frame_region_map, frame_number):
    keyframes = [
        k for k, regions in frame_region_map.items() if regions and k < frame_number
    ]
    return frame_region_map[max(keyframes)] if keyframes else []


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
        "Click izq: Añadir vértice",
        "Click der: Cerrar región",
        "C: Cancelar región actual",
        "Q: Guardar y salir",
        "Esc: Salir sin guardar",
        "Z: Deshacer último vértice",
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


def read_frame(video, frame_number):
    if frame_number < 1:
        return None

    video.set(cv2.CAP_PROP_POS_FRAMES, frame_number - 1)
    _success, frame = video.read()
    return frame if _success else None


def save_labeled_video(video, frame_region_map):
    width = int(video.get(cv2.CAP_PROP_FRAME_WIDTH))
    height = int(video.get(cv2.CAP_PROP_FRAME_HEIGHT))
    fps = video.get(cv2.CAP_PROP_FPS) or 30

    os.makedirs(os.path.dirname(OUTPUT_PATH), exist_ok=True)

    writer = cv2.VideoWriter(
        OUTPUT_PATH, cv2.VideoWriter_fourcc(*"mp4v"), fps, (width, height)
    )

    video.set(cv2.CAP_PROP_POS_FRAMES, 0)
    frame_number = 1
    success, frame = video.read()
    current_regions = []

    while success:

        if frame_region_map.get(frame_number):
            current_regions = frame_region_map[frame_number]

        for region in current_regions:
            draw_region(frame, region, closed=True)

        writer.write(frame)

        frame_number += 1
        success, frame = video.read()

    writer.release()

    print(f"Saved {OUTPUT_PATH} ({len(frame_region_map)} frames labeled)")

## Region: EXTRACT REGION FUNCTIONS
def compute_bounding_box(points):
    xs = [x for x, _ in points]
    ys = [y for _, y in points]

    x_min, x_max = min(xs), max(xs)
    y_min, y_max = min(ys), max(ys)

    return x_min, y_min, x_max - x_min, y_max - y_min


def is_point_inside_region(x, y, points):
    # Review if the point is inside the region
    intersection = 0
    n = len(points)

    for i in range(n):
        x1, y1 = points[i]
        x2, y2 = points[(i + 1) % n]

    # we can not be sure y1 is grather than y2, so the important here is that the y
    # coordinate of the point should be between y1 and y2 to consider intersection
        if (y1 > y) != (y2 > y):
            # m = (y2−y1) / (x2−x1)
            m = (x2 - x1) / (y2 - y1)
            # x2 = x1 + (y2−y1) * m then to calculate received x with that gradient
            # x = x1 + (y - y1) * m
            x_intersect = x1 + (y - y1) * m
            if x < x_intersect:
                intersection += 1

    # the num of intersections should be odd for the point to be inside the region
    return intersection % 2 != 0


def extract_region(frame, points):
    x_min, y_min, width, heigh = compute_bounding_box(points)
    crop = frame[y_min : y_min + heigh, x_min : x_min + width].copy()

    for row in range(heigh):
        for col in range(width):
            if not is_point_inside_region(x_min + col, y_min + row, points):
                crop[row, col] = 0

    return crop

## End Region


def create_region_writer(path, fps, region_points):
    _x, _y, width, height = compute_bounding_box(region_points)
    return cv2.VideoWriter(path, cv2.VideoWriter_fourcc(*"mp4v"), fps, (width, height))


def save_region_videos(video, frame_region_map):
    fps = video.get(cv2.CAP_PROP_FPS) or 30
    total_frames = int(video.get(cv2.CAP_PROP_FRAME_COUNT))

    # a keyframe is a frame where the user defined new regions;
    # those regions stay active until the next keyframe appears
    keyframes = sorted(frame for frame, regions in frame_region_map.items() if regions)

    if not keyframes:
        print("No regions to extract.")
        return

    os.makedirs(REGIONS_OUTPUT_DIR, exist_ok=True)
    saved_videos = 0

    for index, start_frame in enumerate(keyframes):
        is_last_keyframe = index == len(keyframes) - 1
        end_frame = total_frames if is_last_keyframe else keyframes[index + 1]

        regions = frame_region_map[start_frame]

        # one output video per region of this keyframe
        writers = []
        for region_index, region_points in enumerate(regions):
            path = f"{REGIONS_OUTPUT_DIR}/frame_{start_frame}_region_{region_index + 1}.mp4"
            writers.append(create_region_writer(path, fps, region_points))

        video.set(cv2.CAP_PROP_POS_FRAMES, start_frame - 1)

        for _ in range(start_frame, end_frame):
            success, frame = video.read()

            if not success:
                break

            for region_points, writer in zip(regions, writers):
                cropped_frame = extract_region(frame, region_points)
                writer.write(cropped_frame)

        for writer in writers:
            writer.release()

        saved_videos += len(writers)

    print(f"Saved {saved_videos} region video(s) in {REGIONS_OUTPUT_DIR}")


def main():
    print(45 * "=")
    print("5-extra-features.py")
    print(45 * "=")

    video = cv2.VideoCapture("dog.mp4")
    frame_number = 1

    paused = True
    frame_delay = int(1000 / (video.get(cv2.CAP_PROP_FPS) or 30))

    frame = read_frame(video, frame_number)
    total_frames = int(video.get(cv2.CAP_PROP_FRAME_COUNT))

    current_points = []
    frame_region_map = {}

    def finish_current_region():
        if len(current_points) < 3:
            return

        frame_region_map.setdefault(frame_number, []).append(current_points.copy())
        current_points.clear()

    def undo_last_point():
        if current_points:
            current_points.pop()
            return

        own_regions = frame_region_map.get(frame_number)

        if own_regions:
            current_points.extend(own_regions.pop())
            current_points.pop()

    def on_mouse(event, x, y, flags, param):
        if not paused:
            return
        if event == cv2.EVENT_RBUTTONUP:
            finish_current_region()
        elif event == cv2.EVENT_LBUTTONUP:
            if len(current_points) >= 3 and is_close_to_first_point(
                current_points, x, y
            ):
                finish_current_region()
            else:
                current_points.append((x, y))

    cv2.namedWindow(WINDOW_NAME)
    cv2.setMouseCallback(window_name=WINDOW_NAME, on_mouse=on_mouse)

    while True:
        preview = frame.copy()

        # draw finished regions
        own_regions = frame_region_map.get(frame_number)

        if own_regions:
            for region in own_regions:
                draw_region(preview, region, closed=True)
        else:
            for region in get_inherited_regions(frame_region_map, frame_number):
                draw_region(preview, region, closed=True, color=YELLOW)

        # draw the region currently being drawn
        if current_points:
            draw_region(preview, current_points, closed=False, color=YELLOW)

            for point in current_points:
                cv2.circle(preview, point, 4, RED, -1)

        draw_frame_number(preview, frame_number, total_frames, paused)
        draw_menu(preview)

        # show frame with updates
        cv2.imshow(WINDOW_NAME, preview)

        key = cv2.waitKeyEx(frame_delay)

        if key in PAUSE_KEYS:
            paused = not paused

        if key in CANCEL_KEYS:
            current_points.clear()

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
                current_points.clear()
            else:
                # At the first or last frame there is nowhere to go: stay put.
                paused = True

                step = 0

        if key in UNDO_KEYS:
            undo_last_point()

        if key in QUIT_KEYS or key in DISCARD_KEYS:
            break

    cv2.destroyAllWindows()

    if key in QUIT_KEYS:
        save_labeled_video(video, frame_region_map)
        save_region_videos(video, frame_region_map)
    else:
        print("Exited without saving")

    video.release()


main()
