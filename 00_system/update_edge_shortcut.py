import os
import sys

def update_shortcuts():
    import win32com.client
    shell = win32com.client.Dispatch("WScript.Shell")
    
    desktop = os.path.join(os.path.expanduser("~"), "Desktop")
    start_menu = os.path.expandvars(r"%APPDATA%\Microsoft\Windows\Start Menu\Programs")
    
    edge_exe = r"C:\Program Files (x86)\Microsoft\Edge\Application\msedge.exe"
    if not os.path.exists(edge_exe):
        edge_exe = r"C:\Program Files\Microsoft\Edge\Application\msedge.exe"
        
    targets = [
        os.path.join(desktop, "Microsoft Edge.lnk"),
        os.path.join(desktop, "Edge (AI-CDP).lnk"),
        os.path.join(start_menu, "Microsoft Edge.lnk")
    ]
    
    updated = []
    for path in targets:
        try:
            sc = shell.CreateShortcut(path)
            sc.TargetPath = edge_exe
            sc.Arguments = "--remote-debugging-port=9222"
            sc.Description = "Microsoft Edge (AI-CDP Enabled Port 9222)"
            sc.Save()
            updated.append(path)
        except Exception as e:
            print(f"Failed {path}: {e}")
            
    return updated

if __name__ == "__main__":
    res = update_shortcuts()
    print("SUCCESS: Updated shortcuts:")
    for r in res:
        print(" - " + r)
