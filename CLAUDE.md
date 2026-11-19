# Fakta Rumah: aturan kerja untuk Claude

Channel pengetahuan rumah, Bahasa Indonesia santai, penonton 35+. Identitas lengkap di `IDENTITAS.md`; pelajaran dan angka di `PELAJARAN.md`. Di awal sesi baca `README.md`, `KEPUTUSAN-TERBUKA.md`, dan `eksperimen/log.md` saja.

## Prinsip
1. **Satu eksperimen, satu variabel.** Setiap video menguji satu hal (hook, format, suara, topik), dicatat di `eksperimen/log.md` sebelum dibuat dan diisi hasilnya setelah 48 jam.
2. **Data dulu, alat kemudian.** Jangan membangun kit, kerangka, atau otomasi baru sebelum ada bukti bahwa itu mengubah views atau retensi. Alat lama hanya diambil dari repo `channel-penjelasan` bila diminta.
3. **Keputusan milik pemilik channel:** topik, format produksi, suara, seri, frekuensi. Beri rekomendasi + alasan, lalu tunggu jawaban. Jangan memilih diam-diam.
4. **Jujur soal kelemahan.** Katakan di awal bila sesuatu mentok atau lemah; jangan menambal berulang tanpa bilang.

## Isi
- Fakta harus bersumber; tandai "(perkiraan)", [⚠ CEK], dan penyederhanaan visual. Jangan mengarang angka, kutipan, atau tayangan.
- Hook ≤ 3 detik, memakai kata yang sudah ditakuti atau dicari penonton (bukan teka-teki angka).
- Teks publik (naskah, caption, judul, komentar pin) dilewatkan skill `anthropic-skills:humanizer`, gaya `caption/gaya-caption.md`. Komentar pin tidak mengarang pengalaman kreator.
- Setelah naskah di-ACC: caption + komentar pin langsung ditulis.

## Suara dan produksi
- Format produksi diputuskan di `KEPUTUSAN-TERBUKA.md`; belum ada default.
- Bila TTS dipakai: tanya dulu Gemini TTS atau ElevenLabs. ElevenLabs hanya 1 take (`generations_count: 1`), naskah final dulu, revisi hanya kalimat yang berubah.

## Penyimpanan
- Hasil jadi (video, cover, info) di Google Drive, folder "Fakta Rumah" (`1Dx9nqhifWRbixFb_2u4XrHMIaHHJloAt`), satu subfolder per video `#NN judul`. MP4 dan cover tidak di-commit.
- Perbarui log eksperimen setiap ada kemajuan, jangan menunggu akhir sesi.
- PR dan merge ke `main`: tanyakan izin pemilik channel dulu (izin lama berlaku untuk repo lama).

## Gaya jawaban
Singkat: hasil, file, keputusan yang dibutuhkan. Saat berdiskusi dengan pemilik channel boleh selengkapnya.
