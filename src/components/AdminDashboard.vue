<template>
  <div class="min-h-screen bg-slate-50">
    <nav class="bg-white border-b border-gray-200 px-6 py-4 flex justify-between items-center shadow-sm">
      <h1 class="text-xl font-bold text-indigo-700 tracking-tight">VeriZh Chain Admin</h1>
      <button @click="logout" class="text-sm bg-red-50 text-red-600 px-4 py-2 rounded-xl font-bold hover:bg-red-100 transition">Logout</button>
    </nav>

    <div class="max-w-6xl mx-auto px-4 pt-8">
      <div class="flex space-x-2 mb-8 bg-white border border-gray-200 p-1.5 rounded-2xl w-fit shadow-sm">
        <button @click="activeTab = 'issue'" :class="activeTab === 'issue' ? 'bg-indigo-600 text-white shadow-md shadow-indigo-200' : 'text-gray-400 hover:text-gray-700'" class="px-6 py-2.5 rounded-xl font-bold text-sm transition-all">
          ✍️ Terbitkan Sertifikat
        </button>
        <button @click="switchToData" :class="activeTab === 'data' ? 'bg-indigo-600 text-white shadow-md shadow-indigo-200' : 'text-gray-400 hover:text-gray-700'" class="px-6 py-2.5 rounded-xl font-bold text-sm transition-all">
          🗃️ Data Sertifikat
        </button>
      </div>
    </div>

    <!-- TAB ISSUE -->
    <div v-if="activeTab === 'issue'" class="max-w-4xl mx-auto pb-10 px-4">
      <div class="bg-white rounded-3xl shadow-sm border border-gray-200 p-8">
        <div class="mb-8">
          <h2 class="text-2xl font-extrabold text-gray-900">Terbitkan Sertifikat Baru</h2>
          <p class="text-gray-500 text-sm mt-1">Data akan dikunci ke dalam database menggunakan hashing SHA-256.</p>
        </div>
        <div class="grid grid-cols-1 md:grid-cols-2 gap-6">
          <div class="md:col-span-2">
            <label class="block text-xs font-bold text-gray-400 uppercase mb-2 ml-1">Nama Acara / Event</label>
            <input v-model="form.nama_event" type="text" class="w-full p-4 bg-gray-50 border border-gray-200 rounded-2xl focus:ring-2 focus:ring-indigo-500 focus:bg-white outline-none transition" placeholder="Contoh: Webinar Blockchain 2026" />
          </div>
          <div>
            <label class="block text-xs font-bold text-gray-400 uppercase mb-2 ml-1">Lokasi Kegiatan</label>
            <input v-model="form.nama_lokasi" type="text" class="w-full p-4 bg-gray-50 border border-gray-200 rounded-2xl focus:ring-2 focus:ring-indigo-500 focus:bg-white outline-none transition" placeholder="Nama gedung atau tempat" />
          </div>
          <div>
            <label class="block text-xs font-bold text-gray-400 uppercase mb-2 ml-1">
              Koordinat GPS
              <span v-if="gpsStatus" class="ml-2 normal-case font-normal text-emerald-500">{{ gpsStatus }}</span>
            </label>
            <div class="flex space-x-2">
              <input v-model="form.latitude" type="text" placeholder="Latitude" class="w-1/2 p-4 bg-gray-50 border border-gray-200 rounded-2xl text-sm" />
              <input v-model="form.longitude" type="text" placeholder="Longitude" class="w-1/2 p-4 bg-gray-50 border border-gray-200 rounded-2xl text-sm" />
            </div>
            <button @click="getGPS" :disabled="gpsLoading" type="button" class="mt-2 w-full py-2 text-xs font-bold text-indigo-600 bg-indigo-50 rounded-xl hover:bg-indigo-100 transition disabled:opacity-50">
              {{ gpsLoading ? 'Mengambil lokasi...' : 'Ambil Lokasi GPS Sekarang' }}
            </button>
          </div>
          <div>
            <label class="block text-xs font-bold text-gray-400 uppercase mb-2 ml-1">Waktu Mulai</label>
            <input v-model="form.waktu_mulai" type="datetime-local" class="w-full p-4 bg-gray-50 border border-gray-200 rounded-2xl focus:ring-2 focus:ring-indigo-500 focus:bg-white transition" />
          </div>
          <div>
            <label class="block text-xs font-bold text-gray-400 uppercase mb-2 ml-1">Waktu Selesai</label>
            <input v-model="form.waktu_selesai" type="datetime-local" class="w-full p-4 bg-gray-50 border border-gray-200 rounded-2xl focus:ring-2 focus:ring-indigo-500 focus:bg-white transition" />
          </div>
          <div class="md:col-span-2">
            <label class="block text-xs font-bold text-gray-400 uppercase mb-2 ml-1">Nama Lengkap Peserta</label>
            <input v-model="form.nama_peserta" type="text" class="w-full p-4 bg-gray-50 border border-gray-200 rounded-2xl focus:ring-2 focus:ring-indigo-500 focus:bg-white outline-none transition" placeholder="Masukkan nama peserta..." />
          </div>
          <div class="md:col-span-2">
            <label class="block text-xs font-bold text-gray-400 uppercase mb-2 ml-1">Keterangan Tambahan</label>
            <textarea v-model="form.keterangan" rows="3" class="w-full p-4 bg-gray-50 border border-gray-200 rounded-2xl focus:ring-2 focus:ring-indigo-500 focus:bg-white outline-none transition" placeholder="Tuliskan keterangan sertifikat..."></textarea>
          </div>
        </div>
        <div v-if="errorMsg" class="mt-4 p-4 bg-red-50 border border-red-200 rounded-2xl text-red-600 text-sm font-medium">
          {{ errorMsg }}
        </div>
        <button @click="submitCert" :disabled="loading" class="w-full mt-10 bg-indigo-600 text-white font-extrabold py-5 rounded-2xl hover:bg-indigo-700 shadow-lg shadow-indigo-200 transition-all disabled:bg-gray-300 transform active:scale-[0.98]">
          {{ loading ? 'Sedang Memproses Chain...' : 'Kunci Sertifikat ke Blockchain' }}
        </button>
      </div>

      <!-- HASIL SUKSES + QR CODE -->
      <div v-if="result" class="mt-8 bg-emerald-50 p-8 rounded-3xl border-2 border-emerald-200">
        <h3 class="text-lg font-bold text-emerald-800 flex items-center mb-6">
          <span class="mr-2">🛡️</span> Sertifikat Berhasil Disimpan
        </h3>
        <div class="grid grid-cols-1 md:grid-cols-2 gap-6">
          <div class="space-y-4">
            <div class="bg-white p-4 rounded-xl border border-emerald-100">
              <p class="text-[10px] text-gray-400 font-black uppercase tracking-widest mb-1">Digital Signature Hash</p>
              <p class="text-xs font-mono break-all font-bold text-indigo-600">{{ result.hash }}</p>
            </div>
            <div class="bg-white p-4 rounded-xl border border-emerald-100">
              <p class="text-[10px] text-gray-400 font-black uppercase tracking-widest mb-1">Link Verifikasi</p>
              <code class="text-[10px] bg-gray-50 p-2 rounded-lg block break-all text-gray-500 mb-3">{{ verifyUrl }}</code>
              <button @click="goToVerify(result.hash)" class="w-full py-2 bg-indigo-600 text-white text-xs font-bold rounded-xl hover:bg-indigo-700 transition">
                Lihat Sertifikat Publik →
              </button>
            </div>
          </div>
          <!-- QR CODE -->
          <div class="bg-white p-6 rounded-xl border border-emerald-100 flex flex-col items-center justify-center">
            <p class="text-[10px] text-gray-400 font-black uppercase tracking-widest mb-4">QR Code Verifikasi</p>
            <img :src="qrCodeUrl" alt="QR Code" class="w-48 h-48 rounded-xl border border-gray-100 shadow-sm" />
            <p class="text-[10px] text-gray-400 mt-3 text-center">Scan untuk verifikasi sertifikat</p>
            <a :href="qrCodeUrl" download="qrcode-sertifikat.png" class="mt-3 text-xs text-indigo-600 font-bold hover:underline">⬇ Download QR Code</a>
          </div>
        </div>
      </div>
    </div>

    <!-- TAB DATA -->
    <div v-if="activeTab === 'data'" class="max-w-6xl mx-auto pb-10 px-4">
      <div class="bg-white rounded-3xl shadow-sm border border-gray-200 p-8">
        <div class="flex flex-col md:flex-row md:items-center justify-between gap-4 mb-6">
          <div>
            <h2 class="text-2xl font-extrabold text-gray-900">Data Sertifikat</h2>
            <p class="text-gray-400 text-sm mt-1">Total <span class="font-bold text-indigo-600">{{ tableData.length }}</span> sertifikat tersimpan</p>
          </div>
          <div class="flex gap-3">
            <input v-model="search" type="text" placeholder="Cari nama / event..." class="px-4 py-2.5 bg-gray-50 border border-gray-200 rounded-xl text-sm focus:ring-2 focus:ring-indigo-500 outline-none w-60" />
            <button @click="fetchData" class="px-4 py-2.5 bg-indigo-50 text-indigo-600 font-bold text-sm rounded-xl hover:bg-indigo-100 transition">Refresh</button>
          </div>
        </div>

        <div v-if="tableLoading" class="py-20 text-center">
          <div class="w-10 h-10 border-4 border-indigo-500 border-t-transparent rounded-full animate-spin mx-auto mb-4"></div>
          <p class="text-gray-400 text-sm font-medium">Memuat data dari blockchain...</p>
        </div>

        <div v-else-if="tableError" class="py-16 text-center">
          <p class="text-4xl mb-3">⚠️</p>
          <p class="text-red-500 font-bold">{{ tableError }}</p>
          <button @click="fetchData" class="mt-4 text-sm text-indigo-600 font-bold hover:underline">Coba lagi</button>
        </div>

        <div v-else-if="filteredData.length === 0" class="py-16 text-center">
          <p class="text-5xl mb-4">📭</p>
          <p class="text-gray-400 font-medium">{{ search ? 'Tidak ada data yang cocok' : 'Belum ada sertifikat tersimpan' }}</p>
        </div>

        <div v-else class="overflow-x-auto rounded-2xl border border-gray-100">
          <table class="w-full text-sm">
            <thead>
              <tr class="bg-gray-50 text-left">
                <th class="px-4 py-3 text-xs font-black text-gray-400 uppercase tracking-wider">ID</th>
                <th class="px-4 py-3 text-xs font-black text-gray-400 uppercase tracking-wider">Nama Peserta</th>
                <th class="px-4 py-3 text-xs font-black text-gray-400 uppercase tracking-wider">Nama Event</th>
                <th class="px-4 py-3 text-xs font-black text-gray-400 uppercase tracking-wider">Lokasi</th>
                <th class="px-4 py-3 text-xs font-black text-gray-400 uppercase tracking-wider">Waktu Mulai</th>
                <th class="px-4 py-3 text-xs font-black text-gray-400 uppercase tracking-wider">Waktu Selesai</th>
                <th class="px-4 py-3 text-xs font-black text-gray-400 uppercase tracking-wider">Keterangan</th>
                <th class="px-4 py-3 text-xs font-black text-gray-400 uppercase tracking-wider">Hash</th>
                <th class="px-4 py-3 text-xs font-black text-gray-400 uppercase tracking-wider">Aksi</th>
              </tr>
            </thead>
            <tbody class="divide-y divide-gray-50">
              <tr v-for="row in filteredData" :key="row.id" class="hover:bg-indigo-50/30 transition">
                <td class="px-4 py-4 font-bold text-gray-400 text-xs">{{ row.id }}</td>
                <td class="px-4 py-4 font-semibold text-gray-800">{{ row.nama_peserta }}</td>
                <td class="px-4 py-4 text-gray-600">{{ row.nama_event }}</td>
                <td class="px-4 py-4 text-gray-500">{{ row.nama_lokasi }}</td>
                <td class="px-4 py-4 text-gray-500 text-xs whitespace-nowrap">{{ formatDate(row.waktu_mulai) }}</td>
                <td class="px-4 py-4 text-gray-500 text-xs whitespace-nowrap">{{ formatDate(row.waktu_selesai) }}</td>
                <td class="px-4 py-4 text-gray-500 max-w-[150px] truncate" :title="row.keterangan">{{ row.keterangan || '-' }}</td>
                <td class="px-4 py-4">
                  <span class="font-mono text-[10px] text-indigo-500 bg-indigo-50 px-2 py-1 rounded-lg block max-w-[100px] truncate" :title="row.cert_hash">
                    {{ row.cert_hash ? row.cert_hash.substring(0, 12) + '...' : '-' }}
                  </span>
                </td>
                <td class="px-4 py-4">
                  <button @click="goToVerify(row.cert_hash)" class="inline-block px-3 py-1.5 bg-indigo-600 text-white text-xs font-bold rounded-lg hover:bg-indigo-700 transition whitespace-nowrap cursor-pointer">
                    Lihat
                  </button>
                </td>
              </tr>
            </tbody>
          </table>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import axios from 'axios'

