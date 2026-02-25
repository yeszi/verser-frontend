<template>
  <div class="min-h-screen bg-slate-50 flex items-center justify-center p-6">
    <div v-if="loading" class="text-center">
      <div class="w-14 h-14 border-4 border-indigo-600 border-t-transparent rounded-full animate-spin mx-auto"></div>
      <p class="text-gray-400 font-bold mt-4 text-sm tracking-widest uppercase">Mengecek Ledger...</p>
    </div>

    <div v-else-if="data" class="max-w-md w-full bg-white rounded-[2.5rem] shadow-2xl overflow-hidden border border-gray-100">
      <div class="bg-indigo-700 p-8 text-center text-white relative">
        <div class="absolute top-0 right-0 p-4 opacity-10 text-4xl font-black italic underline">BLOCKCHAIN</div>
        <div class="bg-white/20 w-20 h-20 rounded-full flex items-center justify-center mx-auto mb-4 border border-white/30">
          <span class="text-4xl">💎</span>
        </div>
        <h2 class="text-xl font-black tracking-widest uppercase">Verified Authentic</h2>
        <p class="text-[10px] font-bold opacity-60 mt-1">Sertifikat Digital Terenkripsi</p>
      </div>

      <div class="p-10 space-y-8">
        <div class="text-center">
          <p class="text-[10px] font-black text-gray-300 uppercase tracking-[0.2em] mb-2">Nama Pemilik</p>
          <h3 class="text-3xl font-serif italic text-gray-900 leading-tight">{{ data.nama_peserta }}</h3>
        </div>

        <div class="grid grid-cols-2 gap-6 py-6 border-y border-gray-50">
          <div>
            <p class="text-[9px] font-black text-indigo-300 uppercase mb-1">Kegiatan</p>
            <p class="text-sm font-bold text-gray-700 leading-snug">{{ data.nama_event }}</p>
          </div>
          <div>
            <p class="text-[9px] font-black text-indigo-300 uppercase mb-1">Lokasi</p>
            <p class="text-sm font-bold text-gray-700 leading-snug">{{ data.nama_lokasi }}</p>
          </div>
          <div>
            <p class="text-[9px] font-black text-indigo-300 uppercase mb-1">Waktu Mulai</p>
            <p class="text-sm font-bold text-gray-700 leading-snug">{{ formatDate(data.waktu_mulai) }}</p>
          </div>
          <div>
            <p class="text-[9px] font-black text-indigo-300 uppercase mb-1">Waktu Selesai</p>
            <p class="text-sm font-bold text-gray-700 leading-snug">{{ formatDate(data.waktu_selesai) }}</p>
          </div>
          <div v-if="data.keterangan" class="col-span-2">
            <p class="text-[9px] font-black text-indigo-300 uppercase mb-1">Keterangan</p>
            <p class="text-sm text-gray-700 leading-snug">{{ data.keterangan }}</p>
          </div>
        </div>

        <div class="space-y-4">
          <div class="p-5 bg-indigo-50/50 rounded-3xl border border-indigo-100">
            <p class="text-[9px] font-black text-indigo-400 uppercase tracking-widest mb-2">Blockchain Proof (Hash)</p>
            <p class="text-[9px] font-mono break-all text-indigo-800 font-bold">{{ data.cert_hash }}</p>
          </div>
          <div class="p-5 bg-slate-50 rounded-3xl border border-slate-100">
            <p class="text-[9px] font-black text-slate-400 uppercase tracking-widest mb-2">Previous Block Link</p>
            <p class="text-[9px] font-mono break-all text-slate-600">{{ data.previous_hash }}</p>
          </div>
        </div>

        <!-- QR CODE di halaman verify -->
        <div class="flex flex-col items-center pt-2">
          <p class="text-[9px] font-black text-gray-300 uppercase tracking-widest mb-3">QR Verifikasi</p>
          <img :src="qrCodeUrl" alt="QR Code" class="w-36 h-36 rounded-2xl border border-gray-100 shadow-sm" />
          <p class="text-[9px] text-gray-400 mt-2 text-center">Scan untuk verifikasi ulang</p>
        </div>
      </div>

      <div class="bg-indigo-900 py-4 text-center">
        <p class="text-white/40 text-[9px] font-black uppercase tracking-[0.3em]">UMRAH Informatics Engineering • 2026</p>
      </div>
    </div>

    <div v-else class="text-center bg-white p-12 rounded-[3rem] shadow-xl max-w-sm">
      <span class="text-6xl mb-6 block">🚫</span>
      <h2 class="text-2xl font-black text-gray-900">Hash Tidak Valid</h2>
      <p class="text-sm text-gray-500 mt-3 font-medium">Data sertifikat ini tidak terdaftar dalam rantai blockchain kami.</p>
      <button @click="$router.push('/')" class="mt-8 text-indigo-600 font-bold hover:underline">Halaman Utama</button>
    </div>
  </div>
</template>

<script>
import { ref, computed, onMounted } from 'vue'
import { useRoute } from 'vue-router'
import axios from 'axios'

export default {
  setup() {
    const route = useRoute()
    const data = ref(null)
    const loading = ref(true)
    const API_URL = 'https://verser-chain.vercel.app'

    const qrCodeUrl = computed(() => {
      if (!data.value) return ''
      const url = window.location.href
      return `https://api.qrserver.com/v1/create-qr-code/?size=200x200&data=${encodeURIComponent(url)}`
    })

    const formatDate = (val) => {
      if (!val) return '-'
      return new Date(val).toLocaleString('id-ID', {
        day: '2-digit', month: 'short', year: 'numeric',
        hour: '2-digit', minute: '2-digit'
      })
    }

    onMounted(async () => {
      try {
        const hash = route.params.hash
        const res = await axios.get(`${API_URL}/verify/${hash}`)
        if (res.data.status === 'VALID') {
          data.value = res.data.data
        }
      } catch (e) {
        console.error('Verify Error:', e)
      } finally {
        loading.value = false
      }
    })

    return { data, loading, qrCodeUrl, formatDate }
  }
}
</script>
