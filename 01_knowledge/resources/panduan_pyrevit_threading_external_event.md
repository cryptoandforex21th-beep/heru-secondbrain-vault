# ⚡ Panduan Arsitektur Threading Revit API & pyRevit (Mencegah Fatal Crash)

> **Ringkasan Inti:** Revit API bersifat *strictly single-threaded*. Pemanggilan API apapun dari background thread (seperti HTTP route server pyRevit) akan langsung memicu `Unrecoverable Error` (fatal crash). Seluruh pemanggilan Revit API WAJIB didelegasikan ke Main Thread melalui mekanisme `IExternalEventHandler` (`ExternalEvent`).

---

## 1. ⚠️ Penyebab Fatal Crash (Unrecoverable Error)
1. **Background Threading Violation:** HTTP Route pyRevit melayani permintaan di worker thread terpisah. Ketika fungsi route langsung mengakses objek `doc`, `FilteredElementCollector`, atau `Transaction`, Revit mendeteksi pelanggaran akses lintas-thread dan langsung mematikan aplikasi.
2. **Missing Transaction:** Modifikasi model (membuat/mengubah/menghapus elemen) di luar blok `DB.Transaction` yang aktif akan memicu exception kritis.

---

## 2. 🛡️ Solusi: Pola IExternalEventHandler (External Event)

Pola ini memisahkan dua peran:
1. **HTTP Route Thread (Background):** Menerima request JSON, membungkus perintah ke dalam callback function, memanggil `external_event.Raise()`, lalu menunggu (`wait()`) sinyal dari Main Thread.
2. **Revit UI Thread (Main Thread):** Metode `Execute(uiapp)` dieksekusi oleh Revit saat idle. Di sinilah dokumen Revit diakses, dibungkus `Transaction`, dan dieksekusi secara aman.

---

## 3. 📦 Implementasi Kode Siap Pakai

### A. Modul Executor (`safe_executor.py`):
```python
# -*- coding: UTF-8 -*-
import sys
import logging
import threading
from pyrevit import DB, UI

logger = logging.getLogger(__name__)

class SafeRevitExecutor(UI.IExternalEventHandler):
    def __init__(self):
        self._action = None
        self._kwargs = {}
        self._doc_required = True
        self._use_transaction = False
        self._transaction_name = "pyRevit External Command"
        self._result = None
        self._exception = None
        self._completed_event = threading.Event()
        self._lock = threading.Lock()

    def Execute(self, uiapp):
        """Dijalankan HANYA di Revit Main UI Thread saat Revit Idle."""
        try:
            uidoc = getattr(uiapp, "ActiveUIDocument", None)
            doc = getattr(uidoc, "Document", None) if uidoc else None

            if self._doc_required and not doc:
                raise Exception("Tidak ada dokumen Revit aktif.")

            # Bungkus Transaction jika aksi memodifikasi dokumen
            if self._use_transaction and doc:
                trans = DB.Transaction(doc, self._transaction_name)
                trans.Start()
                try:
                    self._result = self._action(uiapp=uiapp, uidoc=uidoc, doc=doc, **self._kwargs)
                    trans.Commit()
                except Exception as t_err:
                    if trans.HasStarted() and not trans.HasEnded():
                        trans.RollBack()
                    raise t_err
            else:
                self._result = self._action(uiapp=uiapp, uidoc=uidoc, doc=doc, **self._kwargs)

        except Exception as ex:
            self._exception = ex
            logger.error("Error pada Main Thread: {}".format(str(ex)))
        finally:
            self._completed_event.set()

    def GetName(self):
        return "SafeRevitExecutor"

    def run_sync(self, external_event, action, kwargs=None, use_transaction=False, transaction_name="pyRevit Command", timeout=30.0, doc_required=True):
        """Dipanggil dari Route Thread. Menunggu Main Thread selesai."""
        with self._lock:
            self._action = action
            self._kwargs = kwargs or {}
            self._use_transaction = use_transaction
            self._transaction_name = transaction_name
            self._doc_required = doc_required
            self._result = None
            self._exception = None
            self._completed_event.clear()

            status = external_event.Raise()
            if status != UI.ExternalEventRequest.Accepted:
                raise Exception("ExternalEvent.Raise() ditolak: {}".format(status))

            signaled = self._completed_event.wait(timeout)
            if not signaled:
                raise Exception("Timeout menunggu eksekusi di Main Thread Revit.")

            if self._exception:
                raise self._exception

            return self._result

# Wajib diinisialisasi saat modul dimuat pertama kali di Main Thread Revit!
EXECUTOR = SafeRevitExecutor()
EXTERNAL_EVENT = UI.ExternalEvent.Create(EXECUTOR)
```

---

### B. Contoh Implementasi di Route Handler:
```python
from pyrevit import routes
from revit_mcp.safe_executor import EXECUTOR, EXTERNAL_EVENT
import json

@api.route("/create_wall/", methods=["POST"])
def create_wall_route(request):
    # Route ini berjalan di Background HTTP Thread
    data = json.loads(request.data) if isinstance(request.data, str) else request.data
    level_id = data.get("level_id")

    # Aksi yang akan dijalankan di Main UI Thread
    def execute_in_main_thread(uiapp, uidoc, doc, **kwargs):
        # DI SINI 100% AMAN MENGAKSES REVIT API
        from pyrevit import DB
        collector = DB.FilteredElementCollector(doc).OfClass(DB.Level)
        # Logika pembuatan elemen...
        return {"created_elements": 1, "status": "success"}

    # Delegasikan ke Main Thread dengan Transaction otomatis
    try:
        result = EXECUTOR.run_sync(
            EXTERNAL_EVENT,
            action=execute_in_main_thread,
            use_transaction=True,
            transaction_name="Membuat Dinding via pyRevit MCP",
            timeout=30.0
        )
        return routes.make_response(data=result, status=200)
    except Exception as e:
        return routes.make_response(data={"error": str(e)}, status=500)
```
