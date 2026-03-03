<template>
  <div class="page-wrap">
    <div v-if="loading" class="loading-screen">
      <div class="spinner"></div>
      <p>Memverifikasi sertifikat...</p>
    </div>

    <div v-else-if="manipulated" class="invalid-screen">
      <div class="invalid-card manipulated">
        <div class="invalid-icon">!</div>
        <h2>Manipulasi Terdeteksi</h2>
        <p>Peringatan: Data pada sertifikat ini telah diubah secara ilegal dan tidak sesuai dengan catatan hash blockchain.</p>
        <button class="back-home" @click="$router.push('/')">Kembali ke Beranda</button>
      </div>
    </div>

    <div v-else-if="!data" class="invalid-screen">
      <div class="invalid-card">
        <div class="invalid-icon">✕</div>
        <h2>Sertifikat Tidak Valid</h2>
        <p>Data sertifikat tidak ditemukan dalam sistem kami.</p>
        <button @click="$router.push('/')">Kembali ke Beranda</button>
      </div>
    </div>

    <div v-else class="cert-outer">
      <div class="print-bar no-print">
        <div class="valid-badge">
          <svg width="16" height="16" viewBox="0 0 16 16" fill="none">
            <circle cx="8" cy="8" r="7" fill="#16a34a"/>
            <path d="M4.5 8l2.5 2.5 4.5-4.5" stroke="white" stroke-width="1.5" stroke-linecap="round" stroke-linejoin="round"/>
          </svg>
          Sertifikat Terverifikasi
        </div>
        <button class="print-btn" @click="printCert">
          <svg width="15" height="15" viewBox="0 0 16 16" fill="none">
            <path d="M4 6V2h8v4M4 12H2V7h12v5h-2M4 10h8v4H4v-4z" stroke="currentColor" stroke-width="1.4" stroke-linejoin="round"/>
          </svg>
          Cetak / Download PDF
        </button>
      </div>

      <div class="cert" id="certificate">
        <div class="border-top"></div>

        <div class="cert-header">
          <div class="header-left">
            <div class="logo-circle">
              <svg width="32" height="32" viewBox="0 0 36 36" fill="none">
                <path d="M18 3L33 11V25L18 33L3 25V11L18 3Z" stroke="#1e3a5f" stroke-width="1.8" fill="none"/>
                <path d="M18 9L27 14V22L18 27L9 22V14L18 9Z" fill="#1e3a5f" opacity="0.15"/>
                <circle cx="18" cy="18" r="3" fill="#1e3a5f"/>
              </svg>
            </div>
          </div>
          <div class="header-center">
            <p class="univ-name">UNIVERSITAS MARITIM RAJA ALI HAJI</p>
            <div class="header-divider"></div>
            <p class="cert-title">SERTIFIKAT</p>
            <p class="cert-subtitle">Certificate of Participation</p>
          </div>
          <div class="header-right"></div>
        </div>

        <div class="deco-lines">
          <div class="deco-line thick"></div>
          <div class="deco-line thin"></div>
        </div>

        <div class="cert-body">
          <p class="given-to">Diberikan kepada</p>
          <h1 class="recipient-name">{{ data.nama_peserta }}</h1>
          <div class="name-underline"></div>
          <p class="body-text">Telah berpartisipasi dan menyelesaikan kegiatan</p>
          <div class="event-box">
            <p class="event-name">{{ data.nama_event }}</p>
          </div>
          <div class="meta-grid">
            <div class="meta-item">
              <span class="meta-label">Lokasi</span>
              <span class="meta-value">{{ data.nama_lokasi }}</span>
            </div>
            <div class="meta-divider"></div>
            <div class="meta-item">
              <span class="meta-label">Tanggal Mulai</span>
              <span class="meta-value">{{ formatDate(data.waktu_mulai) }}</span>
            </div>
            <div class="meta-divider"></div>
            <div class="meta-item">
              <span class="meta-label">Tanggal Selesai</span>
              <span class="meta-value">{{ formatDate(data.waktu_selesai) }}</span>
            </div>
          </div>
          <p v-if="data.keterangan" class="keterangan-text">{{ data.keterangan }}</p>
        </div>

        <div class="cert-footer">
          <div class="footer-left"></div>
          <div class="footer-center">
            <div class="seal">
              <svg width="70" height="70" viewBox="0 0 70 70" fill="none">
                <circle cx="35" cy="35" r="33" stroke="#1e3a5f" stroke-width="1.5" stroke-dasharray="4 2"/>
                <circle cx="35" cy="35" r="27" stroke="#1e3a5f" stroke-width="1"/>
                <circle cx="35" cy="35" r="21" fill="#1e3a5f" opacity="0.06"/>
                <path d="M35 18L33 28H23L31 34L28 44L35 38L42 44L39 34L47 28H37L35 18Z" fill="#1e3a5f" opacity="0.5"/>
                <text x="35" y="57" text-anchor="middle" font-size="5" fill="#1e3a5f" font-family="serif" opacity="0.7">UMRAH • 2026</text>
              </svg>
            </div>
          </div>
          <div class="footer-right">
            <div class="qr-wrap">
              <img :src="qrUrl" alt="QR Verifikasi" class="qr-img" />
              <p class="qr-label">Scan untuk verifikasi</p>
            </div>
          </div>
        </div>

        <div class="deco-lines bottom">
          <div class="deco-line thin"></div>
          <div class="deco-line thick"></div>
        </div>
        <div class="border-bottom"></div>
      </div>
    </div>
  </div>
