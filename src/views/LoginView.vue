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

      <button class="scan-btn" @click="openScanner">
        <svg width="22" height="22" viewBox="0 0 24 24" fill="none">
          <path d="M3 7V5a2 2 0 0 1 2-2h2M17 3h2a2 2 0 0 1 2 2v2M21 17v2a2 2 0 0 1-2 2h-2M7 21H5a2 2 0 0 1-2-2v-2" stroke="currentColor" stroke-width="1.8" stroke-linecap="round"/>
          <rect x="7" y="7" width="10" height="10" rx="1" stroke="currentColor" stroke-width="1.8"/>
          <rect x="9.5" y="9.5" width="5" height="5" rx="0.5" fill="currentColor"/>
        </svg>
        Scan QR Sertifikat
      </button>

      <p class="hint-text">Scan QR Code pada sertifikat untuk verifikasi keasliannya</p>

      <div v-if="healthStatus.status" class="chain-status" :class="healthStatus.status.toLowerCase()">
        <div class="status-dot"></div>
        <span>Sistem: {{ healthStatus.message }}</span>
      </div>
    </div>

    <button class="lock-fab" @click="showLogin = true" title="Admin Login">
      <svg width="18" height="18" viewBox="0 0 24 24" fill="none">
        <rect x="5" y="11" width="14" height="10" rx="2" stroke="currentColor" stroke-width="1.8"/>
        <path d="M8 11V7a4 4 0 1 1 8 0v4" stroke="currentColor" stroke-width="1.8" stroke-linecap="round"/>
      </svg>
    </button>

    <div v-if="showLogin" class="modal-overlay" @click.self="handleModalClose">
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
          <button class="modal-close" @click="handleModalClose">
            <svg width="16" height="16" viewBox="0 0 16 16" fill="none">
              <path d="M3 3l10 10M13 3L3 13" stroke="#94a3b8" stroke-width="1.5" stroke-linecap="round"/>
            </svg>
          </button>
        </div>

        <div v-if="error" class="error-box" role="alert">{{ error }}</div>

        <div v-if="cooldownSeconds > 0" class="cooldown-box" role="status">
          Terlalu banyak percobaan. Coba lagi dalam {{ cooldownSeconds }} detik.
        </div>

        <form @submit.prevent="handleLogin" class="form" novalidate>
          <div class="field">
            <label for="login-username">Username</label>
            <input
              id="login-username"
              v-model="username"
              type="text"
              placeholder="Masukkan username"
              autocomplete="username"
              :disabled="loading || cooldownSeconds > 0"
              :class="{ focused: focused === 'u' }"
              @focus="focused = 'u'"
              @blur="focused = null"
              maxlength="64"
            />
          </div>
          <div class="field">
            <label for="login-password">Password</label>
            <div class="pw-wrap" :class="{ focused: focused === 'p' }">
              <input
                id="login-password"
                v-model="password"
                :type="showPw ? 'text' : 'password'"
                placeholder="Masukkan password"
                autocomplete="current-password"
                :disabled="loading || cooldownSeconds > 0"
                @focus="focused = 'p'"
                @blur="focused = null"
                maxlength="128"
              />
              <button type="button" class="eye" @click="showPw = !showPw" tabindex="-1" :aria-label="showPw ? 'Sembunyikan password' : 'Tampilkan password'">
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
          <button
            type="submit"
            class="btn"
            :disabled="loading || cooldownSeconds > 0 || !username.trim() || !password"
          >
            <span v-if="!loading">Masuk</span>
            <span v-else class="spin-row"><span class="spinner"></span> Memverifikasi...</span>
          </button>
        </form>

        <p class="footer">Made By Student Informatics Engineering</p>
      </div>
    </div>

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

