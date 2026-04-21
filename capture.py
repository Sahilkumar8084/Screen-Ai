import mss
import time
from PIL import Image
import hashlib
import os
import io


# Setting
#-------------------------------------------
CAPTURE_INTERVAL = 5
CAPTURE_THRESHOLD = 0.08
SAVE_SCREENSHOTS = True
SCREENSHOT_DIR = "screenshots"
    
#-----------------------------------

if SAVE_SCREENSHOTS and not os.path.exists(SCREENSHOT_DIR):
    os.makedirs(SCREENSHOT_DIR)
    
# this one will make the DIr of the screenshots tha we will be taking 

def take_screenshots() -> Image.Image:
    with mss.mss() as sct:
        monitor = sct.monitors[1]
        raw = sct.grab(monitor)
        image = Image.frombytes("RGB", raw.size, raw.bgra, "raw", "BGRX")
        return image
    
def image_to_bytes(img: Image.Image, resize_to=(1280,720)) ->bytes:
    img_resized = img.resize(resize_to,Image.LANCZOS)
    img_bytes = io.BytesIO()
    img_resized.save(img_bytes,format="PNG")
    return img_bytes.getvalue()

def get_image_hash(img: Image.Image) -> str:
    small = img.resize((32,32),Image.LANCZOS).convert("L") #changed into he Grayscael image
    return hashlib.md5(small.tobytes()).hexdigest()

def pixel_diff_ratio(img1: Image.Image, img2:Image.Image) ->float:
    size = (64,36)
    a = img1.resize(size,Image.LANCZOS).convert("L")
    b = img2.resize(size,Image.LANCZOS).convert("L")
    
    pixel_a = list(a.getdata())
    pixel_b = list(b.getdata())
    
    total = len(pixel_a )
    changed = sum(1 for x,y in zip(pixel_a,pixel_b) if abs(x-y) >15)
    return changed/total



class ScreenCapture:
    
    def __init__(self):
        
        self.last_screenshot :Image.Image | None=None
        self.last_hash:str=""
        self.frame_count : int =0
        self.processed_count :int =0
        
    def should_process(self, current:Image.Image)->bool:
        # this is changed version lets cehck now
        current_hash = get_image_hash(current)
        if self.last_screenshot is None:
            self.last_hash = current_hash
            return True
        
        current_hash = get_image_hash(current)
        
        if current_hash == self.last_hash:
            return False
        
        diff = pixel_diff_ratio(self.last_screenshot,current)
        if diff >= CAPTURE_THRESHOLD:
            self.last_hash = current_hash
            return True
        
        return False
    
    def capture_loop(self, on_new_frame):
        
        
        print("📸 Screen capture shuru ho gayi!")
        print(f"   Interval  : {CAPTURE_INTERVAL} seconds")
        print(f"   Threshold : {CAPTURE_THRESHOLD * 100:.0f}% change needed")
        print("   Ctrl+C dabao band karne ke liye\n")
        
        while True:
            try:
                screenshot = take_screenshots()
                self.frame_count +=1
                
                if self.should_process(screenshot):
                    self.processed_count +=1
                    img_bytes = image_to_bytes(screenshot)
                    
                    if SAVE_SCREENSHOTS:
                        path =f"{SCREENSHOT_DIR}/frame_{self.processed_count:04d}.png"
                        
                        screenshot.save(path)
                        
                    print(f"[Frame {self.frame_count}] ✅ Change detected → processing...")
                    
                    on_new_frame(img_bytes) #on_new_frame ek function parameter hai jo tum pass karte ho. Jab bhi change detect hota hai, tumhara loop us function ko call karta hai aur image_bytes uske argument ke roop mein bhejta hai.
                    
                    self.last_screenshot = screenshot
                    self.last_hash = get_image_hash(screenshot)
                    
                else:
                     print(f"[Frame {self.frame_count}] ⏭️  No significant change, skipping.")
                
                time.sleep(CAPTURE_INTERVAL)
                
            except KeyboardInterrupt:
                print(f"\n🛑 Capture band kar di.")
                print(f"   Total frames  : {self.frame_count}")
                print(f"   Processed     : {self.processed_count}")
                break

# ── Quick test ────────────────────────────────────────────
if __name__ == "__main__":
    def dummy_callback(img_bytes: bytes):
        print(f"   → Image size: {len(img_bytes) / 1024:.1f} KB")
 
    cap = ScreenCapture()
    cap.capture_loop(on_new_frame=dummy_callback)
 

                

        

    
    
    
    

    
    
    