</template>

<script>
import { ref, computed, onMounted } from 'vue'
import { useRoute } from 'vue-router'
import axios from 'axios'
import API_BASE_URL from '../config/api'

export default {
  name: 'PublicVerify',
  setup() {
    const route = useRoute()
    const data = ref(null)
    const loading = ref(true)
    const manipulated = ref(false)

    const qrUrl = computed(() => {
      if (!data.value) return ''
      const url = window.location.href
      return `https://api.qrserver.com/v1/create-qr-code/?size=120x120&data=${encodeURIComponent(url)}&bgcolor=ffffff&color=1e3a5f&margin=4`
    })

    const formatDate = (val) => {
      if (!val) return '-'
      return new Date(val).toLocaleDateString('id-ID', {
        day: '2-digit', month: 'long', year: 'numeric'
      })
    }

    const printCert = () => {
      const originalTitle = document.title
      document.title = `Sertifikat - ${data.value.nama_peserta} - ${data.value.nama_event}`
      window.print()
      document.title = originalTitle
    }

    onMounted(async () => {
      try {
        const hash = route.params.hash
        const res = await axios.get(`${API_BASE_URL}/verify/${hash}`)
        if (res.data.status === 'VALID') {
          data.value = res.data.data
        }
      } catch (e) {
        if (e.response?.status === 400) {
          manipulated.value = true
        } else {
          console.error('Verify Error:', e)
        }
      } finally {
        loading.value = false
      }
    })

    return { data, loading, manipulated, qrUrl, formatDate, printCert }
  }
}
</script>

<style scoped>
@import url('https://fonts.googleapis.com/css2?family=Cormorant+Garamond:ital,wght@0,400;0,600;0,700;1,400;1,600&family=EB+Garamond:ital,wght@0,400;0,500;1,400&family=Cinzel:wght@400;600;700&display=swap');

* { box-sizing: border-box; margin: 0; padding: 0; }

.page-wrap {
  min-height: 100vh;
  background: #f0ece4;
  display: flex;
  flex-direction: column;
  align-items: center;
  padding: 32px 16px 48px;
  font-family: 'EB Garamond', serif;
}

.loading-screen {
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  min-height: 100vh;
  gap: 16px;
  color: #1e3a5f;
  font-size: 14px;
}
.spinner {
  width: 36px; height: 36px;
  border: 2px solid rgba(30,58,95,0.2);
  border-top-color: #1e3a5f;
  border-radius: 50%;
  animation: spin 0.8s linear infinite;
}
@keyframes spin { to { transform: rotate(360deg); } }

