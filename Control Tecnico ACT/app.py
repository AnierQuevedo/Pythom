import sqlite3
import tkinter as tk
from tkinter import messagebox
from tkinter import ttk
from tkcalendar import DateEntry
import datetime
from dateutil.parser import parse



def init_db():
    conn = sqlite3.connect('ControlTecnico.db')

    conn.execute('''CREATE TABLE IF NOT EXISTS presas (
                        id INTEGER PRIMARY KEY,
                        nombre TEXT NOT NULL UNIQUE)''')

    conn.execute('''CREATE TABLE IF NOT EXISTS controles_tecnicos (
                        id INTEGER PRIMARY KEY,
                        presa_id INTEGER NOT NULL,
                        fecha DATE NOT NULL,
                        hora TIME NOT NULL,
                        control_filtraciones REAL,
                        control_piezometria REAL,
                        deformaciones REAL,
                        analisis_fisico_quimico REAL,
                        nivel_embalse REAL,
                        lluvia REAL,
                        FOREIGN KEY (presa_id) REFERENCES presas (id))''')

    presas = [("Zaza",), ("Tuinucú",), ("Siguaney",), ("Lebrije",), ("La Felicidad",), ("Dignorah",), ("Bana2",), ("Aridanes",), ("Higuanojo",)]
    conn.executemany("INSERT OR IGNORE INTO presas (nombre) VALUES (?)", presas)

    conn.commit()
    conn.close()

init_db()

def generar_lista_horas():
    horas = []
    for hora in range(24):
        for minuto in range(0, 60, 15):  # Incremento de 15 minutos, puedes cambiarlo según tus necesidades
            horas.append(f"{hora:02d}:{minuto:02d}")
    return horas

