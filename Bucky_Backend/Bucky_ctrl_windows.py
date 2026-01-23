import os
import subprocess
import psutil
import platform
import win32com.client
from pathlib import Path
from typing import Optional, List
from livekit.agents import function_tool

# ===============================
# 🔗 APP SHORTCUT ALIASES
# ===============================
app_aliases = {
    "notepad": r"C:\Users\HP\Desktop\msoffice id&passward.txt",
    "youtube": r"C:\Users\HP\Desktop\YouTube (1).lnk",
    "vlc media player": r"C:\Users\Public\Desktop\VLC media player.lnk",
    "youtube music": r"C:\Users\HP\Desktop\YouTube Music.lnk",
    "chat gpt": r"C:\Users\HP\Desktop\CHAT BOTS\ChatGPT.lnk",
    "Gemini": r"C:\Users\HP\Desktop\CHAT BOTS\Google Gemini.lnk"
}

# ===============================
# 📁 FOLDER ALIASES (Add your common folders)
# ===============================
folder_aliases = {
    "desktop": r"C:\Users\HP\Desktop",
    "documents": r"C:\Users\HP\Documents",
    "downloads": r"C:\Users\HP\Downloads",
    "pictures": r"C:\Users\HP\Pictures",
    "videos": r"C:\Users\HP\Videos",
    "music": r"C:\Users\HP\Music",
    "chat bots": r"C:\Users\HP\Desktop\CHAT BOTS",
    "marvel": r"C:\Users\HP\Videos\Marvel"
    # Add more custom folders as needed
}

# ===============================
# 📄 FILE SEARCH PATHS (Locations to search for files)
# ===============================
file_search_paths = [
    r"C:\Users\HP\Desktop",
    r"C:\Users\HP\Documents",
    r"C:\Users\HP\Downloads",
    r"C:\Users\HP\Pictures",
    r"C:\Users\HP\Videos",
    r"C:\Users\HP\Music",
    # Add more search locations
]


# ===============================
# 🔍 HELPER FUNCTIONS
# ===============================
def find_folder_by_name(folder_name: str) -> Optional[str]:
    """
    Search for a folder by name in common locations.
    Returns the full path if found, None otherwise.
    """
    folder_name_lower = folder_name.lower().strip()
    
    # Check aliases first
    if folder_name_lower in folder_aliases:
        return folder_aliases[folder_name_lower]
    
    # Search in common locations
    search_locations = [
        r"C:\Users\HP\Desktop",
        r"C:\Users\HP\Documents",
        r"C:\Users\HP\Downloads",
        r"C:\Users\HP",
    ]
    
    for search_path in search_locations:
        if not os.path.exists(search_path):
            continue
            
        try:
            for item in os.listdir(search_path):
                item_path = os.path.join(search_path, item)
                if os.path.isdir(item_path) and item.lower() == folder_name_lower:
                    return item_path
        except PermissionError:
            continue
    
    return None


def find_file_by_name(file_name: str, search_paths: List[str] = None) -> Optional[str]:
    """
    Search for a file by name in specified search paths.
    Supports partial name matching and extension-less search.
    Returns the full path if found, None otherwise.
    """
    if search_paths is None:
        search_paths = file_search_paths
    
    file_name_lower = file_name.lower().strip()
    
    # Track all matches for better selection
    exact_matches = []
    partial_matches = []
    
    for search_path in search_paths:
        if not os.path.exists(search_path):
            continue
            
        try:
            for item in os.listdir(search_path):
                item_path = os.path.join(search_path, item)
                if os.path.isfile(item_path):
                    item_name_lower = item.lower()
                    
                    # Exact match (with or without extension)
                    if item_name_lower == file_name_lower:
                        exact_matches.append(item_path)
                    elif os.path.splitext(item_name_lower)[0] == file_name_lower:
                        exact_matches.append(item_path)
                    # Partial match
                    elif file_name_lower in item_name_lower:
                        partial_matches.append(item_path)
        except PermissionError:
            continue
    
    # Return best match
    if exact_matches:
        return exact_matches[0]
    elif partial_matches:
        return partial_matches[0]
    
    return None


def get_process_name_from_path(file_path: str) -> str:
    """
    Get the process name that would be created when opening a file.
    """
    ext = os.path.splitext(file_path)[1].lower()
    
    # Common file type to process mappings
    process_map = {
        '.txt': 'notepad.exe',
        '.pdf': 'AcroRd32.exe',  # or 'Acrobat.exe'
        '.docx': 'WINWORD.EXE',
        '.doc': 'WINWORD.EXE',
        '.xlsx': 'EXCEL.EXE',
        '.xls': 'EXCEL.EXE',
        '.pptx': 'POWERPNT.EXE',
        '.ppt': 'POWERPNT.EXE',
        '.png': 'Photos.exe',
        '.jpg': 'Photos.exe',
        '.jpeg': 'Photos.exe',
        '.mp4': 'vlc.exe',
        '.mp3': 'vlc.exe',
        '.avi': 'vlc.exe',
    }
    
    return process_map.get(ext, os.path.basename(file_path))


