import cv2
import numpy as np
import sys
import time
import winsound
#egemenKuzu95
# --- SİSTEM DOĞRULAMA ---
try:
    import mediapipe as mp
    mp_pose = mp.solutions.pose
    mp_drawing = mp.solutions.drawing_utils
except Exception as e:
    print(f"Kritik Hata: {e}")
    sys.exit()

# --- ANALİTİK SAYAÇLARIM ---
# Kullanıcının performansını ölçmek için bu sayaçları başlattım.
session_start_time = time.time()
slouch_total_seconds = 0  # Toplam kambur kalınan saniye
last_frame_time = time.time()

# --- HASSASİYET AYARLARIM ---
# Senin belirlediğin altın oranları korudum.
BODY_ANGLE_THRESHOLD = 142    
NECK_DROP_THRESHOLD = 0.11    
SHOULDER_ROUND_LIMIT = 0.06   

# --- ZAMANLAMA AYARLARI ---
last_beep_time = 0
beep_interval = 4             
slouch_start_time = None      
SABIR_SURESI = 2              

window_name = 'AI Senior Posture Master v20'
cv2.namedWindow(window_name, cv2.WINDOW_NORMAL)

pose = mp_pose.Pose(static_image_mode=False, model_complexity=1, min_detection_confidence=0.7)
cap = cv2.VideoCapture(0)

def get_angle(a, b, c):
    a, b, c = np.array(a), np.array(b), np.array(c)
    rad = np.arctan2(c[1]-b[1], c[0]-b[0]) - np.arctan2(a[1]-b[1], a[0]-b[0])
    angle = np.abs(rad*180.0/np.pi)
    return 360-angle if angle > 180 else angle

print("🚀 Sistem Hazır. Hassasiyet optimize edildi.")

try:
    while cap.isOpened():
        ret, frame = cap.read()
        if not ret: break

        # FPS ve zaman hesaplama mantığım:
        current_frame_time = time.time()
        dt = current_frame_time - last_frame_time
        last_frame_time = current_frame_time

        frame = cv2.flip(frame, 1)
        h, w, _ = frame.shape
        rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        results = pose.process(rgb_frame)
        
        status_color = (80, 255, 80)
        warning_text = "DURUS: OPTIMAL"

        if results.pose_landmarks:
            lm = results.pose_landmarks.landmark
            
            # Analiz Değerleri
            shoulder_rounding = lm[11].x - lm[7].x 
            neck_drop = lm[11].y - lm[7].y
            p_ear = [lm[7].x * w, lm[7].y * h]; p_sh = [lm[11].x * w, lm[11].y * h]; p_hip = [lm[23].x * w, lm[23].y * h]
            body_angle = get_angle(p_ear, p_sh, p_hip)

            # --- KARAR MOTORUM ---
            if body_angle < BODY_ANGLE_THRESHOLD or neck_drop < NECK_DROP_THRESHOLD or shoulder_rounding < SHOULDER_ROUND_LIMIT:
                if slouch_start_time is None:
                    slouch_start_time = time.time()
                
                gecen_sure = time.time() - slouch_start_time
                
                if gecen_sure > SABIR_SURESI:
                    status_color = (0, 0, 255)
                    warning_text = "DIK DUR! POSTUR BOZULDU"
                    
                    # Kambur kalınan süreyi burada biriktiriyorum.
                    slouch_total_seconds += dt
                    
                    current_time = time.time()
                    if current_time - last_beep_time > beep_interval:
                        winsound.Beep(900, 250)
                        last_beep_time = current_time
                else:
                    status_color = (0, 255, 255)
                    warning_text = "DIKKAT: EGILIYORSUN"
            else:
                slouch_start_time = None

            # --- HUD ARAYÜZÜM ---
            overlay = frame.copy()
            cv2.rectangle(overlay, (0, 0), (w, 100), (20, 20, 20), -1)
            cv2.addWeighted(overlay, 0.7, frame, 0.3, 0, frame)
            
            # Türkçe karakter sorununu 'Govde' yazarak çözdüm. 
            # Ayrıca yanına 'Canlı Sayaç' ekledim ki kullanıcı gelişimini görsün.
            cv2.putText(frame, f"Govde: {int(body_angle)}", (20, 35), 1, 1, (255, 255, 255), 1)
            cv2.putText(frame, f"Boyun: {round(neck_drop, 3)}", (20, 60), 1, 1, (255, 255, 255), 1)
            cv2.putText(frame, f"Omuz: {round(shoulder_rounding, 3)}", (20, 85), 1, 1, (255, 255, 255), 1)
            
            # Seans bilgisi paneli
            cv2.putText(frame, f"Kambur Suresi: {int(slouch_total_seconds)}s", (w-250, 90), 1, 0.9, (150, 150, 255), 1)

            t_size = cv2.getTextSize(warning_text, cv2.FONT_HERSHEY_SIMPLEX, 0.8, 2)[0]
            cv2.putText(frame, warning_text, (w - t_size[0] - 20, 50), cv2.FONT_HERSHEY_SIMPLEX, 0.8, status_color, 2)

            mp_drawing.draw_landmarks(frame, results.pose_landmarks, mp_pose.POSE_CONNECTIONS,
                                    mp_drawing.DrawingSpec(color=status_color, thickness=3, circle_radius=2))

        cv2.imshow(window_name, frame)
        
        key = cv2.waitKey(1) & 0xFF
        if key == ord('q') or cv2.getWindowProperty(window_name, cv2.WND_PROP_VISIBLE) < 1:
            break

finally:
    # --- FİNAL RAPORLAMAM ---
    # Program kapanırken kullanıcıya bir 'Sağlık Karnesi' çıkartıyorum.
    session_duration = time.time() - session_start_time
    # Sağlık puanı: Dik durulan sürenin toplam süreye oranı.
    health_score = max(0, 100 - int((slouch_total_seconds / max(1, session_duration)) * 100))
    
    print("\n" + "="*40)
    print("📊 SEANS SAGLIK RAPORU")
    print(f"Toplam Calisma: {int(session_duration)} saniye")
    print(f"Kambur Kalinan: {int(slouch_total_seconds)} saniye")
    print(f"POSTUR PUANI: %{health_score}")
    print("="*40)

    cap.release()
    cv2.destroyAllWindows()
    sys.exit()