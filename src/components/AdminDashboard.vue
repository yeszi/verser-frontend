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

          <div>
            <label class="block text-xs font-bold text-gray-400 uppercase mb-2 ml-1">Koordinat (Opsional)</label>
            <div class="flex space-x-2">
              <input v-model="form.latitude" type="text" placeholder="Lat" class="w-1/2 p-4 bg-gray-50 border border-gray-200 rounded-2xl text-sm" />
              <input v-model="form.longitude" type="text" placeholder="Lng" class="w-1/2 p-4 bg-gray-50 border border-gray-200 rounded-2xl text-sm" />
            </div>
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

        <button @click="submitCert" :disabled="loading" class="w-full mt-10 bg-indigo-600 text-white font-extrabold py-5 rounded-2xl hover:bg-indigo-700 shadow-lg shadow-indigo-200 transition-all disabled:bg-gray-300 transform active:scale-[0.98]">
          {{ loading ? 'Sedang Memproses Chain...' : 'Kunci Sertifikat ke Blockchain' }}
        </button>
      </div>

      <div v-if="result" class="mt-8 bg-emerald-50 p-8 rounded-3xl border-2 border-emerald-200 animate-in fade-in duration-500">
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
      result: null,
      verifyUrl: '',
      // URL BACKEND KAMU
      API_URL: 'https://verser-chain.vercel.app',
      form: {
        nama_peserta: '', nama_event: '', nama_lokasi: '',
        latitude: '', longitude: '', waktu_mulai: '',
        waktu_selesai: '', keterangan: ''
      }
    }
  },
  methods: {
    async submitCert() {
      if(!this.form.nama_peserta || !this.form.nama_event) return alert("Nama dan Event wajib diisi!")
      this.loading = true
      try {
        const res = await axios.post(`${this.API_URL}/issue-sertifikat`, this.form)
        this.result = res.data
        // Link verifikasi arahkan ke domain frontend kamu (vadser.vercel.app)
        this.verifyUrl = `${window.location.origin}/verify/${res.data.hash}`
      } catch (err) {
        alert("Gagal: " + (err.response?.data?.message || err.message))
      } finally { this.loading = false }
    },
    logout() {
      localStorage.removeItem('token')
      this.$router.push('/')
    }
  }
}
</script>