# ===============================
# ⚙️ CORE FUNCTION
# ===============================
async def perform_system_control(action: str, params: Optional[str] = None) -> str:
    """
    Perform Windows system control tasks with logging.
    Works with LiveKit via @function_tool wrappers.
    """
    try:
        # -----------------
        # POWER COMMANDS
        # -----------------
        if action == "shutdown":
            print("[SYSTEM] Initiating system shutdown")
            subprocess.run(["shutdown", "/s", "/t", "0"], check=True)
            return "Sir, shutting down the system now. Goodnight!"

        elif action == "restart":
            print("[SYSTEM] Initiating system restart")
            subprocess.run(["shutdown", "/r", "/t", "0"], check=True)
            return "Sir, restarting the system. Be right back!"

        elif action == "sleep":
            print("[SYSTEM] Putting system to sleep")
            subprocess.run(["rundll32.exe", "powrprof.dll,SetSuspendState", "0,1,0"], check=True)
            return "Sir, system is going to sleep. Sweet dreams!"

        # -----------------
        # APP MANAGEMENT
        # -----------------
        elif action == "open_app":
            if not params:
                return "Sir, please specify an application to open."

            app_name = params.lower().strip()
            app_path = app_aliases.get(app_name)

            if app_path and os.path.exists(app_path):
                print(f"[SYSTEM] Launching {app_name} from {app_path}")
                os.startfile(app_path)
                return f"Sir, opening {app_name} now."
            else:
                return f"Sir, I couldn't find {app_name}. Please check the path in app_aliases."

        elif action == "close_app":
            if not params:
                return "Sir, please specify an application to close."

            app_name = params.lower().strip()
            app_path = app_aliases.get(app_name)

            if not app_path:
                return f"Sir, I couldn't find {app_name} in app aliases."

            # Extract actual target executable (for .lnk)
            exe_name = None
            try:
                if app_path.endswith(".lnk"):
                    shell = win32com.client.Dispatch("WScript.Shell")
                    shortcut = shell.CreateShortCut(app_path)
                    target_path = shortcut.TargetPath
                    exe_name = os.path.basename(target_path)
                else:
                    exe_name = os.path.basename(app_path)
            except Exception as e:
                print(f"[ERROR] Could not read shortcut target: {e}")
                return f"Sir, I couldn't read the shortcut for {app_name}."

            print(f"[SYSTEM] Attempting to close {app_name} (process: {exe_name})")

            try:
                closed_any = False
                for proc in psutil.process_iter(['name']):
                    if proc.info['name'] and proc.info['name'].lower() == exe_name.lower():
                        print(f"[SYSTEM] Closing {proc.info['name']} (PID: {proc.pid})")
                        proc.terminate()
                        closed_any = True

                # Wait a bit to allow graceful shutdown
                psutil.wait_procs(
                    [p for p in psutil.process_iter() if p.name().lower() == exe_name.lower()],
                    timeout=3
                )

                if closed_any:
                    return f"Sir, {app_name} has been closed gracefully."
                else:
                    return f"Sir, {app_name} isn't currently running."

            except Exception as e:
                print(f"[ERROR] Failed to close app: {e}")
                return f"Sir, I couldn't close {app_name}. Check if it's running with admin privileges."

        # -----------------
        # FOLDER MANAGEMENT
        # -----------------
        elif action == "open_folder":
            if not params:
                return "Sir, please specify a folder to open."
            
            folder_name = params.strip()
            folder_path = find_folder_by_name(folder_name)
            
            if folder_path and os.path.exists(folder_path):
                print(f"[SYSTEM] Opening folder: {folder_path}")
                os.startfile(folder_path)
                return f"Sir, opening {folder_name} folder now."
            else:
                return f"Sir, I couldn't find the folder '{folder_name}'. Please check if it exists."

        elif action == "close_folder":
            if not params:
                return "Sir, please specify a folder to close."
            
            folder_name = params.strip()
            folder_path = find_folder_by_name(folder_name)
            
            if not folder_path:
                return f"Sir, I couldn't find the folder '{folder_name}'."
            
            print(f"[SYSTEM] Attempting to close folder: {folder_path}")
            
            try:
                closed_any = False
                # Close all explorer windows showing this folder
                for proc in psutil.process_iter(['name', 'exe', 'cmdline']):
                    if proc.info['name'] and proc.info['name'].lower() == 'explorer.exe':
                        try:
                            cmdline = proc.info.get('cmdline', [])
                            if cmdline and any(folder_path.lower() in str(arg).lower() for arg in cmdline):
                                print(f"[SYSTEM] Closing explorer window (PID: {proc.pid})")
                                proc.terminate()
                                closed_any = True
                        except (psutil.NoSuchProcess, psutil.AccessDenied):
                            continue
                
                if closed_any:
                    return f"Sir, {folder_name} folder has been closed."
                else:
                    return f"Sir, no open windows found for {folder_name} folder."
                    
            except Exception as e:
                print(f"[ERROR] Failed to close folder: {e}")
                return f"Sir, I couldn't close the {folder_name} folder window."

        # -----------------
        # FILE MANAGEMENT
        # -----------------
        elif action == "open_file":
            if not params:
                return "Sir, please specify a file to open."
            
            file_name = params.strip()
            file_path = find_file_by_name(file_name)
            
            if file_path and os.path.exists(file_path):
                print(f"[SYSTEM] Opening file: {file_path}")
                os.startfile(file_path)
                return f"Sir, opening {os.path.basename(file_path)} now."
            else:
                return f"Sir, I couldn't find the file '{file_name}'. Please check if it exists in the search paths."

        elif action == "close_file":
            if not params:
                return "Sir, please specify a file to close."
            
            file_name = params.strip()
            file_path = find_file_by_name(file_name)
            
            if not file_path:
                return f"Sir, I couldn't find the file '{file_name}'."
            
            # Determine which process to close
            process_name = get_process_name_from_path(file_path)
            print(f"[SYSTEM] Attempting to close file: {file_path} (process: {process_name})")
            
            try:
                closed_any = False
                for proc in psutil.process_iter(['name', 'exe', 'cmdline']):
                    if proc.info['name'] and proc.info['name'].lower() == process_name.lower():
                        try:
                            # Check if this process has the file open
                            cmdline = proc.info.get('cmdline', [])
                            if cmdline and any(file_path.lower() in str(arg).lower() for arg in cmdline):
                                print(f"[SYSTEM] Closing {proc.info['name']} (PID: {proc.pid})")
                                proc.terminate()
                                closed_any = True
                        except (psutil.NoSuchProcess, psutil.AccessDenied):
                            continue
                
                if closed_any:
                    return f"Sir, {os.path.basename(file_path)} has been closed."
                else:
                    return f"Sir, no application found with {os.path.basename(file_path)} open."
                    
            except Exception as e:
                print(f"[ERROR] Failed to close file: {e}")
                return f"Sir, I couldn't close {os.path.basename(file_path)}."

        # -----------------
        # STATUS COMMANDS
        # -----------------
        elif action == "list_apps":
            apps = [proc.name() for proc in psutil.process_iter(['name']) if proc.name().endswith('.exe')]
            for app in apps:
                print(f" - {app}")
            return f"Sir, running applications: {', '.join(apps) if apps else 'none'}."

        elif action == "pc_config":
            sys_info = {
                "OS": platform.system() + " " + platform.release(),
                "Processor": platform.processor(),
                "RAM": f"{psutil.virtual_memory().total / (1024**3):.2f} GB",
                "Machine": platform.machine()
            }
            for key, value in sys_info.items():
                print(f"{key}: {value}")
            return f"Sir, your system: {sys_info['OS']}, {sys_info['Processor']}, {sys_info['RAM']} RAM, {sys_info['Machine']} architecture."

        elif action == "battery":
            battery = psutil.sensors_battery()
            if not battery:
                return "Sir, battery status is unavailable. Are you on a desktop?"
            percent = battery.percent
            plugged = "plugged in" if battery.power_plugged else "on battery"
            print(f"[SYSTEM] Battery status: {percent}% ({plugged})")
            return f"Sir, battery is at {percent}% and {plugged}."

        # -----------------
        # UNKNOWN ACTION
        # -----------------
        else:
            return f"Sir, I don't recognize the action '{action}'."

    except subprocess.CalledProcessError as e:
        print(f"[ERROR] System command failed: {e}")
        return f"Sir, the {action} command failed. Try running with admin privileges."

    except Exception as e:
        print(f"[ERROR] Unexpected error: {e}")
        return f"Sir, something went wrong with {action}. Check the terminal for details."


