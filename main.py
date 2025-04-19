import os
import uuid
import time

# Generate a random device ID
device_id = "Prial-device-" + str(uuid.uuid4())[:8]

# Create the approve file if not exists
approve_file = "approve.txt"

# Create the file with some approved IDs if it doesn't exist
if not os.path.exists(approve_file):
    with open(approve_file, "w") as f:
        f.write("# Add approved device IDs below:\n")

# Read approved device IDs
with open(approve_file, "r") as f:
    approved_ids = [line.strip() for line in f if not line.startswith("#")]

if device_id not in approved_ids:
    print(f"\nYour device ID: {device_id}")
    print("This device is not approved!")
    print("Please send the device ID above to the admin for approval.")
    print("After approval, add it manually in approve.txt file.")
    input("\nPress ENTER to exit...")
    exit()

# If approved, run your main tool
print("✅ Device approved. Running the tool...")
