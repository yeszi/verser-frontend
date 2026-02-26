<template>
  <div class="root">

    <div class="hero">
      <div class="hero-icon">
        <svg width="36" height="36" viewBox="0 0 24 24" fill="none">
          <path d="M12 2L22 7V17L12 22L2 17V7L12 2Z" stroke="#0ea5e9" stroke-width="1.8"/>
          <path d="M12 8L16 10.5V15L12 17.5L8 15V10.5L12 8Z" fill="#0ea5e9" opacity="0.25"/>
          <circle cx="12" cy="12" r="2.2" fill="#0ea5e9"/>
        </svg>
      </div>
      <h1>VeriZh Chain</h1>
      <p>Sistem Verifikasi Sertifikat Digital</p>
      <p class="hero-sub">Universitas Maritim Raja Ali Haji</p>

      <!-- Tombol Scan QR -->
      <button class="scan-btn" @click="openScanner">
        <svg width="22" height="22" viewBox="0 0 24 24" fill="none">
          <path d="M3 7V5a2 2 0 0 1 2-2h2M17 3h2a2 2 0 0 1 2 2v2M21 17v2a2 2 0 0 1-2 2h-2M7 21H5a2 2 0 0 1-2-2v-2" stroke="currentColor" stroke-width="1.8" stroke-linecap="round"/>
          <rect x="7" y="7" width="10" height="10" rx="1" stroke="currentColor" stroke-width="1.8"/>
          <rect x="9.5" y="9.5" width="5" height="5" rx="0.5" fill="currentColor"/>
        </svg>
        Scan QR Sertifikat
      </button>

      <p class="hint-text">Scan QR Code pada sertifikat untuk verifikasi keasliannya</p>
    </div>


    <button class="lock-fab" @click="showLogin = true" title="Admin Login">
      <svg width="18" height="18" viewBox="0 0 24 24" fill="none">
        <rect x="5" y="11" width="14" height="10" rx="2" stroke="currentColor" stroke-width="1.8"/>
        <path d="M8 11V7a4 4 0 1 1 8 0v4" stroke="currentColor" stroke-width="1.8" stroke-linecap="round"/>
      </svg>
    </button>

    <div v-if="showLogin" class="modal-overlay" @click.self="showLogin = false">
      <div class="modal-card">
        <div class="modal-header">
          <div class="modal-icon">
            <svg width="20" height="20" viewBox="0 0 24 24" fill="none">
              <rect x="5" y="11" width="14" height="10" rx="2" stroke="#0ea5e9" stroke-width="1.8"/>
              <path d="M8 11V7a4 4 0 1 1 8 0v4" stroke="#0ea5e9" stroke-width="1.8" stroke-linecap="round"/>
            </svg>
          </div>
          <div>
            <p class="modal-title">Form Login</p>
            <p class="modal-sub">Hanya Untuk Pemegang Hak Akses</p>
          </div>
          <button class="modal-close" @click="showLogin = false">
            <svg width="16" height="16" viewBox="0 0 16 16" fill="none">
              <path d="M3 3l10 10M13 3L3 13" stroke="#94a3b8" stroke-width="1.5" stroke-linecap="round"/>
            </svg>
          </button>
        </div>

        <div v-if="error" class="error-box">{{ error }}</div>

        <form @submit.prevent="handleLogin" class="form">
          <div class="field">
            <label>Username</label>
            <input v-model="username" type="text" placeholder="Masukkan username" required :class="{ focused: focused === 'u' }" @focus="focused = 'u'" @blur="focused = null"/>
          </div>
          <div class="field">
            <label>Password</label>
            <div class="pw-wrap" :class="{ focused: focused === 'p' }">
              <input v-model="password" :type="showPw ? 'text' : 'password'" placeholder="Masukkan password" required @focus="focused = 'p'" @blur="focused = null"/>
              <button type="button" class="eye" @click="showPw = !showPw" tabindex="-1">
                <svg v-if="!showPw" width="16" height="16" viewBox="0 0 16 16" fill="none">
                  <path d="M1 8s2.5-5 7-5 7 5 7 5-2.5 5-7 5-7-5-7-5z" stroke="#94a3b8" stroke-width="1.3"/>
                  <circle cx="8" cy="8" r="2" stroke="#94a3b8" stroke-width="1.3"/>
                </svg>
                <svg v-else width="16" height="16" viewBox="0 0 16 16" fill="none">
                  <path d="M2 2l12 12M6.5 6.6A2 2 0 0 0 9.4 9.5M4.2 4.3C2.8 5.3 1.7 6.8 1 8c1.3 2.5 4 5 7 5a7 7 0 0 0 3.8-1.2M7 3.1A7.3 7.3 0 0 1 8 3c3 0 5.7 2.5 7 5a9 9 0 0 1-1.5 2.2" stroke="#94a3b8" stroke-width="1.3" stroke-linecap="round"/>
                </svg>
              </button>
            </div>
          </div>
          <button type="submit" class="btn" :disabled="loading">
            <span v-if="!loading">Masuk</span>
            <span v-else class="spin-row"><span class="spinner"></span> Memverifikasi...</span>
          </button>
        </form>

        <p class="footer">Made By Student Informatics Engineering</p>
      </div>
    </div>

    <!-- Pop Up Scanner QR -->
    <div v-if="showScanner" class="modal-overlay" @click.self="closeScanner">
      <div class="scanner-card">
        <div class="scanner-header">
          <p class="scanner-title">Scan QR Sertifikat</p>
          <button class="modal-close" @click="closeScanner">
            <svg width="16" height="16" viewBox="0 0 16 16" fill="none">
              <path d="M3 3l10 10M13 3L3 13" stroke="#94a3b8" stroke-width="1.5" stroke-linecap="round"/>
            </svg>
          </button>
        </div>

        <div class="scanner-body">
          <div class="video-wrap">
            <video ref="videoEl" class="video" autoplay playsinline></video>
            <div class="scan-frame">
              <div class="corner tl"></div>
              <div class="corner tr"></div>
              <div class="corner bl"></div>
              <div class="corner br"></div>
              <div class="scan-line"></div>
            </div>
          </div>
          <p class="scanner-hint">Arahkan kamera ke QR Code pada sertifikat</p>
          <p v-if="scanError" class="scan-error">{{ scanError }}</p>
        </div>
      </div>
    </div>

  </div>
