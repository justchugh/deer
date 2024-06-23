# distance_measurement.py

DEFAULT_KNOWN_WIDTH = 16.0  # Real-world width of the object (cm)
DEFAULT_KNOWN_DISTANCE = 65  # Known distance from camera to your face in centimeters
DEFAULT_KNOWN_PIXEL_WIDTH = 200  # Measured width of your face in pixels at that distance

#DEFAULT_FOCAL_LENGTH = 300  # Focal length of the camera (same units as width)
DEFAULT_FOCAL_LENGTH = (DEFAULT_KNOWN_PIXEL_WIDTH * DEFAULT_KNOWN_DISTANCE) / DEFAULT_KNOWN_WIDTH


def distance_to_camera(perWidth, knownWidth=DEFAULT_KNOWN_WIDTH, focalLength=DEFAULT_FOCAL_LENGTH):
    if perWidth > 0:
        distance = (knownWidth * focalLength) / perWidth
        print(f"Distance from the camera: {distance:.2f} cm")
        return distance
    else:
        print("Invalid perceived width provided.")
        return 0

distance_to_camera(16)