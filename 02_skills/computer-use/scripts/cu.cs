using System;
using System.Collections.Generic;
using System.Diagnostics;
using System.IO;
using System.Net.Sockets;
using System.Text;
using System.Threading;
using System.Web.Script.Serialization;

namespace AntigravityComputerUse
{
    class Program
    {
        static int Main(string[] args)
        {
            if (args.Length == 0)
            {
                Console.WriteLine("{\"ok\":false,\"error\":\"No action specified. Usage: cu <action> [options]\"}");
                return 1;
            }

            string stateDir = Path.Combine(Environment.GetFolderPath(Environment.SpecialFolder.LocalApplicationData), "AntigravityComputerUse");
            string portFile = Path.Combine(stateDir, "controller.port");
            string pidFile = Path.Combine(stateDir, "controller.pid");
            string stopFile = Path.Combine(stateDir, "stop.flag");
            string exitFile = Path.Combine(stateDir, "exit.flag");

            // Parse arguments
            Dictionary<string, object> payload = new Dictionary<string, object>(StringComparer.OrdinalIgnoreCase);
            bool noOverlay = false;
            bool confirmResume = false;

            // Handle shorthand first argument: e.g. "cu cursor" or "cu session-status"
            int argIndex = 0;
            string firstArg = args[0];
            if (!firstArg.StartsWith("-") && !firstArg.StartsWith("/"))
            {
                payload["action"] = firstArg.ToLowerInvariant();
                argIndex = 1;
            }

            for (int i = argIndex; i < args.Length; i++)
            {
                string key = args[i].TrimStart('-', '/');
                string val = (i + 1 < args.Length && !args[i + 1].StartsWith("-") && !args[i + 1].StartsWith("/")) ? args[++i] : "true";

                if (string.Equals(key, "Action", StringComparison.OrdinalIgnoreCase))
                {
                    payload["action"] = val.ToLowerInvariant();
                }
                else if (string.Equals(key, "X", StringComparison.OrdinalIgnoreCase))
                {
                    int x; if (int.TryParse(val, out x)) payload["x"] = x;
                }
                else if (string.Equals(key, "Y", StringComparison.OrdinalIgnoreCase))
                {
                    int y; if (int.TryParse(val, out y)) payload["y"] = y;
                }
                else if (string.Equals(key, "FromX", StringComparison.OrdinalIgnoreCase))
                {
                    int fx; if (int.TryParse(val, out fx)) payload["fromX"] = fx;
                }
                else if (string.Equals(key, "FromY", StringComparison.OrdinalIgnoreCase))
                {
                    int fy; if (int.TryParse(val, out fy)) payload["fromY"] = fy;
                }
                else if (string.Equals(key, "ToX", StringComparison.OrdinalIgnoreCase))
                {
                    int tx; if (int.TryParse(val, out tx)) payload["toX"] = tx;
                }
                else if (string.Equals(key, "ToY", StringComparison.OrdinalIgnoreCase))
                {
                    int ty; if (int.TryParse(val, out ty)) payload["toY"] = ty;
                }
                else if (string.Equals(key, "Steps", StringComparison.OrdinalIgnoreCase))
                {
                    int s; if (int.TryParse(val, out s)) payload["steps"] = s;
                }
                else if (string.Equals(key, "Button", StringComparison.OrdinalIgnoreCase))
                {
                    payload["button"] = val;
                }
                else if (string.Equals(key, "Delta", StringComparison.OrdinalIgnoreCase))
                {
                    int delta; if (int.TryParse(val, out delta)) payload["delta"] = delta;
                }
                else if (string.Equals(key, "Text", StringComparison.OrdinalIgnoreCase))
                {
                    payload["text"] = val;
                }
                else if (string.Equals(key, "Keys", StringComparison.OrdinalIgnoreCase))
                {
                    payload["keys"] = val.Split(new char[] { ',' }, StringSplitOptions.RemoveEmptyEntries);
                }
                else if (string.Equals(key, "Title", StringComparison.OrdinalIgnoreCase))
                {
                    payload["title"] = val;
                }
                else if (string.Equals(key, "Handle", StringComparison.OrdinalIgnoreCase))
                {
                    long h; if (long.TryParse(val, out h)) payload["handle"] = h;
                }
                else if (string.Equals(key, "ControlName", StringComparison.OrdinalIgnoreCase))
                {
                    payload["controlName"] = val;
                }
                else if (string.Equals(key, "AutomationId", StringComparison.OrdinalIgnoreCase))
                {
                    payload["automationId"] = val;
                }
                else if (string.Equals(key, "ControlType", StringComparison.OrdinalIgnoreCase))
                {
                    payload["controlType"] = val;
                }
                else if (string.Equals(key, "Value", StringComparison.OrdinalIgnoreCase))
                {
                    payload["value"] = val;
                }
                else if (string.Equals(key, "Exact", StringComparison.OrdinalIgnoreCase))
                {
                    payload["exact"] = true;
                }
                else if (string.Equals(key, "Refresh", StringComparison.OrdinalIgnoreCase))
                {
                    payload["refresh"] = true;
                }
                else if (string.Equals(key, "NoOverlay", StringComparison.OrdinalIgnoreCase))
                {
                    noOverlay = true;
                }
                else if (string.Equals(key, "ConfirmResume", StringComparison.OrdinalIgnoreCase))
                {
                    confirmResume = true;
                }
                else if (string.Equals(key, "Limit", StringComparison.OrdinalIgnoreCase))
                {
                    int lim; if (int.TryParse(val, out lim)) payload["limit"] = lim;
                }
                else if (string.Equals(key, "Path", StringComparison.OrdinalIgnoreCase))
                {
                    payload["path"] = val;
                }
                else if (string.Equals(key, "DelayMs", StringComparison.OrdinalIgnoreCase))
                {
                    int d; if (int.TryParse(val, out d)) payload["delayMs"] = d;
                }
                else if (string.Equals(key, "Batch", StringComparison.OrdinalIgnoreCase) || string.Equals(key, "Steps", StringComparison.OrdinalIgnoreCase))
                {
                    try {
                        JavaScriptSerializer js = new JavaScriptSerializer();
                        payload["steps"] = js.DeserializeObject(val);
                    } catch {
                        Console.WriteLine("{\"ok\":false,\"action\":\"batch\",\"error\":\"Invalid JSON in -Batch/-Steps\"}");
                        return 1;
                    }
                }
                else if (string.Equals(key, "BatchPath", StringComparison.OrdinalIgnoreCase) || string.Equals(key, "StepsPath", StringComparison.OrdinalIgnoreCase))
                {
                    try {
                        if (File.Exists(val)) {
                            JavaScriptSerializer js = new JavaScriptSerializer();
                            string content = File.ReadAllText(val);
                            payload["steps"] = js.DeserializeObject(content);
                        } else {
                            Console.WriteLine("{\"ok\":false,\"action\":\"batch\",\"error\":\"BatchPath file not found: " + val + "\"}");
                            return 1;
                        }
                    } catch (Exception ex) {
                        Console.WriteLine("{\"ok\":false,\"action\":\"batch\",\"error\":\"Failed reading BatchPath: " + ex.Message + "\"}");
                        return 1;
                    }
                }
            }

            string action = payload.ContainsKey("action") ? Convert.ToString(payload["action"]) : "";
            if (string.IsNullOrEmpty(action))
            {
                Console.WriteLine("{\"ok\":false,\"error\":\"Missing action parameter.\"}");
                return 1;
            }
            if (action == "list-windows") { action = "windows"; payload["action"] = "windows"; }

            // Check emergency stop
            if (File.Exists(stopFile))
            {
                if (action == "resume" || (action == "session-start" && confirmResume))
                {
                    try { File.Delete(stopFile); } catch { }
                }
                else if (action != "session-status" && action != "session-stop")
                {
                    Console.WriteLine("{\"ok\":false,\"action\":\"" + action + "\",\"error\":\"user_aborted: ESC was pressed. Computer control is latched off until explicit resume.\"}");
                    return 130;
                }
            }

            // Determine port
            int port = GetActivePort(portFile, pidFile);

            // If session-start or mutating action and daemon is not running -> auto-launch daemon
            string[] mutating = new string[] {
                "invoke-control", "set-control-value", "focus-control", "select-control", "find-control",
                "focus", "move", "click", "double-click", "drag", "down", "up", "mouse-down", "mouse-up", "scroll", "type", "key", "hotkey", "wait", "batch"
            };

            if (port <= 0 && (action == "session-start" || Array.IndexOf(mutating, action) >= 0 || action == "observe" || action == "cursor" || action == "windows" || action == "foreground" || action == "screen-info"))
            {
                StartDaemon(stateDir, noOverlay);
                port = WaitForPort(portFile, 8000);
            }

            if (port > 0)
            {
                string response = SendTcp(port, payload);
                if (response != null)
                {
                    Console.WriteLine(response);
                    if (response.IndexOf("\"error\":\"user_aborted", StringComparison.OrdinalIgnoreCase) >= 0)
                        return 130;
                    if (response.IndexOf("\"ok\":false", StringComparison.OrdinalIgnoreCase) >= 0)
                        return 1;
                    return 0;
                }
            }

            // Fallback for session-status if controller not running
            if (action == "session-status")
            {
                bool isStopped = File.Exists(stopFile);
                Console.WriteLine("{\"ok\":true,\"action\":\"session-status\",\"session\":{\"active\":false,\"stopped\":" + (isStopped ? "true" : "false") + ",\"controllerPid\":null,\"indicator\":\"hidden\"}}");
                return 0;
            }

            if (action == "session-stop")
            {
                Console.WriteLine("{\"ok\":true,\"action\":\"session-stop\",\"session\":{\"active\":false}}");
                return 0;
            }

            Console.WriteLine("{\"ok\":false,\"action\":\"" + action + "\",\"error\":\"Control daemon is not running and could not be reached.\"}");
            return 1;
        }

