# Sistema con nuevo diseño de interfaz gráfica mejorado con logo
import tkinter as tk
from tkinter import messagebox
from tkinter import PhotoImage
import os
import datetime
import tempfile
import platform
import subprocess

productos = {
    "Presidente Normal": {"precio": 200, "costo": 175},
    "Presidente Pequeña": {"precio": 125, "costo": 100},
    "Brugal XV": {"precio": 800, "costo": 650},
    "Brugal Extra Viejo": {"precio": 750, "costo": 600},
    "Brugal Doble Reserva": {"precio": 900, "costo": 700},
    "Corona": {"precio": 150, "costo": 100},
    "Vive 100 V/R/A": {"precio": 100, "costo": 50},
    "911": {"precio": 75, "costo": 50},
    "Gaytorade": {"precio": 50, "costo": 50},
    "Ciclon": {"precio": 75, "costo": 50},
    "Red bull": {"precio": 100, "costo": 50},
}

ventas_dia = {producto: 0 for producto in productos}

root = tk.Tk()
root.title("D Xiomara Bar")
root.geometry("1200x750")
root.configure(bg="#001f3f")  # azul marino

# Logo
logo_img = PhotoImage(file="logo.png")  # Asegúrate de tener un archivo llamado logo.png en la misma carpeta
logo_label = tk.Label(root, image=logo_img, bg="#001f3f")
logo_label.pack(pady=10)

main_frame = tk.Frame(root, bg="#001f3f")
main_frame.pack(padx=20, pady=5, fill="both", expand=True)

izquierda = tk.Frame(main_frame, bg="#001f3f")
izquierda.pack(side="left", padx=10, pady=10)

derecha = tk.Frame(main_frame, bg="#001f3f")
derecha.pack(side="right", padx=10, pady=10)

cliente_label = tk.Label(izquierda, text="Cliente:", font=('Arial', 14), bg="#001f3f", fg="white")
cliente_label.grid(row=0, column=0, sticky="w")
cliente_entry = tk.Entry(izquierda, font=('Arial', 14))
cliente_entry.grid(row=0, column=1, pady=5, sticky="w")

cantidades = {}
row_b = 1
row_m = 1

bebidas_frame = tk.LabelFrame(izquierda, text="Bebidas", font=('Arial', 14, 'bold'), bg="#001f3f", fg="white")
bebidas_frame.grid(row=1, column=0, padx=5, pady=10, sticky="n")

mezclas_frame = tk.LabelFrame(izquierda, text="Mezclas", font=('Arial', 14, 'bold'), bg="#001f3f", fg="white")
mezclas_frame.grid(row=1, column=1, padx=5, pady=10, sticky="n")

for i, producto in enumerate(productos):
    if i < 6:
        tk.Label(bebidas_frame, text=producto, font=('Arial', 12), bg="#001f3f", fg="white").grid(row=row_b, column=0, sticky='w')
        entry = tk.Entry(bebidas_frame, width=5, font=('Arial', 12))
        entry.grid(row=row_b, column=1, padx=5, pady=2)
        cantidades[producto] = entry
        row_b += 1
    else:
        tk.Label(mezclas_frame, text=producto, font=('Arial', 12), bg="#001f3f", fg="white").grid(row=row_m, column=0, sticky='w')
        entry = tk.Entry(mezclas_frame, width=5, font=('Arial', 12))
        entry.grid(row=row_m, column=1, padx=5, pady=2)
        cantidades[producto] = entry
        row_m += 1

resultado = tk.StringVar()
cuadro_factura = tk.Label(derecha, textvariable=resultado, justify='left', bg="white", anchor='nw', font=('Courier', 12), width=70, height=30, bd=2, relief="sunken")
cuadro_factura.pack()

def agregar_a_factura(event=None):
    factura = "Factura de Compra\n"
    total = 0
    for producto, entry in cantidades.items():
        try:
            cantidad = int(entry.get())
        except:
            cantidad = 0
        if cantidad > 0:
            subtotal = cantidad * productos[producto]["precio"]
            factura += f"{producto}: {cantidad} x {productos[producto]['precio']} = {subtotal}\n"
            total += subtotal
    factura += f"\nTotal: {total} RD$"
    resultado.set(factura)

