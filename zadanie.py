droga = float(input("droga: "))
średnie_spalanie = float(input("spalanie: "))
cena_za_litr = 6.5

litr_na_kilometr = średnie_spalanie/100
zużycie_paliwa = litr_na_kilometr*droga
koszt_podróży = zużycie_paliwa*cena_za_litr

print(f"Spalanie {zużycie_paliwa}l, Koszt podróży {koszt_podróży}zł")