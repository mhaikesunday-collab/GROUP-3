import math
import pandas as pd
from datetime import datetime
def calculate_burden(diameter, rock_density):
    return 25 * diameter * (1 / rock_density)
def calculate_spacing(burden):
    return 1.25 * burden
def calculate_holes(area, burden, spacing):
    return int(area / (burden * spacing))
def charge_per_hole(diameter, bench_height, explosive_density):
    radius = diameter / 2
    volume = math.pi * (radius ** 2) * bench_height
    return volume * explosive_density
def powder_factor(total_explosive, rock_volume):
    return total_explosive / rock_volume
def total_cost(total_explosive, unit_cost):
    return total_explosive * unit_cost
# ✅ NEW: Save to Excel with unique name every run
def save_results(data):
    file_name = f"FRANK_{datetime.now().strftime('%Y%m%d_%H%M%S')}.xlsx"
    df = pd.DataFrame([data])
    df.to_excel(file_name, index=False)
    print("Saved as:", file_name)
def main() -> None:
    print("\n--- BLAST DESIGN TOOL ---\n")
    bench_height = float(input("Bench height (m): "))
    hole_diameter = float(input("Hole diameter (m): "))
    rock_density = float(input("Rock density (t/m3): "))
    explosive_density = float(input("Explosive density (t/m3): "))
    unit_cost = float(input("Explosive cost ($/t): "))
    area = float(input("Bench area (m2): "))
    burden = calculate_burden(hole_diameter, rock_density)
    spacing = calculate_spacing(burden)
    holes = calculate_holes(area, burden, spacing)
    charge = charge_per_hole(hole_diameter, bench_height, explosive_density)
    total_explosive = charge * holes
    rock_volume = area * bench_height
    pf = powder_factor(total_explosive, rock_volume)
    cost = total_cost(total_explosive, unit_cost)
    print("\n--- RESULTS ---")
    print(f"Burden: {burden:.2f} m")
    print(f"Spacing: {spacing:.2f} m")
    print(f"Number of holes: {holes}")
    print(f"Charge per hole: {charge:.2f} t")
    print(f"Total explosive: {total_explosive:.2f} t")
    print(f"Powder factor: {pf:.2f} t/m3")
    print(f"Total cost: ${cost:.2f}")
    record = {
        "Date": str(datetime.now()),
        "Bench Height (m)": bench_height,
        "Hole Diameter (m)": hole_diameter,
        "Rock Density (t/m3)": rock_density,
        "Explosive Density (t/m3)": explosive_density,
        "Area (m2)": area,
        "Burden (m)": burden,
        "Spacing (m)": spacing,
        "Number of Holes": holes,
        "Charge per Hole (t)": charge,
        "Total Explosive (t)": total_explosive,
        "Powder Factor (t/m3)": pf,
        "Total Cost ($)": cost
    }
    save_results(record)
    print("\nData saved successfully.\n")
if __name__ == "__main__":
    main()
