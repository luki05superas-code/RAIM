from io import StringIO
import pandas as pd
import matplotlib.pyplot as plt

csv_data = """Timestamp,Latency,Jitter
22:57:31,0.0052,0
22:57:32,0.002,0.0032
22:57:35,0.002,0.0
22:57:36,0.002,0.0
22:57:38,0.002,0.0
22:57:39,0.0031,0.0011
22:57:41,0.002,0.0011
22:57:42,0.0015,0.0005
22:57:43,0.002,0.0005
22:57:45,0.002,0.0
22:57:46,0.002,0.0
22:57:47,0.0025,0.0005
22:57:48,0.0015,0.001
22:57:50,0.002,0.0005
22:57:51,0.002,0.0
22:57:52,0.0021,0.0001
22:57:53,0.0015,0.0006
22:57:55,0.002,0.0005
22:57:56,0.0025,0.0005
22:57:58,0.002,0.0005
22:57:59,0.0021,0.0001
22:58:02,0.002,0.0001
22:58:04,0.002,0.0
22:58:05,0.0015,0.0005
22:58:07,0.003,0.0015
22:58:08,0.003,0.0
22:58:09,0.002,0.001
22:58:10,0.002,0.0
22:58:11,0.001,0.001
22:58:12,0.002,0.001
22:58:13,0.0015,0.0005
22:58:14,0.0022,0.0007
22:58:15,0.002,0.0002
22:58:16,0.002,0.0
22:58:17,0.002,0.0
22:58:18,0.002,0.0
22:58:20,0.001,0.001
22:58:22,0.002,0.001


"""

# wczytanie danych
df = pd.read_csv(StringIO(csv_data))

# =========================
# WYKRES LATENCJI
# =========================

plt.figure(figsize=(12, 5))

plt.plot(
    df.index,
    df["Latency"],
    marker='o',
    linewidth=2
)

plt.xlabel("Numer pomiaru")
plt.ylabel("Latencja [s]")
plt.title("Latencja transmisji – scenariusz LOSS")

plt.grid(True)

# zapis wykresu
plt.savefig("latency_loss.png", bbox_inches='tight')

plt.close()

# =========================
# WYKRES JITTERA
# =========================

plt.figure(figsize=(12, 5))

plt.plot(
    df.index,
    df["Jitter"],
    marker='o',
    linewidth=2
)

plt.xlabel("Numer pomiaru")
plt.ylabel("Jitter [s]")
plt.title("Jitter transmisji – scenariusz loss")

plt.grid(True)

# zapis wykresu
plt.savefig("jitter_loss.png", bbox_inches='tight')

plt.close()

print("Wykresy zapisane.")
print("latency_loss.png")
print("jitter_loss.png")