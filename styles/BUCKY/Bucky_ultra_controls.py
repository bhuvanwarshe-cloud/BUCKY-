# import pyautogui
# import keyboard
# import time
# import pyperclip
# import requests
# import json
# from datetime import datetime
# from typing import Optional, Literal, List
# from livekit.agents import function_tool
# import win32clipboard
# from PIL import ImageGrab
# import io
# import base64
# import subprocess
# import threading

# # ===============================
# # 🔒 SECURITY CONFIGURATION
# # ===============================
# class SecurityManager:
#     """Manages security and authorization for keyboard/mouse control."""
    
#     def __init__(self):
#         self.control_enabled = False
#         self.session_password = None
#         self.auto_disable_timer = None
#         self.auto_disable_duration = 300  # 5 minutes default
        
#     def enable_control(self, password: Optional[str] = None) -> bool:
#         """Enable keyboard and mouse control."""
#         if password and self.session_password:
#             if password != self.session_password:
#                 print("[SECURITY] Invalid password")
#                 return False
        
#         self.control_enabled = True
#         print("[SECURITY] ✅ Control ENABLED")
        
#         # Start auto-disable timer
#         self._start_auto_disable_timer()
#         return True
    
#     def disable_control(self):
#         """Disable keyboard and mouse control."""
#         self.control_enabled = False
#         print("[SECURITY] 🔒 Control DISABLED")
        
#         # Cancel auto-disable timer
#         if self.auto_disable_timer:
#             self.auto_disable_timer.cancel()
    
#     def is_enabled(self) -> bool:
#         """Check if control is enabled."""
#         return self.control_enabled
    
#     def set_password(self, password: str):
#         """Set a session password for added security."""
#         self.session_password = password
#         print("[SECURITY] Password has been set")
    
#     def _start_auto_disable_timer(self):
#         """Start timer to auto-disable control after inactivity."""
#         if self.auto_disable_timer:
#             self.auto_disable_timer.cancel()
        
#         self.auto_disable_timer = threading.Timer(
#             self.auto_disable_duration,
#             self._auto_disable_callback
#         )
#         self.auto_disable_timer.daemon = True
#         self.auto_disable_timer.start()
    
#     def _auto_disable_callback(self):
#         """Callback for auto-disable timer."""
#         self.disable_control()
#         print("[SECURITY] ⏰ Auto-disabled due to inactivity")
    
#     def extend_session(self):
#         """Extend the current session by resetting the timer."""
#         if self.control_enabled:
#             self._start_auto_disable_timer()
#             print("[SECURITY] 🔄 Session extended")

# # Global security manager instance
# security = SecurityManager()

# # ===============================
# # 🛡️ SECURITY DECORATOR
# # ===============================
# def require_authorization(func):
#     """Decorator to check authorization before executing control functions."""
#     async def wrapper(*args, **kwargs):
#         if not security.is_enabled():
#             print(f"[SECURITY] ⛔ Blocked: {func.__name__} - Control is disabled")
#             return "Sir, keyboard and mouse control is currently disabled. Please say 'Bucky enable control' first."
        
#         # Extend session on each successful action
#         security.extend_session()
#         return await func(*args, **kwargs)
#     return wrapper


# # ===============================
# # ⚙️ CONFIGURATION
# # ===============================
# pyautogui.FAILSAFE = False
# pyautogui.PAUSE = 0.1

# CURSOR_MOVE_SMALL = 50
# CURSOR_MOVE_MEDIUM = 200
# CURSOR_MOVE_LARGE = 500

# SCROLL_AMOUNT_SMALL = 3
# SCROLL_AMOUNT_MEDIUM = 5
# SCROLL_AMOUNT_LARGE = 10


# # ===============================
# # 🎹 KEYBOARD CONTROL FUNCTIONS
# # ===============================
# @require_authorization
# async def press_single_key(key_name: str) -> str:
#     """Press a single key."""
#     try:
#         print(f"[KEYBOARD] Pressing key: {key_name}")
#         keyboard.press_and_release(key_name)
#         return f"Sir, pressed {key_name} key."
#     except Exception as e:
#         print(f"[ERROR] Failed to press key {key_name}: {e}")
#         return f"Sir, I couldn't press the {key_name} key. Please check the key name."


