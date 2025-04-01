import cv2
import numpy as np


def compare_frame_to_template(frame, template):
    # Convert images to grayscale
    gray_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    gray_template = cv2.cvtColor(template, cv2.COLOR_BGR2GRAY)

    # Initialize ORB detector
    orb = cv2.ORB_create()

    # Find keypoints and descriptors
    kp1, des1 = orb.detectAndCompute(gray_template, None)
    kp2, des2 = orb.detectAndCompute(gray_frame, None)

    # Use BFMatcher to match features
    bf = cv2.BFMatcher(cv2.NORM_HAMMING, crossCheck=True)
    if des1 is not None and des2 is not None:
        matches = bf.match(des1, des2)
        matches = sorted(matches, key=lambda x: x.distance)

        # Draw matches
        match_img = cv2.drawMatches(template, kp1, frame, kp2, matches[:10], None, flags=2)
        return match_img, len(matches)
    else:
        return frame, 0


# Load template image
template = cv2.imread("template.jpg")
if template is None:
    print("Error: Template image not found!")
    exit()

# Start video capture
cap = cv2.VideoCapture(0)

while True:
    ret, frame = cap.read()
    if not ret:
        break

    # Compare frame to template
    match_img, match_count = compare_frame_to_template(frame, template)

    # Display the result
    cv2.putText(match_img, f"Matches: {match_count}", (10, 50), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)
    cv2.imshow('Template Matching', match_img)

    # Break on 'q' key
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# Cleanup
cap.release()
cv2.destroyAllWindows()