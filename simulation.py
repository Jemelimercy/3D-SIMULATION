import pygame
import mediapipe as mp
import cv2
import numpy as np
import math

# --- 1. SETTINGS ---
WIDTH, HEIGHT = 800, 600
FPS = 60

pygame.init()
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Inverted 3D Cube: Far = Big, Close = Small")
clock = pygame.time.Clock()

# MediaPipe Setup
mp_hands = mp.solutions.hands
mp_draw = mp.solutions.drawing_utils
hands = mp_hands.Hands(max_num_hands=1, min_detection_confidence=0.7)
cap = cv2.VideoCapture(0)

# --- 2. 3D GEOMETRY ---
base_nodes = np.array([
    [-1, -1, -1], [1, -1, -1], [1, 1, -1], [-1, 1, -1],
    [-1, -1, 1], [1, -1, 1], [1, 1, 1], [-1, 1, 1]
])

faces = [(0,1,2,3), (4,5,6,7), (0,1,5,4), (2,3,7,6), (0,3,7,4), (1,2,6,5)]
edges = [(0,1), (1,2), (2,3), (3,0), (4,5), (5,6), (6,7), (7,4), (0,4), (1,5), (2,6), (3,7)]

# Red, Pink, Yellow, Blue, Green, Orange
face_colors = [(255,0,0), (255,20,147), (255,255,0), (0,0,255), (0,255,0), (255,165,0)]

wireframe_mode = False
current_scale = 100

def rotate_and_project(nodes, pitch, roll, scale):
    projected_points = []
    rotated_nodes = []
    focal_length = 500 
    scaled_nodes = nodes * scale
    
    for x, y, z in scaled_nodes:
        # Rotation
        ny = y * math.cos(pitch) - z * math.sin(pitch)
        nz = y * math.sin(pitch) + z * math.cos(pitch)
        y, z = ny, nz
        nx = x * math.cos(roll) - y * math.sin(roll)
        ny = x * math.sin(roll) + y * math.cos(roll)
        x, y = nx, ny
        rotated_nodes.append((x, y, z))
        
        # Perspective
        z_offset = 400 
        factor = focal_length / (z + z_offset)
        px = x * factor + WIDTH // 2
        py = y * factor + HEIGHT // 2
        projected_points.append((px, py))
    return projected_points, rotated_nodes

# --- 3. MAIN LOOP ---
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT: running = False
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_w:
                wireframe_mode = not wireframe_mode

    success, frame = cap.read()
    if not success: break
    frame = cv2.flip(frame, 1)
    results = hands.process(cv2.cvtColor(frame, cv2.COLOR_BGR2RGB))

    pitch, roll = 0, 0
    
    if results.multi_hand_landmarks:
        hand = results.multi_hand_landmarks[0]
        mp_draw.draw_landmarks(frame, hand, mp_hands.HAND_CONNECTIONS)
        
        w, m = hand.landmark[0], hand.landmark[9]
        i, p = hand.landmark[5], hand.landmark[17]
        
        pitch = (m.y - w.y) * 2.5
        roll = math.atan2(i.y - p.y, i.x - p.x)
        
        # Distance calculation
        dx = (w.x - m.x) * WIDTH
        dy = (w.y - m.y) * HEIGHT
        hand_dist = math.sqrt(dx**2 + dy**2)
        
        # --- THE INVERSION ---
        # When hand_dist is 220 (Close), scale is 50. 
        # When hand_dist is 60 (Far), scale is 300.
        current_scale = np.interp(hand_dist, [60, 220], [300, 50])

    cv2.imshow("Hand Tracker View", frame)
    screen.fill((5, 5, 10))

    projected_nodes, rotated_nodes = rotate_and_project(base_nodes, pitch, roll, current_scale)

    if wireframe_mode:
        for edge in edges:
            pygame.draw.line(screen, (255, 255, 255), projected_nodes[edge[0]], projected_nodes[edge[1]], 2)
    else:
        face_depths = []
        for i, face in enumerate(faces):
            avg_z = sum(rotated_nodes[j][2] for j in face) / 4
            face_depths.append((i, avg_z))
        face_depths.sort(key=lambda x: x[1], reverse=True)

        for i, depth in face_depths:
            face_points = [projected_nodes[j] for j in faces[i]]
            # Adjusted shading for the inverted effect
            brightness = max(0.4, min(1.0, 1 - (depth / (current_scale + 200))))
            shaded_color = tuple(int(c * brightness) for c in face_colors[i])
            pygame.draw.polygon(screen, shaded_color, face_points)
            pygame.draw.polygon(screen, (0, 0, 0), face_points, 2)

    pygame.display.flip()
    if cv2.waitKey(1) & 0xFF == ord('q'): running = False
    clock.tick(FPS)

cap.release()
cv2.destroyAllWindows()
pygame.quit()