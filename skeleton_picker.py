from pathlib import Path
import streamlit as st
from streamlit_image_coordinates import streamlit_image_coordinates
from PIL import Image, ImageDraw

ASSETS = Path(__file__).parent / "assets"

IMAGE_WIDTH = 200
DOT_RADIUS = 3


def identify_body_region(relative_x, relative_y, view):
    if view == "Front":
        side = "Right" if relative_x < 0.5 else "Left"
    else:
        side = "Left" if relative_x < 0.5 else "Right"

    if 0.42 <= relative_x <= 0.58 and 0.03 <= relative_y <= 0.15:
        return "Head"

    if 0.46 <= relative_x <= 0.54 and 0.15 < relative_y < 0.19:
        return "Neck"

    # Shoulders
    if 0.19 <= relative_y <= 0.24:
        if 0.31 <= relative_x <= 0.38 or 0.62 <= relative_x <= 0.69:
            return f"{side} shoulder"

    # Upper arms
    if 0.24 < relative_y < 0.335:
        if 0.28 <= relative_x <= 0.37 or 0.63 <= relative_x <= 0.72:
            return f"{side} upper arm"

    # Elbows
    if 0.335 <= relative_y <= 0.375:
        if 0.27 <= relative_x <= 0.34 or 0.66 <= relative_x <= 0.73:
            return f"{side} elbow"

    if 0.37 <= relative_x <= 0.63 and 0.19 <= relative_y <= 0.36:
        return "Chest" if view == "Front" else "Upper back"

    if 0.40 <= relative_x <= 0.60 and 0.36 < relative_y < 0.41:
        return "Abdomen" if view == "Front" else "Lower back"

    if 0.35 <= relative_x <= 0.65 and 0.41 <= relative_y <= 0.51:
        if relative_x < 0.44 or relative_x > 0.56:
            return f"{side} hip"
        return "Abdomen" if view == "Front" else "Lower back"

    # Thighs
    if 0.51 < relative_y < 0.65:
        if 0.35 <= relative_x <= 0.46 or 0.54 <= relative_x <= 0.65:
            return f"{side} thigh"

    # Knees
    if 0.65 <= relative_y <= 0.70:
        if 0.36 <= relative_x <= 0.46 or 0.54 <= relative_x <= 0.64:
            return f"{side} knee"

    # Lower legs
    if 0.70 < relative_y < 0.89:
        if 0.36 <= relative_x <= 0.46 or 0.54 <= relative_x <= 0.64:
            return f"{side} lower leg"

    # Feet, including ankles
    if 0.89 <= relative_y <= 0.97:
        if 0.34 <= relative_x <= 0.46 or 0.54 <= relative_x <= 0.66:
            return f"{side} foot"

    return None


def pick_injury_location():
    if "skeleton_location" not in st.session_state:
        st.session_state["skeleton_location"] = None

    if "skeleton_last_click" not in st.session_state:
        st.session_state["skeleton_last_click"] = 0

    view = st.radio(
        "Choose a view:",
        ["Front", "Back"],
        horizontal=True,
        key="skeleton_view",
    )

    image_path = ASSETS / f"skeleton_{view.lower()}.png"

    with Image.open(image_path) as original:
        image = original.convert("RGB")

    image_height = round(image.height * IMAGE_WIDTH / image.width)
    image = image.resize((IMAGE_WIDTH, image_height))

    saved_location = st.session_state["skeleton_location"]

    if saved_location is not None and saved_location["view"] == view:
        x = saved_location["x"]
        y = saved_location["y"]

        draw = ImageDraw.Draw(image)
        draw.ellipse(
            (
                x - DOT_RADIUS,
                y - DOT_RADIUS,
                x + DOT_RADIUS,
                y + DOT_RADIUS,
            ),
            fill="red",
            outline="black",
        )

    clicked = streamlit_image_coordinates(
        image,
        width=IMAGE_WIDTH,
        key=f"skeleton_{view}",
    )

    if clicked:
        if clicked["unix_time"] > st.session_state["skeleton_last_click"]:
            st.session_state["skeleton_last_click"] = clicked["unix_time"]

            relative_x = clicked["x"] / image.width
            relative_y = clicked["y"] / image.height

            region = identify_body_region(relative_x, relative_y, view)

            st.session_state["skeleton_location"] = {
                "view": view,
                "x": clicked["x"],
                "y": clicked["y"],
                "relative_x": relative_x,
                "relative_y": relative_y,
                "region": region,
            }

            st.rerun()

    return st.session_state["skeleton_location"]