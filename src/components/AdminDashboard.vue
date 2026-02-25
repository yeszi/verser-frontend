<template>
  <div class="min-h-screen bg-slate-50">
    <nav class="bg-white border-b border-gray-200 px-6 py-4 flex justify-between items-center shadow-sm">
      <h1 class="text-xl font-bold text-indigo-700 tracking-tight">VeriZh Chain Admin</h1>
      <button @click="logout" class="text-sm bg-red-50 text-red-600 px-4 py-2 rounded-xl font-bold hover:bg-red-100 transition">Logout</button>
    </nav>

    <div class="max-w-4xl mx-auto py-10 px-4">
      <div class="bg-white rounded-3xl shadow-sm border border-gray-200 p-8">
        <div class="mb-8">
          <h2 class="text-2xl font-extrabold text-gray-900">Terbitkan Sertifikat Baru</h2>
          <p class="text-gray-500 text-sm mt-1">Data akan dikunci ke dalam database menggunakan hashing SHA-256.</p>
        </div>

        <div class="grid grid-cols-1 md:grid-cols-2 gap-6">
          <div class="md:col-span-2">
            <label class="block text-xs font-bold text-gray-400 uppercase mb-2 ml-1">Nama Lengkap Peserta</label>
            <input v-model="form.nama_peserta" type="text" class="w-full p-4 bg-gray-50 border border-gray-200 rounded-2xl focus:ring-2 focus:ring-indigo-500 focus:bg-white outline-none transition" placeholder="Masukkan nama peserta..." />
          </div>

          <div class="md:col-span-2">
            <label class="block text-xs font-bold text-gray-400 uppercase mb-2 ml-1">Nama Acara / Event</label>
            <input v-model="form.nama_event" type="text" class="w-full p-4 bg-gray-50 border border-gray-200 rounded-2xl focus:ring-2 focus:ring-indigo-500 focus:bg-white outline-none transition" placeholder="Contoh: Webinar Blockchain 2026" />
          </div>

          <div>
            <label class="block text-xs font-bold text-gray-400 uppercase mb-2 ml-1">Lokasi Kegiatan</label>
            <input v-model="form.nama_lokasi" type="text" class="w-full p-4 bg-gray-50 border border-gray-200 rounded-2xl focus:ring-2 focus:ring-indigo-500 focus:bg-white outline-none transition" placeholder="Nama gedung atau tempat" />
          </div>

          <!-- ✅ FIX: GPS auto-fill dengan tombol ambil lokasi -->
          <div>
            <label class="block text-xs font-bold text-gray-400 uppercase mb-2 ml-1">
              Koordinat GPS
              <span v-if="gpsStatus" :class="gpsStatus.includes('✅') ? 'text-emerald-500' : 'text-red-400'" class="ml-2 normal-case font-normal">{{ gpsStatus }}</span>
            </label>
            <div class="flex space-x-2">
              <input v-model="form.latitude" type="text" placeholder="Latitude" class="w-1/2 p-4 bg-gray-50 border border-gray-200 rounded-2xl text-sm" readonly />
              <input v-model="form.longitude" type="text" placeholder="Longitude" class="w-1/2 p-4 bg-gray-50 border border-gray-200 rounded-2xl text-sm" readonly />
            </div>
            <button
              @click="getGPS"
              :disabled="gpsLoading"
              type="button"
              class="mt-2 w-full py-2 text-xs font-bold text-indigo-600 bg-indigo-50 rounded-xl hover:bg-indigo-100 transition disabled:opacity-50"
            >
              {{ gpsLoading ? '📡 Mengambil lokasi...' : '📍 Ambil Lokasi GPS Sekarang' }}
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
            <label class="block text-xs font-bold text-gray-400 uppercase mb-2 ml-1">Keterangan Tambahan</label>
            <textarea v-model="form.keterangan" rows="3" class="w-full p-4 bg-gray-50 border border-gray-200 rounded-2xl focus:ring-2 focus:ring-indigo-500 focus:bg-white outline-none transition" placeholder="Tuliskan keterangan sertifikat..."></textarea>
          </div>
        </div>

        <!-- Error message -->
        <div v-if="errorMsg" class="mt-4 p-4 bg-red-50 border border-red-200 rounded-2xl text-red-600 text-sm font-medium">
          ❌ {{ errorMsg }}
        </div>

        <button @click="submitCert" :disabled="loading" class="w-full mt-10 bg-indigo-600 text-white font-extrabold py-5 rounded-2xl hover:bg-indigo-700 shadow-lg shadow-indigo-200 transition-all disabled:bg-gray-300 transform active:scale-[0.98]">
          {{ loading ? 'Sedang Memproses Chain...' : 'Kunci Sertifikat ke Blockchain' }}
        </button>
      </div>

      <div v-if="result" class="mt-8 bg-emerald-50 p-8 rounded-3xl border-2 border-emerald-200">
        <h3 class="text-lg font-bold text-emerald-800 flex items-center mb-4">
          <span class="mr-2">🛡️</span> Sertifikat Berhasil Diverifikasi & Disimpan
        </h3>
        <div class="space-y-4">
          <div class="bg-white p-4 rounded-xl border border-emerald-100">
            <p class="text-[10px] text-gray-400 font-black uppercase tracking-widest">Digital Signature Hash</p>
            <p class="text-xs font-mono break-all font-bold text-indigo-600 mt-1">{{ result.hash }}</p>
          </div>
          <div class="p-6 bg-white rounded-2xl border border-emerald-100 text-center">
            <p class="text-sm text-gray-600 mb-4">Gunakan link verifikasi ini:</p>
            <code class="text-[10px] bg-gray-50 p-3 rounded-lg block break-all mb-4 text-gray-500">{{ verifyUrl }}</code>
            <a :href="verifyUrl" target="_blank" class="inline-block px-6 py-2 bg-indigo-600 text-white text-sm font-bold rounded-full hover:bg-indigo-700 transition">Lihat Sertifikat Publik</a>
          </div>
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
      loading: false,
      gpsLoading: false,
      gpsStatus: '',
      result: null,
      errorMsg: null,
      verifyUrl: '',
      API_URL: 'https://verser-chain.vercel.app',
      form: {
        nama_peserta: '',
        nama_event: '',
        nama_lokasi: '',
        latitude: '',
        longitude: '',
        waktu_mulai: '',
        waktu_selesai: '',
        keterangan: ''
      }
    }
  },

  // ✅ FIX: Auto ambil GPS saat halaman dibuka
  mounted() {
    this.getGPS()
  },

  methods: {
    // ✅ FIX: Method GPS yang proper
    getGPS() {
      if (!navigator.geolocation) {
        this.gpsStatus = '❌ Browser tidak support GPS'
        return
      }
      this.gpsLoading = true
      this.gpsStatus = '📡 Mengambil lokasi...'
      navigator.geolocation.getCurrentPosition(
        (pos) => {
          this.form.latitude = pos.coords.latitude.toFixed(7)
          this.form.longitude = pos.coords.longitude.toFixed(7)
          this.gpsStatus = '✅ Lokasi berhasil didapat'
          this.gpsLoading = false
        },
        (err) => {
          this.gpsStatus = '❌ GPS ditolak, isi manual jika perlu'
          this.gpsLoading = false
          // Kalau GPS ditolak, biarkan input bisa diisi manual
          this.$nextTick(() => {
            const inputs = document.querySelectorAll('input[placeholder="Latitude"], input[placeholder="Longitude"]')
            inputs.forEach(el => el.removeAttribute('readonly'))
          })
        },
        { timeout: 10000 }
      )
    },

    async submitCert() {
      this.errorMsg = null

      // ✅ FIX: Validasi field wajib lebih lengkap
      if (!this.form.nama_peserta) return this.errorMsg = 'Nama peserta wajib diisi!'
      if (!this.form.nama_event) return this.errorMsg = 'Nama event wajib diisi!'
      if (!this.form.nama_lokasi) return this.errorMsg = 'Lokasi kegiatan wajib diisi!'
      if (!this.form.waktu_mulai) return this.errorMsg = 'Waktu mulai wajib diisi!'
      if (!this.form.waktu_selesai) return this.errorMsg = 'Waktu selesai wajib diisi!'

      this.loading = true
      try {
        // ✅ FIX: Kirim data dengan benar, konversi lat/lng ke number jika ada
        const payload = {
          ...this.form,
          latitude: this.form.latitude ? parseFloat(this.form.latitude) : null,
          longitude: this.form.longitude ? parseFloat(this.form.longitude) : null,
        }

        const res = await axios.post(`${this.API_URL}/issue-sertifikat`, payload)
        this.result = res.data
        this.verifyUrl = `${window.location.origin}/verify/${res.data.hash}`

        // Reset form setelah sukses
        this.form = {
          nama_peserta: '', nama_event: '', nama_lokasi: '',
          latitude: '', longitude: '', waktu_mulai: '',
          waktu_selesai: '', keterangan: ''
        }
        this.gpsStatus = ''

      } catch (err) {
        this.errorMsg = err.response?.data?.message || err.message || 'Terjadi kesalahan, coba lagi.'
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