# @require_authorization
# async def press_key_combination(keys: str) -> str:
#     """Press a combination of keys."""
#     try:
#         print(f"[KEYBOARD] Pressing key combination: {keys}")
#         keyboard.press_and_release(keys)
#         return f"Sir, pressed {keys} combination."
#     except Exception as e:
#         print(f"[ERROR] Failed to press combination {keys}: {e}")
#         return f"Sir, I couldn't press the {keys} combination."


# @require_authorization
# async def type_text(text: str) -> str:
#     """Type text using keyboard."""
#     try:
#         print(f"[KEYBOARD] Typing text: {text}")
#         keyboard.write(text)
#         return f"Sir, typed the text."
#     except Exception as e:
#         print(f"[ERROR] Failed to type text: {e}")
#         return f"Sir, I couldn't type the text."


# @require_authorization
# async def hold_key(key_name: str, duration: float = 1.0) -> str:
#     """Hold a key for specified duration."""
#     try:
#         print(f"[KEYBOARD] Holding key {key_name} for {duration} seconds")
#         keyboard.press(key_name)
#         time.sleep(duration)
#         keyboard.release(key_name)
#         return f"Sir, held {key_name} key for {duration} seconds."
#     except Exception as e:
#         print(f"[ERROR] Failed to hold key {key_name}: {e}")
#         return f"Sir, I couldn't hold the {key_name} key."


# # ===============================
# # 🖱️ MOUSE CONTROL FUNCTIONS
# # ===============================
# @require_authorization
# async def move_cursor(direction: str, distance: str = "medium") -> str:
#     """Move cursor in specified direction."""
#     try:
#         move_dist = {
#             "small": CURSOR_MOVE_SMALL,
#             "medium": CURSOR_MOVE_MEDIUM,
#             "large": CURSOR_MOVE_LARGE
#         }.get(distance.lower(), CURSOR_MOVE_MEDIUM)

#         current_x, current_y = pyautogui.position()
#         print(f"[MOUSE] Moving cursor {direction} by {move_dist} pixels")

#         direction = direction.lower()
#         if direction in ["left", "l"]:
#             pyautogui.moveTo(current_x - move_dist, current_y, duration=0.2)
#         elif direction in ["right", "r"]:
#             pyautogui.moveTo(current_x + move_dist, current_y, duration=0.2)
#         elif direction in ["up", "u"]:
#             pyautogui.moveTo(current_x, current_y - move_dist, duration=0.2)
#         elif direction in ["down", "d"]:
#             pyautogui.moveTo(current_x, current_y + move_dist, duration=0.2)
#         else:
#             return f"Sir, I don't recognize the direction '{direction}'."

#         return f"Sir, moved cursor {direction}."
#     except Exception as e:
#         print(f"[ERROR] Failed to move cursor: {e}")
#         return f"Sir, I couldn't move the cursor."


# @require_authorization
# async def move_cursor_to_position(x: int, y: int) -> str:
#     """Move cursor to specific coordinates."""
#     try:
#         print(f"[MOUSE] Moving cursor to position ({x}, {y})")
#         pyautogui.moveTo(x, y, duration=0.3)
#         return f"Sir, moved cursor to position ({x}, {y})."
#     except Exception as e:
#         print(f"[ERROR] Failed to move cursor to position: {e}")
#         return f"Sir, I couldn't move the cursor to that position."


# @require_authorization
# async def click_mouse(button: str = "left", clicks: int = 1) -> str:
#     """Click mouse button at current position."""
#     try:
#         button = button.lower()
#         print(f"[MOUSE] {button.capitalize()} clicking {clicks} time(s)")
        
#         if button == "left":
#             pyautogui.click(clicks=clicks)
#         elif button == "right":
#             pyautogui.rightClick()
#         elif button == "middle":
#             pyautogui.middleClick()
#         else:
#             return f"Sir, I don't recognize the mouse button '{button}'."

