import tkinter as tk
from tkinter import ttk, filedialog, messagebox
import sys
from pathlib import Path
from typing import List
import os
import sys

current_dir = Path(__file__).parent 
ruta_proyecto = current_dir.parent   

sys.path.append(str(ruta_proyecto))
# -------------------------------------------------

from core.proceso import Proceso
from core.simulador import Simulador
from utils.archivo_reader import LectorArchivos

class SimuladorGUI:
    """
    Clase que encapsula la interfaz gráfica del simulador.
    """
    def __init__(self, master: tk.Tk):
        self.master = master
        self.master.title("📊 Simulador de Planificación y Memoria")
        self.master.geometry("800x600")

        self.procesos_cargados: List[Proceso] = []

        self._crear_widgets()

    def _crear_widgets(self):
        # --- Frame de Controles (Superior) ---
        frame_controles = ttk.Frame(self.master, padding="10")
        frame_controles.pack(fill=tk.X)

        self.btn_cargar = ttk.Button(frame_controles, text="Cargar Archivo CSV", command=self._cargar_archivo)
        self.btn_cargar.pack(side=tk.LEFT, padx=5)

        self.btn_simular = ttk.Button(frame_controles, text="▶️ Iniciar Simulación", command=self._iniciar_simulacion, state="disabled")
        self.btn_simular.pack(side=tk.LEFT, padx=5)

        self.lbl_ruta_archivo = ttk.Label(frame_controles, text="Ningún archivo cargado")
        self.lbl_ruta_archivo.pack(side=tk.LEFT, padx=10)

        # --- Frame de Tabla de Procesos (Medio) ---
        frame_tabla = ttk.Frame(self.master, padding="10")
        frame_tabla.pack(fill=tk.BOTH, expand=True)
        
        ttk.Label(frame_tabla, text="Procesos Cargados", font=("Helvetica", 12, "bold")).pack(anchor=tk.W)

        self.tree = ttk.Treeview(frame_tabla, columns=("ID", "Tamaño", "Arribo", "Irrupción"), show="headings")
        self.tree.heading("ID", text="ID")
        self.tree.heading("Tamaño", text="Tamaño (K)")
        self.tree.heading("Arribo", text="T. Arribo")
        self.tree.heading("Irrupción", text="T. Irrupción")
        
        # Ajustar ancho de columnas
        self.tree.column("ID", width=50, anchor=tk.CENTER)
        self.tree.column("Tamaño", width=100, anchor=tk.CENTER)
        self.tree.column("Arribo", width=100, anchor=tk.CENTER)
        self.tree.column("Irrupción", width=100, anchor=tk.CENTER)
        
        scrollbar = ttk.Scrollbar(frame_tabla, orient=tk.VERTICAL, command=self.tree.yview)
        self.tree.configure(yscroll=scrollbar.set)
        
        self.tree.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

        # --- Frame de Consola de Salida (Inferior) ---
        frame_consola = ttk.Frame(self.master, padding="10")
        frame_consola.pack(fill=tk.BOTH, expand=True)
        
        ttk.Label(frame_consola, text="Log de Simulación", font=("Helvetica", 12, "bold")).pack(anchor=tk.W)

        self.consola = tk.Text(frame_consola, height=15, bg="black", fg="white", font=("Courier", 10), state="disabled")
        
        scrollbar_consola = ttk.Scrollbar(frame_consola, orient=tk.VERTICAL, command=self.consola.yview)
        self.consola.configure(yscroll=scrollbar_consola.set)
        
        self.consola.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        scrollbar_consola.pack(side=tk.RIGHT, fill=tk.Y)

    def _escribir_en_consola(self, texto: str):
        """Inserta texto en el widget de la consola."""
        self.consola.config(state="normal")
        self.consola.insert(tk.END, texto)
        self.consola.see(tk.END) # Auto-scroll
        self.consola.config(state="disabled")
        self.master.update_idletasks() # Actualiza la GUI

    def _limpiar_consola(self):
        self.consola.config(state="normal")
        self.consola.delete(1.0, tk.END)
        self.consola.config(state="disabled")

    def _limpiar_tabla(self):
        for item in self.tree.get_children():
            self.tree.delete(item)

    def _cargar_archivo(self):
        """Abre un diálogo para seleccionar un archivo y lo procesa."""
        ruta = filedialog.askopenfilename(
            title="Seleccionar archivo de procesos",
            filetypes=[("Archivos CSV", "*.csv"), ("Todos los archivos", "*.*")]
        )
        if not ruta:
            return

        self._limpiar_tabla()
        self._limpiar_consola()
        
        self.lbl_ruta_archivo.config(text=Path(ruta).name)
        
        procesos, errores = LectorArchivos.leer_procesos_desde_csv(ruta)
        
        if errores:
            self._escribir_en_consola("--- Errores encontrados ---\n")
            for error in errores:
                self._escribir_en_consola(f"• {error}\n")
        
        if procesos:
            self.procesos_cargados = procesos
            for p in self.procesos_cargados:
                self.tree.insert("", tk.END, values=(p.id, p.tamaño, p.tiempo_arribo, p.tiempo_irrupcion))
            self.btn_simular.config(state="normal")
            self._escribir_en_consola("\n--- Procesos cargados exitosamente ---\n")
        else:
            self.procesos_cargados = []
            self.btn_simular.config(state="disabled")
            messagebox.showerror("Error de Carga", "No se pudo cargar ningún proceso válido del archivo.")

    def _iniciar_simulacion(self):
        """Configura y ejecuta la simulación."""
        if not self.procesos_cargados:
            messagebox.showwarning("Advertencia", "No hay procesos cargados para simular.")
            return

        self._limpiar_consola()
        self.btn_cargar.config(state="disabled")
        self.btn_simular.config(state="disabled")

        # Redirigir stdout a la consola de la GUI
        stdout_original = sys.stdout
        sys.stdout = ConsolaRedirector(self)

        try:
            simulador = Simulador(self.procesos_cargados)
            simulador.run()
            simulador.generar_reporte_estadistico()
        except Exception as e:
            messagebox.showerror("Error en Simulación", f"Ocurrió un error inesperado:\n{e}")
        finally:
            # Restaurar stdout y reactivar botones
            sys.stdout = stdout_original
            self.btn_cargar.config(state="normal")
            self.btn_simular.config(state="normal")

class ConsolaRedirector:
    def __init__(self, gui_app: SimuladorGUI):
        self.gui_app = gui_app

    def write(self, texto: str):
        self.gui_app._escribir_en_consola(texto)

    def flush(self):
        # Requerido por la interfaz de sys.stdout
        pass

if __name__ == "__main__":
    root = tk.Tk()
    app = SimuladorGUI(root)
    root.mainloop()