</template>

<script>
import axios from 'axios'
import API_BASE_URL from '../config/api'

export default {
  name: 'LoginView',
  data() {
    return {
      username: '',
      password: '',
      loading: false,
      error: null,
      focused: null,
      showPw: false,
      showLogin: false,
      showScanner: false,
      scanError: null,
      stream: null,
      scanInterval: null,
      canvas: null,
      ctx: null,
    }
  },
  methods: {
    async handleLogin() {
      try {
        this.error = null
        this.loading = true
        const response = await axios.post(`${API_BASE_URL}/login`, {
          username: this.username,
          password: this.password
        })
        if (response.data.success) {
          localStorage.setItem('token', response.data.token)
          this.showLogin = false
          this.$router.push('/admin')
        } else {
          throw new Error(response.data.message || 'Login gagal')
        }
      } catch (err) {
        this.error = err.response?.data?.message || err.message
      } finally {
        this.loading = false
      }
    },

    async openScanner() {
      this.showScanner = true
      this.scanError = null
      await this.$nextTick()
      try {
        this.stream = await navigator.mediaDevices.getUserMedia({
          video: { facingMode: 'environment' }
        })
        this.$refs.videoEl.srcObject = this.stream
        this.canvas = document.createElement('canvas')
        this.ctx = this.canvas.getContext('2d')
        this.startScanning()
      } catch (e) {
        this.scanError = 'Kamera tidak dapat diakses. Pastikan izin kamera sudah diberikan.'
      }
    },

    startScanning() {
      this.scanInterval = setInterval(async () => {
        const video = this.$refs.videoEl
        if (!video || video.readyState !== 4) return
        this.canvas.width = video.videoWidth
        this.canvas.height = video.videoHeight
        this.ctx.drawImage(video, 0, 0)
        try {
          const imageData = this.ctx.getImageData(0, 0, this.canvas.width, this.canvas.height)
          if (window.jsQR) {
            const code = window.jsQR(imageData.data, imageData.width, imageData.height)
            if (code && code.data) {
              this.handleQRResult(code.data)
            }
          }
        } catch (e) {}
      }, 300)
    },

    handleQRResult(data) {
      this.closeScanner()
      try {
        const url = new URL(data)
        const path = url.pathname
        if (path.includes('/verify/')) {
          const hash = path.split('/verify/')[1]
          this.$router.push({ name: 'verify', params: { hash } })
        } else {
          this.scanError = 'QR Code tidak valid untuk sertifikat ini.'
          this.showScanner = true
          this.openScanner()
        }
      } catch (e) {
        this.scanError = 'QR Code tidak dikenali. Coba lagi.'
      }
    },

    closeScanner() {
      clearInterval(this.scanInterval)
      if (this.stream) {
        this.stream.getTracks().forEach(t => t.stop())
        this.stream = null
      }
      this.showScanner = false
    }
  },

  mounted() {
    // Load jsQR library
    if (!window.jsQR) {
      const script = document.createElement('script')
      script.src = 'https://cdn.jsdelivr.net/npm/jsqr@1.4.0/dist/jsQR.min.js'
      document.head.appendChild(script)
    }
  },

  beforeUnmount() {
    this.closeScanner()
  }
}
</script>

