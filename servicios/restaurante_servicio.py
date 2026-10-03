import os
from modelos.producto import Producto
from modelos.usuario import Usuario
from modelos.venta import Venta
from servicios.archivo_servicio import ArchivoServicio

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

RUTA_PRODUCTOS = os.path.join(BASE_DIR, "datos", "productos.json")
RUTA_USUARIOS = os.path.join(BASE_DIR, "datos", "usuarios.json")
RUTA_VENTAS = os.path.join(BASE_DIR, "datos", "ventas.json")

class RestauranteServicio:
    def __init__(self):
        datos_productos = ArchivoServicio.cargar(RUTA_PRODUCTOS) if os.path.exists(RUTA_PRODUCTOS) else []
        datos_usuarios = ArchivoServicio.cargar(RUTA_USUARIOS) if os.path.exists(RUTA_USUARIOS) else []
        datos_ventas = ArchivoServicio.cargar(RUTA_VENTAS) if os.path.exists(RUTA_VENTAS) else []

        self.productos = [Producto.desde_diccionario(p) for p in datos_productos]
        self.usuarios = [Usuario.desde_diccionario(u) for u in datos_usuarios]
        self.ventas = [Venta.desde_diccionario(v) for v in datos_ventas]
        self.usuario_actual = None  # Almacena el usuario logueado en la sesión

    # ==========================
    # LOGIN / AUTENTICACIÓN
    # ==========================
    def validar_login(self, usuario, contrasena):
        for u in self.usuarios:
            if u.usuario.strip() == usuario.strip() and u.contrasena.strip() == contrasena.strip():
                self.usuario_actual = u
                return True
        return False

    def obtener_usuario_actual(self):
        return self.usuario_actual

    # ==========================
    # GESTIÓN DE PRODUCTOS
    # ==========================
    def obtener_productos(self):
        return self.productos

    def guardar_productos(self):
        ArchivoServicio.guardar(RUTA_PRODUCTOS, [p.convertir_a_diccionario() for p in self.productos])

    def registrar_producto(self, producto):
        self.productos.append(producto)
        self.guardar_productos()

    def buscar_producto(self, codigo):
        for producto in self.productos:
            if producto.codigo == codigo:
                return producto
        return None

    def actualizar_producto(self, codigo, nombre, categoria, precio):
        producto = self.buscar_producto(codigo)
        if producto:
            producto.nombre = nombre
            producto.categoria = categoria
            producto.precio = precio
            self.guardar_productos()
            return True
        return False

    def eliminar_producto(self, codigo):
        producto = self.buscar_producto(codigo)
        if producto:
            self.productos.remove(producto)
            self.guardar_productos()
            return True
        return False

    # ==========================
    # GESTIÓN DE USUARIOS (CRUD SEMANA 16)
    # ==========================
    def obtener_usuarios(self):
        return self.usuarios

    def guardar_usuarios(self):
        ArchivoServicio.guardar(RUTA_USUARIOS, [u.convertir_a_diccionario() for u in self.usuarios])

    def buscar_usuario(self, usuario_id):
        for u in self.usuarios:
            if u.usuario == usuario_id:
                return u
        return None

    def registrar_usuario(self, usuario_obj) -> tuple[bool, str]:
        if not usuario_obj.usuario or not usuario_obj.contrasena or not usuario_obj.nombre:
            return False, "Todos los campos son obligatorios."
        if self.buscar_usuario(usuario_obj.usuario):
            return False, "El nombre de usuario ya se encuentra registrado."

        self.usuarios.append(usuario_obj)
        self.guardar_usuarios()
        return True, "Usuario registrado correctamente."

    def actualizar_usuario(self, usuario_id, nombre, contrasena, rol) -> tuple[bool, str]:
        u = self.buscar_usuario(usuario_id)
        if not u:
            return False, "El usuario a actualizar no existe."

        u.nombre = nombre
        if contrasena.strip():  # Actualizar solo si se ingresa una nueva contraseña
            u.contrasena = contrasena
        u.rol = rol

        self.guardar_usuarios()
        return True, "Usuario actualizado con éxito."

    def eliminar_usuario(self, usuario_id) -> tuple[bool, str]:
        if self.usuario_actual and self.usuario_actual.usuario == usuario_id:
            return False, "No puedes eliminar tu propia cuenta en sesión activa."

        u = self.buscar_usuario(usuario_id)
        if not u:
            return False, "El usuario seleccionado no existe."

        self.usuarios.remove(u)
        self.guardar_usuarios()
        return True, "Usuario eliminado correctamente."

    # ==========================
    # GESTIÓN DE VENTAS
    # ==========================
    def obtener_ventas(self):
        return self.ventas

    def guardar_ventas(self):
        ArchivoServicio.guardar(RUTA_VENTAS, [v.convertir_a_diccionario() for v in self.ventas])

    def registrar_venta(self, usuario_id: str, codigo_producto: str) -> tuple[bool, str]:
        if not usuario_id or not codigo_producto:
            return False, "Debe seleccionar un usuario y un producto válidos."

        usuario_existe = any(u.usuario == usuario_id for u in self.usuarios)
        producto_existe = any(p.codigo == codigo_producto for p in self.productos)

        if not usuario_existe:
            return False, "El usuario seleccionado no existe."
        if not producto_existe:
            return False, "El producto seleccionado no existe."

        nuevo_id = f"V-{len(self.ventas) + 1:04d}"
        nueva_venta = Venta(id_venta=nuevo_id, usuario=usuario_id, producto_codigo=codigo_producto)
        
        self.ventas.append(nueva_venta)
        self.guardar_ventas()
        return True, f"Venta {nuevo_id} registrada con éxito."