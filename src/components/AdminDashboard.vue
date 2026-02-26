<template>
  <div class="root">
    <aside class="sidebar" :class="{ open: sidebarOpen }">
      <div class="sidebar-header">
        <div class="sidebar-logo">
          <svg width="22" height="22" viewBox="0 0 36 36" fill="none">
            <path d="M18 3L33 11V25L18 33L3 25V11L18 3Z" stroke="white" stroke-width="1.8" fill="none"/>
            <path d="M18 9L27 14V22L18 27L9 22V14L18 9Z" fill="white" opacity="0.2"/>
            <circle cx="18" cy="18" r="3" fill="white"/>
          </svg>
        </div>
        <div>
          <p class="sidebar-title">Admin Dashboard</p>
          <p class="sidebar-sub">VeriZh Chain</p>
        </div>
        <button class="sidebar-close" @click="sidebarOpen = false">✕</button>
      </div>

      <nav class="sidebar-nav">
        <button @click="setTab('issue')" :class="{ active: activeTab === 'issue' }" class="nav-item">
          <svg width="18" height="18" viewBox="0 0 20 20" fill="none">
            <path d="M10 4v12M4 10h12" stroke="currentColor" stroke-width="1.8" stroke-linecap="round"/>
          </svg>
          Terbitkan Sertifikat
        </button>
        <button @click="setTab('data')" :class="{ active: activeTab === 'data' }" class="nav-item">
          <svg width="18" height="18" viewBox="0 0 20 20" fill="none">
            <rect x="3" y="5" width="14" height="2" rx="1" fill="currentColor"/>
            <rect x="3" y="9" width="14" height="2" rx="1" fill="currentColor"/>
            <rect x="3" y="13" width="9" height="2" rx="1" fill="currentColor"/>
          </svg>
          Data Sertifikat
          <span v-if="tableData.length > 0" class="badge">{{ tableData.length }}</span>
        </button>
      </nav>

      <button @click="logout" class="logout-btn">
        <svg width="16" height="16" viewBox="0 0 20 20" fill="none">
          <path d="M13 3h4v14h-4M8 14l4-4-4-4M2 10h10" stroke="currentColor" stroke-width="1.6" stroke-linecap="round" stroke-linejoin="round"/>
        </svg>
        Logout
      </button>
    </aside>

    <div class="overlay" v-if="sidebarOpen" @click="sidebarOpen = false"></div>

    <main class="main">
      <header class="topbar">
        <button class="hamburger" @click="sidebarOpen = true">
          <span></span><span></span><span></span>
        </button>
        <div class="topbar-title">
          <p class="page-title">{{ activeTab === 'issue' ? 'Terbitkan Sertifikat' : 'Data Sertifikat' }}</p>
          <p class="page-sub">Universitas Maritim Raja Ali Haji</p>
        </div>
        <div class="topbar-logo">
          <svg width="18" height="18" viewBox="0 0 36 36" fill="none">
            <path d="M18 3L33 11V25L18 33L3 25V11L18 3Z" stroke="#6366f1" stroke-width="1.8" fill="none"/>
            <circle cx="18" cy="18" r="3" fill="#6366f1"/>
          </svg>
        </div>
      </header>

      <div class="content">

        <div v-if="activeTab === 'issue'" class="tab-panel">
          <div class="form-card">
            <div class="form-grid">
              <div class="field full">
                <label>Nama Acara / Event</label>
                <input v-model="form.nama_event" type="text" placeholder="Contoh: Webinar Blockchain 2026" />
              </div>
              <div class="field">
                <label>Lokasi Kegiatan</label>
                <input v-model="form.nama_lokasi" type="text" placeholder="Nama gedung atau tempat" />
              </div>
              <div class="field">
                <label>
                  Koordinat GPS
                  <span v-if="gpsStatus" class="gps-status">{{ gpsStatus }}</span>
                </label>
                <div class="gps-inputs">
                  <input v-model="form.latitude" type="text" placeholder="Latitude" />
                  <input v-model="form.longitude" type="text" placeholder="Longitude" />
                </div>
                <button @click="getGPS" :disabled="gpsLoading" type="button" class="gps-btn">
                  <svg width="13" height="13" viewBox="0 0 16 16" fill="none">
                    <circle cx="8" cy="8" r="3" stroke="currentColor" stroke-width="1.4"/>
                    <path d="M8 1v2M8 13v2M1 8h2M13 8h2" stroke="currentColor" stroke-width="1.4" stroke-linecap="round"/>
                  </svg>
                  {{ gpsLoading ? 'Mengambil lokasi...' : 'Ambil Lokasi GPS' }}
                </button>
              </div>
              <div class="field">
                <label>Waktu Mulai</label>
                <input v-model="form.waktu_mulai" type="datetime-local" />
              </div>
              <div class="field">
                <label>Waktu Selesai</label>
                <input v-model="form.waktu_selesai" type="datetime-local" />
              </div>
              <div class="field full">
                <label>Nama Lengkap Peserta</label>
                <input v-model="form.nama_peserta" type="text" placeholder="Masukkan nama peserta..." />
              </div>
              <div class="field full">
                <label>Keterangan Tambahan</label>
                <textarea v-model="form.keterangan" rows="3" placeholder="Tuliskan keterangan sertifikat..."></textarea>
              </div>
            </div>

            <div v-if="errorMsg" class="error-msg">{{ errorMsg }}</div>

            <button @click="submitCert" :disabled="loading" class="submit-btn">
              <svg v-if="!loading" width="16" height="16" viewBox="0 0 20 20" fill="none">
                <path d="M10 3v14M3 10l7-7 7 7" stroke="currentColor" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round"/>
              </svg>
              <span v-if="loading" class="spinner-sm"></span>
              {{ loading ? 'Memproses Chain...' : 'Kunci Sertifikat ke Blockchain' }}
            </button>
          </div>

          <div v-if="result" class="result-card">
            <div class="result-header">
              <div class="result-check">
                <svg width="20" height="20" viewBox="0 0 20 20" fill="none">
                  <circle cx="10" cy="10" r="9" fill="#10b981"/>
                  <path d="M5.5 10l3 3 6-6" stroke="white" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round"/>
                </svg>
              </div>
              <div>
                <p class="result-title">Sertifikat Berhasil Disimpan</p>
                <p class="result-sub">Data telah dikunci ke blockchain</p>
              </div>
            </div>
            <div class="result-body">
              <div class="result-info">
                <div class="info-block">
                  <p class="info-label">Digital Signature Hash</p>
                  <p class="info-hash">{{ result.hash }}</p>
                </div>
                <div class="info-block">
                  <p class="info-label">Link Verifikasi</p>
                  <code class="info-url">{{ verifyUrl }}</code>
                  <button @click="goToVerify(result.hash)" class="verify-btn">
                    Lihat Sertifikat Publik →
                  </button>
                </div>
              </div>
              <div class="qr-block">
                <p class="info-label">QR Code Verifikasi</p>
                <img :src="qrCodeUrl" alt="QR Code" class="qr-img" />
                <p class="qr-hint">Scan untuk verifikasi</p>
                <a :href="qrCodeUrl" download="qrcode-sertifikat.png" class="qr-dl">⬇ Download QR</a>
              </div>
            </div>
          </div>
        </div>

        <div v-if="activeTab === 'data'" class="tab-panel">
          <div class="data-card">
            <div class="data-header">
              <div>
                <p class="data-title">Data Sertifikat</p>
                <p class="data-count">Total <strong>{{ tableData.length }}</strong> sertifikat tersimpan</p>
              </div>
              <div class="data-actions">
                <div class="search-wrap">
                  <svg width="14" height="14" viewBox="0 0 16 16" fill="none">
                    <circle cx="7" cy="7" r="5" stroke="#94a3b8" stroke-width="1.4"/>
                    <path d="M11 11l3 3" stroke="#94a3b8" stroke-width="1.4" stroke-linecap="round"/>
                  </svg>
                  <input v-model="search" type="text" placeholder="Cari nama / event..." />
                </div>
                <button @click="fetchData" class="refresh-btn">
                  <svg width="14" height="14" viewBox="0 0 16 16" fill="none">
                    <path d="M13.5 8A5.5 5.5 0 1 1 8 2.5M13.5 2.5v3h-3" stroke="currentColor" stroke-width="1.4" stroke-linecap="round" stroke-linejoin="round"/>
                  </svg>
                  Refresh
                </button>
              </div>
            </div>

            <div v-if="tableLoading" class="table-loading">
              <div class="spinner-lg"></div>
              <p>Memuat data dari blockchain...</p>
            </div>

            <div v-else-if="tableError" class="table-empty">
              <p class="empty-icon">⚠️</p>
              <p class="empty-text">{{ tableError }}</p>
              <button @click="fetchData" class="retry-btn">Coba lagi</button>
            </div>

            <div v-else-if="filteredData.length === 0" class="table-empty">
              <p class="empty-icon">📭</p>
              <p class="empty-text">{{ search ? 'Tidak ada data yang cocok' : 'Belum ada sertifikat tersimpan' }}</p>
            </div>

            <div v-else>
              <div class="table-wrap">
                <table>
                  <thead>
                    <tr>
                      <th>ID</th>
                      <th>Nama Peserta</th>
                      <th>Nama Event</th>
                      <th>Lokasi</th>
                      <th>Waktu Mulai</th>
                      <th>Waktu Selesai</th>
                      <th>Keterangan</th>
                      <th>Hash</th>
                      <th>Aksi</th>
                    </tr>
                  </thead>
                  <tbody>
                    <tr v-for="row in filteredData" :key="row.id">
                      <td class="td-id">{{ row.id }}</td>
                      <td class="td-name">{{ row.nama_peserta }}</td>
                      <td class="td-event">{{ row.nama_event }}</td>
                      <td class="td-grey">{{ row.nama_lokasi }}</td>
                      <td class="td-date">{{ formatDate(row.waktu_mulai) }}</td>
                      <td class="td-date">{{ formatDate(row.waktu_selesai) }}</td>
                      <td class="td-ket" :title="row.keterangan">{{ row.keterangan || '-' }}</td>
                      <td>
                        <span class="hash-chip" :title="row.cert_hash">
                          {{ row.cert_hash ? row.cert_hash.substring(0, 10) + '...' : '-' }}
                        </span>
                      </td>
                      <td>
                        <button @click="goToVerify(row.cert_hash)" class="lihat-btn">Lihat</button>
                      </td>
                    </tr>
                  </tbody>
                </table>
              </div>

              <div class="mobile-cards">
                <div v-for="row in filteredData" :key="'m' + row.id" class="mobile-card">
                  <div class="mc-top">
                    <span class="mc-id">#{{ row.id }}</span>
                    <button @click="goToVerify(row.cert_hash)" class="lihat-btn">Lihat</button>
                  </div>
                  <p class="mc-name">{{ row.nama_peserta }}</p>
                  <p class="mc-event">{{ row.nama_event }}</p>
                  <div class="mc-meta">
                    <span>📍 {{ row.nama_lokasi }}</span>
                    <span>🗓 {{ formatDate(row.waktu_mulai) }}</span>
                  </div>
                  <div class="mc-hash">{{ row.cert_hash ? row.cert_hash.substring(0, 16) + '...' : '-' }}</div>
                </div>
              </div>
            </div>
          </div>
        </div>

      </div>
    </main>
  </div>
