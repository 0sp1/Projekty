import qrcode

def generate_qr(data, filename="qrcode.png"):
    qr = qrcode.QRCode(
        version=1,  # Controls size: 1 (21x21) to 40 (177x177)
        error_correction=qrcode.constants.ERROR_CORRECT_H,
        box_size=10,
        border=4
    )
    qr.add_data(data)
    qr.make(fit=True)

    img = qr.make_image(fill_color="black", back_color="white")
    img.save(filename)
    print(f"✅ QR code saved as {filename}")

def main():
    print("🔳 QR Code Generator")
    while True:
        data = input("\nEnter text or URL to encode (or 'exit' to quit): ")
        if data.lower() == "exit":
            print("👋 Goodbye!")
            break

        filename = input("Filename to save as (default: qrcode.png): ").strip()
        if not filename:
            filename = "qrcode.png"
        elif not filename.endswith(".png"):
            filename += ".png"

        generate_qr(data, filename)

if __name__ == "__main__":
    main()
