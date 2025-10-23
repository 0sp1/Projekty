droga = float(input("droga: "))
średnie_spalanie = float(input("spalanie: "))
cena_za_litr = 6.5

dystans_do_litra_paliwa = średnie_spalanie/100
spalanie = dystans_do_litra_paliwa*droga

print(f"Spalanie {spalanie}l, Koszt podróży {spalanie*cena_za_litr}zł")