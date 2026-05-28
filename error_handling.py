# Tanpa error handling — berbahaya
data = ["15000", "N/A", "25000", "error", "50000"]

# for item in data:
#     nilai = int(item)
#     print(f"Nilai: {nilai}")

for item in data:
    try:
        nilai = int(item)
        print(f"Nilai: {nilai}")
    except ValueError:
        print(f"Data tidak valid, dilewati: {item}")

with open("error_log.txt", "w") as log:
    for item in data:
        try:
            nilai = int(item)
            print(f"Nilai: {nilai}")
        except ValueError:
            pesan = f"Data tidak valid: {item}\n"
            print(pesan)
            log.write(pesan)

print("Selesai - cek error_log.txt")
