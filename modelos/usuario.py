class Usuario:
    def __init__(self, usuario, contrasena, nombre, rol="Cliente"):
        self.usuario = usuario
        self.contrasena = contrasena
        self.nombre = nombre
        self.rol = rol

    @staticmethod
    def desde_diccionario(data):
        return Usuario(
            data["usuario"],
            data["contrasena"],
            data["nombre"],
            data.get("rol", "Cliente")  # Compatibilidad si no existe el campo rol
        )

    def convertir_a_diccionario(self):
        return {
            "usuario": self.usuario,
            "contrasena": self.contrasena,
            "nombre": self.nombre,
            "rol": self.rol
        }

    def __str__(self):
        return f"{self.nombre} ({self.usuario}) - {self.rol}"