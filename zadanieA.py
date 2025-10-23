import random
droga = random.randint(20, 200)
droga = 79
średnie_spalanie = float(input("Spalanie: "))
cena_za_litr = int(input("Cena paliwa: "))

litr_na_kilometr = średnie_spalanie/100
zużycie_paliwa = litr_na_kilometr*droga
koszt_podróży = zużycie_paliwa*cena_za_litr

print(f"Spalanie {zużycie_paliwa:.2f}L, Koszt podróży {koszt_podróży:.2f}zł")