export default {
  data() {
    return {
      activeTab: 'issue',
      loading: false,
      gpsLoading: false,
      gpsStatus: '',
      result: null,
      errorMsg: null,
      verifyUrl: '',
      qrCodeUrl: '',
      API_URL: 'https://verser-chain.vercel.app',
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
    }
  },

  methods: {
    goToVerify(hash) {
      this.$router.push({ name: 'verify', params: { hash } })
    },

    switchToData() {
      this.activeTab = 'data'
      this.fetchData()
    },

    async fetchData() {
      this.tableLoading = true
      this.tableError = null
      try {
        const res = await axios.get(this.API_URL + '/sertifikat')
        this.tableData = res.data.data || []
      } catch (err) {
        this.tableError = (err.response && err.response.data && err.response.data.message) || err.message || 'Gagal memuat data'
      } finally {
        this.tableLoading = false
      }
    },

    formatDate(val) {
      if (!val) return '-'
      const d = new Date(val)
      return d.toLocaleString('id-ID', { day: '2-digit', month: 'short', year: 'numeric', hour: '2-digit', minute: '2-digit' })
    },

    getGPS() {
      if (!navigator.geolocation) {
        this.gpsStatus = 'Browser tidak support GPS'
        return
      }
      this.gpsLoading = true
      this.gpsStatus = 'Mengambil lokasi...'
      navigator.geolocation.getCurrentPosition(
        (pos) => {
          this.form.latitude = pos.coords.latitude.toFixed(7)
          this.form.longitude = pos.coords.longitude.toFixed(7)
          this.gpsStatus = 'Lokasi berhasil didapat ✓'
          this.gpsLoading = false
        },
        () => {
          this.gpsStatus = 'GPS ditolak, isi manual jika perlu'
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
        const res = await axios.post(this.API_URL + '/issue-sertifikat', payload)
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
