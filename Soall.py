import sqlite3 #Modul untuk bekerja dengan database SQLite
from tkinter import Tk, Label, Entry, Button, StringVar, messagebox, ttk #Modul untuk GUI

def create_database(): #fungsi untuk membuat database 
    conn = sqlite3.connect('nilai_siswa_.db') #membuat/menghubungkan ke database
    cursor = conn.cursor() #membuat objek cursor untuk eksekusi SQL
    #Fungsi untuk Membuat tabel
    cursor.execute('''  
        CREATE TABLE IF NOT EXISTS nilai_siswa (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            nama_siswa TEXT NOT NULL,
            biologi INTEGER,
            fisika INTEGER,
            inggris INTEGER,
            prediksi_fakultas TEXT
        )
    ''')
    conn.commit() #Menyimpan perubahan
    conn.close() #menutup koneksi

#Fungsi untuk mengambil data dari database
def fetch_data():
    conn = sqlite3.connect('nilai_siswa_.db')
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM nilai_siswa') #Mengambil semua data
    rows = cursor.fetchall()
    conn.close()
    return rows

#FUngsi untuk menyimpan data baru ke database
def save_to_database(nama, biologi, fisika, inggris, prediksi):
    conn = sqlite3.connect('nilai_siswa_.db')
    cursor = conn.cursor()
    #Menambah data baru ke tabel
    cursor.execute('''
        INSERT INTO nilai_siswa (nama_siswa, biologi, fisika, inggris, prediksi_fakultas)
        VALUES (?, ?, ?, ?, ?)
    ''', (nama, biologi, fisika, inggris, prediksi))
    conn.commit()
    conn.close()

#Fungsi untuk memperbarui data di database
def update_database(record_id, nama, biologi, fisika, inggris, prediksi):
    conn = sqlite3.connect('nilai_siswa_.db')
    cursor = conn.cursor()
    #update data berdasarkan ID
    cursor.execute('''
        UPDATE nilai_siswa
        SET nama_siswa = ?, biologi = ?, fisika = ?, inggris = ?, prediksi_fakultas = ?
        WHERE id = ?
    ''', (nama, biologi, fisika, inggris, prediksi, record_id))
    conn.commit()
    conn.close()

#Fungsi untuk menghapus data di database
def delete_database(record_id):
    conn = sqlite3.connect('nilai_siswa_.db')
    cursor = conn.cursor()
    #Menghapus data berdasarkan ID
    cursor.execute('DELETE FROM nilai_siswa WHERE id = ?', (record_id,))
    conn.commit()
    conn.close()

#Fungsi untuk menghitung prediksi dakultas berdasarkan nilai tertinggi
def calculate_prediction(biologi, fisika, inggris):
    if biologi > fisika and biologi > inggris:
        return "Kedokteran" #Jika yang tertinggi nilai Biologi
    elif fisika > biologi and fisika > inggris:
        return "Teknik" #Jika yang tertinggi nilai Fisika
    elif inggris > biologi and inggris > fisika:
        return "Bahasa" #Jika yang tertinggi nilai Bahasa inggris
    else:
        return "Tidak diketahui" #Jika nilainya sama atau tidak jelas

#Fungsi untuk menambah data baru
def submit():
    try:
        #MEngambil input dari pengguna
        nama = nama_var.get()
        biologi = int(biologi_var.get())
        fisika = int(fisika_var.get())
        inggris = int(inggris_var.get())

        #Validasi input nama
        if not nama:
            raise ValueError("Nama siswa tidak boleh kosong.")
        
        prediksi = calculate_prediction(biologi, fisika, inggris) #Hitung prediksi
        save_to_database(nama, biologi, fisika, inggris, prediksi) #Simpan ke database
        messagebox.showinfo("Sukses", f"Data Berhasil disimpan!\nPrediksi fakultas: {prediksi}")
        clear_inputs() #Bersihkan input setelah disimpan
        populate_table() #Perbarui tabel dengan data baru

    except ValueError as e:
        messagebox.showerror("Error", f"Input tidak valid: {e}")