#         click_type = "double-clicked" if clicks == 2 else "clicked"
#         return f"Sir, {click_type} the {button} mouse button."
#     except Exception as e:
#         print(f"[ERROR] Failed to click mouse: {e}")
#         return f"Sir, I couldn't click the mouse."


# @require_authorization
# async def scroll_action(direction: str, amount: str = "medium") -> str:
#     """Scroll up or down."""
#     try:
#         scroll_dist = {
#             "small": SCROLL_AMOUNT_SMALL,
#             "medium": SCROLL_AMOUNT_MEDIUM,
#             "large": SCROLL_AMOUNT_LARGE
#         }.get(amount.lower(), SCROLL_AMOUNT_MEDIUM)

#         direction = direction.lower()
#         print(f"[MOUSE] Scrolling {direction} by {scroll_dist} units")

#         if direction in ["up", "u"]:
#             pyautogui.scroll(scroll_dist * 100)
#         elif direction in ["down", "d"]:
#             pyautogui.scroll(-scroll_dist * 100)
#         else:
#             return f"Sir, I don't recognize the scroll direction '{direction}'."

#         return f"Sir, scrolled {direction}."
#     except Exception as e:
#         print(f"[ERROR] Failed to scroll: {e}")
#         return f"Sir, I couldn't scroll."


# @require_authorization
# async def drag_mouse(direction: str, distance: int = 200) -> str:
#     """Drag mouse in specified direction."""
#     try:
#         print(f"[MOUSE] Dragging {direction} by {distance} pixels")

#         direction = direction.lower()
#         if direction == "left":
#             pyautogui.drag(-distance, 0, duration=0.5)
#         elif direction == "right":
#             pyautogui.drag(distance, 0, duration=0.5)
#         elif direction == "up":
#             pyautogui.drag(0, -distance, duration=0.5)
#         elif direction == "down":
#             pyautogui.drag(0, distance, duration=0.5)
#         else:
#             return f"Sir, I don't recognize the drag direction '{direction}'."

#         return f"Sir, dragged mouse {direction}."
#     except Exception as e:
#         print(f"[ERROR] Failed to drag mouse: {e}")
#         return f"Sir, I couldn't drag the mouse."


# # ===============================
# # 🖐️ WINDOWS GESTURES & SHORTCUTS
# # ===============================
# @require_authorization
# async def windows_gesture(gesture_name: str) -> str:
#     """Execute Windows gestures and shortcuts."""
#     try:
#         gesture_name = gesture_name.lower().strip()
#         print(f"[GESTURE] Executing: {gesture_name}")

#         gestures = {
#             "task view": "win+tab",
#             "show desktop": "win+d",
#             "new virtual desktop": "win+ctrl+d",
#             "close virtual desktop": "win+ctrl+f4",
#             "switch virtual desktop left": "win+ctrl+left",
#             "switch virtual desktop right": "win+ctrl+right",
#             "minimize window": "win+down",
#             "maximize window": "win+up",
#             "snap left": "win+left",
#             "snap right": "win+right",
#             "minimize all": "win+m",
#             "close window": "alt+f4",
#             "switch window": "alt+tab",
#             "switch window reverse": "alt+shift+tab",
#             "swipe up": "win+tab",
#             "swipe down": "win+d",
#             "swipe left": "alt+left",
#             "swipe right": "alt+right",
#             "action center": "win+a",
#             "notification center": "win+n",
#             "settings": "win+i",
#             "screenshot": "win+shift+s",
#             "screen snip": "win+shift+s",
#             "lock screen": "win+l",
#             "emoji": "win+.",
#             "open explorer": "win+e",
#             "search": "win+s",
#             "project display": "win+p",
#             "brightness up": "fn+f6",
#             "brightness down": "fn+f5",
#             "volume up": "volumeup",
#             "volume down": "volumedown",
#             "mute": "volumemute",
#             "play pause": "playpause",
#             "next track": "nexttrack",
#             "previous track": "prevtrack",
#             "copy": "ctrl+c",
#             "paste": "ctrl+v",
#             "cut": "ctrl+x",
#             "undo": "ctrl+z",
#             "redo": "ctrl+y",
#             "select all": "ctrl+a",
#             "find": "ctrl+f",
#             "save": "ctrl+s",
#             "print": "ctrl+p",
#             "new tab": "ctrl+t",
#             "close tab": "ctrl+w",
#             "reopen tab": "ctrl+shift+t",
#             "refresh": "f5",
#             "hard refresh": "ctrl+f5",
#             "full screen": "f11",
#             "zoom in": "ctrl+plus",
#             "zoom out": "ctrl+minus",
#             "zoom reset": "ctrl+0",
#             "task manager": "ctrl+shift+esc",
#             "run dialog": "win+r",
#         }

