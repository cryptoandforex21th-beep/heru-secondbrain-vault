[CmdletBinding()]
param(
    [Parameter(Mandatory = $true)][string]$StateDirectory,
    [ValidateRange(1, 120)][int]$IdleTimeoutMinutes = 10,
    [switch]$NoOverlay
)

$ErrorActionPreference = 'Stop'

[IO.Directory]::CreateDirectory($StateDirectory) | Out-Null
$stopFile = Join-Path $StateDirectory 'stop.flag'
$exitFile = Join-Path $StateDirectory 'exit.flag'
$heartbeatFile = Join-Path $StateDirectory 'heartbeat.txt'
$readyFile = Join-Path $StateDirectory 'ready.flag'
$pidFile = Join-Path $StateDirectory 'controller.pid'
$portFile = Join-Path $StateDirectory 'controller.port'

$uiaClient = [System.Reflection.Assembly]::LoadWithPartialName('UIAutomationClient').Location
$uiaTypes = [System.Reflection.Assembly]::LoadWithPartialName('UIAutomationTypes').Location
$webExt = [System.Reflection.Assembly]::LoadWithPartialName('System.Web.Extensions').Location
$winBase = [System.Reflection.Assembly]::LoadWithPartialName('WindowsBase').Location

if (-not ('AntigravityComputerUse.ControlEngine' -as [type])) {
    Add-Type -ReferencedAssemblies @(
        'System.Windows.Forms.dll',
        'System.Drawing.dll',
        $webExt,
        $winBase,
        $uiaClient,
        $uiaTypes
    ) -TypeDefinition @'
using System;
using System.Collections;
using System.Collections.Generic;
using System.Diagnostics;
using System.Drawing;
using System.Drawing.Drawing2D;
using System.Drawing.Imaging;
using System.IO;
using System.Net;
using System.Net.Sockets;
using System.Runtime.InteropServices;
using System.Security.Cryptography;
using System.Text;
using System.Threading;
using System.Web.Script.Serialization;
using System.Windows.Automation;
using System.Windows.Forms;

namespace AntigravityComputerUse
{
    public sealed class WindowInfo
    {
        public long handle { get; set; }
        public string title { get; set; }
        public string process { get; set; }
        public int processId { get; set; }
        public int x { get; set; }
        public int y { get; set; }
        public int width { get; set; }
        public int height { get; set; }
        public bool minimized { get; set; }
    }

    public static class NativeBridge
    {
        public delegate bool EnumWindowsProc(IntPtr hWnd, IntPtr lParam);

        [StructLayout(LayoutKind.Sequential)] public struct POINT { public int X; public int Y; }
        [StructLayout(LayoutKind.Sequential)] public struct RECT { public int Left; public int Top; public int Right; public int Bottom; }
        [StructLayout(LayoutKind.Sequential)] public struct INPUT { public uint type; public InputUnion U; }
        [StructLayout(LayoutKind.Explicit)]
        public struct InputUnion
        {
            [FieldOffset(0)] public MOUSEINPUT mi;
            [FieldOffset(0)] public KEYBDINPUT ki;
            [FieldOffset(0)] public HARDWAREINPUT hi;
        }
        [StructLayout(LayoutKind.Sequential)]
        public struct MOUSEINPUT
        {
            public int dx; public int dy; public uint mouseData; public uint dwFlags; public uint time; public UIntPtr dwExtraInfo;
        }
        [StructLayout(LayoutKind.Sequential)]
        public struct KEYBDINPUT
        {
            public ushort wVk; public ushort wScan; public uint dwFlags; public uint time; public UIntPtr dwExtraInfo;
        }
        [StructLayout(LayoutKind.Sequential)]
        public struct HARDWAREINPUT
        {
            public uint uMsg; public ushort wParamL; public ushort wParamH;
        }

        [DllImport("user32.dll")] public static extern bool SetProcessDPIAware();
        [DllImport("user32.dll")] public static extern bool SetProcessDpiAwarenessContext(IntPtr value);
        [DllImport("user32.dll", EntryPoint = "GetCursorPos")] public static extern bool RawGetCursorPos(out POINT point);
        [DllImport("user32.dll", EntryPoint = "SetCursorPos")] public static extern bool RawSetCursorPos(int x, int y);
        [DllImport("user32.dll", EntryPoint = "mouse_event")] public static extern void RawMouseEvent(uint flags, uint dx, uint dy, uint data, UIntPtr extraInfo);
        [DllImport("user32.dll", EntryPoint = "keybd_event")] public static extern void RawKeybdEvent(byte virtualKey, byte scanCode, uint flags, UIntPtr extraInfo);
        [DllImport("user32.dll", EntryPoint = "SendInput")] public static extern uint RawSendInput(uint count, INPUT[] inputs, int size);
        [DllImport("user32.dll")] public static extern IntPtr OpenDesktop(string lpszDesktop, uint dwFlags, bool fInherit, uint dwDesiredAccess);
        [DllImport("user32.dll")] public static extern bool SetThreadDesktop(IntPtr hDesktop);
        [DllImport("user32.dll")] public static extern bool CloseDesktop(IntPtr hDesktop);
        [DllImport("user32.dll")] public static extern bool EnumDesktopWindows(IntPtr hDesktop, EnumWindowsProc callback, IntPtr lParam);
        [DllImport("user32.dll")] public static extern bool EnumWindows(EnumWindowsProc callback, IntPtr lParam);
        [DllImport("user32.dll")] public static extern bool IsWindow(IntPtr hWnd);
        [DllImport("user32.dll")] public static extern bool IsWindowVisible(IntPtr hWnd);
        [DllImport("user32.dll")] public static extern bool IsIconic(IntPtr hWnd);
        [DllImport("user32.dll", CharSet = CharSet.Unicode)] public static extern int GetWindowText(IntPtr hWnd, StringBuilder text, int maxCount);
        [DllImport("user32.dll")] public static extern int GetWindowTextLength(IntPtr hWnd);
        [DllImport("user32.dll")] public static extern bool GetWindowRect(IntPtr hWnd, out RECT rect);
        [DllImport("user32.dll")] public static extern uint GetWindowThreadProcessId(IntPtr hWnd, out uint processId);
        [DllImport("user32.dll")] public static extern IntPtr GetForegroundWindow();
        [DllImport("user32.dll")] public static extern bool SetForegroundWindow(IntPtr hWnd);
        [DllImport("user32.dll")] public static extern bool ShowWindow(IntPtr hWnd, int command);
        [DllImport("user32.dll")] public static extern bool BringWindowToTop(IntPtr hWnd);
        [DllImport("user32.dll")] public static extern bool SetWindowPos(IntPtr hWnd, IntPtr hWndInsertAfter, int X, int Y, int cx, int cy, uint uFlags);
        [DllImport("user32.dll")] public static extern bool AttachThreadInput(uint idAttach, uint idAttachTo, bool fAttach);
        [DllImport("kernel32.dll")] public static extern uint GetCurrentThreadId();

        public const uint INPUT_KEYBOARD = 1;
        public const uint KEYEVENTF_KEYUP = 0x0002;
        public const uint KEYEVENTF_UNICODE = 0x0004;

        public static WindowInfo DescribeWindow(IntPtr hWnd)
        {
            if (hWnd == IntPtr.Zero || !IsWindowVisible(hWnd)) return null;
            int length = GetWindowTextLength(hWnd);
            if (length <= 0) return null;
            StringBuilder title = new StringBuilder(length + 1);
            GetWindowText(hWnd, title, title.Capacity);
            if (string.IsNullOrWhiteSpace(title.ToString())) return null;

            RECT rect;
            if (!GetWindowRect(hWnd, out rect)) return null;
            uint pid;
            GetWindowThreadProcessId(hWnd, out pid);
            string processName = "";
            try { processName = Process.GetProcessById((int)pid).ProcessName; } catch { }

            return new WindowInfo {
                handle = hWnd.ToInt64(), title = title.ToString(), process = processName,
                processId = (int)pid, x = rect.Left, y = rect.Top,
                width = rect.Right - rect.Left, height = rect.Bottom - rect.Top,
                minimized = IsIconic(hWnd)
            };
        }

        public static List<WindowInfo> GetWindows()
        {
            List<WindowInfo> result = new List<WindowInfo>();
            EnumWindowsProc callback = (hWnd, lParam) => {
                WindowInfo info = DescribeWindow(hWnd);
                if (info != null) result.Add(info);
                return true;
            };

            IntPtr hDesk = OpenDesktop("default", 0, false, 0x01FF);
            if (hDesk != IntPtr.Zero)
            {
                EnumDesktopWindows(hDesk, callback, IntPtr.Zero);
                CloseDesktop(hDesk);
            }
            else
            {
                EnumWindows(callback, IntPtr.Zero);
            }
            GC.KeepAlive(callback);
            return result;
        }

        public static IntPtr GetActiveForegroundWindow()
        {
            IntPtr hDesk = OpenDesktop("default", 0, false, 0x01FF);
            if (hDesk != IntPtr.Zero) SetThreadDesktop(hDesk);
            IntPtr fg = GetForegroundWindow();
            if (hDesk != IntPtr.Zero) CloseDesktop(hDesk);
            return fg;
        }

        public static WindowInfo GetForeground()
        {
            IntPtr fg = GetActiveForegroundWindow();
            return DescribeWindow(fg);
        }

        public static bool FocusWindow(long handle)
        {
            IntPtr hWnd = new IntPtr(handle);
            IntPtr hDesk = OpenDesktop("default", 0, false, 0x01FF);
            if (hDesk != IntPtr.Zero) SetThreadDesktop(hDesk);

            IntPtr curFg = GetForegroundWindow();
            uint fgPid = 0;
            uint fgThread = (curFg != IntPtr.Zero) ? GetWindowThreadProcessId(curFg, out fgPid) : 0;
            uint curThread = GetCurrentThreadId();

            if (fgThread != 0 && fgThread != curThread)
            {
                AttachThreadInput(curThread, fgThread, true);
            }

            RawKeybdEvent(0x12, 0, 0, UIntPtr.Zero);
            RawKeybdEvent(0x12, 0, 2, UIntPtr.Zero);

            if (IsIconic(hWnd)) ShowWindow(hWnd, 9); // SW_RESTORE
            else ShowWindow(hWnd, 3); // SW_MAXIMIZE
            BringWindowToTop(hWnd);
            bool res = SetForegroundWindow(hWnd);

            if (fgThread != 0 && fgThread != curThread)
            {
                AttachThreadInput(curThread, fgThread, false);
            }

            if (hDesk != IntPtr.Zero) CloseDesktop(hDesk);
            return res;
        }

        public static void SendUnicodeChar(char ch)
        {
            INPUT down = new INPUT();
            down.type = INPUT_KEYBOARD;
            down.U.ki.wScan = ch;
            down.U.ki.dwFlags = KEYEVENTF_UNICODE;
            INPUT up = down;
            up.U.ki.dwFlags = KEYEVENTF_UNICODE | KEYEVENTF_KEYUP;
            INPUT[] pair = new INPUT[] { down, up };
            uint sent = RawSendInput(2, pair, Marshal.SizeOf(typeof(INPUT)));
            if (sent != 2) throw new InvalidOperationException("SendInput failed typing Unicode char.");
        }
    }

    public sealed class SideGlowForm : Form
    {
        const int WS_EX_NOACTIVATE = 0x08000000;
        const int WS_EX_TOOLWINDOW = 0x00000080;
        const int WS_EX_TRANSPARENT = 0x00000020;
        const int WS_EX_LAYERED = 0x00080000;

        const byte AC_SRC_OVER = 0x00;
        const byte AC_SRC_ALPHA = 0x01;
        const uint ULW_ALPHA = 0x02;

        [StructLayout(LayoutKind.Sequential)] public struct POINT { public int X; public int Y; }
        [StructLayout(LayoutKind.Sequential)] public struct SIZE { public int cx; public int cy; }
        [StructLayout(LayoutKind.Sequential, Pack = 1)]
        public struct BLENDFUNCTION
        {
            public byte BlendOp; public byte BlendFlags; public byte SourceConstantAlpha; public byte AlphaFormat;
        }

        [DllImport("user32.dll", SetLastError = true)]
        public static extern bool UpdateLayeredWindow(IntPtr hwnd, IntPtr hdcDst, ref POINT pptDst, ref SIZE psize, IntPtr hdcSrc, ref POINT pptSrc, uint crKey, [In] ref BLENDFUNCTION pblend, uint dwFlags);
        [DllImport("user32.dll")] public static extern IntPtr GetDC(IntPtr hWnd);
        [DllImport("user32.dll")] public static extern int ReleaseDC(IntPtr hWnd, IntPtr hDC);
        [DllImport("gdi32.dll")] public static extern IntPtr CreateCompatibleDC(IntPtr hDC);
        [DllImport("gdi32.dll")] public static extern bool DeleteDC(IntPtr hdc);
        [DllImport("gdi32.dll")] public static extern IntPtr SelectObject(IntPtr hDC, IntPtr hObject);
        [DllImport("gdi32.dll")] public static extern bool DeleteObject(IntPtr hObject);

        readonly bool isLeft;
        const int StripWidth = 100;
        byte currentAlpha = 245;

        public SideGlowForm(bool left)
        {
            isLeft = left;
            FormBorderStyle = FormBorderStyle.None;
            ShowInTaskbar = false;
            TopMost = true;
            Width = StripWidth;
            Height = Screen.PrimaryScreen.Bounds.Height;
            StartPosition = FormStartPosition.Manual;
            int screenWidth = Screen.PrimaryScreen.Bounds.Width;
            Location = new Point(isLeft ? 0 : (screenWidth - StripWidth), 0);
        }

        protected override bool ShowWithoutActivation { get { return true; } }
        protected override CreateParams CreateParams
        {
            get
            {
                CreateParams cp = base.CreateParams;
                cp.ExStyle |= WS_EX_NOACTIVATE | WS_EX_TOOLWINDOW | WS_EX_TRANSPARENT | WS_EX_LAYERED | 0x00000008;
                return cp;
            }
        }

        protected override void OnHandleCreated(EventArgs e)
        {
            base.OnHandleCreated(e);
            RenderGlow(currentAlpha);
            try { NativeBridge.SetWindowPos(Handle, new IntPtr(-1), 0, 0, 0, 0, 0x0001 | 0x0002 | 0x0010 | 0x0040); } catch { }
        }

        public void SetGlowAlpha(byte alpha)
        {
            if (currentAlpha != alpha)
            {
                currentAlpha = alpha;
                if (IsHandleCreated) RenderGlow(alpha);
            }
        }

        void RenderGlow(byte maxAlpha)
        {
            using (Bitmap bmp = new Bitmap(Width, Height, PixelFormat.Format32bppArgb))
            {
                BitmapData data = bmp.LockBits(new Rectangle(0, 0, Width, Height), ImageLockMode.WriteOnly, PixelFormat.Format32bppArgb);
                int stride = data.Stride;
                IntPtr scan0 = data.Scan0;

                byte[] row = new byte[Width * 4];
                for (int x = 0; x < Width; x++)
                {
                    double progress = isLeft ? ((double)x / (Width - 1)) : ((double)(Width - 1 - x) / (Width - 1));
                    double factor = Math.Pow(1.0 - progress, 1.5);
                    byte a = (byte)Math.Max(0, Math.Min(255, (int)(maxAlpha * factor)));
                    row[x * 4 + 0] = a; // B (Pure White Premultiplied)
                    row[x * 4 + 1] = a; // G
                    row[x * 4 + 2] = a; // R
                    row[x * 4 + 3] = a; // A
                }

                byte[] allPixels = new byte[stride * Height];
                for (int y = 0; y < Height; y++)
                {
                    Buffer.BlockCopy(row, 0, allPixels, y * stride, Width * 4);
                }
                Marshal.Copy(allPixels, 0, scan0, allPixels.Length);
                bmp.UnlockBits(data);

                IntPtr screenDc = GetDC(IntPtr.Zero);
                IntPtr memDc = CreateCompatibleDC(screenDc);
                IntPtr hBitmap = bmp.GetHbitmap(Color.FromArgb(0));
                IntPtr oldBitmap = SelectObject(memDc, hBitmap);

                POINT pointSource = new POINT { X = 0, Y = 0 };
                POINT topPos = new POINT { X = Location.X, Y = Location.Y };
                SIZE size = new SIZE { cx = Width, cy = Height };
                BLENDFUNCTION blend = new BLENDFUNCTION
                {
                    BlendOp = AC_SRC_OVER,
                    BlendFlags = 0,
                    SourceConstantAlpha = 255,
                    AlphaFormat = AC_SRC_ALPHA
                };

                UpdateLayeredWindow(Handle, screenDc, ref topPos, ref size, memDc, ref pointSource, 0, ref blend, ULW_ALPHA);
                SelectObject(memDc, oldBitmap);
                DeleteObject(hBitmap);
                DeleteDC(memDc);
                ReleaseDC(IntPtr.Zero, screenDc);
            }
        }
    }

    public sealed class StatusOverlay : Form
    {
        const int WM_HOTKEY = 0x0312;
        public const int HOTKEY_ID = 0x41C7;
        public const int VK_ESCAPE = 0x1B;
        const int WS_EX_NOACTIVATE = 0x08000000;
        const int WS_EX_TOOLWINDOW = 0x00000080;
        const int WS_EX_TRANSPARENT = 0x00000020;

        readonly ControlEngine engine;
        SideGlowForm leftGlow;
        SideGlowForm rightGlow;

        [DllImport("user32.dll")] public static extern bool RegisterHotKey(IntPtr hWnd, int id, uint modifiers, uint virtualKey);
        [DllImport("user32.dll")] public static extern bool UnregisterHotKey(IntPtr hWnd, int id);

        public StatusOverlay(ControlEngine eng)
        {
            engine = eng;
            Text = "AGY computer control";
            FormBorderStyle = FormBorderStyle.None;
            ShowInTaskbar = false;
            TopMost = true;
            Width = 430;
            Height = 40;
            BackColor = Color.FromArgb(248, 250, 252);
            Opacity = 0.98;
            StartPosition = FormStartPosition.Manual;
            DoubleBuffered = true;

            Rectangle area = Screen.PrimaryScreen.WorkingArea;
            Location = new Point(area.Left + (area.Width - Width) / 2, area.Top + 10);

            using (GraphicsPath path = GetRoundRectPath(new Rectangle(0, 0, Width, Height), 16))
            {
                this.Region = new Region(path);
            }
        }

        protected override bool ShowWithoutActivation { get { return true; } }
        protected override CreateParams CreateParams
        {
            get
            {
                CreateParams cp = base.CreateParams;
                cp.ExStyle |= WS_EX_NOACTIVATE | WS_EX_TOOLWINDOW | WS_EX_TRANSPARENT | 0x00000008;
                return cp;
            }
        }

        static GraphicsPath GetRoundRectPath(Rectangle rect, int radius)
        {
            GraphicsPath path = new GraphicsPath();
            int d = radius * 2;
            path.AddArc(rect.X, rect.Y, d, d, 180, 90);
            path.AddArc(rect.Right - d, rect.Y, d, d, 270, 90);
            path.AddArc(rect.Right - d, rect.Bottom - d, d, d, 0, 90);
            path.AddArc(rect.X, rect.Bottom - d, d, d, 90, 90);
            path.CloseFigure();
            return path;
        }

        protected override void OnPaint(PaintEventArgs e)
        {
            base.OnPaint(e);
            Graphics g = e.Graphics;
            g.SmoothingMode = SmoothingMode.AntiAlias;
            g.TextRenderingHint = System.Drawing.Text.TextRenderingHint.ClearTypeGridFit;

            Rectangle rect = new Rectangle(0, 0, Width, Height);
            using (LinearGradientBrush brush = new LinearGradientBrush(rect, Color.FromArgb(255, 255, 255), Color.FromArgb(244, 246, 249), LinearGradientMode.Vertical))
            {
                g.FillRectangle(brush, rect);
            }

            using (Pen borderPen = new Pen(Color.FromArgb(218, 224, 233), 1.5f))
            {
                using (GraphicsPath bPath = GetRoundRectPath(new Rectangle(0, 0, Width - 1, Height - 1), 16))
                {
                    g.DrawPath(borderPen, bPath);
                }
            }

            int dotY = (Height - 10) / 2;
            using (SolidBrush dotGlow = new SolidBrush(Color.FromArgb(50, 16, 185, 129)))
            {
                g.FillEllipse(dotGlow, 14, dotY - 3, 16, 16);
            }
            using (SolidBrush dotBrush = new SolidBrush(Color.FromArgb(16, 185, 129)))
            {
                g.FillEllipse(dotBrush, 17, dotY, 10, 10);
            }

            using (Font fontText = new Font("Segoe UI", 9.5f, FontStyle.Bold))
            using (SolidBrush textBrush = new SolidBrush(Color.FromArgb(15, 23, 42)))
            {
                g.DrawString("AGY \u0443\u043f\u0440\u0430\u0432\u043b\u044f\u0435\u0442 \u043a\u043e\u043c\u043f\u044c\u044e\u0442\u0435\u0440\u043e\u043c...", fontText, textBrush, 36, (Height - 18) / 2);
            }

            Rectangle escPill = new Rectangle(284, (Height - 24) / 2, 134, 24);
            using (SolidBrush pillBg = new SolidBrush(Color.FromArgb(238, 242, 246)))
            {
                using (GraphicsPath pillPath = GetRoundRectPath(escPill, 10))
                {
                    g.FillPath(pillBg, pillPath);
                    using (Pen pillPen = new Pen(Color.FromArgb(203, 213, 225), 1.0f))
                    {
                        g.DrawPath(pillPen, pillPath);
                    }
                }
            }

            using (Font fontKey = new Font("Segoe UI", 8.5f, FontStyle.Bold))
            using (SolidBrush keyBrush = new SolidBrush(Color.FromArgb(71, 85, 105)))
            {
                g.DrawString("ESC \u2014 \u043e\u0441\u0442\u0430\u043d\u043e\u0432\u0438\u0442\u044c", fontKey, keyBrush, 292, (Height - 16) / 2);
            }
        }

        public void SetBusy(bool busy)
        {
        }

        public void EnsureTopMost()
        {
            try {
                NativeBridge.SetWindowPos(Handle, new IntPtr(-1), 0, 0, 0, 0, 0x0001 | 0x0002 | 0x0010 | 0x0040);
                if (leftGlow != null && leftGlow.IsHandleCreated)
                    NativeBridge.SetWindowPos(leftGlow.Handle, new IntPtr(-1), 0, 0, 0, 0, 0x0001 | 0x0002 | 0x0010 | 0x0040);
                if (rightGlow != null && rightGlow.IsHandleCreated)
                    NativeBridge.SetWindowPos(rightGlow.Handle, new IntPtr(-1), 0, 0, 0, 0, 0x0001 | 0x0002 | 0x0010 | 0x0040);
            } catch { }
        }

        System.Windows.Forms.Timer topmostTimer;

        protected override void OnHandleCreated(EventArgs e)
        {
            base.OnHandleCreated(e);
            RegisterHotKey(Handle, HOTKEY_ID, 0, VK_ESCAPE);
            try
            {
                leftGlow = new SideGlowForm(true);
                rightGlow = new SideGlowForm(false);
                leftGlow.Show();
                rightGlow.Show();
            }
            catch { }

            topmostTimer = new System.Windows.Forms.Timer();
            topmostTimer.Interval = 200;
            topmostTimer.Tick += (s, ev) => {
                EnsureTopMost();
            };
            topmostTimer.Start();
        }

        public void SetHiddenForCapture(bool hidden)
        {
            // Do not hide - keeps HUD and side glow permanently visible
            EnsureTopMost();
        }

        public void Dismiss()
        {
            if (InvokeRequired) { Invoke(new Action(Dismiss)); return; }
            Close();
        }

        protected override void OnFormClosed(FormClosedEventArgs e)
        {
            UnregisterHotKey(Handle, HOTKEY_ID);
            try
            {
                if (leftGlow != null) { leftGlow.Close(); leftGlow.Dispose(); leftGlow = null; }
                if (rightGlow != null) { rightGlow.Close(); rightGlow.Dispose(); rightGlow = null; }
            }
            catch { }
            base.OnFormClosed(e);
        }

        protected override void WndProc(ref Message m)
        {
            if (m.Msg == WM_HOTKEY && m.WParam.ToInt32() == HOTKEY_ID)
            {
                engine.TriggerEmergencyStop();
                Close();
                return;
            }
            base.WndProc(ref m);
        }
    }

    public sealed class HeadlessKeepAliveForm : Form
    {
        const int WM_HOTKEY = 0x0312;
        readonly ControlEngine engine;

        public HeadlessKeepAliveForm(ControlEngine eng)
        {
            engine = eng;
            FormBorderStyle = FormBorderStyle.None;
            ShowInTaskbar = false;
            WindowState = FormWindowState.Minimized;
            Opacity = 0;
            Size = new Size(0, 0);
        }

        protected override void OnHandleCreated(EventArgs e)
        {
            base.OnHandleCreated(e);
            StatusOverlay.RegisterHotKey(Handle, StatusOverlay.HOTKEY_ID, 0, StatusOverlay.VK_ESCAPE);
        }

        protected override void WndProc(ref Message m)
        {
            if (m.Msg == WM_HOTKEY && m.WParam.ToInt32() == StatusOverlay.HOTKEY_ID)
            {
                engine.TriggerEmergencyStop();
                return;
            }
            base.WndProc(ref m);
        }

        protected override void OnFormClosed(FormClosedEventArgs e)
        {
            StatusOverlay.UnregisterHotKey(Handle, StatusOverlay.HOTKEY_ID);
            base.OnFormClosed(e);
        }
    }

    public sealed class ControlEngine
    {
        readonly string stateDir;
        readonly int idleTimeoutMinutes;
        readonly bool noOverlay;
        readonly JavaScriptSerializer serializer = new JavaScriptSerializer();

        TcpListener listener;
        Thread serverThread;
        System.Windows.Forms.Timer idleTimer;
        bool running = true;
        bool isStopped = false;
        DateTime lastActivityUtc = DateTime.UtcNow;

        StatusOverlay overlayForm;
        HeadlessKeepAliveForm headlessForm;
        ApplicationContext appContext;

        // In-memory UI Automation & Observe Cache
        long cachedWindowHandle = 0;
        string cachedSha256 = "";
        string cachedImagePath = "";
        List<AutomationElement> cachedElements = null;
        List<Dictionary<string, object>> cachedControls = null;
        DateTime cachedTime = DateTime.MinValue;
        long activeTargetHandle = 0;

        static CacheRequest uiaCacheRequest = null;
        static CacheRequest GetCacheRequest()
        {
            if (uiaCacheRequest == null)
            {
                CacheRequest cr = new CacheRequest();
                cr.Add(AutomationElement.NameProperty);
                cr.Add(AutomationElement.AutomationIdProperty);
                cr.Add(AutomationElement.ControlTypeProperty);
                cr.Add(AutomationElement.ClassNameProperty);
                cr.Add(AutomationElement.IsEnabledProperty);
                cr.Add(AutomationElement.IsOffscreenProperty);
                cr.Add(AutomationElement.IsKeyboardFocusableProperty);
                cr.Add(AutomationElement.BoundingRectangleProperty);
                cr.Add(InvokePattern.Pattern);
                cr.Add(ValuePattern.Pattern);
                cr.Add(SelectionItemPattern.Pattern);
                cr.TreeScope = TreeScope.Element | TreeScope.Descendants;
                cr.AutomationElementMode = AutomationElementMode.Full;
                uiaCacheRequest = cr;
            }
            return uiaCacheRequest;
        }

        public ControlEngine(string stateDirectory, int timeoutMinutes, bool headless)
        {
            stateDir = stateDirectory;
            idleTimeoutMinutes = timeoutMinutes;
            noOverlay = headless;
            Directory.CreateDirectory(stateDir);
            isStopped = File.Exists(Path.Combine(stateDir, "stop.flag"));
            serializer.MaxJsonLength = 50 * 1024 * 1024;
        }

        public void TriggerEmergencyStop()
        {
            isStopped = true;
            try { File.WriteAllText(Path.Combine(stateDir, "stop.flag"), DateTime.UtcNow.ToString("o")); } catch { }
            InvalidateCache();
            if (overlayForm != null) overlayForm.Dismiss();
        }

        public void InvalidateCache()
        {
            cachedWindowHandle = 0;
            cachedSha256 = "";
            cachedImagePath = "";
            cachedElements = null;
            cachedControls = null;
        }

        public void Start()
        {
            listener = new TcpListener(IPAddress.Loopback, 0);
            listener.Start();
            int port = ((IPEndPoint)listener.LocalEndpoint).Port;

            File.WriteAllText(Path.Combine(stateDir, "controller.port"), port.ToString());
            File.WriteAllText(Path.Combine(stateDir, "controller.pid"), Process.GetCurrentProcess().Id.ToString());
            File.WriteAllText(Path.Combine(stateDir, "ready.flag"), DateTime.UtcNow.ToString("o"));

            serverThread = new Thread(ListenLoop) { IsBackground = true };
            serverThread.Start();

            // Set up idle check timer on message loop
            idleTimer = new System.Windows.Forms.Timer();
            idleTimer.Interval = 500;
            idleTimer.Tick += (s, e) => {
                if (File.Exists(Path.Combine(stateDir, "exit.flag")))
                {
                    Stop();
                    return;
                }
                if (DateTime.UtcNow - lastActivityUtc > TimeSpan.FromMinutes(idleTimeoutMinutes))
                {
                    Stop();
                    return;
                }
            };
            idleTimer.Start();

            // Run Windows Message Loop on STA thread for HotKey & UI
            Application.EnableVisualStyles();
            appContext = new ApplicationContext();
            if (noOverlay)
            {
                headlessForm = new HeadlessKeepAliveForm(this);
                headlessForm.Show();
            }
            else
            {
                overlayForm = new StatusOverlay(this);
                overlayForm.Show();
            }
            Application.Run(appContext);
        }

        void ListenLoop()
        {
            while (running)
            {
                try
                {
                    TcpClient client = listener.AcceptTcpClient();
                    lastActivityUtc = DateTime.UtcNow;
                    Thread worker = new Thread(() => HandleClient(client)) { IsBackground = true };
                    worker.Start();
                }
                catch
                {
                    if (!running) break;
                }
            }
        }

        void HandleClient(TcpClient client)
        {
            IntPtr hDesk = NativeBridge.OpenDesktop("default", 0, false, 0x01FF);
            if (hDesk != IntPtr.Zero) NativeBridge.SetThreadDesktop(hDesk);
            try
            {
                using (NetworkStream stream = client.GetStream())
                using (StreamReader reader = new StreamReader(stream, Encoding.UTF8))
                using (StreamWriter writer = new StreamWriter(stream, Encoding.UTF8) { AutoFlush = true })
                {
                    string line = reader.ReadLine();
                    if (!string.IsNullOrEmpty(line))
                    {
                        string resp = ProcessCommand(line);
                        writer.WriteLine(resp);
                    }
                }
            }
            catch { }
            finally
            {
                if (hDesk != IntPtr.Zero) NativeBridge.CloseDesktop(hDesk);
                try { client.Close(); } catch { }
            }
        }

        public void Stop()
        {
            running = false;
            try { if (idleTimer != null) idleTimer.Stop(); } catch { }
            try { listener.Stop(); } catch { }
            if (overlayForm != null) overlayForm.Dismiss();
            if (headlessForm != null) {
                try { headlessForm.Close(); headlessForm.Dispose(); } catch { }
                headlessForm = null;
            }
            try { if (appContext != null) appContext.ExitThread(); } catch { }
            Application.Exit();
        }

        string ProcessCommand(string json)
        {
            Dictionary<string, object> req;
            try
            {
                req = serializer.Deserialize<Dictionary<string, object>>(json);
            }
            catch (Exception ex)
            {
                return serializer.Serialize(new Dictionary<string, object> { { "ok", false }, { "error", "Invalid JSON: " + ex.Message } });
            }

            string action = req.ContainsKey("action") ? Convert.ToString(req["action"]) : "";
            var res = ExecuteAction(action, req);
            return serializer.Serialize(res);
        }

        private bool IsForegroundForeign(IntPtr fg, long targetHwnd)
        {
            if (fg == IntPtr.Zero || targetHwnd == 0 || fg.ToInt64() == targetHwnd) return false;
            uint targetPid = 0, fgPid = 0;
            NativeBridge.GetWindowThreadProcessId(new IntPtr(targetHwnd), out targetPid);
            NativeBridge.GetWindowThreadProcessId(fg, out fgPid);
            if (targetPid != 0 && fgPid != 0 && targetPid == fgPid) return false;
            return true;
        }

        Dictionary<string, object> ExecuteAction(string action, Dictionary<string, object> req)
        {
            lastActivityUtc = DateTime.UtcNow;

            if (File.Exists(Path.Combine(stateDir, "stop.flag"))) isStopped = true;

            string[] mutating = new string[] {
                "invoke-control", "set-control-value", "focus-control", "select-control",
                "focus", "move", "click", "double-click", "drag", "down", "up", "mouse-down", "mouse-up", "scroll", "type", "key", "hotkey", "wait"
            };

            bool isMutating = (Array.IndexOf(mutating, action) >= 0 || action == "batch");
            if (isMutating)
            {
                if (isStopped)
                {
                    return new Dictionary<string, object> {
                        { "ok", false }, { "action", action },
                        { "error", "user_aborted: ESC was pressed. Computer control is latched off until explicit resume." }
                    };
                }
                if (activeTargetHandle != 0 && action != "focus")
                {
                    if (!NativeBridge.IsWindow(new IntPtr(activeTargetHandle)))
                    {
                        activeTargetHandle = 0;
                    }
                    else
                    {
                        IntPtr fg = NativeBridge.GetActiveForegroundWindow();
                        if (IsForegroundForeign(fg, activeTargetHandle))
                        {
                            NativeBridge.RawMouseEvent(0x0004, 0, 0, 0, UIntPtr.Zero);
                            NativeBridge.RawMouseEvent(0x0010, 0, 0, 0, UIntPtr.Zero);
                            TriggerEmergencyStop();
                            return new Dictionary<string, object> {
                                { "ok", false }, { "action", action },
                                { "error", "user_aborted: Alt+Tab detected! Target window lost focus. Actions paused immediately to protect your application." }
                            };
                        }
                    }
                }
                InvalidateCache();
            }

            if (overlayForm != null && !overlayForm.IsDisposed)
            {
                overlayForm.EnsureTopMost();
                if (isMutating) overlayForm.SetBusy(true);
            }

            try
            {
                switch (action)
                {
                    case "ping":
                        return new Dictionary<string, object> { { "ok", true }, { "action", action }, { "pong", true } };

                    case "session-start":
                        if (GetBool(req, "confirmResume", false))
                        {
                            isStopped = false;
                            try { File.Delete(Path.Combine(stateDir, "stop.flag")); } catch { }
                        }
                        if (!noOverlay && (overlayForm == null || overlayForm.IsDisposed))
                        {
                            try {
                                overlayForm = new StatusOverlay(this);
                                overlayForm.Show();
                            } catch { }
                        }
                        return new Dictionary<string, object> {
                            { "ok", true }, { "action", action },
                            { "session", new Dictionary<string, object> {
                                { "active", true },
                                { "stopped", isStopped },
                                { "controllerPid", Process.GetCurrentProcess().Id },
                                { "headless", noOverlay },
                                { "indicator", noOverlay ? "hidden" : "visible" }
                            }}
                        };

                    case "session-status":
                        return new Dictionary<string, object> {
                            { "ok", true }, { "action", action },
                            { "session", new Dictionary<string, object> {
                                { "active", true },
                                { "stopped", isStopped },
                                { "controllerPid", Process.GetCurrentProcess().Id },
                                { "headless", noOverlay },
                                { "activeTargetHandle", activeTargetHandle },
                                { "indicator", noOverlay ? "hidden" : "visible" }
                            }}
                        };

                    case "abort":
                        TriggerEmergencyStop();
                        return new Dictionary<string, object> { { "ok", true }, { "action", action }, { "stopped", true } };

                    case "resume":
                        isStopped = false;
                        try { File.Delete(Path.Combine(stateDir, "stop.flag")); } catch { }
                        return new Dictionary<string, object> { { "ok", true }, { "action", action }, { "stopped", false } };

                    case "clear-target":
                        activeTargetHandle = 0;
                        return new Dictionary<string, object> { { "ok", true }, { "action", action }, { "activeTargetHandle", 0 } };

                    case "session-stop":
                    case "exit":
                        Stop();
                        return new Dictionary<string, object> { { "ok", true }, { "action", action }, { "stopping", true } };

                    case "cursor":
                    {
                        NativeBridge.POINT p = new NativeBridge.POINT();
                        NativeBridge.RawGetCursorPos(out p);
                        return new Dictionary<string, object> { { "ok", true }, { "action", action }, { "x", p.X }, { "y", p.Y } };
                    }

                    case "windows":
                    {
                        return new Dictionary<string, object> { { "ok", true }, { "action", action }, { "windows", NativeBridge.GetWindows() } };
                    }

                    case "foreground":
                    {
                        return new Dictionary<string, object> { { "ok", true }, { "action", action }, { "window", NativeBridge.GetForeground() } };
                    }

                    case "focus":
                    {
                        long handle = GetLong(req, "handle", 0);
                        string title = GetString(req, "title", "");
                        WindowInfo target = FindTargetWindow(handle, title);
                        activeTargetHandle = target.handle;
                        bool focused = NativeBridge.FocusWindow(target.handle);
                        Thread.Sleep(GetDelay(req));
                        if (overlayForm != null && !overlayForm.IsDisposed) overlayForm.EnsureTopMost();
                        WindowInfo fg = NativeBridge.GetForeground();
                        bool ok = (fg != null && fg.handle == target.handle) || focused;
                        return new Dictionary<string, object> {
                            { "ok", ok }, { "action", action }, { "requested", target }, { "foreground", fg }, { "apiResult", focused }
                        };
                    }

                    case "move":
                    {
                        int x = GetInt(req, "x", 0);
                        int y = GetInt(req, "y", 0);
                        bool set = NativeBridge.RawSetCursorPos(x, y);
                        Thread.Sleep(GetDelay(req));
                        NativeBridge.POINT p = new NativeBridge.POINT();
                        NativeBridge.RawGetCursorPos(out p);
                        bool verified = (p.X == x && p.Y == y);
                        return new Dictionary<string, object> { { "ok", verified }, { "action", action }, { "x", p.X }, { "y", p.Y } };
                    }

                    case "click":
                    case "double-click":
                    {
                        int x = GetInt(req, "x", 0);
                        int y = GetInt(req, "y", 0);
                        string button = GetString(req, "button", "left").ToLowerInvariant();
                        uint down = 0x0002; uint up = 0x0004;
                        if (button == "right") { down = 0x0008; up = 0x0010; }
                        else if (button == "middle") { down = 0x0020; up = 0x0040; }

                        NativeBridge.RawSetCursorPos(x, y);
                        int count = (action == "double-click") ? 2 : 1;
                        for (int i = 0; i < count; i++)
                        {
                            if (isStopped) break;
                            NativeBridge.RawMouseEvent(down, 0, 0, 0, UIntPtr.Zero);
                            NativeBridge.RawMouseEvent(up, 0, 0, 0, UIntPtr.Zero);
                            if (count > 1) Thread.Sleep(80);
                        }
                        Thread.Sleep(GetDelay(req));
                        return new Dictionary<string, object> { { "ok", true }, { "action", action }, { "x", x }, { "y", y }, { "button", button } };
                    }

                    case "mouse-down":
                    case "down":
                    {
                        string button = GetString(req, "button", "left").ToLowerInvariant();
                        uint down = 0x0002;
                        if (button == "right") down = 0x0008;
                        else if (button == "middle") down = 0x0020;
                        if (req.ContainsKey("x") && req.ContainsKey("y"))
                        {
                            NativeBridge.RawSetCursorPos(GetInt(req, "x", 0), GetInt(req, "y", 0));
                        }
                        NativeBridge.RawMouseEvent(down, 0, 0, 0, UIntPtr.Zero);
                        return new Dictionary<string, object> { { "ok", true }, { "action", action } };
                    }

                    case "mouse-up":
                    case "up":
                    {
                        string button = GetString(req, "button", "left").ToLowerInvariant();
                        uint up = 0x0004;
                        if (button == "right") up = 0x0010;
                        else if (button == "middle") up = 0x0040;
                        if (req.ContainsKey("x") && req.ContainsKey("y"))
                        {
                            NativeBridge.RawSetCursorPos(GetInt(req, "x", 0), GetInt(req, "y", 0));
                        }
                        NativeBridge.RawMouseEvent(up, 0, 0, 0, UIntPtr.Zero);
                        return new Dictionary<string, object> { { "ok", true }, { "action", action } };
                    }

                    case "drag":
                    {
                        int fromX = GetInt(req, "fromX", GetInt(req, "x", 0));
                        int fromY = GetInt(req, "fromY", GetInt(req, "y", 0));
                        int toX = GetInt(req, "toX", 0);
                        int toY = GetInt(req, "toY", 0);
                        int steps = GetInt(req, "steps", 15);
                        if (steps < 1) steps = 1;

                        Rectangle bounds = Screen.PrimaryScreen.Bounds;
                        int sw = bounds.Width;
                        int sh = bounds.Height;

                        uint ax1 = (uint)(fromX * 65535 / (sw - 1));
                        uint ay1 = (uint)(fromY * 65535 / (sh - 1));

                        NativeBridge.RawSetCursorPos(fromX, fromY);
                        NativeBridge.RawMouseEvent(0x8001, ax1, ay1, 0, UIntPtr.Zero);
                        Thread.Sleep(20);
                        NativeBridge.RawMouseEvent(0x8002, ax1, ay1, 0, UIntPtr.Zero);
                        Thread.Sleep(20);

                        for (int s = 1; s <= steps; s++)
                        {
                            if (isStopped) break;
                            if (activeTargetHandle != 0)
                            {
                                if (!NativeBridge.IsWindow(new IntPtr(activeTargetHandle)))
                                {
                                    activeTargetHandle = 0;
                                }
                                else
                                {
                                    IntPtr curFg = NativeBridge.GetActiveForegroundWindow();
                                    if (IsForegroundForeign(curFg, activeTargetHandle))
                                    {
                                        uint curAx = (uint)(fromX * 65535 / (sw - 1));
                                        uint curAy = (uint)(fromY * 65535 / (sh - 1));
                                        NativeBridge.RawMouseEvent(0x8004, curAx, curAy, 0, UIntPtr.Zero);
                                        TriggerEmergencyStop();
                                        return new Dictionary<string, object> {
                                            { "ok", false }, { "action", action },
                                            { "error", "user_aborted: Alt+Tab detected! Target window lost focus. Actions paused immediately to protect your application." }
                                        };
                                    }
                                }
                            }
                            int cx = fromX + (toX - fromX) * s / steps;
                            int cy = fromY + (toY - fromY) * s / steps;
                            uint ax = (uint)(cx * 65535 / (sw - 1));
                            uint ay = (uint)(cy * 65535 / (sh - 1));
                            NativeBridge.RawSetCursorPos(cx, cy);
                            NativeBridge.RawMouseEvent(0x8001, ax, ay, 0, UIntPtr.Zero);
                            Thread.Sleep(8);
                        }

                        uint ax2 = (uint)(toX * 65535 / (sw - 1));
                        uint ay2 = (uint)(toY * 65535 / (sh - 1));
                        Thread.Sleep(20);
                        NativeBridge.RawMouseEvent(0x8004, ax2, ay2, 0, UIntPtr.Zero);
                        Thread.Sleep(GetDelay(req));
                        return new Dictionary<string, object> { { "ok", true }, { "action", action }, { "fromX", fromX }, { "fromY", fromY }, { "toX", toX }, { "toY", toY } };
                    }

                    case "scroll":
                    {
                        int delta = GetInt(req, "delta", 0);
                        if (delta == 0) throw new ArgumentException("Delta must be non-zero for scroll.");
                        uint wheel = (uint)(delta * 120);
                        IntPtr hDesk = NativeBridge.OpenDesktop("default", 0, false, 0x01FF);
                        if (hDesk != IntPtr.Zero) NativeBridge.SetThreadDesktop(hDesk);
                        NativeBridge.RawMouseEvent(0x0800, 0, 0, wheel, UIntPtr.Zero);
                        if (hDesk != IntPtr.Zero) NativeBridge.CloseDesktop(hDesk);
                        Thread.Sleep(GetDelay(req));
                        return new Dictionary<string, object> { { "ok", true }, { "action", action }, { "delta", delta } };
                    }

                    case "type":
                    {
                        string text = GetString(req, "text", "");
                        if (string.IsNullOrEmpty(text)) throw new ArgumentException("Text must be non-empty.");
                        IntPtr hDesk = NativeBridge.OpenDesktop("default", 0, false, 0x01FF);
                        if (hDesk != IntPtr.Zero) NativeBridge.SetThreadDesktop(hDesk);
                        foreach (char c in text)
                        {
                            if (isStopped) throw new InvalidOperationException("user_aborted: Aborted during typing.");
                            NativeBridge.SendUnicodeChar(c);
                            Thread.Sleep(2);
                        }
                        if (hDesk != IntPtr.Zero) NativeBridge.CloseDesktop(hDesk);
                        Thread.Sleep(GetDelay(req));
                        return new Dictionary<string, object> { { "ok", true }, { "action", action }, { "characters", text.Length } };
                    }

                    case "key":
                    case "hotkey":
                    {
                        List<byte> vkList = ResolveKeys(req);
                        if (vkList.Count == 0) throw new ArgumentException("At least one key is required.");
                        IntPtr hDesk = NativeBridge.OpenDesktop("default", 0, false, 0x01FF);
                        if (hDesk != IntPtr.Zero) NativeBridge.SetThreadDesktop(hDesk);
                        foreach (byte vk in vkList)
                        {
                            if (isStopped) break;
                            NativeBridge.RawKeybdEvent(vk, 0, 0, UIntPtr.Zero);
                        }
                        for (int i = vkList.Count - 1; i >= 0; i--)
                        {
                            NativeBridge.RawKeybdEvent(vkList[i], 0, NativeBridge.KEYEVENTF_KEYUP, UIntPtr.Zero);
                        }
                        if (hDesk != IntPtr.Zero) NativeBridge.CloseDesktop(hDesk);
                        Thread.Sleep(GetDelay(req));
                        return new Dictionary<string, object> { { "ok", true }, { "action", action }, { "keysCount", vkList.Count } };
                    }

                    case "wait":
                    {
                        int delay = GetInt(req, "delayMs", 150);
                        int remaining = delay;
                        while (remaining > 0)
                        {
                            if (isStopped) throw new InvalidOperationException("user_aborted: Latched stop during wait.");
                            int slice = Math.Min(50, remaining);
                            Thread.Sleep(slice);
                            remaining -= slice;
                        }
                        return new Dictionary<string, object> { { "ok", true }, { "action", action }, { "delayMs", delay } };
                    }

                    case "screen-info":
                    {
                        Rectangle v = SystemInformation.VirtualScreen;
                        return new Dictionary<string, object> {
                            { "ok", true }, { "action", action },
                            { "x", v.X }, { "y", v.Y }, { "width", v.Width }, { "height", v.Height },
                            { "monitors", Screen.AllScreens.Length }
                        };
                    }

                    case "screenshot":
                    {
                        Rectangle v = SystemInformation.VirtualScreen;
                        string outPath = GetString(req, "path", "");
                        string saved = CaptureScreen(v.Left, v.Top, v.Width, v.Height, outPath);
                        return new Dictionary<string, object> {
                            { "ok", true }, { "action", action }, { "path", saved },
                            { "x", v.X }, { "y", v.Y }, { "width", v.Width }, { "height", v.Height }
                        };
                    }

                    case "screenshot-window":
                    {
                        long handle = GetLong(req, "handle", 0);
                        string title = GetString(req, "title", "");
                        WindowInfo target = FindTargetWindow(handle, title);
                        if (target.minimized) throw new InvalidOperationException("Window is minimized.");
                        string outPath = GetString(req, "path", "");
                        string saved = CaptureScreen(target.x, target.y, target.width, target.height, outPath);
                        return new Dictionary<string, object> {
                            { "ok", true }, { "action", action }, { "path", saved }, { "window", target }
                        };
                    }

                    case "observe":
                    {
                        long handle = GetLong(req, "handle", 0);
                        string title = GetString(req, "title", "");
                        WindowInfo target = FindTargetWindow(handle, title);
                        if (target.minimized) throw new InvalidOperationException("Window is minimized.");

                        string outPath = GetString(req, "path", "");
                        string sha;
                        bool isFrameUnchanged;
                        string saved = CaptureAndHashScreen(target.x, target.y, target.width, target.height, outPath, out sha, out isFrameUnchanged);

                        bool forceRefresh = GetBool(req, "refresh", false);
                        bool changed = true;
                        List<Dictionary<string, object>> controls;

                        if (!forceRefresh && isFrameUnchanged && cachedWindowHandle == target.handle && cachedControls != null)
                        {
                            changed = false;
                            controls = cachedControls;
                        }
                        else
                        {
                            var uiaRoot = AutomationElement.FromHandle(new IntPtr(target.handle));
                            var rawElements = QueryUiaElements(uiaRoot, "", "", "", 200, false);
                            var dictList = new List<Dictionary<string, object>>();
                            foreach (var el in rawElements) dictList.Add(ControlToDict(el));

                            cachedWindowHandle = target.handle;
                            cachedSha256 = sha;
                            cachedElements = rawElements;
                            cachedControls = dictList;
                            cachedTime = DateTime.UtcNow;

                            controls = dictList;
                            changed = true;
                        }

                        return new Dictionary<string, object> {
                            { "ok", true }, { "action", action }, { "window", target },
                            { "path", saved }, { "sha256", sha }, { "changed", changed },
                            { "count", controls.Count }, { "controls", controls }
                        };
                    }

                    case "controls":
                    case "find-control":
                    {
                        long handle = GetLong(req, "handle", 0);
                        string title = GetString(req, "title", "");
                        WindowInfo target = FindTargetWindow(handle, title);

                        string ctrlName = GetString(req, "controlName", "");
                        string autoId = GetString(req, "automationId", "");
                        string ctrlType = GetString(req, "controlType", "");
                        int limit = GetInt(req, "limit", 120);
                        bool exact = GetBool(req, "exact", false);
                        bool forceRefresh = GetBool(req, "refresh", false);

                        List<Dictionary<string, object>> resultList = new List<Dictionary<string, object>>();

                        if (!forceRefresh && cachedWindowHandle == target.handle && cachedElements != null)
                        {
                            foreach (var el in cachedElements)
                            {
                                if (MatchesFilter(el, ctrlName, autoId, ctrlType, exact))
                                {
                                    resultList.Add(ControlToDict(el));
                                    if (resultList.Count >= limit) break;
                                }
                            }
                        }
                        else
                        {
                            var uiaRoot = AutomationElement.FromHandle(new IntPtr(target.handle));
                            var raw = QueryUiaElements(uiaRoot, ctrlName, autoId, ctrlType, limit, exact);
                            foreach (var el in raw) resultList.Add(ControlToDict(el));
                        }

                        return new Dictionary<string, object> {
                            { "ok", true }, { "action", action }, { "window", target },
                            { "count", resultList.Count }, { "controls", resultList }
                        };
                    }

                    case "invoke-control":
                    {
                        long handle = GetLong(req, "handle", 0);
                        string title = GetString(req, "title", "");
                        WindowInfo target = FindTargetWindow(handle, title);
                        var uiaRoot = AutomationElement.FromHandle(new IntPtr(target.handle));
                        AutomationElement element = FindSingleControl(uiaRoot, req);

                        string method = "";
                        object pattern = null;
                        if (element.TryGetCurrentPattern(InvokePattern.Pattern, out pattern))
                        {
                            ((InvokePattern)pattern).Invoke();
                            method = "InvokePattern";
                        }
                        else
                        {
                            var bounds = element.Current.BoundingRectangle;
                            if (bounds.IsEmpty || element.Current.IsOffscreen)
                                throw new InvalidOperationException("Control cannot be invoked and has no visible bounds.");
                            int cx = (int)Math.Round(bounds.X + (bounds.Width / 2));
                            int cy = (int)Math.Round(bounds.Y + (bounds.Height / 2));

                            IntPtr hDesk = NativeBridge.OpenDesktop("default", 0, false, 0x01FF);
                            if (hDesk != IntPtr.Zero) NativeBridge.SetThreadDesktop(hDesk);
                            NativeBridge.RawSetCursorPos(cx, cy);
                            NativeBridge.RawMouseEvent(0x0002, 0, 0, 0, UIntPtr.Zero);
                            NativeBridge.RawMouseEvent(0x0004, 0, 0, 0, UIntPtr.Zero);
                            if (hDesk != IntPtr.Zero) NativeBridge.CloseDesktop(hDesk);
                            method = "BoundingRectangleClick";
                        }
                        Thread.Sleep(GetDelay(req));
                        return new Dictionary<string, object> {
                            { "ok", true }, { "action", action }, { "method", method }, { "control", ControlToDict(element) }
                        };
                    }

                    case "set-control-value":
                    {
                        long handle = GetLong(req, "handle", 0);
                        string title = GetString(req, "title", "");
                        WindowInfo target = FindTargetWindow(handle, title);
                        var uiaRoot = AutomationElement.FromHandle(new IntPtr(target.handle));
                        AutomationElement element = FindSingleControl(uiaRoot, req);
                        string val = GetString(req, "value", "");

                        string method = "";
                        object pattern = null;
                        if (element.TryGetCurrentPattern(ValuePattern.Pattern, out pattern))
                        {
                            ValuePattern vp = (ValuePattern)pattern;
                            if (vp.Current.IsReadOnly) throw new InvalidOperationException("Selected control is read-only.");
                            vp.SetValue(val);
                            method = "ValuePattern";
                        }
                        else
                        {
                            var bounds = element.Current.BoundingRectangle;
                            if (bounds.IsEmpty || element.Current.IsOffscreen)
                                throw new InvalidOperationException("Selected control has no writable pattern or clickable bounds.");
                            int cx = (int)Math.Round(bounds.X + (bounds.Width / 2));
                            int cy = (int)Math.Round(bounds.Y + (bounds.Height / 2));

                            IntPtr hDesk = NativeBridge.OpenDesktop("default", 0, false, 0x01FF);
                            if (hDesk != IntPtr.Zero) NativeBridge.SetThreadDesktop(hDesk);
                            NativeBridge.RawSetCursorPos(cx, cy);
                            NativeBridge.RawMouseEvent(0x0002, 0, 0, 0, UIntPtr.Zero);
                            NativeBridge.RawMouseEvent(0x0004, 0, 0, 0, UIntPtr.Zero);
                            Thread.Sleep(80);
                            NativeBridge.RawKeybdEvent(0x11, 0, 0, UIntPtr.Zero);
                            NativeBridge.RawKeybdEvent((byte)'A', 0, 0, UIntPtr.Zero);
                            NativeBridge.RawKeybdEvent((byte)'A', 0, NativeBridge.KEYEVENTF_KEYUP, UIntPtr.Zero);
                            NativeBridge.RawKeybdEvent(0x11, 0, NativeBridge.KEYEVENTF_KEYUP, UIntPtr.Zero);

                            foreach (char c in val)
                            {
                                if (isStopped) throw new InvalidOperationException("user_aborted: Typing aborted.");
                                NativeBridge.SendUnicodeChar(c);
                            }
                            if (hDesk != IntPtr.Zero) NativeBridge.CloseDesktop(hDesk);
                            method = "BoundingRectangleKeyboard";
                        }
                        Thread.Sleep(GetDelay(req));
                        return new Dictionary<string, object> {
                            { "ok", true }, { "action", action }, { "method", method }, { "characters", val.Length }, { "control", ControlToDict(element) }
                        };
                    }

                    case "focus-control":
                    {
                        long handle = GetLong(req, "handle", 0);
                        string title = GetString(req, "title", "");
                        WindowInfo target = FindTargetWindow(handle, title);
                        var uiaRoot = AutomationElement.FromHandle(new IntPtr(target.handle));
                        AutomationElement element = FindSingleControl(uiaRoot, req);
                        element.SetFocus();
                        Thread.Sleep(GetDelay(req));
                        return new Dictionary<string, object> { { "ok", true }, { "action", action }, { "control", ControlToDict(element) } };
                    }

                    case "select-control":
                    {
                        long handle = GetLong(req, "handle", 0);
                        string title = GetString(req, "title", "");
                        WindowInfo target = FindTargetWindow(handle, title);
                        var uiaRoot = AutomationElement.FromHandle(new IntPtr(target.handle));
                        AutomationElement element = FindSingleControl(uiaRoot, req);
                        object pattern = null;
                        if (!element.TryGetCurrentPattern(SelectionItemPattern.Pattern, out pattern))
                            throw new InvalidOperationException("The control does not support SelectionItemPattern.");
                        ((SelectionItemPattern)pattern).Select();
                        Thread.Sleep(GetDelay(req));
                        return new Dictionary<string, object> { { "ok", true }, { "action", action }, { "control", ControlToDict(element) } };
                    }

                    case "batch":
                    {
                        object stepsObj = req.ContainsKey("steps") ? req["steps"] : null;
                        if (stepsObj is Dictionary<string, object>)
                        {
                            var dictSteps = (Dictionary<string, object>)stepsObj;
                            if (dictSteps.ContainsKey("value")) stepsObj = dictSteps["value"];
                        }
                        IEnumerable steps = stepsObj as IEnumerable;
                        if (steps == null) throw new ArgumentException("Batch requires a 'steps' array of actions.");

                        List<Dictionary<string, object>> stepResults = new List<Dictionary<string, object>>();
                        foreach (object item in steps)
                        {
                            if (isStopped)
                            {
                                return new Dictionary<string, object> {
                                    { "ok", false }, { "action", "batch" },
                                    { "error", "user_aborted: ESC pressed during batch execution." },
                                    { "completedSteps", stepResults }
                                };
                            }
                            Dictionary<string, object> stepReq = item as Dictionary<string, object>;
                            if (stepReq == null) continue;
                            string subAction = GetString(stepReq, "action", "");
                            if (activeTargetHandle != 0 && subAction != "focus")
                            {
                                if (!NativeBridge.IsWindow(new IntPtr(activeTargetHandle)))
                                {
                                    activeTargetHandle = 0;
                                }
                                else
                                {
                                    IntPtr curFg = NativeBridge.GetActiveForegroundWindow();
                                    if (IsForegroundForeign(curFg, activeTargetHandle))
                                    {
                                        NativeBridge.RawMouseEvent(0x0004, 0, 0, 0, UIntPtr.Zero);
                                        NativeBridge.RawMouseEvent(0x0010, 0, 0, 0, UIntPtr.Zero);
                                        TriggerEmergencyStop();
                                        return new Dictionary<string, object> {
                                            { "ok", false }, { "action", "batch" },
                                            { "error", "user_aborted: Alt+Tab detected! Target window lost focus. Actions paused immediately to protect your application." },
                                            { "failedStep", subAction },
                                            { "completedSteps", stepResults }
                                        };
                                    }
                                }
                            }
                            var subRes = ExecuteAction(subAction, stepReq);
                            stepResults.Add(subRes);
                            if (subRes.ContainsKey("ok") && !Convert.ToBoolean(subRes["ok"]))
                            {
                                return new Dictionary<string, object> {
                                    { "ok", false }, { "action", "batch" },
                                    { "error", "Batch step '" + subAction + "' failed: " + (subRes.ContainsKey("error") ? subRes["error"] : "unknown") },
                                    { "failedStep", subAction },
                                    { "completedSteps", stepResults }
                                };
                            }
                        }
                        return new Dictionary<string, object> {
                            { "ok", true }, { "action", "batch" }, { "results", stepResults }
                        };
                    }

                    default:
                        return new Dictionary<string, object> { { "ok", false }, { "action", action }, { "error", "Unknown action: " + action } };
                }
            }
            catch (Exception ex)
            {
                return new Dictionary<string, object> { { "ok", false }, { "action", action }, { "error", ex.Message } };
            }
            finally
            {
                if (overlayForm != null && !overlayForm.IsDisposed && isMutating)
                {
                    overlayForm.SetBusy(false);
                }
            }
        }

        WindowInfo FindTargetWindow(long handle, string title)
        {
            var windows = NativeBridge.GetWindows();
            if (handle != 0)
            {
                foreach (var w in windows) if (w.handle == handle) return w;
                throw new ArgumentException("No window found with handle " + handle);
            }
            if (!string.IsNullOrWhiteSpace(title))
            {
                foreach (var w in windows)
                {
                    if (w.title.IndexOf(title, StringComparison.OrdinalIgnoreCase) >= 0) return w;
                }
                // Check if application process is running
                Process[] procs = Process.GetProcesses();
                foreach (var p in procs)
                {
                    if (p.ProcessName.IndexOf(title, StringComparison.OrdinalIgnoreCase) >= 0)
                    {
                        if (p.MainWindowHandle != IntPtr.Zero)
                        {
                            var dw = NativeBridge.DescribeWindow(p.MainWindowHandle);
                            if (dw != null) return dw;
                        }
                    }
                }
                throw new ArgumentException("Target application '" + title + "' is not running. Please launch it first.");
            }
            var fg = NativeBridge.GetForeground();
            if (fg == null) throw new InvalidOperationException("No foreground window available.");
            return fg;
        }

        string CaptureAndHashScreen(int left, int top, int width, int height, string requestedPath, out string shaHash, out bool isUnchanged)
        {
            Rectangle vs = SystemInformation.VirtualScreen;
            int srcLeft = Math.Max(vs.Left, left);
            int srcTop = Math.Max(vs.Top, top);
            int srcRight = Math.Min(vs.Right, left + width);
            int srcBottom = Math.Min(vs.Bottom, top + height);
            int captureW = Math.Max(1, srcRight - srcLeft);
            int captureH = Math.Max(1, srcBottom - srcTop);

            if (overlayForm != null) overlayForm.SetHiddenForCapture(true);
            Thread.Sleep(30);
            try
            {
                using (Bitmap bmp = new Bitmap(captureW, captureH, PixelFormat.Format32bppArgb))
                {
                    using (Graphics g = Graphics.FromImage(bmp))
                    {
                        g.CopyFromScreen(srcLeft, srcTop, 0, 0, new Size(captureW, captureH), CopyPixelOperation.SourceCopy);
                    }

                    BitmapData bData = bmp.LockBits(new Rectangle(0, 0, captureW, captureH), ImageLockMode.ReadOnly, PixelFormat.Format32bppArgb);
                    try
                    {
                        int byteCount = Math.Abs(bData.Stride) * captureH;
                        byte[] rawPixels = new byte[byteCount];
                        Marshal.Copy(bData.Scan0, rawPixels, 0, byteCount);
                        using (var sha = SHA256.Create())
                        {
                            byte[] hashBytes = sha.ComputeHash(rawPixels);
                            shaHash = BitConverter.ToString(hashBytes).Replace("-", "").ToUpperInvariant();
                        }
                    }
                    finally
                    {
                        bmp.UnlockBits(bData);
                    }

                    if (string.IsNullOrWhiteSpace(requestedPath) && cachedSha256 == shaHash && !string.IsNullOrEmpty(cachedImagePath) && File.Exists(cachedImagePath))
                    {
                        isUnchanged = true;
                        return cachedImagePath;
                    }

                    isUnchanged = false;
                    string outputPath = requestedPath;
                    if (string.IsNullOrWhiteSpace(outputPath))
                    {
                        string dir = Path.Combine(Path.GetTempPath(), "antigravity-computer-use");
                        Directory.CreateDirectory(dir);
                        outputPath = Path.Combine(dir, "screen-" + DateTime.UtcNow.ToString("yyyyMMdd-HHmmss-fff") + ".png");
                    }
                    outputPath = Path.GetFullPath(outputPath);
                    string parent = Path.GetDirectoryName(outputPath);
                    if (!string.IsNullOrEmpty(parent)) Directory.CreateDirectory(parent);

                    bmp.Save(outputPath, ImageFormat.Png);
                    cachedImagePath = outputPath;
                    return outputPath;
                }
            }
            finally
            {
                if (overlayForm != null) overlayForm.SetHiddenForCapture(false);
            }
        }

        string CaptureScreen(int left, int top, int width, int height, string outputPath)
        {
            string dummySha;
            bool dummyUnchanged;
            return CaptureAndHashScreen(left, top, width, height, outputPath, out dummySha, out dummyUnchanged);
        }

        static bool MatchesFilter(AutomationElement el, string name, string autoId, string type, bool exact)
        {
            try
            {
                AutomationElement.AutomationElementInformation info;
                try { info = el.Cached; } catch { info = el.Current; }

                if (!string.IsNullOrWhiteSpace(name))
                {
                    string elName = info.Name;
                    if (exact) { if (!string.Equals(elName, name, StringComparison.OrdinalIgnoreCase)) return false; }
                    else { if (elName == null || elName.IndexOf(name, StringComparison.OrdinalIgnoreCase) < 0) return false; }
                }
                if (!string.IsNullOrWhiteSpace(autoId))
                {
                    if (!string.Equals(info.AutomationId, autoId, StringComparison.OrdinalIgnoreCase)) return false;
                }
                if (!string.IsNullOrWhiteSpace(type))
                {
                    string tName = (info.ControlType != null && info.ControlType.ProgrammaticName != null)
                        ? info.ControlType.ProgrammaticName.Replace("ControlType.", "") : "";
                    string targetT = type.Replace("ControlType.", "");
                    if (!string.Equals(tName, targetT, StringComparison.OrdinalIgnoreCase)) return false;
                }
                return true;
            }
            catch { return false; }
        }

        List<AutomationElement> QueryUiaElements(AutomationElement root, string name, string autoId, string type, int limit, bool exact)
        {
            AutomationElementCollection coll;
            using (GetCacheRequest().Activate())
            {
                coll = root.FindAll(TreeScope.Descendants, Condition.TrueCondition);
            }
            var list = new List<AutomationElement>();
            for (int i = 0; i < coll.Count; i++)
            {
                try
                {
                    var el = coll[i];
                    if (MatchesFilter(el, name, autoId, type, exact))
                    {
                        list.Add(el);
                        if (list.Count >= limit) break;
                    }
                }
                catch { }
            }
            return list;
        }

        AutomationElement FindSingleControl(AutomationElement root, Dictionary<string, object> req)
        {
            string name = GetString(req, "controlName", "");
            string autoId = GetString(req, "automationId", "");
            string type = GetString(req, "controlType", "");
            bool exact = GetBool(req, "exact", false);
            var list = QueryUiaElements(root, name, autoId, type, 1, exact);
            if (list.Count == 0) throw new InvalidOperationException("No matching UI Automation control found.");
            return list[0];
        }

        static Dictionary<string, object> ControlToDict(AutomationElement el)
        {
            AutomationElement.AutomationElementInformation info;
            try { info = el.Cached; } catch { info = el.Current; }

            var rect = info.BoundingRectangle;
            var dict = new Dictionary<string, object>();
            dict["name"] = info.Name ?? "";
            dict["automationId"] = info.AutomationId ?? "";
            dict["controlType"] = (info.ControlType != null && info.ControlType.ProgrammaticName != null)
                ? info.ControlType.ProgrammaticName.Replace("ControlType.", "") : "";
            dict["className"] = info.ClassName ?? "";
            dict["enabled"] = info.IsEnabled;
            dict["offscreen"] = info.IsOffscreen;
            dict["focusable"] = info.IsKeyboardFocusable;
            var patterns = new List<string>();
            try
            {
                foreach (var p in el.GetSupportedPatterns())
                {
                    patterns.Add(p.ProgrammaticName.Replace("PatternIdentifiers.", ""));
                }
            }
            catch { }
            dict["patterns"] = patterns;
            dict["x"] = (int)Math.Round(rect.X);
            dict["y"] = (int)Math.Round(rect.Y);
            dict["width"] = (int)Math.Round(rect.Width);
            dict["height"] = (int)Math.Round(rect.Height);
            return dict;
        }

        static string GetString(Dictionary<string, object> dict, string key, string def)
        {
            return dict.ContainsKey(key) && dict[key] != null ? Convert.ToString(dict[key]) : def;
        }

        static int GetInt(Dictionary<string, object> dict, string key, int def)
        {
            return dict.ContainsKey(key) && dict[key] != null ? Convert.ToInt32(dict[key]) : def;
        }

        static long GetLong(Dictionary<string, object> dict, string key, long def)
        {
            return dict.ContainsKey(key) && dict[key] != null ? Convert.ToInt64(dict[key]) : def;
        }

        static bool GetBool(Dictionary<string, object> dict, string key, bool def)
        {
            return dict.ContainsKey(key) && dict[key] != null ? Convert.ToBoolean(dict[key]) : def;
        }

        static int GetDelay(Dictionary<string, object> req)
        {
            return GetInt(req, "delayMs", 150);
        }

        static List<byte> ResolveKeys(Dictionary<string, object> req)
        {
            List<byte> list = new List<byte>();
            if (!req.ContainsKey("keys") || req["keys"] == null) return list;
            var obj = req["keys"];
            string[] rawKeys;
            if (obj is string) rawKeys = ((string)obj).Split(new char[] { ',' }, StringSplitOptions.RemoveEmptyEntries);
            else if (obj is IEnumerable)
            {
                List<string> sList = new List<string>();
                foreach (var it in (IEnumerable)obj) if (it != null) sList.Add(it.ToString());
                rawKeys = sList.ToArray();
            }
            else rawKeys = new string[0];

            Dictionary<string, byte> map = new Dictionary<string, byte>(StringComparer.OrdinalIgnoreCase) {
                { "CTRL", 0x11 }, { "CONTROL", 0x11 }, { "SHIFT", 0x10 }, { "ALT", 0x12 }, { "WIN", 0x5B },
                { "ENTER", 0x0D }, { "RETURN", 0x0D }, { "TAB", 0x09 }, { "ESC", 0x1B }, { "ESCAPE", 0x1B },
                { "SPACE", 0x20 }, { "BACKSPACE", 0x08 }, { "DELETE", 0x2E }, { "DEL", 0x2E }, { "INSERT", 0x2D },
                { "HOME", 0x24 }, { "END", 0x23 }, { "PAGEUP", 0x21 }, { "PAGEDOWN", 0x22 },
                { "LEFT", 0x25 }, { "UP", 0x26 }, { "RIGHT", 0x27 }, { "DOWN", 0x28 },
                { "F1", 0x70 }, { "F2", 0x71 }, { "F3", 0x72 }, { "F4", 0x73 }, { "F5", 0x74 }, { "F6", 0x75 },
                { "F7", 0x76 }, { "F8", 0x77 }, { "F9", 0x78 }, { "F10", 0x79 }, { "F11", 0x7A }, { "F12", 0x7B },
                { "[", 0xDB }, { "]", 0xDD }, { "OEM_4", 0xDB }, { "OEM_6", 0xDD }
            };

            foreach (string k in rawKeys)
            {
                string norm = k.Trim().ToUpperInvariant();
                if (map.ContainsKey(norm)) list.Add(map[norm]);
                else if (norm.Length == 1 && ((norm[0] >= 'A' && norm[0] <= 'Z') || (norm[0] >= '0' && norm[0] <= '9')))
                    list.Add((byte)norm[0]);
                else throw new ArgumentException("Unsupported key: " + k);
            }
            return list;
        }
    }

    public static class DesktopRunner
    {
        [DllImport("user32.dll", SetLastError = true)]
        public static extern IntPtr OpenDesktop(string lpszDesktop, uint dwFlags, bool fInherit, uint dwDesiredAccess);

        [DllImport("user32.dll", SetLastError = true)]
        public static extern bool SetThreadDesktop(IntPtr hDesktop);

        [DllImport("user32.dll", SetLastError = true)]
        public static extern bool CloseDesktop(IntPtr hDesktop);

        public static void Run(string stateDirectory, int idleTimeoutMinutes, bool noOverlay)
        {
            IntPtr hDesk = OpenDesktop("default", 0, false, 0x01FF);
            Thread t = new Thread(() => {
                try {
                    if (hDesk != IntPtr.Zero) SetThreadDesktop(hDesk);
                    ControlEngine engine = new ControlEngine(stateDirectory, idleTimeoutMinutes, noOverlay);
                    engine.Start();
                }
                catch (Exception ex) {
                    try {
                        File.WriteAllText(Path.Combine(stateDirectory, "crash.log"), ex.ToString());
                    } catch { }
                }
                finally {
                    if (hDesk != IntPtr.Zero) CloseDesktop(hDesk);
                }
            });
            t.SetApartmentState(ApartmentState.STA);
            t.Start();
            t.Join();
        }
    }
}
'@
}

try {
    [AntigravityComputerUse.DesktopRunner]::Run($StateDirectory, $IdleTimeoutMinutes, [bool]$NoOverlay)
}
finally {
    Remove-Item -LiteralPath $readyFile -Force -ErrorAction SilentlyContinue
    Remove-Item -LiteralPath $pidFile -Force -ErrorAction SilentlyContinue
    Remove-Item -LiteralPath $portFile -Force -ErrorAction SilentlyContinue
    Remove-Item -LiteralPath $exitFile -Force -ErrorAction SilentlyContinue
}