const MAX_ATTEMPTS = 5
const COOLDOWN_DURATION = 240

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
      failedAttempts: 0,
      cooldownSeconds: 0,
      cooldownTimer: null,
      healthStatus: {
        status: '',
        message: 'Mengecek Integritas...'
      }
    }
  },
  methods: {
    async checkSystemHealth() {
      try {
        await axios.get(`${API_BASE_URL}/audit-chain`)
        this.healthStatus = { status: 'SECURE', message: 'Blockchain Aman & Utuh' }
      } catch (err) {
        if (err.response && err.response.status === 400) {
          this.healthStatus = { status: 'CORRUPTED', message: 'Terdeteksi Manipulasi Data!' }
        } else {
          this.healthStatus = { status: 'ERROR', message: 'Gagal Terhubung ke Chain' }
        }
      }
    },

    async handleLogin() {
      if (this.cooldownSeconds > 0) return
      if (!this.username.trim() || !this.password) {
        this.error = 'Username dan password wajib diisi'
        return
      }

      try {
        this.error = null
        this.loading = true
        const response = await axios.post(
          `${API_BASE_URL}/login`,
          { username: this.username.trim(), password: this.password },
          { timeout: 10000, headers: { 'Content-Type': 'application/json' } }
        )

        if (response.data.success) {
          this.failedAttempts = 0
          localStorage.setItem('token', response.data.token)
          this.clearForm()
          this.showLogin = false
          this.$router.push('/admin')
        } else {
          this.handleLoginFailure(response.data.message || 'Login gagal')
        }
      } catch (err) {
        const msg = err.response?.data?.message || 'Terjadi kesalahan, coba lagi'
        this.handleLoginFailure(msg)
      } finally {
        this.loading = false
      }
    },

    handleLoginFailure(message) {
      this.failedAttempts++
      this.error = message
      if (this.failedAttempts >= MAX_ATTEMPTS) {
        this.startCooldown()
      }
    },

    startCooldown() {
      this.cooldownSeconds = COOLDOWN_DURATION
      this.error = null
      clearInterval(this.cooldownTimer)
      this.cooldownTimer = setInterval(() => {
        this.cooldownSeconds--
        if (this.cooldownSeconds <= 0) {
          clearInterval(this.cooldownTimer)
          this.cooldownTimer = null
          this.failedAttempts = 0
        }
      }, 1000)
    },

    handleModalClose() {
      if (this.loading) return
      this.showLogin = false
      this.clearForm()
    },

    clearForm() {
      this.username = ''
      this.password = ''
      this.error = null
      this.showPw = false
    },

    async openScanner() {
      this.showScanner = true
      this.scanError = null
      await this.$nextTick()
      try {
        this.stream = await navigator.mediaDevices.getUserMedia({ video: { facingMode: 'environment' } })
        this.$refs.videoEl.srcObject = this.stream
        this.canvas = document.createElement('canvas')
        this.ctx = this.canvas.getContext('2d')
        this.startScanning()
      } catch (e) {
        this.scanError = 'Kamera tidak dapat diakses.'
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
            if (code && code.data) this.handleQRResult(code.data)
          }
        } catch (e) {}
      }, 300)
    },

    handleQRResult(data) {
      clearInterval(this.scanInterval)
      this.scanInterval = null
      try {
        const url = new URL(data)
        const path = url.pathname
        const allowedOrigin = new URL(API_BASE_URL).origin
        if (url.origin !== window.location.origin && url.origin !== allowedOrigin) {
          this.scanError = 'QR Code tidak valid.'
          this.startScanning()
          return
        }
        if (path.includes('/verify/')) {
          const hash = path.split('/verify/')[1]
          this.closeScanner()
          this.$router.push({ name: 'verify', params: { hash } })
        } else {
          this.scanError = 'Bukan sertifikat terbitan VeriZh.'
          this.startScanning()
        }
      } catch (e) {
        this.scanError = 'QR Code tidak dikenali.'
        this.startScanning()
      }
    },

    closeScanner() {
      clearInterval(this.scanInterval)
      this.scanInterval = null
      if (this.stream) {
        this.stream.getTracks().forEach(t => t.stop())
        this.stream = null
      }
      this.showScanner = false
      this.scanError = null
    }
  },
  mounted() {
    this.checkSystemHealth()
    if (!window.jsQR) {
      const script = document.createElement('script')
      script.src = 'https://cdn.jsdelivr.net/npm/jsqr@1.4.0/dist/jsQR.min.js'
      script.crossOrigin = 'anonymous'
      document.head.appendChild(script)
    }
  },
  beforeUnmount() {
    this.closeScanner()
    clearInterval(this.cooldownTimer)
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

.hero {
  display: flex;
  flex-direction: column;
  align-items: center;
  gap: 10px;
  text-align: center;
}
.hero-icon {
  width: 68px; height: 68px;
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

.chain-status {
  margin-top: 24px;
  display: flex;
  align-items: center;
  gap: 8px;
  padding: 8px 16px;
  border-radius: 100px;
  font-size: 12px;
  font-weight: 600;
}
.chain-status.secure { background: #f0fdf4; color: #16a34a; border: 1px solid #bbf7d0; }
.chain-status.secure .status-dot { background: #22c55e; box-shadow: 0 0 8px #22c55e; }
.chain-status.corrupted { background: #fef2f2; color: #dc2626; border: 1px solid #fecaca; animation: pulse-red 2s infinite; }
.chain-status.corrupted .status-dot { background: #ef4444; }
.chain-status.error { background: #f8fafc; color: #64748b; border: 1px solid #e2e8f0; }
.status-dot { width: 8px; height: 8px; border-radius: 50%; }

@keyframes pulse-red {
  0% { transform: scale(1); }
  50% { transform: scale(1.05); box-shadow: 0 0 12px rgba(239, 68, 68, 0.2); }
  100% { transform: scale(1); }
}

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
.lock-fab:hover { border-color: #0ea5e9; color: #0ea5e9; }

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

.modal-card {
  background: white;
  border-radius: 20px;
  padding: 28px;
  width: 100%;
  max-width: 360px;
  box-shadow: 0 20px 60px rgba(0,0,0,0.15);
  animation: up 0.3s ease both;
}
.modal-header { display: flex; align-items: center; gap: 10px; margin-bottom: 20px; }
.modal-icon { width: 38px; height: 38px; background: #e0f2fe; border-radius: 10px; display: flex; align-items: center; justify-content: center; }
.modal-title { font-size: 14px; font-weight: 700; color: #0f172a; }
.modal-sub { font-size: 11px; color: #94a3b8; }
.modal-close { margin-left: auto; background: none; border: none; cursor: pointer; }

.error-box { background: #fef2f2; border: 1px solid #fecaca; color: #ef4444; font-size: 13px; padding: 10px 14px; border-radius: 10px; margin-bottom: 16px; text-align: center; }
.cooldown-box { background: #fffbeb; border: 1px solid #fde68a; color: #d97706; font-size: 13px; padding: 10px 14px; border-radius: 10px; margin-bottom: 16px; text-align: center; font-weight: 600; }

.form { display: flex; flex-direction: column; gap: 14px; }
.field label { display: block; font-size: 12px; font-weight: 600; color: #475569; margin-bottom: 6px; }
.field input { width: 100%; padding: 11px 14px; border: 1.5px solid #e2e8f0; border-radius: 10px; font-size: 14px; background: #f8fafc; outline: none; }
.pw-wrap { display: flex; align-items: center; border: 1.5px solid #e2e8f0; border-radius: 10px; background: #f8fafc; padding-right: 12px; }
.pw-wrap input { flex: 1; border: none; background: transparent; padding: 11px 14px; outline: none; }
.eye { background: none; border: none; cursor: pointer; }

.btn { width: 100%; padding: 13px; background: #0ea5e9; border: none; border-radius: 10px; color: white; font-weight: 600; cursor: pointer; }
.btn:hover:not(:disabled) { background: #0284c7; transform: translateY(-1px); }
.btn:disabled { opacity: 0.55; cursor: not-allowed; }

.spinner { width: 13px; height: 13px; border: 2px solid rgba(255,255,255,0.3); border-top-color: white; border-radius: 50%; animation: spin 0.7s linear infinite; }
@keyframes spin { to { transform: rotate(360deg); } }
@keyframes up { from { opacity: 0; transform: translateY(16px); } to { opacity: 1; transform: translateY(0); } }

.footer { text-align: center; font-size: 12px; color: #0ea5e9; margin-top: 20px; font-weight: 700; }

.scanner-card { background: white; border-radius: 20px; width: 100%; max-width: 380px; overflow: hidden; animation: up 0.3s ease both; }
.scanner-header { display: flex; align-items: center; justify-content: space-between; padding: 18px 20px; border-bottom: 1px solid #f1f5f9; }
.scanner-body { padding: 20px; display: flex; flex-direction: column; align-items: center; gap: 14px; }
.video-wrap { position: relative; width: 100%; aspect-ratio: 1; border-radius: 12px; overflow: hidden; background: #0f172a; }
.video { width: 100%; height: 100%; object-fit: cover; }
.scan-frame { position: absolute; inset: 20px; pointer-events: none; }
.corner { position: absolute; width: 24px; height: 24px; border-color: #0ea5e9; border-style: solid; }
.tl { top: 0; left: 0; border-width: 3px 0 0 3px; border-radius: 4px 0 0 0; }
.tr { top: 0; right: 0; border-width: 3px 3px 0 0; border-radius: 0 4px 0 0; }
.bl { bottom: 0; left: 0; border-width: 0 0 3px 3px; border-radius: 0 0 0 4px; }
.br { bottom: 0; right: 0; border-width: 0 3px 3px 0; border-radius: 0 0 4px 0; }
.scan-line { position: absolute; left: 0; right: 0; height: 2px; background: linear-gradient(90deg, transparent, #0ea5e9, transparent); animation: scanMove 2s ease-in-out infinite; }
@keyframes scanMove { 0% { top: 0; } 50% { top: calc(100% - 2px); } 100% { top: 0; } }
.scan-error { font-size: 12px; color: #ef4444; background: #fef2f2; padding: 8px 14px; border-radius: 8px; }
</style>