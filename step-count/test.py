from walking_data import WalkingData
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent

data_p1_1 = WalkingData(BASE_DIR / "data" / "p1.1_Female_20-29_170-179cm_Hand_held.out.csv")
data_p1_4 = WalkingData(BASE_DIR / "data" / "p1.4_Female_20-29_170-179cm_Handbag.out.csv")
data_p2_2 = WalkingData(BASE_DIR / "data" / "p2.2_Male_20-29_180-189cm_Hand_held.out.csv")
data_p9_2 = WalkingData(BASE_DIR / "data" / "p9.2_Female_15-19_160-169cm_Trousers_back_pocket.out.csv")
data_p11_3 = WalkingData(BASE_DIR / "data" / "p11.3_Male_20-29_170-179cm_Backpack.out.csv")
data_p27_1 = WalkingData(BASE_DIR / "data" / "p27.1_Male_15-19_170-179cm_Hand_held.dat.csv")

print(f"Participant\tSteps Taken\tSteps Found")
print(f"p1.1\t\t70\t\t{  data_p1_1.get_steps()}")
print(f"p1.4\t\t70\t\t{  data_p1_4.get_steps()}")
print(f"p2.2\t\t66\t\t{  data_p2_2.get_steps()}")
print(f"p9.2\t\t70\t\t{  data_p9_2.get_steps()}")
print(f"p11.3\t\t76\t\t{data_p11_3.get_steps()}")
print(f"p27.1\t\t68\t\t{data_p27_1.get_steps()}")