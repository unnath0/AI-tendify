import cv2
from ultralytics import YOLO
from collections import defaultdict

# Load your trained YOLO model
model = YOLO("runs/detect/train2/weights/best.pt")  # Replace with your model path

# Video input
video_path = "/home/anand/Documents/misc/cctv-footage/A1st 113_20250417114033.avi"  # Replace with your video file
cap = cv2.VideoCapture(video_path)

fps = cap.get(cv2.CAP_PROP_FPS) or 25  # fallback if fps not readable
interval_frames = int(fps * 5)  # update summary every 5 seconds

# Define action weights
action_weights = {
    "Distracted": -1,
    "Paying Attention": 1,
    "Taking Notes": 2,
    "Talking to others": -1,
    "Using Phone": -2,
}

# Custom messages for each dominant action
dominant_messages = {
    "Paying Attention": "✅ Great! Most students are focused and attentive.",
    "Taking Notes": "📝 Students are actively taking notes. Good engagement!",
    "Distracted": "⚠️ Students appear distracted. Consider re-engaging them.",
    "Talking to others": "💬 There is chatter in the classroom. Might be group discussion or distraction.",
    "Using Phone": "📱 Phone usage detected — possible distraction.",
}

# Trackers
total_counts = defaultdict(int)
duration_counts = defaultdict(int)
frame_index = 0

print("--- Starting Inference ---")


last_results = None  # store last inference result

while cap.isOpened():
    ret, frame = cap.read()
    if not ret:
        break

    # Run model every 5 seconds
    if frame_index % interval_frames == 0:
        last_results = model.predict(frame, verbose=False)[0]

        frame_counts = defaultdict(int)
        for box in last_results.boxes:
            cls_id = int(box.cls[0])
            label = model.names[cls_id]
            conf = float(box.conf[0])
            xyxy = box.xyxy[0].cpu().numpy().astype(int)

            frame_counts[label] += 1
            total_counts[label] += 1
            duration_counts[label] += interval_frames  # count frames skipped too

        # Score and summary
        frame_score = sum(
            count * action_weights.get(label, 0)
            for label, count in frame_counts.items()
        )
        print(f"\n--- Summary at {frame_index / fps:.1f}s ---")
        for label in total_counts:
            seconds = duration_counts[label] / fps
            print(
                f"{label}: {total_counts[label]} instances, approx. {seconds:.1f} seconds"
            )

        dominant = max(total_counts.items(), key=lambda x: x[1])[0]
        print(f"🧠 Most frequent action: {dominant}")
        print(dominant_messages.get(dominant, "Student behavior detected."))

    # Always draw boxes from last_results (even between detections)
    if last_results:
        for box in last_results.boxes:
            cls_id = int(box.cls[0])
            label = model.names[cls_id]
            conf = float(box.conf[0])
            xyxy = box.xyxy[0].cpu().numpy().astype(int)

            cv2.rectangle(frame, (xyxy[0], xyxy[1]), (xyxy[2], xyxy[3]), (0, 255, 0), 2)
            cv2.putText(
                frame,
                f"{label} {conf:.2f}",
                (xyxy[0], xyxy[1] - 10),
                cv2.FONT_HERSHEY_SIMPLEX,
                0.5,
                (0, 255, 0),
                2,
            )

    # Show score on every frame (optional: use last frame_score)
    if "frame_score" in locals():
        cv2.putText(
            frame,
            f"Score: {frame_score}",
            (10, 30),
            cv2.FONT_HERSHEY_SIMPLEX,
            1,
            (255, 255, 0),
            2,
        )

    # Show frame and wait based on FPS
    cv2.imshow("Classroom Engagement", frame)
    if cv2.waitKey(int(1000 / fps)) & 0xFF == ord("q"):
        break

    frame_index += 1

# Wrap up
cap.release()
cv2.destroyAllWindows()

print("\n--- Final Engagement Summary ---")
for action in total_counts:
    seconds = duration_counts[action] / fps
    print(f"{action}: {total_counts[action]} times, approx. {seconds:.1f} seconds")

dominant = max(total_counts.items(), key=lambda x: x[1])[0]
print(f"✅ Overall Dominant Behavior: {dominant}")
print(dominant_messages.get(dominant, "Student behavior detected."))