def facturar():
    cliente = cliente_entry.get()
    if not cliente:
        messagebox.showwarning("Falta información", "Debe ingresar el nombre del cliente.")
        return

    factura = f"Factura de {cliente}\n"
    total = 0
    for producto, entry in cantidades.items():
        try:
            cantidad = int(entry.get())
        except:
            cantidad = 0
        if cantidad > 0:
            ventas_dia[producto] += cantidad
            subtotal = cantidad * productos[producto]["precio"]
            factura += f"{producto}: {cantidad} x {productos[producto]['precio']} = {subtotal}\n"
            total += subtotal
    factura += f"\nTotal: {total} RD$"
    resultado.set(factura)

    fecha = datetime.datetime.now().strftime("%Y-%m-%d")
    os.makedirs("facturas", exist_ok=True)
    filename = f"facturas/{cliente}_{fecha}.txt"
    with open(filename, "w") as f:
        f.write(factura)
    imprimir_factura(factura)
    limpiar()

def imprimir_factura(texto):
    temp = tempfile.NamedTemporaryFile(delete=False, suffix=".txt")
    temp.write(texto.encode('utf-8'))
    temp.close()

    if platform.system() == "Windows":
        os.startfile(temp.name, "print")
    elif platform.system() == "Darwin":
        subprocess.run(["lp", temp.name])
    else:
        subprocess.run(["lpr", temp.name])

def limpiar():
    for entry in cantidades.values():
        entry.delete(0, tk.END)
    resultado.set("")
    cliente_entry.delete(0, tk.END)

def cerrar_dia():
    total_dia = 0
    ganancia_total = 0
    cuadre = "Cuadre del Día\n"
    for producto, cantidad in ventas_dia.items():
        if cantidad > 0:
            precio = productos[producto]["precio"]
            costo = productos[producto]["costo"]
            subtotal = cantidad * precio
            ganancia = cantidad * (precio - costo)
            cuadre += f"{producto}: {cantidad} x {precio} = {subtotal} | Ganancia: {ganancia}\n"
            total_dia += subtotal
            ganancia_total += ganancia
    cuadre += f"\nTotal Vendido: {total_dia} RD$\nGanancia Total: {ganancia_total} RD$"
    resultado.set(cuadre)

def buscar_factura():
    cliente = cliente_entry.get()
    if not cliente:
        messagebox.showwarning("Falta información", "Debe ingresar el nombre del cliente para buscar su factura.")
        return
    fecha = datetime.datetime.now().strftime("%Y-%m-%d")
    filename = f"facturas/{cliente}_{fecha}.txt"
    if os.path.exists(filename):
        with open(filename, "r") as f:
            contenido = f.read()
            resultado.set(contenido)
    else:
        messagebox.showinfo("Factura no encontrada", f"No se encontró factura para {cliente} en {fecha}.")

btn_frame = tk.Frame(izquierda, bg="#001f3f")
btn_frame.grid(row=2, column=0, columnspan=2, pady=20)

btn1 = tk.Button(btn_frame, text="Facturar", command=facturar, font=('Arial', 14), width=12, bg="#0074D9", fg="white")
btn1.grid(row=0, column=0, padx=5)

btn2 = tk.Button(btn_frame, text="Limpiar", command=limpiar, font=('Arial', 14), width=12, bg="#FF4136", fg="white")
btn2.grid(row=0, column=1, padx=5)

btn3 = tk.Button(btn_frame, text="Cerrar Día", command=cerrar_dia, font=('Arial', 14), width=12, bg="#2ECC40", fg="white")
btn3.grid(row=0, column=2, padx=5)

btn4 = tk.Button(btn_frame, text="Buscar Factura", command=buscar_factura, font=('Arial', 14), width=15, bg="#FF851B", fg="white")
btn4.grid(row=0, column=3, padx=5)

btn5 = tk.Button(btn_frame, text="Imprimir", command=lambda: imprimir_factura(resultado.get()), font=('Arial', 14), width=12, bg="#B10DC9", fg="white")
btn5.grid(row=0, column=4, padx=5)

root.bind('<Return>', agregar_a_factura)
root.mainloop()
