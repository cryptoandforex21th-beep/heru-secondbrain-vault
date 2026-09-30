# -*- coding: UTF-8 -*-
"""
Safe External Event Dispatcher for pyRevit / Revit API
Memastikan semua pemanggilan Revit API (Document, Transaction, FilteredElementCollector)
dieksekusi secara aman di Revit Main UI Thread, mencegah fatal crash (Unrecoverable Error).
"""
import sys
import time
import logging
import threading
from pyrevit import DB, UI

logger = logging.getLogger(__name__)


class SafeRevitExecutor(UI.IExternalEventHandler):
    """
    Implementasi IExternalEventHandler untuk mendelegasikan tugas
    dari background thread (HTTP route server) ke Revit Main UI Thread.
    """
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
        """
        Dijalankan HANYA di Revit Main UI Thread saat Revit dalam kondisi Idle.
        """
        try:
            uidoc = getattr(uiapp, "ActiveUIDocument", None)
            doc = getattr(uidoc, "Document", None) if uidoc else None

            if self._doc_required and not doc:
                raise Exception("Tidak ada dokumen Revit aktif yang sedang dibuka.")

            # Jika tugas memodifikasi dokumen, bungkus otomatis dengan Transaction
            if self._use_transaction and doc:
                trans = DB.Transaction(doc, self._transaction_name)
                trans.Start()
                try:
                    # Jalankan aksi yang diminta
                    self._result = self._action(uiapp=uiapp, uidoc=uidoc, doc=doc, **self._kwargs)
                    trans.Commit()
                except Exception as t_err:
                    if trans.HasStarted() and not trans.HasEnded():
                        trans.RollBack()
                    raise t_err
            else:
                # Pembacaan data (read-only) atau aksi tanpa transaction
                self._result = self._action(uiapp=uiapp, uidoc=uidoc, doc=doc, **self._kwargs)

        except Exception as ex:
            self._exception = ex
            logger.error("Error pada Revit Main Thread: {}".format(str(ex)))
        finally:
            # Sinyalkan ke background HTTP thread bahwa eksekusi selesai
            self._completed_event.set()

    def GetName(self):
        return "SafeRevitExecutor"

    def run_sync(self, external_event, action, kwargs=None, use_transaction=False, transaction_name="pyRevit Command", timeout=30.0, doc_required=True):
        """
        Dipanggil dari HTTP/Route background thread.
        Membungkus aksi, memanggil Raise(), dan menunggu hingga Main Thread selesai.
        """
        with self._lock:
            self._action = action
            self._kwargs = kwargs or {}
            self._use_transaction = use_transaction
            self._transaction_name = transaction_name
            self._doc_required = doc_required
            self._result = None
            self._exception = None
            self._completed_event.clear()

            # Panggil Raise() agar event dimasukkan ke antrean Main Thread Revit
            status = external_event.Raise()
            if status != UI.ExternalEventRequest.Accepted:
                raise Exception("ExternalEvent.Raise() ditolak oleh Revit: {}".format(status))

            # Tunggu Main Thread selesai mengeksekusi
            signaled = self._completed_event.wait(timeout)
            if not signaled:
                raise Exception("Timeout ({} detik) menunggu giliran eksekusi di Revit Main UI Thread.".format(timeout))

            if self._exception:
                raise self._exception

            return self._result


# Inisialisasi Singleton Instance & ExternalEvent
# WAJIB diinisialisasi saat modul dimuat pertama kali di Main Thread Revit!
EXECUTOR = SafeRevitExecutor()
EXTERNAL_EVENT = UI.ExternalEvent.Create(EXECUTOR)
