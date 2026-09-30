# 🌵 PROJECT: Kaktus Towers 80M & Generative VAE Architecture
> **Status:** `Active / Research & Prototyping`  
> **Source Directory:** `D:\Proyek Arsitektur ML`  
> **Tech Stack:** Rhino 8, Grasshopper (Hops), PyTorch (VAE / Variational Autoencoder), Python 3.11/3.14  
> **Author:** Heru Ardiansyah (GradiEnt Studio)

---

## 1. 📐 Deskripsi & Konsep Proyek
Proyek komputasi arsitektur generatif yang mengintegrasikan model Machine Learning (VAE) langsung dengan viewport 3D Rhino dan Grasshopper. 

### Fitur Kunci:
1. **Kaktus Towers 80M (`KAKTUS_TOWERS_80M_SITE_READY.3dm`):**
   * Menara tinggi 80 meter dengan geometri fasad terinspirasi struktur kaktus (pelindung pasif terhadap radiasi termal).
   * Generator parametrik otomatis via `KAKTUS_TOWER_GENERATOR.py` dan `KAKTUS_TOWERS_80M_LIVE.ghx`.
2. **Twist VAE Paviliun (`TWIST_VAE_MORPH.ghx`):**
   * Melatih neural network VAE dari 12 parameter desain arsitektur nyata.
   * Menghasilkan 4 rail kurva memanjang yang di-Loft secara dinamis.
   * Ruang laten (*latent space*) dapat diinterpolasi secara *real-time* untuk menghasilkan variasi bentuk (*morphing*) di Grasshopper.
3. **AI Bridge (`AI_BRIDGE.ghx`):**
   * Jembatan komunikasi dua arah antara script AI eksternal dengan kanvas Grasshopper.

---

## 2. 📂 File-File Inti:
* Model 3D: `D:\Proyek Arsitektur ML\KAKTUS_TOWERS_80M_SITE_READY.3dm`
* Grasshopper Scripts: `TWIST_VAE_GENERATE.ghx`, `TWIST_VAE_MORPH.ghx`, `KAKTUS_TOWERS_80M_LIVE.ghx`
* Python Builders: `GHX_BUILDER.py`, `AI_BRIDGE_BUILDER.py`, `build_minimalist_house.py`
* Panduan Setup: `D:\Proyek Arsitektur ML\PANDUAN_TWIST_VAE.md`

---
*Indexed in SecondBrain for seamless multi-agent access by Ai and Profesor LUNA.*