.invalid-screen {
  display: flex;
  align-items: center;
  justify-content: center;
  min-height: 100vh;
}
.invalid-card {
  background: white;
  border-radius: 16px;
  padding: 48px 40px;
  text-align: center;
  max-width: 380px;
  box-shadow: 0 8px 40px rgba(0,0,0,0.08);
}
.invalid-card.manipulated {
  border: 2px solid #ef4444;
  background: #fffafa;
}
.invalid-card.manipulated .invalid-icon {
  background: #ef4444;
  color: white;
  font-weight: bold;
  animation: pulse 1.5s infinite;
}
@keyframes pulse {
  0% { transform: scale(1); box-shadow: 0 0 0 0 rgba(239, 68, 68, 0.4); }
  70% { transform: scale(1.1); box-shadow: 0 0 0 10px rgba(239, 68, 68, 0); }
  100% { transform: scale(1); box-shadow: 0 0 0 0 rgba(239, 68, 68, 0); }
}
.invalid-icon {
  width: 56px; height: 56px;
  background: #fef2f2;
  border-radius: 50%;
  display: flex;
  align-items: center;
  justify-content: center;
  font-size: 22px;
  color: #ef4444;
  margin: 0 auto 20px;
}
.invalid-card h2 {
  font-family: 'Cinzel', serif;
  font-size: 18px;
  color: #1e293b;
  margin-bottom: 12px;
}
.invalid-card p { font-size: 14px; color: #64748b; margin-bottom: 24px; line-height: 1.6; }
.invalid-card button {
  padding: 10px 24px;
  background: #1e3a5f;
  color: white;
  border: none;
  border-radius: 8px;
  font-size: 13px;
  cursor: pointer;
}
.invalid-card .back-home { background: #ef4444; }

.print-bar {
  display: flex;
  align-items: center;
  justify-content: space-between;
  width: 100%;
  max-width: 860px;
  margin-bottom: 16px;
  padding: 0 4px;
}
.valid-badge {
  display: flex;
  align-items: center;
  gap: 7px;
  font-size: 13px;
  font-family: sans-serif;
  color: #16a34a;
  font-weight: 600;
}
.print-btn {
  display: flex;
  align-items: center;
  gap: 7px;
  padding: 9px 18px;
  background: #1e3a5f;
  color: white;
  border: none;
  border-radius: 8px;
  font-size: 13px;
  cursor: pointer;
}

.cert-outer { width: 100%; max-width: 860px; }
.cert { background: #fffef9; width: 100%; box-shadow: 0 8px 60px rgba(0,0,0,0.15); }
.border-top, .border-bottom { height: 10px; background: linear-gradient(90deg, #1e3a5f, #c9a84c, #1e3a5f); }

.deco-lines { display: flex; flex-direction: column; gap: 3px; padding: 6px 28px; }
.deco-lines.bottom { padding-bottom: 6px; }
.deco-line { height: 1px; background: #1e3a5f; opacity: 0.2; }
.deco-line.thick { height: 2px; opacity: 0.5; }

.cert-header { display: flex; align-items: center; justify-content: space-between; padding: 28px 44px 12px; gap: 20px; }
.header-left, .header-right { flex: 0 0 80px; }
.header-center { flex: 1; text-align: center; }
.logo-circle { width: 60px; height: 60px; border: 1.5px solid #1e3a5f; border-radius: 50%; display: flex; align-items: center; justify-content: center; }
.univ-name { font-family: 'Cinzel', serif; font-size: 12px; font-weight: 600; color: #1e3a5f; letter-spacing: 2px; margin-bottom: 8px; }
.header-divider { width: 80px; height: 1.5px; background: #c9a84c; margin: 0 auto 8px; }
.cert-title { font-family: 'Cinzel', serif; font-size: 28px; font-weight: 700; color: #1e3a5f; letter-spacing: 6px; }
.cert-subtitle { font-style: italic; font-size: 14px; color: #7a6a4f; }

.cert-body { padding: 24px 60px 20px; text-align: center; }
.given-to { font-style: italic; font-size: 16px; color: #7a6a4f; margin-bottom: 8px; }
.recipient-name { font-family: 'Cormorant Garamond', serif; font-size: 48px; font-weight: 600; font-style: italic; color: #1e3a5f; line-height: 1.1; margin-bottom: 8px; }
.name-underline { width: 200px; height: 1px; background: linear-gradient(90deg, transparent, #c9a84c, transparent); margin: 0 auto 18px; }
.body-text { font-size: 15px; color: #4a4033; margin-bottom: 14px; font-style: italic; }
.event-box { border-top: 1px solid rgba(30,58,95,0.15); border-bottom: 1px solid rgba(30,58,95,0.15); padding: 12px 40px; margin: 0 auto 20px; display: inline-block; }
.event-name { font-family: 'Cinzel', serif; font-size: 17px; font-weight: 600; color: #1e3a5f; }
.meta-grid { display: flex; align-items: center; justify-content: center; max-width: 600px; margin: 0 auto 14px; background: rgba(30,58,95,0.03); border: 1px solid rgba(30,58,95,0.1); border-radius: 4px; }
.meta-item { flex: 1; padding: 10px 16px; }
.meta-divider { width: 1px; height: 36px; background: rgba(30,58,95,0.15); }
.meta-label { display: block; font-size: 9px; text-transform: uppercase; letter-spacing: 1.5px; color: #94a3b8; margin-bottom: 3px; }
.meta-value { display: block; font-size: 13px; color: #1e3a5f; font-weight: 500; }
.keterangan-text { font-size: 13px; font-style: italic; color: #7a6a4f; }

.cert-footer { display: flex; align-items: center; justify-content: space-between; padding: 20px 44px 24px; gap: 20px; }
.footer-left, .footer-right { flex: 1; }
.footer-center { flex: 0 0 auto; }
.qr-wrap { display: flex; flex-direction: column; align-items: flex-end; gap: 6px; }
.qr-img { width: 90px; height: 90px; border: 1px solid rgba(30,58,95,0.2); padding: 4px; background: white; }
.qr-label { font-size: 9px; color: #94a3b8; }
.seal { display: flex; justify-content: center; }

@media print {
  .no-print { display: none !important; }
  .page-wrap { background: white; padding: 0; }
  .cert { box-shadow: none; }
  @page { size: A4 landscape; margin: 8mm; }
}

@media (max-width: 640px) {
  .cert-header { flex-direction: column; padding: 20px; }
  .cert-body { padding: 20px 24px; }
  .recipient-name { font-size: 32px; }
  .meta-grid { flex-direction: column; }
  .meta-divider { width: 80%; height: 1px; }
  .cert-footer { flex-direction: column; }
  .qr-wrap { align-items: center; }
}
</style>