#Fungsi untuk memperbarui data yang dipilih
def update():
    try:
        #VAlidasi jika tidak ada data yang dipilih
        if not selected_record_id.get():
            raise ValueError("Pilih data dari tabel untuk di-update.")

        #Ambil input baru
        record_id = int(selected_record_id.get())
        nama = nama_var.get()
        biologi = int(biologi_var.get())
        fisika = int(fisika_var.get())
        inggris = int(inggris_var.get())

        if not nama:
            raise ValueError("Nama siswa tidak boleh kosong.")
        
        prediksi = calculate_prediction(biologi, fisika, inggris)
        update_database(record_id, nama, biologi, fisika, inggris, prediksi)
        messagebox.showinfo("Sukses", "Data Berhasil diperbarui!")
        clear_inputs()
        populate_table()

    except ValueError as e:
        messagebox.showerror("Error", f"Kesalahan: {e}")

#Fungsi untuk menghapus data yang dipilih 
def delete():
    try:
        #Validasi jika tidak ada data yang dipilih
        if not selected_record_id.get():
            raise ValueError("Pilih data dari tabel untuk dihapus!")

        record_id = int(selected_record_id.get())
        delete_database(record_id)
        messagebox.showinfo("Sukses", "Data Berhasil dihapus!")
        clear_inputs()
        populate_table()

    except ValueError as e:
        messagebox.showerror("Error", f"Kesalahan: {e}")

#Fungsi untuk mengosongkan input
def clear_inputs():
    nama_var.set("")
    biologi_var.set("")
    fisika_var.set("")
    inggris_var.set("")
    selected_record_id.set("")

#FUngsi untuk menampilkan data di tabel
def populate_table():
    for row in tree.get_children(): #Hapus semua baris lama di tabel
        tree.delete(row)
    for row in fetch_data(): #Tambah baris baru dari database
        tree.insert('', 'end', values=row)

#Fungsi untuk isi input berdasarkan data yang dipilih di tabel
def fill_inputs_from_table(event):
    try:
        selected_item = tree.selection()[0] #Ambil baris yang dipilih
        selected_row = tree.item(selected_item)['values'] #Ambil data dari baris tsb

        #Isi input berdasarkan data yang dipilih
        selected_record_id.set(selected_row[0])
        nama_var.set(selected_row[1])
        biologi_var.set(selected_row[2])
        fisika_var.set(selected_row[3])
        inggris_var.set(selected_row[4])
    except IndexError:
        messagebox.showerror("Error", "Pilih data yang valid")
#Membuat database
create_database()

#Membuat GUI
root = Tk()
root.title("Prediksi Fakultas Siswa")

#Variabel input
nama_var = StringVar()
biologi_var = StringVar()
fisika_var = StringVar()
inggris_var = StringVar()
selected_record_id = StringVar()

#Label dan Entry untuk input data
Label(root, text="Nama Siswa").grid(row=0, column=0, padx=10, pady=5)
Entry(root, textvariable=nama_var).grid(row=0, column=1, padx=10, pady=5)

Label(root, text="Nilai Biologi").grid(row=1, column=0, padx=10, pady=5)
Entry(root, textvariable=biologi_var).grid(row=1, column=1, padx=10, pady=5)

Label(root, text="Nilai Fisika").grid(row=2, column=0, padx=10, pady=5)
Entry(root, textvariable=fisika_var).grid(row=2, column=1, padx=10, pady=5)

Label(root, text="Nilai Bahasa Inggris").grid(row=3, column=0, padx=10, pady=5)
Entry(root, textvariable=inggris_var).grid(row=3, column=1, padx=10, pady=5)

#Tombol Add, Update, dan Delete
Button(root, text="Add", command=submit).grid(row=4, column=0, pady=10)
Button(root, text="Update", command=update).grid(row=4, column=1, pady=10)
Button(root, text="Delete", command=delete).grid(row=4, column=2, pady=10)

#Tabel untuk menampilkan data
columns = ('id', 'nama_siswa', 'biologi', 'fisika', 'inggris', 'prediksi_fakultas')
tree = ttk.Treeview(root, columns=columns, show='headings')

#Konfigurasi kolom tabel
for col in columns:
    tree.heading(col, text=col.capitalize()) #Judul kolom
    tree.column(col, anchor='center') #Perataan teks

tree.grid(row=5, column=0, columnspan=3, padx=10, pady=10)

tree.bind('<ButtonRelease-1>', fill_inputs_from_table) #Event saat memilih data di tabel

populate_table() #Tampilkan data di tabel

root.mainloop() #Menjalankan aplikasi