---
name: arena
description: >-
  Runs a structured adversarial tournament between multiple sub-agent reasoning
  strategies to produce a battle-tested, high-rigor solution for complex tasks.
  Equipped with Token-Shield: safe default agent sizing (4-8 agents instead of 100),
  subagent model gating (flash_lite/flash), and pre-flight token estimation.
  TRIGGER ONLY on explicit slash command `/arena` or when the user explicitly requests
  "arena tournament". NEVER auto-trigger on casual retries or corrections.
argument-hint: "[--micro (4 agents) | --quick (8 agents) | --standard (16 agents) | --agents N] <task>"
---

# ⚔️ The Arena Skill (Token-Shielded Edition)

Skill turnamen komparasi multi-strategi untuk memecahkan masalah arsitektur, koding, atau penalaran kompleks yang sulit diselesaikan dengan satu prompt biasa.

> 🛡️ **TOKEN SHIELD PROTOCOL (Anti-Drain Guardrail):**
> 1. **No Auto-Trigger:** Skill ini **DILARANG OTOMATIS BERJALAN** hanya karena pengguna bilang *"salah"*, *"ulang"*, atau *"coba lagi"*. Wajib dipicu secara sadar lewat `/arena` atau perintah eksplisit.
> 2. **Aman & Hemat Token secara Default:**
>    - **Default (`--micro`):** 4 Agen, 2 Ronde, **~19 total panggilan** (~40.000–60.000 token). Sangat hemat kuota!
>    - **Quick (`--quick`):** 8 Agen, 3 Ronde, **~43 total panggilan** (~100.000 token).
>    - **Standard (`--standard`):** 16 Agen, 4 Ronde, **~91 total panggilan** (~250.000 token).
>    - **Extreme (`--agents 100`):** 100 Agen, 7 Ronde, **595 total panggilan** (~2.500.000+ token). **WAJIB KONFIRMASI EKSPLISIT DARI USER!**
> 3. **Subagent Model Gating:** Dalam ekosistem Antigravity, subagent turnamen wajib diset ke `Model: "flash_lite"` atau `Model: "flash"` agar konsumsi token 95% lebih murah dibanding model `pro`.

---

## 🛠️ Cara Kerja Turnamen

1. **Spawn:** $N$ agen dibuat secara paralel. Setiap agen mendapat tugas yang sama persis, tetapi dipasangi **Kartu Strategi berbeda** (Kombinasi dari 15 pola penalaran, 12 alur kerja, dan 12 strategi = 2.160 kombinasi unik dari `strategies.json`).
2. **Attack:** Solusi dipasangkan satu lawan satu (bracket tournament). Agen A mengkritisi kelemahan solusi Agen B (mencari celah fatal/mayor/minor), dan sebaliknya.
3. **Defend:** Masing-masing agen merevisi solusinya berdasarkan kritik yang valid.
4. **Judge:** Agen juri independen menilai kedua solusi revisi berdasarkan [rubrik penilaian](rubric.md) (Correctness 30, Completeness 25, Robustness 20, Specificity 15, Clarity 10). Solusi dengan skor lebih tinggi lolos ke babak berikutnya.
5. **Winner:** Survivor terakhir yang bertahan menyajikan solusi terbaik dan rangkuman mengapa solusi tersebut mengalahkan seluruh alternatif lainnya.

---

## 💻 Eksekusi & State Machine (`bracket.py`)

Seluruh state turnamen dicatat secara deterministik di `.arena/<run>/arena.json`:

```bash
# 1. Rencana & Estimasi Token (Tanpa Menulis File)
python D:/SecondBrain/02_skills/arena/bracket.py plan --agents 4

# 2. Inisialisasi Turnamen
python D:/SecondBrain/02_skills/arena/bracket.py init --agents 4 --task-file .arena/task.md

# 3. Pengecekan Alur Berikutnya
python D:/SecondBrain/02_skills/arena/bracket.py next

# 4. Generate Prompt per Fase (spawn, attack, defend, judge)
python D:/SecondBrain/02_skills/arena/bracket.py prompts <phase>

# 5. Rekam Pemenang & Babak Berikutnya
python D:/SecondBrain/02_skills/arena/bracket.py collect
python D:/SecondBrain/02_skills/arena/bracket.py advance

# 6. Lihat Pemenang Akhir
python D:/SecondBrain/02_skills/arena/bracket.py winner
```

---

## 🛡️ Prosedur Orkestrasi Agen di Antigravity

Saat menjalankan `/arena`:
1. **Hitung Estimasi:** Informasikan ke Heru: *"Turnamen Arena: 4 agen, 2 ronde, estimasi ~19 panggilan subagent (~50k token). Lanjutkan?"*
2. **Tulis `.arena/task.md`:** Masukkan instruksi lengkap tanpa bias agar para agen mengeksplorasi strategi murni dari kartu masing-masing.
3. **Panggil Subagent secara Terkontrol:** Gunakan `invoke_subagent` dengan batch kecil (wave 4-8 agen) dan `Model: 'flash_lite'`.
4. **Sajikan Solusi Juara:** Tampilkan solusi pemenang akhir, alasan keunggulannya, dan serangan kritis yang berhasil ia tangkal.