<style scoped>
@import url('https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:wght@400;500;600;700&display=swap');

* { box-sizing: border-box; margin: 0; padding: 0; }

.root {
  min-height: 100vh;
  display: flex;
  align-items: center;
  justify-content: center;
  background: linear-gradient(135deg, #f1f5f9 0%, #e0f2fe 100%);
  font-family: 'Plus Jakarta Sans', sans-serif;
  padding: 24px;
  position: relative;
}

/* Hero */
.hero {
  text-align: center;
  display: flex;
  flex-direction: column;
  align-items: center;
  gap: 10px;
  animation: up 0.45s cubic-bezier(0.34, 1.56, 0.64, 1) both;
}
@keyframes up {
  from { opacity: 0; transform: translateY(20px); }
  to   { opacity: 1; transform: translateY(0); }
}
.hero-icon {
  width: 72px; height: 72px;
  background: white;
  border-radius: 20px;
  display: flex;
  align-items: center;
  justify-content: center;
  box-shadow: 0 4px 20px rgba(14,165,233,0.15);
  margin-bottom: 4px;
}
.hero h1 {
  font-size: 26px;
  font-weight: 800;
  color: #0f172a;
  letter-spacing: -0.5px;
}
.hero > p {
  font-size: 14px;
  color: #475569;
  font-weight: 500;
}
.hero-sub {
  font-size: 11px !important;
  color: #94a3b8 !important;
  font-weight: 400 !important;
  margin-top: -4px;
}

.scan-btn {
  display: flex;
  align-items: center;
  gap: 10px;
  margin-top: 20px;
  padding: 16px 32px;
  background: #0ea5e9;
  border: none;
  border-radius: 14px;
  color: white;
  font-family: 'Plus Jakarta Sans', sans-serif;
  font-size: 15px;
  font-weight: 700;
  cursor: pointer;
  transition: all 0.18s;
  box-shadow: 0 4px 20px rgba(14,165,233,0.3);
}
.scan-btn:hover {
  background: #0284c7;
  transform: translateY(-2px);
  box-shadow: 0 8px 28px rgba(14,165,233,0.4);
}

.hint-text {
  font-size: 12px;
  color: #94a3b8;
  max-width: 260px;
  line-height: 1.5;
}

/* Tombol Gembok */
.lock-fab {
  position: fixed;
  bottom: 24px;
  right: 24px;
  width: 46px; height: 46px;
  background: white;
  border: 1.5px solid #e2e8f0;
  border-radius: 50%;
  display: flex;
  align-items: center;
  justify-content: center;
  cursor: pointer;
  color: #94a3b8;
  transition: all 0.18s;
  box-shadow: 0 2px 12px rgba(0,0,0,0.08);
}
.lock-fab:hover {
  border-color: #0ea5e9;
  color: #0ea5e9;
  box-shadow: 0 4px 16px rgba(14,165,233,0.2);
}

/* Modal Overlay */
.modal-overlay {
  position: fixed;
  inset: 0;
  background: rgba(15,23,42,0.5);
  display: flex;
  align-items: center;
  justify-content: center;
  z-index: 200;
  padding: 20px;
  backdrop-filter: blur(4px);
}

/* Modal Login */
.modal-card {
  background: white;
  border-radius: 20px;
  padding: 28px;
  width: 100%;
  max-width: 360px;
  box-shadow: 0 20px 60px rgba(0,0,0,0.15);
  animation: up 0.3s ease both;
}
.modal-header {
  display: flex;
  align-items: center;
  gap: 10px;
  margin-bottom: 20px;
}
.modal-icon {
  width: 38px; height: 38px;
  background: #e0f2fe;
  border-radius: 10px;
  display: flex;
  align-items: center;
  justify-content: center;
  flex-shrink: 0;
}
.modal-title { font-size: 14px; font-weight: 700; color: #0f172a; }
.modal-sub { font-size: 11px; color: #94a3b8; }
.modal-close {
  margin-left: auto;
  background: none;
  border: none;
  cursor: pointer;
  padding: 4px;
  display: flex;
  align-items: center;
}

.error-box {
  background: #fef2f2;
  border: 1px solid #fecaca;
  color: #ef4444;
  font-size: 13px;
  padding: 10px 14px;
  border-radius: 10px;
  margin-bottom: 16px;
  text-align: center;
}

.form { display: flex; flex-direction: column; gap: 14px; }

.field label {
  display: block;
  font-size: 12px;
  font-weight: 600;
  color: #475569;
  margin-bottom: 6px;
}
.field input {
  width: 100%;
  padding: 11px 14px;
  border: 1.5px solid #e2e8f0;
  border-radius: 10px;
  font-family: 'Plus Jakarta Sans', sans-serif;
  font-size: 14px;
  color: #0f172a;
  background: #f8fafc;
  outline: none;
  transition: border-color 0.18s, box-shadow 0.18s, background 0.18s;
}
.field input::placeholder { color: #cbd5e1; }
.field input:focus, .field input.focused {
  border-color: #0ea5e9;
  background: white;
  box-shadow: 0 0 0 3px rgba(14,165,233,0.1);
}

.pw-wrap {
  display: flex;
  align-items: center;
  border: 1.5px solid #e2e8f0;
  border-radius: 10px;
  background: #f8fafc;
  transition: border-color 0.18s, box-shadow 0.18s;
  padding-right: 12px;
}
.pw-wrap.focused { border-color: #0ea5e9; background: white; box-shadow: 0 0 0 3px rgba(14,165,233,0.1); }
.pw-wrap input { flex: 1; border: none; background: transparent; padding: 11px 14px; font-family: 'Plus Jakarta Sans', sans-serif; font-size: 14px; color: #0f172a; outline: none; }
.pw-wrap input::placeholder { color: #cbd5e1; }
.eye { background: none; border: none; cursor: pointer; display: flex; align-items: center; padding: 0; }

.btn {
  width: 100%;
  padding: 13px;
  background: #0ea5e9;
  border: none;
  border-radius: 10px;
  color: white;
  font-family: 'Plus Jakarta Sans', sans-serif;
  font-size: 14px;
  font-weight: 600;
  cursor: pointer;
  transition: background 0.18s, transform 0.12s, box-shadow 0.18s;
  box-shadow: 0 2px 12px rgba(14,165,233,0.25);
}
.btn:hover:not(:disabled) { background: #0284c7; box-shadow: 0 4px 20px rgba(14,165,233,0.35); transform: translateY(-1px); }
.btn:disabled { opacity: 0.55; cursor: not-allowed; }

.spin-row { display: flex; align-items: center; justify-content: center; gap: 8px; }
.spinner { width: 13px; height: 13px; border: 2px solid rgba(255,255,255,0.3); border-top-color: white; border-radius: 50%; animation: spin 0.7s linear infinite; }
@keyframes spin { to { transform: rotate(360deg); } }

.footer { text-align: center; font-size: 12px; color: #0ea5e9; margin-top: 20px; letter-spacing: 0.3px; font-weight: 700; }

/* Scanner */
.scanner-card {
  background: white;
  border-radius: 20px;
  width: 100%;
  max-width: 380px;
  overflow: hidden;
  box-shadow: 0 20px 60px rgba(0,0,0,0.2);
  animation: up 0.3s ease both;
}
.scanner-header {
  display: flex;
  align-items: center;
  justify-content: space-between;
  padding: 18px 20px;
  border-bottom: 1px solid #f1f5f9;
}
.scanner-title { font-size: 15px; font-weight: 700; color: #0f172a; }
.scanner-body { padding: 20px; display: flex; flex-direction: column; align-items: center; gap: 14px; }

.video-wrap {
  position: relative;
  width: 100%;
  aspect-ratio: 1;
  border-radius: 12px;
  overflow: hidden;
  background: #0f172a;
}
.video { width: 100%; height: 100%; object-fit: cover; }

.scan-frame {
  position: absolute;
  inset: 20px;
  pointer-events: none;
}
.corner {
  position: absolute;
  width: 24px; height: 24px;
  border-color: #0ea5e9;
  border-style: solid;
}
.tl { top: 0; left: 0; border-width: 3px 0 0 3px; border-radius: 4px 0 0 0; }
.tr { top: 0; right: 0; border-width: 3px 3px 0 0; border-radius: 0 4px 0 0; }
.bl { bottom: 0; left: 0; border-width: 0 0 3px 3px; border-radius: 0 0 0 4px; }
.br { bottom: 0; right: 0; border-width: 0 3px 3px 0; border-radius: 0 0 4px 0; }

.scan-line {
  position: absolute;
  left: 0; right: 0;
  height: 2px;
  background: linear-gradient(90deg, transparent, #0ea5e9, transparent);
  animation: scanMove 2s ease-in-out infinite;
}
@keyframes scanMove {
  0% { top: 0; }
  50% { top: calc(100% - 2px); }
  100% { top: 0; }
}

.scanner-hint { font-size: 13px; color: #64748b; text-align: center; }
.scan-error { font-size: 12px; color: #ef4444; text-align: center; background: #fef2f2; padding: 8px 14px; border-radius: 8px; }
</style>