# ===============================
# 🧠 LIVEKIT FUNCTION WRAPPERS
# ===============================

# App Management
@function_tool
async def livekit_open_app(app_name: str):
    """Open an application by name."""
    return await perform_system_control("open_app", app_name)

@function_tool
async def livekit_close_app(app_name: str):
    """Close an application by name."""
    return await perform_system_control("close_app", app_name)

# Folder Management
@function_tool
async def livekit_open_folder(folder_name: str):
    """Open a folder by name. Searches common locations like Desktop, Documents, Downloads."""
    return await perform_system_control("open_folder", folder_name)

@function_tool
async def livekit_close_folder(folder_name: str):
    """Close an open folder window by name."""
    return await perform_system_control("close_folder", folder_name)

# File Management
@function_tool
async def livekit_open_file(file_name: str):
    """Open a file by name. Searches in Desktop, Documents, Downloads, Pictures, Videos, and Music folders."""
    return await perform_system_control("open_file", file_name)

@function_tool
async def livekit_close_file(file_name: str):
    """Close an open file by closing the application that has it open."""
    return await perform_system_control("close_file", file_name)

# Power Management
@function_tool
async def shutdown_pc():
    """Shut down the computer."""
    return await perform_system_control("shutdown")

@function_tool
async def restart_pc():
    """Restart the computer."""
    return await perform_system_control("restart")

@function_tool
async def sleep_pc():
    """Put the computer to sleep."""
    return await perform_system_control("sleep")

# System Status
@function_tool
async def battery_status():
    """Get the current battery status."""
    return await perform_system_control("battery")