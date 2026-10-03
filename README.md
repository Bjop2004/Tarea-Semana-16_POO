# Restaurante App — Semana 16: Manejo de Eventos Avanzado

Aplicación gráfica de escritorio para la gestión integral de un restaurante desarrollada en Python con Tkinter. En esta **Semana 16**, el proyecto concluye con la evolución completa del módulo de **Gestión de Usuarios**, aplicando roles de acceso, atajos de teclado y eventos avanzados con `bind()`.

---

## 📌 Propósito de la Semana 16

Demostrar el control avanzado de eventos e interacciones de la interfaz de usuario en Tkinter mediante `bind()`, eventos virtuales de componentes y atajos de teclado.

### **Eventos Implementados:**
1. **`<<TreeviewSelect>>`**: Al seleccionar una fila en la tabla de usuarios, sus datos son consultados mediante `RestauranteServicio` y cargados automáticamente en el formulario.
2. **`<Return>`**: Atajo de teclado (tecla *Enter*) para ejecutar la acción de registro desde los campos del formulario.
3. **`<Escape>`**: Atajo de teclado (tecla *Esc*) para limpiar los campos del formulario y remover selecciones de la tabla.
4. **`<<ComboboxSelected>>`**: Evento asignado al selector de rol (`Administrador`, `Empleado`, `Cliente`).
5. **`command=`**: Mantenido en los botones de acción principal (Registrar, Actualizar, Eliminar, Limpiar).

---

## 🔒 Gestión de Roles y Permisos

* **Administrador**: Acceso completo al sistema, incluyendo la pestaña de administración de usuarios (registro, modificación, eliminación).
* **Empleado / Cliente**: Acceso a la gestión operativa (Productos y Ventas), restringiendo la vista de administración de usuarios.
* **Seguridad Activa**: La cuenta administrativa con sesión activa no puede eliminarse a sí misma.

---

## 📁 Estructura del Proyecto

```text
restaurante_app/
├── assets/
│   ├── logo.png                # Logotipo del restaurante
│   └── icon_sale.png           # Ícono para ventas
├── datos/
│   ├── productos.json          # Persistencia de productos
│   ├── usuarios.json           # Persistencia de usuarios (con rol)
│   └── ventas.json             # Persistencia de ventas
├── modelos/
│   ├── __init__.py
│   ├── producto.py             # Modelo Producto
│   ├── usuario.py              # Modelo Usuario (con rol)
│   └── venta.py                # Modelo Venta
├── servicios/
│   ├── __init__.py
│   ├── archivo_servicio.py     # Servicio genérico de persistencia JSON
│   └── restaurante_servicio.py # Lógica de negocio y reglas de permisos
├── ui/
│   ├── __init__.py
│   ├── login_view.py           # Vista de autenticación
│   └── main_view.py            # Vista principal (Events, Bindings, Tabs)
├── main.py                     # Punto de entrada de la aplicación
└── README.md                   # Documentación técnica