#         shortcut = gestures.get(gesture_name)
#         if shortcut:
#             keyboard.press_and_release(shortcut)
#             return f"Sir, executed {gesture_name} gesture."
#         else:
#             return f"Sir, I don't recognize the gesture '{gesture_name}'."

#     except Exception as e:
#         print(f"[ERROR] Failed to execute gesture: {e}")
#         return f"Sir, I couldn't execute the {gesture_name} gesture."


# @require_authorization
# async def three_finger_swipe(direction: str) -> str:
#     """Simulate three-finger swipe gestures."""
#     try:
#         direction = direction.lower()
#         print(f"[GESTURE] Three-finger swipe: {direction}")

#         if direction == "up":
#             keyboard.press_and_release("win+tab")
#             return "Sir, opened Task View (three-finger swipe up)."
#         elif direction == "down":
#             keyboard.press_and_release("win+d")
#             return "Sir, showing desktop (three-finger swipe down)."
#         elif direction == "left":
#             keyboard.press_and_release("alt+tab")
#             return "Sir, switching to previous window (three-finger swipe left)."
#         elif direction == "right":
#             keyboard.press_and_release("alt+shift+tab")
#             return "Sir, switching to next window (three-finger swipe right)."
#         else:
#             return f"Sir, I don't recognize the swipe direction '{direction}'."

#     except Exception as e:
#         print(f"[ERROR] Failed to execute swipe: {e}")
#         return f"Sir, I couldn't execute the three-finger swipe."


# # ===============================
# # 📋 CLIPBOARD OPERATIONS (JARVIS-LIKE)
# # ===============================
# @require_authorization
# async def copy_to_clipboard() -> str:
#     """Copy selected text/content to clipboard."""
#     try:
#         print("[CLIPBOARD] Copying to clipboard")
#         keyboard.press_and_release("ctrl+c")
#         time.sleep(0.2)
#         content = pyperclip.paste()
#         return f"Sir, copied to clipboard: '{content[:50]}...'" if len(content) > 50 else f"Sir, copied to clipboard: '{content}'"
#     except Exception as e:
#         print(f"[ERROR] Failed to copy: {e}")
#         return "Sir, I couldn't copy to clipboard."


# @require_authorization
# async def paste_from_clipboard() -> str:
#     """Paste content from clipboard."""
#     try:
#         print("[CLIPBOARD] Pasting from clipboard")
#         keyboard.press_and_release("ctrl+v")
#         return "Sir, pasted from clipboard."
#     except Exception as e:
#         print(f"[ERROR] Failed to paste: {e}")
#         return "Sir, I couldn't paste from clipboard."


# async def get_clipboard_content() -> str:
#     """Read clipboard content - NO AUTHORIZATION NEEDED."""
#     try:
#         content = pyperclip.paste()
#         print(f"[CLIPBOARD] Current content: {content[:100]}")
#         return f"Sir, clipboard contains: {content}"
#     except Exception as e:
#         print(f"[ERROR] Failed to read clipboard: {e}")
#         return "Sir, I couldn't read the clipboard."


# async def set_clipboard_content(text: str) -> str:
#     """Set clipboard content without pasting - NO AUTHORIZATION NEEDED."""
#     try:
#         pyperclip.copy(text)
#         print(f"[CLIPBOARD] Set content: {text[:100]}")
#         return f"Sir, clipboard has been set to: '{text[:50]}...'" if len(text) > 50 else f"Sir, clipboard set to: '{text}'"
#     except Exception as e:
#         print(f"[ERROR] Failed to set clipboard: {e}")
#         return "Sir, I couldn't set the clipboard."


