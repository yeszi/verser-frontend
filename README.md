# VeriZh Chain 🔗
A Lightweight Blockchain-based Digital Certificate Verification System.

Built with **Vue.js** (Frontend) + **Flask** (Backend) + **Supabase** (Database), deployed on **Vercel**.

---

## Live Demo
- Frontend: [verser-phi.vercel.app](https://verser-phi.vercel.app)
- Backend API: [verser-chain.vercel.app](https://verser-chain.vercel.app)

---

## How It Works
1. Admin logs in and issues a certificate → system generates a SHA-256 hash
2. A QR Code is created from the certificate's verify URL
3. Anyone can scan the QR Code to verify the certificate — no login required

---

## Environment Variables
```env
SUPABASE_URL=
SUPABASE_KEY=
ADMIN_USERNAME=
ADMIN_PASSWORD=
JWT_SECRET=
```

---

## Tech Stack
- **Frontend** — Vue.js 3, Vue Router
- **Backend** — Python, Flask, PyJWT, Flask-Limiter
- **Database** — Supabase (PostgreSQL)
- **Deployment** — Vercel

---

**Grayesi Silitonga** — Informatics Engineering, UMRAH 2026