class App:
    def __init__(self, root):
        self.root = root
        self.root.title("Control Hidráulico Sancti Spíritus")

        # Widgets para seleccionar la presa
        self.presa_label = tk.Label(self.root, text="Presa:")
        self.presa_label.grid(row=0, column=0)
        self.presa_combobox = ttk.Combobox(self.root, values=["Zaza", "Tuinucú", "Siguaney"])
        self.presa_combobox.grid(row=0, column=1)

        # Widgets para ingresar la fecha y hora
        self.fecha_label = tk.Label(self.root, text="Fecha:")
        self.fecha_label.grid(row=1, column=0)
        self.fecha_entry = DateEntry(self.root)
        self.fecha_entry.grid(row=1, column=1)

        self.hora_label = tk.Label(self.root, text="Hora:")
        self.hora_label.grid(row=2, column=0)
        self.hora_combobox = ttk.Combobox(self.root, values=generar_lista_horas())
        self.hora_combobox.grid(row=2, column=1)

        # Widgets para ingresar los controles técnicos
        self.control_filtraciones_label = tk.Label(self.root, text="Nivel:")
        self.control_filtraciones_label.grid(row=3, column=0)
        self.control_filtraciones_entry = tk.Entry(self.root)
        self.control_filtraciones_entry.grid(row=3, column=1)

        self.control_piezometria_label = tk.Label(self.root, text="Lectura:")
        self.control_piezometria_label.grid(row=4, column=0)
        self.control_piezometria_entry = tk.Entry(self.root)
        self.control_piezometria_entry.grid(row=4, column=1)

        self.deformaciones_label = tk.Label(self.root, text="Volumen:")
        self.deformaciones_label.grid(row=5, column=0)
        self.deformaciones_entry = tk.Entry(self.root)
        self.deformaciones_entry.grid(row=5, column=1)

        self.analisis_fisico_quimico_label = tk.Label(self.root, text="Lluvia:")
        self.analisis_fisico_quimico_label.grid(row=6, column=0)
        self.analisis_fisico_quimico_entry = tk.Entry(self.root)
        self.analisis_fisico_quimico_entry.grid(row=6, column=1)

        self.agregar_button = tk.Button(self.root, text="Agregar Registro", command=self.agregar_registro)
        self.agregar_button.grid(row=7, column=0)

        self.mostrar_button = tk.Button(self.root, text="Mostrar Registros", command=self.mostrar_registros)
        self.mostrar_button.grid(row=7, column=1)

        self.eliminar_button = tk.Button(self.root, text="Eliminar Registro", command=self.eliminar_registro)
        self.eliminar_button.grid(row=8, column=0)

        self.editar_button = tk.Button(self.root, text="Editar Registro", command=self.editar_registro)
        self.editar_button.grid(row=8, column=1, columnspan=2)

        # Crear el Treeview y el Scrollbar
        self.treeview = ttk.Treeview(self.root, selectmode="browse")
        self.treeview.grid(row=9, column=0, columnspan=2, padx=10, pady=10)

        self.scrollbar = ttk.Scrollbar(self.root, orient='vertical', command=self.treeview.yview)
        self.scrollbar.grid(row=9, column=2, sticky='ns')

        self.treeview.configure(yscrollcommand=self.scrollbar.set)



        # Crear las columnas
        self.crear_columnas_treeview()

        # Mostrar registros al iniciar la aplicación
        self.mostrar_registros()

    def crear_columnas_treeview(self):
        self.treeview['columns'] = ('presa', 'fecha', 'hora', 'nivel', 'lectura', 'volumen', 'lluvia')
        
        for col in self.treeview['columns']:
            self.treeview.heading(col, text=col.title())
            self.treeview.column(col, anchor='center', width=100)


    
    def agregar_registro(self):
           presa_seleccionada = self.presa_combobox.get()
         
           fecha = self.fecha_entry.get_date()
           hora = self.hora_combobox.get()
           nivel = float(self.control_filtraciones_entry.get())
           lectura = float(self.control_piezometria_entry.get())
           volumen = float(self.deformaciones_entry.get())
           lluvia = float(self.analisis_fisico_quimico_entry.get())

           print("Presa seleccionada:", presa_seleccionada)
           print("Nombre de la presa en minúsculas:", presa_seleccionada.lower())

           self.insert_data_to_db(presa_seleccionada, fecha, hora, nivel, lectura, volumen, lluvia)
  

    def insert_data_to_db(self, presa_seleccionada, fecha, hora, nivel, lectura, volumen, lluvia):
        conn = sqlite3.connect('ControlTecnico.db')
        cursor = conn.cursor()

        try:
          presa_seleccionada = presa_seleccionada.lower()
          cursor.execute("SELECT id FROM presas WHERE LOWER(nombre)=?", (presa_seleccionada,))
          result = cursor.fetchone()  # Guardar el resultado en una variable
          print("Resultado de la consulta:", result)
          presa_id = result[0]  # Obtener presa_id del resultado
        
          cursor.execute("INSERT INTO controles_tecnicos (presa_id, fecha, hora, control_filtraciones, control_piezometria, nivel_embalse, lluvia) VALUES (?, ?, ?, ?, ?, ?, ?)",
                       (presa_id, fecha, hora, nivel, lectura, volumen, lluvia))
          conn.commit()
          messagebox.showinfo("Éxito", "Registro agregado exitosamente")

        except sqlite3.Error as e:
          messagebox.showerror("Error", f"Error al agregar el registro: {e}")
        finally:
         conn.close()




    def mostrar_registros(self):
    # Limpiar la tabla de la interfaz
       for i in self.treeview.get_children():
           self.treeview.delete(i)

       # Obtener los registros de la base de datos               
       conn = sqlite3.connect('ControlTecnico.db')
       cursor = conn.cursor()
        # Realizar la consulta SQL para obtener los registros de la base de datos
       cursor.execute('''SELECT controles_tecnicos.id, presas.nombre, controles_tecnicos.fecha, controles_tecnicos.hora, controles_tecnicos.control_filtraciones,
            controles_tecnicos.control_piezometria, controles_tecnicos.deformaciones, controles_tecnicos.lluvia
            FROM controles_tecnicos
            JOIN presas ON controles_tecnicos.presa_id = presas.id
            ORDER BY controles_tecnicos.id ASC''')  # Modificar la consulta para hacer un JOIN con la tabla presas
       registros = cursor.fetchall()
       conn.close()

    # Actualizar la tabla en la interfaz con los registros obtenidos
       for registro in registros:
          self.treeview.insert('', 'end', values=(registro[1], registro[2], registro[3], registro[4], registro[5], registro[6], registro[7]))

        
    def editar_registro(self):
        selected_item = self.treeview.selection()[0]
        if not selected_item:
          messagebox.showwarning("Advertencia", "Por favor, seleccione un registro para editar.")
          return

        registro_id = self.treeview.item(selected_item)['values'][0]  # Obtener el registro_id aquí

        self.edit_window = tk.Toplevel(self.root)
        self.edit_window.title("Editar Registro")

        # Widgets para seleccionar la presa
        self.edit_presa_label = tk.Label(self.edit_window, text="Presa:")
        self.edit_presa_label.grid(row=0, column=0)
        self.edit_presa_combobox = ttk.Combobox(self.edit_window, values=["Zaza", "Tuinucú", "Siguaney"])
        self.edit_presa_combobox.grid(row=0, column=1)

        # Widgets para ingresar la fecha y hora
        self.edit_fecha_label = tk.Label(self.edit_window, text="Fecha:")
        self.edit_fecha_label.grid(row=1, column=0)
        self.edit_fecha_entry = DateEntry(self.edit_window)
        self.edit_fecha_entry.grid(row=1, column=1)

        self.edit_hora_label = tk.Label(self.edit_window, text="Hora:")
        self.edit_hora_label.grid(row=2, column=0)
        self.edit_hora_combobox = ttk.Combobox(self.edit_window, values=generar_lista_horas())
        self.edit_hora_combobox.grid(row=2, column=1)

        # Widgets para ingresar los controles técnicos
        self.edit_control_filtraciones_label = tk.Label(self.edit_window, text="Nivel:")
        self.edit_control_filtraciones_label.grid(row=3, column=0)
        self.edit_control_filtraciones_entry = tk.Entry(self.edit_window)
        self.edit_control_filtraciones_entry.grid(row=3, column=1)

        self.edit_control_piezometria_label = tk.Label(self.edit_window, text="Lectura:")
        self.edit_control_piezometria_label.grid(row=4, column=0)
        self.edit_control_piezometria_entry = tk.Entry(self.edit_window)
        self.edit_control_piezometria_entry.grid(row=4, column=1)

        self.edit_deformaciones_label = tk.Label(self.edit_window, text="Volumen:")
        self.edit_deformaciones_label.grid(row=5, column=0)
        self.edit_deformaciones_entry = tk.Entry(self.edit_window)
        self.edit_deformaciones_entry.grid(row=5, column=1)

        self.edit_analisis_fisico_quimico_label = tk.Label(self.edit_window, text="Lluvia:")
        self.edit_analisis_fisico_quimico_label.grid(row=6, column=0)
        self.edit_analisis_fisico_quimico_entry = tk.Entry(self.edit_window)
        self.edit_analisis_fisico_quimico_entry.grid(row=6, column=1)


        # Botón para guardar cambios
        save_button = tk.Button(self.edit_window, text="Guardar cambios",
                        command=lambda: (
                            print("Botón Guardar cambios presionado"),
                            self.actualizar_registro(
                                registro_id,  # Pasar registro_id como argumento
                                self.edit_presa_combobox.get(),
                                self.edit_fecha_entry.get_date(),
                                self.edit_hora_combobox.get(),
                                float(self.edit_control_filtraciones_entry.get()),
                                float(self.edit_control_piezometria_entry.get()),
                                float(self.edit_deformaciones_entry.get()),
                                float(self.edit_analisis_fisico_quimico_entry.get())
                            )))
        save_button.grid(row=7, column=0, columnspan=2)


       # Obtener los valores actuales del registro seleccionado
        selected_values = self.treeview.item(selected_item)['values']
        self.edit_presa_combobox.set(selected_values[0])
        self.edit_fecha_entry.delete(0, 'end')
        self.edit_fecha_entry.insert(0, datetime.datetime.strptime(selected_values[1], '%Y-%m-%d').strftime('%Y-%m-%d'))
        self.edit_hora_combobox.set(selected_values[2])
        self.edit_control_filtraciones_entry.insert(0, selected_values[3])
        self.edit_control_piezometria_entry.insert(0, selected_values[4])
        self.edit_deformaciones_entry.insert(0, selected_values[5])
        self.edit_analisis_fisico_quimico_entry.insert(0, selected_values[6])
         
    def actualizar_registro(self, registro_id, presa_seleccionada, fecha, hora, nivel, lectura, volumen, lluvia):
        # Obtener el ID de la presa seleccionada
        conn = sqlite3.connect('ControlTecnico.db')
        cursor = conn.cursor()
        cursor.execute("SELECT id FROM presas WHERE LOWER(nombre)=?", (presa_seleccionada.lower(),))
        result = cursor.fetchone()
        presa_id = result[0]

        try:
           # Imprimir los valores antes de actualizar
             print(f"Valores antes de actualizar: {registro_id}, {presa_seleccionada}, {fecha}, {hora}, {nivel}, {lectura}, {volumen}, {lluvia}")

             cursor.execute('''UPDATE controles_tecnicos SET
            presa_id=?, fecha=?, hora=?, control_filtraciones=?, control_piezometria=?, deformaciones=?, lluvia=?
            WHERE id=?''', (presa_id, fecha, hora, nivel, lectura, volumen, lluvia, registro_id))  # Corrección: Cambiar 'presa_seleccionada' a 'presa_id'
             conn.commit()
             messagebox.showinfo("Éxito", "Registro actualizado exitosamente")

             # Imprimir los valores después de actualizar
             cursor.execute("SELECT * FROM controles_tecnicos WHERE id=?", (registro_id,))
             registro_actualizado = cursor.fetchone()
             print(f"Valores después de actualizar: {registro_actualizado}")

        except sqlite3.Error as e:
          messagebox.showerror("Error", f"Error al actualizar el registro: {e}")
        finally:
         
          # Cerrar la ventana de edición y actualizar la tabla en la interfaz principal
         self.edit_window.destroy()
         self.mostrar_registros()
         conn.close()


            
        
    def eliminar_registro(self):
        selected_item = self.treeview.selection()[0]
        registro_id = self.treeview.item(selected_item)['values'][0]

        # Eliminar el registro de la base de datos
        conn = sqlite3.connect('DatosTecnicos.db')
        cursor = conn.cursor()
        try:
            cursor.execute("DELETE FROM controles_tecnicos WHERE id=?", (registro_id,))
            conn.commit()
            messagebox.showinfo("Éxito", "Registro eliminado exitosamente")
        except sqlite3.Error as e:
            messagebox.showerror("Error", f"Error al eliminar el registro: {e}")
        finally:
            conn.close()

        # Eliminar el registro de la interfaz
        self.treeview.delete(selected_item)
          
      
        conn.close()

if __name__ == "__main__":
    root = tk.Tk()
    app = App(root)
    root.mainloop()