# # ===============================
# # 📸 SCREENSHOT CAPABILITIES (JARVIS-LIKE)
# # ===============================
# async def take_screenshot(save_path: Optional[str] = None) -> str:
#     """Take a screenshot - NO AUTHORIZATION NEEDED."""
#     try:
#         print("[SCREENSHOT] Capturing screen")
#         screenshot = ImageGrab.grab()
        
#         if save_path:
#             screenshot.save(save_path)
#             return f"Sir, screenshot saved to {save_path}"
#         else:
#             default_path = f"screenshot_{datetime.now().strftime('%Y%m%d_%H%M%S')}.png"
#             screenshot.save(default_path)
#             return f"Sir, screenshot saved as {default_path}"
#     except Exception as e:
#         print(f"[ERROR] Failed to take screenshot: {e}")
#         return "Sir, I couldn't take the screenshot."


# async def take_region_screenshot(x1: int, y1: int, x2: int, y2: int, save_path: Optional[str] = None) -> str:
#     """Take a screenshot of a specific region - NO AUTHORIZATION NEEDED."""
#     try:
#         print(f"[SCREENSHOT] Capturing region ({x1}, {y1}) to ({x2}, {y2})")
#         screenshot = ImageGrab.grab(bbox=(x1, y1, x2, y2))
        
#         if save_path:
#             screenshot.save(save_path)
#             return f"Sir, region screenshot saved to {save_path}"
#         else:
#             default_path = f"screenshot_region_{datetime.now().strftime('%Y%m%d_%H%M%S')}.png"
#             screenshot.save(default_path)
#             return f"Sir, region screenshot saved as {default_path}"
#     except Exception as e:
#         print(f"[ERROR] Failed to take region screenshot: {e}")
#         return "Sir, I couldn't take the region screenshot."


# # ===============================
# # 🔍 SCREEN ANALYSIS (JARVIS-LIKE)
# # ===============================
# async def locate_on_screen(image_path: str) -> str:
#     """Locate an image on screen - NO AUTHORIZATION NEEDED."""
#     try:
#         print(f"[SCREEN] Locating image: {image_path}")
#         location = pyautogui.locateOnScreen(image_path, confidence=0.8)
        
#         if location:
#             center = pyautogui.center(location)
#             return f"Sir, found the image at position ({center.x}, {center.y})"
#         else:
#             return "Sir, I couldn't locate that image on the screen."
#     except Exception as e:
#         print(f"[ERROR] Failed to locate image: {e}")
#         return "Sir, I couldn't search for the image on screen."


# @require_authorization
# async def click_on_image(image_path: str) -> str:
#     """Find and click on an image - REQUIRES AUTHORIZATION."""
#     try:
#         print(f"[SCREEN] Finding and clicking image: {image_path}")
#         location = pyautogui.locateOnScreen(image_path, confidence=0.8)
        
#         if location:
#             center = pyautogui.center(location)
#             pyautogui.click(center)
#             return f"Sir, clicked on the image at position ({center.x}, {center.y})"
#         else:
#             return "Sir, I couldn't locate that image on the screen to click."
#     except Exception as e:
#         print(f"[ERROR] Failed to click on image: {e}")
#         return "Sir, I couldn't click on the image."


# # ===============================
# # 🌐 WEB & URL OPERATIONS (JARVIS-LIKE)
# # ===============================
# async def open_url(url: str) -> str:
#     """Open a URL - NO AUTHORIZATION NEEDED."""
#     try:
#         print(f"[WEB] Opening URL: {url}")
#         import webbrowser
#         webbrowser.open(url)
#         return f"Sir, opening {url} in your browser."
#     except Exception as e:
#         print(f"[ERROR] Failed to open URL: {e}")
#         return f"Sir, I couldn't open {url}."