</template>

<script>
import axios from 'axios'

export default {
  data() {
    return {
      activeTab: 'issue',
      sidebarOpen: false,
      loading: false,
      gpsLoading: false,
      gpsStatus: '',
      result: null,
      errorMsg: null,
      verifyUrl: '',
      qrCodeUrl: '',
      API_URL: 'https://verser-chain.vercel.app',
      TOKEN: localStorage.getItem('token') || '',
      form: {
        nama_event: '', nama_lokasi: '',
        latitude: '', longitude: '',
        waktu_mulai: '', waktu_selesai: '',
        nama_peserta: '', keterangan: ''
      },
      tableData: [],
      tableLoading: false,
      tableError: null,
      search: ''
    }
  },

  mounted() {
    this.getGPS()
  },

  computed: {
    filteredData() {
      if (!this.search) return this.tableData
      const q = this.search.toLowerCase()
      return this.tableData.filter(row =>
        (row.nama_peserta || '').toLowerCase().includes(q) ||
        (row.nama_event || '').toLowerCase().includes(q) ||
        (row.nama_lokasi || '').toLowerCase().includes(q)
      )
    },
    authHeaders() {
      return { Authorization: `Bearer ${this.TOKEN}` }
    }
  },

  methods: {
    setTab(tab) {
      this.activeTab = tab
      this.sidebarOpen = false
      if (tab === 'data') this.fetchData()
    },

    goToVerify(hash) {
      this.$router.push({ name: 'verify', params: { hash } })
    },

    async fetchData() {
      this.tableLoading = true
      this.tableError = null
      try {
        const res = await axios.get(this.API_URL + '/sertifikat', {
          headers: this.authHeaders
        })
        this.tableData = (res.data.data || []).sort((a, b) => a.id - b.id)
      } catch (err) {
        this.tableError = (err.response && err.response.data && err.response.data.message) || err.message || 'Gagal memuat data'
      } finally {
        this.tableLoading = false
      }
    },

    formatDate(val) {
      if (!val) return '-'
      return new Date(val).toLocaleString('id-ID', { day: '2-digit', month: 'short', year: 'numeric', hour: '2-digit', minute: '2-digit' })
    },

    getGPS() {
      if (!navigator.geolocation) { this.gpsStatus = 'GPS tidak tersedia'; return }
      this.gpsLoading = true
      this.gpsStatus = 'Mengambil...'
      navigator.geolocation.getCurrentPosition(
        (pos) => {
          this.form.latitude = pos.coords.latitude.toFixed(7)
          this.form.longitude = pos.coords.longitude.toFixed(7)
          this.gpsStatus = 'Berhasil ✓'
          this.gpsLoading = false
        },
        () => {
          this.gpsStatus = 'Ditolak'
          this.gpsLoading = false
        },
        { timeout: 10000 }
      )
    },

    async submitCert() {
      this.errorMsg = null
      if (!this.form.nama_event) return (this.errorMsg = 'Nama event wajib diisi!')
      if (!this.form.nama_lokasi) return (this.errorMsg = 'Lokasi kegiatan wajib diisi!')
      if (!this.form.waktu_mulai) return (this.errorMsg = 'Waktu mulai wajib diisi!')
      if (!this.form.waktu_selesai) return (this.errorMsg = 'Waktu selesai wajib diisi!')
      if (!this.form.nama_peserta) return (this.errorMsg = 'Nama peserta wajib diisi!')
      this.loading = true
      try {
        const payload = {
          ...this.form,
          latitude: this.form.latitude ? parseFloat(this.form.latitude) : null,
          longitude: this.form.longitude ? parseFloat(this.form.longitude) : null,
        }
        const res = await axios.post(this.API_URL + '/issue-sertifikat', payload, {
          headers: this.authHeaders
        })
        this.result = res.data
        this.verifyUrl = window.location.origin + '/verify/' + res.data.hash
        this.qrCodeUrl = `https://api.qrserver.com/v1/create-qr-code/?size=200x200&data=${encodeURIComponent(this.verifyUrl)}`
        this.form = { nama_event: '', nama_lokasi: '', latitude: '', longitude: '', waktu_mulai: '', waktu_selesai: '', nama_peserta: '', keterangan: '' }
        this.gpsStatus = ''
      } catch (err) {
        this.errorMsg = (err.response && err.response.data && err.response.data.message) || err.message || 'Terjadi kesalahan.'
      } finally {
        this.loading = false
      }
    },

    logout() {
      localStorage.removeItem('token')
      this.$router.push('/')
    }
  }
}
</script>