        static int GetActivePort(string portFile, string pidFile)
        {
            try
            {
                if (!File.Exists(portFile) || !File.Exists(pidFile)) return 0;
                int pid = int.Parse(File.ReadAllText(pidFile).Trim());
                Process.GetProcessById(pid); // Throws if process dead
                return int.Parse(File.ReadAllText(portFile).Trim());
            }
            catch
            {
                return 0;
            }
        }

        static int WaitForPort(string portFile, int timeoutMs)
        {
            Stopwatch sw = Stopwatch.StartNew();
            while (sw.ElapsedMilliseconds < timeoutMs)
            {
                try
                {
                    if (File.Exists(portFile))
                    {
                        string txt = File.ReadAllText(portFile).Trim();
                        int p;
                        if (int.TryParse(txt, out p) && p > 0) return p;
                    }
                }
                catch { }
                Thread.Sleep(50);
            }
            return 0;
        }

        static void StartDaemon(string stateDir, bool noOverlay)
        {
            string baseDir = AppDomain.CurrentDomain.BaseDirectory;
            string controllerScript = Path.Combine(baseDir, "computer-use-controller.ps1");
            if (!File.Exists(controllerScript))
                controllerScript = Path.Combine(baseDir, "..", "scripts", "computer-use-controller.ps1");
            if (!File.Exists(controllerScript))
            {
                string userProfile = Environment.GetFolderPath(Environment.SpecialFolder.UserProfile);
                string configPath = Path.Combine(userProfile, ".gemini", "config", "skills", "computer-use", "scripts", "computer-use-controller.ps1");
                if (File.Exists(configPath)) controllerScript = configPath;
            }
            controllerScript = Path.GetFullPath(controllerScript);

            Directory.CreateDirectory(stateDir);
            try { File.Delete(Path.Combine(stateDir, "exit.flag")); } catch { }
            try { File.Delete(Path.Combine(stateDir, "ready.flag")); } catch { }
            try { File.Delete(Path.Combine(stateDir, "controller.port")); } catch { }
            try { File.Delete(Path.Combine(stateDir, "controller.pid")); } catch { }

            string args = "-STA -NoProfile -ExecutionPolicy Bypass -File \"" + controllerScript + "\" -StateDirectory \"" + stateDir + "\"";
            if (noOverlay) args += " -NoOverlay";

            ProcessStartInfo psi = new ProcessStartInfo("powershell.exe", args)
            {
                UseShellExecute = true,
                WindowStyle = ProcessWindowStyle.Hidden
            };
            Process.Start(psi);
        }

        static string SendTcp(int port, Dictionary<string, object> payload)
        {
            try
            {
                using (TcpClient client = new TcpClient())
                {
                    IAsyncResult ar = client.BeginConnect("127.0.0.1", port, null, null);
                    if (!ar.AsyncWaitHandle.WaitOne(2000))
                    {
                        client.Close();
                        return null;
                    }
                    client.EndConnect(ar);

                    JavaScriptSerializer js = new JavaScriptSerializer();
                    js.MaxJsonLength = 50 * 1024 * 1024;
                    string json = js.Serialize(payload);

                    NetworkStream stream = client.GetStream();
                    stream.ReadTimeout = 120000;
                    stream.WriteTimeout = 30000;

                    using (StreamWriter writer = new StreamWriter(stream, Encoding.UTF8) { AutoFlush = true })
                    using (StreamReader reader = new StreamReader(stream, Encoding.UTF8))
                    {
                        writer.WriteLine(json);
                        return reader.ReadLine();
                    }
                }
            }
            catch
            {
                return null;
            }
        }
    }
}