# async def search_google(query: str) -> str:
#     """Search Google - NO AUTHORIZATION NEEDED."""
#     try:
#         print(f"[WEB] Searching Google for: {query}")
#         import webbrowser
#         search_url = f"https://www.google.com/search?q={query.replace(' ', '+')}"
#         webbrowser.open(search_url)
#         return f"Sir, searching Google for '{query}'."
#     except Exception as e:
#         print(f"[ERROR] Failed to search Google: {e}")
#         return f"Sir, I couldn't search for '{query}'."


# async def search_youtube(query: str) -> str:
#     """Search YouTube - NO AUTHORIZATION NEEDED."""
#     try:
#         print(f"[WEB] Searching YouTube for: {query}")
#         import webbrowser
#         search_url = f"https://www.youtube.com/results?search_query={query.replace(' ', '+')}"
#         webbrowser.open(search_url)
#         return f"Sir, searching YouTube for '{query}'."
#     except Exception as e:
#         print(f"[ERROR] Failed to search YouTube: {e}")
#         return f"Sir, I couldn't search YouTube for '{query}'."


# # ===============================
# # 🕐 TIME & SYSTEM INFO (JARVIS-LIKE)
# # ===============================
# async def get_current_time() -> str:
#     """Get current time - NO AUTHORIZATION NEEDED."""
#     try:
#         current_time = datetime.now().strftime("%I:%M %p")
#         print(f"[TIME] Current time: {current_time}")
#         return f"Sir, the current time is {current_time}."
#     except Exception as e:
#         print(f"[ERROR] Failed to get time: {e}")
#         return "Sir, I couldn't get the current time."


# async def get_current_date() -> str:
#     """Get current date - NO AUTHORIZATION NEEDED."""
#     try:
#         current_date = datetime.now().strftime("%A, %B %d, %Y")
#         print(f"[DATE] Current date: {current_date}")
#         return f"Sir, today is {current_date}."
#     except Exception as e:
#         print(f"[ERROR] Failed to get date: {e}")
#         return "Sir, I couldn't get the current date."


# # ===============================
# # 💡 SMART AUTOMATION (JARVIS-LIKE)
# # ===============================
# @require_authorization
# async def auto_type_and_enter(text: str) -> str:
#     """Type text and press enter - REQUIRES AUTHORIZATION."""
#     try:
#         print(f"[AUTO] Typing and entering: {text}")
#         keyboard.write(text)
#         time.sleep(0.1)
#         keyboard.press_and_release("enter")
#         return f"Sir, typed '{text}' and pressed enter."
#     except Exception as e:
#         print(f"[ERROR] Failed to auto-type: {e}")
#         return "Sir, I couldn't complete the typing."


# @require_authorization
# async def open_and_search(search_term: str) -> str:
#     """Open Windows search - REQUIRES AUTHORIZATION."""
#     try:
#         print(f"[AUTO] Opening search for: {search_term}")
#         keyboard.press_and_release("win+s")
#         time.sleep(0.5)
#         keyboard.write(search_term)
#         return f"Sir, searching for '{search_term}' in Windows search."
#     except Exception as e:
#         print(f"[ERROR] Failed to search: {e}")
#         return "Sir, I couldn't perform the search."


# @require_authorization
# async def quick_note(note_text: str) -> str:
#     """Create quick note - REQUIRES AUTHORIZATION."""
#     try:
#         print(f"[NOTE] Creating quick note: {note_text}")
#         subprocess.Popen(['notepad.exe'])
#         time.sleep(1)
#         keyboard.write(note_text)
#         return f"Sir, created a quick note in Notepad."
#     except Exception as e:
#         print(f"[ERROR] Failed to create note: {e}")
#         return "Sir, I couldn't create the note."


# # ===============================
# # 🔒 SECURITY CONTROL FUNCTIONS
# # ===============================
# async def enable_control_mode(password: Optional[str] = None) -> str:
#     """Enable keyboard and mouse control."""
#     try:
#         if security.enable_control(password):
#             return "Sir, keyboard and mouse control is now ENABLED. I'm ready to assist you. Control will auto-disable after 5 minutes of inactivity for security."
#         else:
#             return "Sir, invalid password. Control remains disabled."
#     except Exception as e:
#         print(f"[ERROR] Failed to enable control: {e}")
#         return "Sir, I couldn't enable control mode."