<style scoped>
@import url('https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:wght@400;500;600;700;800&display=swap');

* { box-sizing: border-box; margin: 0; padding: 0; }

.root {
  display: flex;
  min-height: 100vh;
  background: #f4f6fb;
  font-family: 'Plus Jakarta Sans', sans-serif;
}

.sidebar {
  width: 240px;
  background: #1e1b4b;
  display: flex;
  flex-direction: column;
  flex-shrink: 0;
  position: relative;
  z-index: 100;
}

.sidebar-header {
  display: flex;
  align-items: center;
  gap: 10px;
  padding: 20px 18px;
  border-bottom: 1px solid rgba(255,255,255,0.07);
}
.sidebar-logo {
  width: 38px; height: 38px;
  background: rgba(255,255,255,0.1);
  border-radius: 10px;
  display: flex;
  align-items: center;
  justify-content: center;
  flex-shrink: 0;
}
.sidebar-title { font-size: 13px; font-weight: 700; color: white; line-height: 1.2; }
.sidebar-sub { font-size: 10px; color: rgba(255,255,255,0.4); }
.sidebar-close { display: none; }

.sidebar-nav {
  flex: 1;
  padding: 16px 10px;
  display: flex;
  flex-direction: column;
  gap: 4px;
}
.nav-item {
  display: flex;
  align-items: center;
  gap: 10px;
  padding: 10px 12px;
  border-radius: 10px;
  border: none;
  background: none;
  color: rgba(255,255,255,0.5);
  font-family: 'Plus Jakarta Sans', sans-serif;
  font-size: 13px;
  font-weight: 500;
  cursor: pointer;
  transition: all 0.18s;
  text-align: left;
  width: 100%;
}
.nav-item:hover { background: rgba(255,255,255,0.07); color: rgba(255,255,255,0.8); }
.nav-item.active { background: rgba(99,102,241,0.25); color: white; }
.badge {
  margin-left: auto;
  background: #6366f1;
  color: white;
  font-size: 10px;
  font-weight: 700;
  padding: 2px 7px;
  border-radius: 20px;
}

