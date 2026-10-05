import matplotlib.pyplot as plt


class Visualization:
    def show_results(self, results, title):
        times = [result["time"] for result in results]
        indexes = [result["index"] for result in results]

        plt.figure(figsize=(10, 5))
        plt.plot(times, indexes, marker="o")
        plt.axhline(0.40, linestyle="--", label="Baja posibilidad")
        plt.axhline(0.60, linestyle="--", label="Lluvia probable")
        plt.axhline(0.75, linestyle="--", label="Lluvia")

        plt.title(title)
        plt.xlabel("Hora")
        plt.ylabel("Índice de lluvia")
        plt.ylim(0, 1)
        plt.grid(True)
        plt.legend()
        plt.tight_layout()
        plt.show()