# async def disable_control_mode() -> str:
#     """Disable keyboard and mouse control."""
#     try:
#         security.disable_control()
#         return "Sir, keyboard and mouse control is now DISABLED. Your system is secure."
#     except Exception as e:
#         print(f"[ERROR] Failed to disable control: {e}")
#         return "Sir, I couldn't disable control mode."


# async def check_control_status() -> str:
#     """Check if control is enabled."""
#     try:
#         status = "ENABLED ✅" if security.is_enabled() else "DISABLED 🔒"
#         return f"Sir, keyboard and mouse control is currently {status}."
#     except Exception as e:
#         print(f"[ERROR] Failed to check status: {e}")
#         return "Sir, I couldn't check the control status."


# async def set_control_password(password: str) -> str:
#     """Set a password for control mode."""
#     try:
#         security.set_password(password)
#         return "Sir, security password has been set. You'll need this password to enable control in future sessions."
#     except Exception as e:
#         print(f"[ERROR] Failed to set password: {e}")
#         return "Sir, I couldn't set the password."


# # ===============================
# # 🧠 LIVEKIT FUNCTION WRAPPERS
# # ===============================

# # ===== SECURITY CONTROLS =====
# @function_tool
# async def enable_keyboard_mouse_control(password: Optional[str] = None):
#     """
#     Enable keyboard and mouse control. Must be called before any control actions.
#     Say: 'Bucky, enable control' or 'Bucky, activate keyboard control'
#     """
#     return await enable_control_mode(password)


# @function_tool
# async def disable_keyboard_mouse_control():
#     """
#     Disable keyboard and mouse control for security.
#     Say: 'Bucky, disable control' or 'Bucky, deactivate keyboard control'
#     """
#     return await disable_control_mode()


# @function_tool
# async def check_control_status_tool():
#     """
#     Check if keyboard and mouse control is enabled or disabled.
#     Say: 'Bucky, is control enabled?' or 'Bucky, check control status'
#     """
#     return await check_control_status()


# @function_tool
# async def set_security_password(password: str):
#     """
#     Set a password for keyboard/mouse control for added security.
#     Say: 'Bucky, set password to [your_password]'
#     """
#     return await set_control_password(password)


# # ===== KEYBOARD CONTROLS =====
# @function_tool
# async def press_key(key_name: str):
#     """Press a single keyboard key. Requires control to be enabled."""
#     return await press_single_key(key_name)


# @function_tool
# async def press_shortcut(shortcut: str):
#     """Press keyboard shortcut. Requires control to be enabled."""
#     return await press_key_combination(shortcut)


# @function_tool
# async def type_text_input(text: str):
#     """Type text at cursor. Requires control to be enabled."""
#     return await type_text(text)


# @function_tool
# async def hold_key_down(key_name: str, duration: float = 1.0):
#     """Hold key for duration. Requires control to be enabled."""
#     return await hold_key(key_name, duration)


# # ===== MOUSE CONTROLS =====
# @function_tool
# async def move_mouse_cursor(
#     direction: Literal["left", "right", "up", "down"],
#     distance: Literal["small", "medium", "large"] = "medium"
# ):
#     """Move mouse cursor. Requires control to be enabled."""
#     return await move_cursor(direction, distance)


# @function_tool
# async def move_mouse_to(x: int, y: int):
#     """Move mouse to coordinates. Requires control to be enabled."""
#     return await move_cursor_to_position(x, y)


# @function_tool
# async def click_at_cursor(
#     button: Literal["left", "right", "middle"] = "left",
#     clicks: int = 1
# ):
#     """Click mouse. Requires control to be enabled."""
#     return await click_mouse(button, clicks)


# @function_tool
# async def scroll_page(
#     direction: Literal["up", "down"],
#     amount: Literal["small", "medium", "large"] = "medium"
# ):
#     """Scroll page. Requires control to be enabled."""
#     return await scroll_action(direction, amount)