.logout-btn {
  display: flex;
  align-items: center;
  gap: 8px;
  margin: 10px;
  padding: 10px 12px;
  border-radius: 10px;
  border: 1px solid rgba(255,255,255,0.08);
  background: none;
  color: rgba(255,255,255,0.4);
  font-family: 'Plus Jakarta Sans', sans-serif;
  font-size: 13px;
  cursor: pointer;
  transition: all 0.18s;
}
.logout-btn:hover { background: rgba(239,68,68,0.15); color: #fca5a5; border-color: rgba(239,68,68,0.3); }

.overlay {
  display: none;
  position: fixed;
  inset: 0;
  background: rgba(0,0,0,0.4);
  z-index: 90;
}

.main { flex: 1; display: flex; flex-direction: column; min-width: 0; }

.topbar {
  background: white;
  border-bottom: 1px solid #e8ecf4;
  padding: 14px 24px;
  display: flex;
  align-items: center;
  gap: 14px;
}
.hamburger {
  display: none;
  flex-direction: column;
  gap: 4px;
  background: none;
  border: none;
  cursor: pointer;
  padding: 4px;
}
.hamburger span { width: 20px; height: 2px; background: #374151; border-radius: 2px; display: block; }
.topbar-title { flex: 1; }
.page-title { font-size: 15px; font-weight: 700; color: #111827; }
.page-sub { font-size: 11px; color: #94a3b8; }
.topbar-logo { display: flex; align-items: center; }

.content { flex: 1; padding: 24px; overflow-y: auto; }
.tab-panel { max-width: 900px; }

.form-card {
  background: white;
  border-radius: 16px;
  padding: 28px;
  box-shadow: 0 1px 4px rgba(0,0,0,0.05);
  border: 1px solid #e8ecf4;
}

.form-grid {
  display: grid;
  grid-template-columns: 1fr 1fr;
  gap: 18px;
  margin-bottom: 20px;
}
.field { display: flex; flex-direction: column; gap: 6px; }
.field.full { grid-column: 1 / -1; }

.field label {
  font-size: 11px;
  font-weight: 700;
  color: #64748b;
  text-transform: uppercase;
  letter-spacing: 0.6px;
  display: flex;
  align-items: center;
  gap: 8px;
}
.gps-status { font-size: 10px; font-weight: 500; color: #10b981; text-transform: none; letter-spacing: 0; }

.field input,
.field textarea {
  padding: 11px 14px;
  border: 1.5px solid #e2e8f0;
  border-radius: 10px;
  font-family: 'Plus Jakarta Sans', sans-serif;
  font-size: 14px;
  color: #0f172a;
  background: #f8fafc;
  outline: none;
  transition: border-color 0.18s, box-shadow 0.18s, background 0.18s;
  resize: none;
}
.field input:focus, .field textarea:focus {
  border-color: #6366f1;
  background: white;
  box-shadow: 0 0 0 3px rgba(99,102,241,0.1);
}

.gps-inputs { display: flex; gap: 8px; }
.gps-inputs input { flex: 1; }

.gps-btn {
  display: flex;
  align-items: center;
  justify-content: center;
  gap: 6px;
  margin-top: 6px;
  padding: 9px;
  background: #eef2ff;
  border: none;
  border-radius: 9px;
  color: #6366f1;
  font-family: 'Plus Jakarta Sans', sans-serif;
  font-size: 12px;
  font-weight: 600;
  cursor: pointer;
  transition: background 0.18s;
}
.gps-btn:hover:not(:disabled) { background: #e0e7ff; }
.gps-btn:disabled { opacity: 0.5; cursor: not-allowed; }

.error-msg {
  background: #fef2f2;
  border: 1px solid #fecaca;
  color: #ef4444;
  font-size: 13px;
  padding: 11px 14px;
  border-radius: 10px;
  margin-bottom: 16px;
}

.submit-btn {
  display: flex;
  align-items: center;
  justify-content: center;
  gap: 8px;
  width: 100%;
  padding: 14px;
  background: #6366f1;
  border: none;
  border-radius: 12px;
  color: white;
  font-family: 'Plus Jakarta Sans', sans-serif;
  font-size: 14px;
  font-weight: 700;
  cursor: pointer;
  transition: background 0.18s, transform 0.12s, box-shadow 0.18s;
  box-shadow: 0 2px 12px rgba(99,102,241,0.25);
}
.submit-btn:hover:not(:disabled) { background: #4f46e5; transform: translateY(-1px); box-shadow: 0 4px 20px rgba(99,102,241,0.35); }
.submit-btn:disabled { opacity: 0.55; cursor: not-allowed; transform: none; }

.spinner-sm {
  width: 14px; height: 14px;
  border: 2px solid rgba(255,255,255,0.3);
  border-top-color: white;
  border-radius: 50%;
  animation: spin 0.7s linear infinite;
}
@keyframes spin { to { transform: rotate(360deg); } }

.result-card {
  margin-top: 20px;
  background: white;
  border-radius: 16px;
  border: 1.5px solid #d1fae5;
  overflow: hidden;
  box-shadow: 0 1px 4px rgba(0,0,0,0.05);
}
.result-header {
  display: flex;
  align-items: center;
  gap: 12px;
  padding: 18px 24px;
  background: #f0fdf4;
  border-bottom: 1px solid #d1fae5;
}
.result-title { font-size: 14px; font-weight: 700; color: #065f46; }
.result-sub { font-size: 12px; color: #6ee7b7; }
.result-body { display: flex; gap: 20px; padding: 20px 24px; }
.result-info { flex: 1; display: flex; flex-direction: column; gap: 14px; }
.info-block { display: flex; flex-direction: column; gap: 4px; }
.info-label { font-size: 9px; font-weight: 700; text-transform: uppercase; letter-spacing: 1.2px; color: #94a3b8; }
.info-hash {
  font-family: 'Courier New', monospace;
  font-size: 11px;
  color: #6366f1;
  font-weight: 700;
  word-break: break-all;
  background: #f5f3ff;
  padding: 8px 10px;
  border-radius: 8px;
}
.info-url {
  font-family: 'Courier New', monospace;
  font-size: 10px;
  color: #64748b;
  word-break: break-all;
  background: #f8fafc;
  padding: 8px 10px;
  border-radius: 8px;
  display: block;
  margin-bottom: 8px;
}
.verify-btn {
  padding: 9px 16px;
  background: #6366f1;
  color: white;
  border: none;
  border-radius: 8px;
  font-family: 'Plus Jakarta Sans', sans-serif;
  font-size: 12px;
  font-weight: 600;
  cursor: pointer;
  transition: background 0.18s;
}
.verify-btn:hover { background: #4f46e5; }

.qr-block { display: flex; flex-direction: column; align-items: center; gap: 6px; flex-shrink: 0; }
.qr-img { width: 130px; height: 130px; border-radius: 10px; border: 1px solid #e2e8f0; }
.qr-hint { font-size: 10px; color: #94a3b8; }
.qr-dl { font-size: 11px; color: #6366f1; font-weight: 600; text-decoration: none; }
.qr-dl:hover { text-decoration: underline; }

.data-card {
  background: white;
  border-radius: 16px;
  padding: 24px;
  box-shadow: 0 1px 4px rgba(0,0,0,0.05);
  border: 1px solid #e8ecf4;
}
.data-header {
  display: flex;
  align-items: center;
  justify-content: space-between;
  gap: 16px;
  margin-bottom: 20px;
  flex-wrap: wrap;
}
.data-title { font-size: 16px; font-weight: 700; color: #111827; }
.data-count { font-size: 12px; color: #94a3b8; margin-top: 2px; }
.data-count strong { color: #6366f1; }
.data-actions { display: flex; gap: 8px; align-items: center; flex-wrap: wrap; }

.search-wrap {
  display: flex;
  align-items: center;
  gap: 8px;
  background: #f8fafc;
  border: 1.5px solid #e2e8f0;
  border-radius: 10px;
  padding: 8px 12px;
}
.search-wrap input {
  border: none;
  background: none;
  outline: none;
  font-family: 'Plus Jakarta Sans', sans-serif;
  font-size: 13px;
  color: #374151;
  width: 180px;
}
.search-wrap input::placeholder { color: #cbd5e1; }

.refresh-btn {
  display: flex;
  align-items: center;
  gap: 6px;
  padding: 9px 14px;
  background: #eef2ff;
  border: none;
  border-radius: 10px;
  color: #6366f1;
  font-family: 'Plus Jakarta Sans', sans-serif;
  font-size: 12px;
  font-weight: 600;
  cursor: pointer;
  transition: background 0.18s;
}
.refresh-btn:hover { background: #e0e7ff; }

.table-loading { display: flex; flex-direction: column; align-items: center; padding: 48px; gap: 12px; color: #94a3b8; font-size: 13px; }
.spinner-lg { width: 32px; height: 32px; border: 3px solid #e2e8f0; border-top-color: #6366f1; border-radius: 50%; animation: spin 0.8s linear infinite; }
.table-empty { text-align: center; padding: 48px; }
.empty-icon { font-size: 40px; margin-bottom: 10px; }
.empty-text { font-size: 14px; color: #94a3b8; }
.retry-btn { margin-top: 12px; background: none; border: none; color: #6366f1; font-size: 13px; font-weight: 600; cursor: pointer; }

.table-wrap { overflow-x: auto; }
table { width: 100%; border-collapse: collapse; font-size: 13px; }
thead tr { background: #f8fafc; }
th { padding: 10px 12px; text-align: left; font-size: 10px; font-weight: 700; text-transform: uppercase; letter-spacing: 0.8px; color: #94a3b8; white-space: nowrap; }
tbody tr { border-top: 1px solid #f1f5f9; transition: background 0.15s; }
tbody tr:hover { background: #fafbff; }
td { padding: 12px 12px; }
.td-id { font-size: 11px; font-weight: 700; color: #cbd5e1; }
.td-name { font-weight: 600; color: #111827; }
.td-event { color: #374151; }
.td-grey { color: #64748b; }
.td-date { color: #64748b; font-size: 12px; white-space: nowrap; }
.td-ket { color: #64748b; max-width: 130px; overflow: hidden; text-overflow: ellipsis; white-space: nowrap; }
.hash-chip { font-family: 'Courier New', monospace; font-size: 10px; color: #6366f1; background: #eef2ff; padding: 3px 8px; border-radius: 6px; display: inline-block; }
.lihat-btn { padding: 6px 14px; background: #6366f1; color: white; border: none; border-radius: 7px; font-family: 'Plus Jakarta Sans', sans-serif; font-size: 12px; font-weight: 600; cursor: pointer; transition: background 0.15s; white-space: nowrap; }
.lihat-btn:hover { background: #4f46e5; }

.mobile-cards { display: none; }
.mobile-card { border: 1px solid #e8ecf4; border-radius: 12px; padding: 14px; margin-bottom: 10px; }
.mc-top { display: flex; justify-content: space-between; align-items: center; margin-bottom: 6px; }
.mc-id { font-size: 10px; font-weight: 700; color: #cbd5e1; }
.mc-name { font-size: 14px; font-weight: 700; color: #111827; margin-bottom: 2px; }
.mc-event { font-size: 12px; color: #64748b; margin-bottom: 8px; }
.mc-meta { display: flex; flex-wrap: wrap; gap: 8px; font-size: 11px; color: #94a3b8; margin-bottom: 8px; }
.mc-hash { font-family: 'Courier New', monospace; font-size: 10px; color: #6366f1; background: #eef2ff; padding: 4px 8px; border-radius: 6px; word-break: break-all; }

@media (max-width: 768px) {
  .sidebar { position: fixed; top: 0; left: 0; height: 100%; transform: translateX(-100%); transition: transform 0.25s ease; z-index: 200; }
  .sidebar.open { transform: translateX(0); }
  .sidebar-close { display: flex; margin-left: auto; background: none; border: none; color: rgba(255,255,255,0.5); font-size: 16px; cursor: pointer; padding: 4px; }
  .overlay { display: block; }
  .hamburger { display: flex; }
  .content { padding: 12px; }
  .tab-panel { max-width: 100%; }

  /* Form responsive */
  .form-card { padding: 18px; }
  .form-grid { grid-template-columns: 1fr; gap: 14px; }
  .field.full { grid-column: 1; }
  .gps-inputs { flex-direction: column; gap: 8px; }
  .gps-inputs input { width: 100%; }

  /* Result card responsive */
  .result-body { flex-direction: column; }
  .result-card { margin-top: 16px; }
  .result-header { padding: 14px 16px; }
  .result-body { padding: 16px; }
  .result-info { width: 100%; }
  .qr-block { align-items: center; width: 100%; }
  .info-hash { font-size: 10px; word-break: break-all; }
  .info-url { font-size: 9px; word-break: break-all; }
  .verify-btn { width: 100%; text-align: center; }

  /* Data tab responsive */
  .data-card { padding: 16px; }
  .data-header { flex-direction: column; align-items: flex-start; gap: 12px; }
  .data-actions { width: 100%; flex-direction: column; align-items: stretch; }
  .search-wrap { width: 100%; }
  .search-wrap input { width: 100%; flex: 1; }
  .refresh-btn { width: 100%; justify-content: center; }
  .table-wrap { display: none; }
  .mobile-cards { display: block; }
  .topbar { padding: 12px 16px; }
  .submit-btn { font-size: 13px; padding: 13px; }
}

@media (max-width: 480px) {
  .content { padding: 10px; }
  .form-card { padding: 14px; }
  .field input, .field textarea { font-size: 13px; padding: 10px 12px; }
  .result-header { flex-wrap: wrap; gap: 8px; }
}
</style>