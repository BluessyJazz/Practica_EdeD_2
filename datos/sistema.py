import csv
import os
from listas.list import List  # Importa la clase List para usarla en el sistema de mensajería
from listas.double_list import DoubleList  # Importa la clase DoubleList para usarla en el sistema de mensajería
from dequeues.stack import Stack  # Importa la clase Stack para usarla en el sistema de mensajería
from dequeues.queue import Queue  # Importa la clase Queue para usarla en el sistema de mensajería
from .empleados import Empleado
from .admin import Administrador
from .fecha import Fecha
from .direccion import Direccion
from .registro import Registro

class Sistema:
    def __init__(self):
        self.empleados = DoubleList()  # Lista de empleados
        self.noEmpleados = 0
        self.message_queue = Queue()  # Cola de mensajes leídos
        self.draft_stack = Stack()  # Pila de borradores

    def agregarEmpleado(self, empleado):
        if self.buscarUsuario(empleado.id):
            print(f"Ya existe un usuario con el ID {empleado.id}.")
            return False
        self.empleados.addOrder(empleado)
        self.noEmpleados +=1
        self.createtxt(empleado.id)
        return True

    def eliminarEmpleado(self, id, empleado):
        if empleado.cargo == "administrador":
            if self.empleados.search(id):
                return self.empleados.remove(id)
                self.noEmpleados -= 1
        return None
      
    def buscarUsuario(self, id):
        current = self.empleados.head
        while current:
            if current.data.id == id:
                return current
            current = current.next
        return None

    def cargarEmpleados(self, archivo_empleados):
        with open(archivo_empleados, "r", newline='', encoding='utf-8') as file:
            reader = csv.DictReader(file)
            self.noEmpleados = 0
            for row in reader:
                id = int(row['ID'])
                nombre = row['Nombre']
                fecha_nac_str = row['Fecha de nacimiento']
                fecha_nac_data = fecha_nac_str.split('/')
                dia, mes, año = map(int, fecha_nac_data)
                fecha_nac = Fecha(dia, mes, año)
                ciudad_nac = row['Ciudad de nacimiento']

                direccion_data = row['Direccion'].split('-')
                calle = direccion_data[0]
                noCalle = direccion_data[1]
                nomenclatura = direccion_data[2]
                barrio = direccion_data[3]
                ciudad = direccion_data[-1]

                dir = Direccion(calle, noCalle, nomenclatura, barrio, ciudad)
                tel = int(row['Telefono'])
                email = row['Correo electronico']

                empleado = Empleado(id, nombre, fecha_nac, ciudad_nac, dir, tel, email, None, None)
                self.agregarEmpleado(empleado)


    def cargarPassword(self, archivo_password):
        
        with open(archivo_password, 'r') as file:
            for line in file:
                data = [x.strip() for x in line.split(" ")]
                id = data[0]
                password = data[1]
                cargo = data[2]

                #print(id, password, cargo)

                current_node = self.buscarUsuario(int(id))
                #print(current_node)
                if current_node.data.id == int(id):
                    current_node.data.setPassword(password)
                    current_node.data.setCargo(cargo)

    def toFileEmpleados(self, filename):
        with open(filename, "w", newline='') as file:
            writer = csv.writer(file)

            # Escribir los encabezados
            writer.writerow(["ID", "Nombre", "Fecha de nacimiento", "Ciudad de nacimiento", "Direccion", "Telefono", "Correo electronico"])

            # Escribir los datos de los usuarios
            for i in range(self.noEmpleados):
                usuario = self.empleados[i]

                # Formatear la dirección con espacios en lugar de comas
                direccion_str = f"{usuario.dir.calle}-{usuario.dir.noCalle}-{usuario.dir.nomenclatura}-{usuario.dir.barrio}-{usuario.dir.ciudad}"

                writer.writerow([usuario.id, usuario.nombre, usuario.fecha_nac.obtener_fecha(),
                                usuario.ciudad_nac, direccion_str, usuario.tel, usuario.email])
                
    def toFilePassword(self, filename):
        with open(filename, "w") as file:
            for empleado in self.empleados:
                line = f"{empleado.getId()} {empleado.password} {empleado.cargo}\n"
                file.write(line)

    def verificarAcceso(self, id, password):
        current = self.buscarUsuario(id)
        print(current)
        if current.data.password == password:
            return current.data.cargo
        return None
    
    def createtxt(self, id):
        carpeta_destino = "./txt"
        nombre_archivo = f"{id}.txt"
        ruta_completa = os.path.join(carpeta_destino, nombre_archivo)
        
        # Verificar si el archivo ya existe
        if os.path.exists(ruta_completa):
            return None
        else:
            # Intenta crear el archivo en la carpeta de destino
            try:
                with open(ruta_completa, "w") as archivo:
                    archivo.write(id)
                print(f"Archivo '{nombre_archivo}' creado en '{carpeta_destino}'")
            except Exception as e:
                print(f"Error al crear el archivo: {str(e)}")

    def cambiar_contrasena(self, empleado, nueva_contrasena):
        if empleado.cargo == "administrador":
            # Cambia la contraseña del empleado
            empleado.setPassword(nueva_contrasena)
            # Actualiza el archivo Password.txt