# @function_tool
# async def drag_cursor(
#     direction: Literal["left", "right", "up", "down"],
#     distance: int = 200
# ):
#     """Drag mouse. Requires control to be enabled."""
#     return await drag_mouse(direction, distance)


# # ===== GESTURES & SHORTCUTS =====
# @function_tool
# async def execute_gesture(gesture_name: str):
#     """Execute Windows gesture. Requires control to be enabled."""
#     return await windows_gesture(gesture_name)


# @function_tool
# async def three_finger_swipe_gesture(
#     direction: Literal["up", "down", "left", "right"]
# ):
#     """Three-finger swipe. Requires control to be enabled."""
#     return await three_finger_swipe(direction)


# @function_tool
# async def get_cursor_position():
#     """Get cursor position. No authorization needed."""
#     try:
#         x, y = pyautogui.position()
#         print(f"[MOUSE] Current position: ({x}, {y})")
#         return f"Sir, cursor is at position ({x}, {y})."
#     except Exception as e:
#         return "Sir, I couldn't get the cursor position."


# @function_tool
# async def get_screen_size():
#     """Get screen resolution. No authorization needed."""
#     try:
#         width, height = pyautogui.size()
#         print(f"[SCREEN] Size: {width}x{height}")
#         return f"Sir, screen resolution is {width} by {height} pixels."
#     except Exception as e:
#         return "Sir, I couldn't get the screen size."


# # ===== CLIPBOARD OPERATIONS =====
# @function_tool
# async def copy_selection():
#     """Copy selected content. Requires control to be enabled."""
#     return await copy_to_clipboard()


# @function_tool
# async def paste_clipboard():
#     """Paste from clipboard. Requires control to be enabled."""
#     return await paste_from_clipboard()


# @function_tool
# async def read_clipboard():
#     """Read clipboard content. No authorization needed."""
#     return await get_clipboard_content()


# @function_tool
# async def write_clipboard(text: str):
#     """Write to clipboard. No authorization needed."""
#     return await set_clipboard_content(text)


# # ===== SCREENSHOT OPERATIONS =====
# @function_tool
# async def capture_screenshot(save_path: Optional[str] = None):
#     """Take screenshot. No authorization needed."""
#     return await take_screenshot(save_path)


# @function_tool
# async def capture_region(x1: int, y1: int, x2: int, y2: int, save_path: Optional[str] = None):
#     """Capture screen region. No authorization needed."""
#     return await take_region_screenshot(x1, y1, x2, y2, save_path)


# # ===== SCREEN ANALYSIS =====
# @function_tool
# async def find_image_on_screen(image_path: str):
#     """Find image on screen. No authorization needed."""
#     return await locate_on_screen(image_path)


# @function_tool
# async def click_image_on_screen(image_path: str):
#     """Click on image. Requires control to be enabled."""
#     return await click_on_image(image_path)


# # ===== WEB OPERATIONS =====
# @function_tool
# async def open_website(url: str):
#     """Open URL. No authorization needed."""
#     return await open_url(url)


# @function_tool
# async def google_search(query: str):
#     """Search Google. No authorization needed."""
#     return await search_google(query)


# @function_tool
# async def youtube_search(query: str):
#     """Search YouTube. No authorization needed."""
#     return await search_youtube(query)


# # ===== TIME & DATE =====
# @function_tool
# async def tell_time():
#     """Get current time. No authorization needed."""
#     return await get_current_time()


# @function_tool
# async def tell_date():
#     """Get current date. No authorization needed."""
#     return await get_current_date()


# # ===== SMART AUTOMATION =====
# @function_tool
# async def type_and_submit(text: str):
#     """Type and press enter. Requires control to be enabled."""
#     return await auto_type_and_enter(text)


# @function_tool
# async def windows_search(search_term: str):
#     """Windows search. Requires control to be enabled."""
#     return await open_and_search(search_term)


# @function_tool
# async def create_quick_note(note_text: str):
#     """Create note in Notepad. Requires control to be enabled."""
#     return await quick_note(note_text)