"""
SISTEMA DE TIENDA ONLINE - EJEMPLO COMPLEMENTARIO
================================================

FINALIDAD DEL EJEMPLO:
Este segundo ejemplo complementa el sistema de biblioteca mostrando conceptos adicionales 
de POO aplicados a una tienda online del mundo real:

1. COMPOSICIÓN Y AGREGACIÓN: Carrito compuesto por productos, Pedidos con múltiples items
2. SOBRECARGA DE OPERADORES: Operaciones matemáticas entre objetos
3. MÉTODOS ESTÁTICOS Y DE CLASE: Funcionalidades a nivel de clase
4. PROPIEDADES CALCULADAS: Atributos que se calculan dinámicamente
5. INTERFACES (PROTOCOLOS): Definición de contratos comunes

CONCEPTOS DEL MUNDO REAL MODELADOS:
- Catálogo de productos con categorías y precios
- Sistema de carrito de compras con cálculos automáticos
- Gestión de inventario con stock y reposición
- Procesamiento de pedidos con estados y seguimiento
- Sistema de descuentos y promociones
- Métodos de pago y facturación
"""

from abc import ABC, abstractmethod
from datetime import datetime, timedelta
from enum import Enum
from typing import List, Dict, Optional
import uuid

# ENUMERACIONES PARA ESTADOS
class EstadoPedido(Enum):
    PENDIENTE = "Pendiente"
    CONFIRMADO = "Confirmado"
    ENVIADO = "Enviado"
    ENTREGADO = "Entregado"
    CANCELADO = "Cancelado"

class CategoriaProducto(Enum):
    ELECTRONICA = "Electrónica"
    ROPA = "Ropa"
    HOGAR = "Hogar"
    LIBROS = "Libros"
    DEPORTES = "Deportes"

# INTERFACE/PROTOCOLO PARA DESCUENTOS
class Descuentable(ABC):
    """
    Interfaz que define el comportamiento para aplicar descuentos.
    Demuestra el concepto de ABSTRACCIÓN mediante interfaces.
    """
    
    @abstractmethod
    def aplicar_descuento(self, porcentaje: float) -> float:
        """Aplica un descuento y retorna el nuevo precio"""
        pass
    
    @abstractmethod
    def obtener_precio_original(self) -> float:
        """Obtiene el precio original sin descuentos"""
        pass

# CLASE BASE PARA PRODUCTOS
class Producto(Descuentable):
    """
    Clase base para todos los productos de la tienda.
    Demuestra ENCAPSULACIÓN y implementa la interfaz Descuentable.
    """
    
    # ATRIBUTO DE CLASE - CONTADOR DE PRODUCTOS
    _contador_productos = 0
    
    def __init__(self, nombre: str, precio: float, categoria: CategoriaProducto, 
                 stock: int, descripcion: str = ""):
        # ENCAPSULACIÓN - Atributos privados
        self._id = self._generar_id()
        self._nombre = nombre
        self._precio_original = precio
        self._precio_actual = precio
        self._categoria = categoria
        self._stock = stock
        self._descripcion = descripcion
        self._ventas_totales = 0
        
        # Incrementar contador de clase
        Producto._contador_productos += 1
    
    @classmethod
    def _generar_id(cls) -> str:
        """MÉTODO DE CLASE para generar IDs únicos"""
        return f"PROD-{cls._contador_productos + 1:04d}"
    
    @staticmethod
    def validar_precio(precio: float) -> bool:
        """MÉTODO ESTÁTICO para validar precios"""
        return precio > 0
    
    # PROPIEDADES - ENCAPSULACIÓN
    @property
    def id(self) -> str:
        return self._id
    
    @property
    def nombre(self) -> str:
        return self._nombre
    
    @property
    def precio(self) -> float:
        return self._precio_actual
    
    @property
    def categoria(self) -> CategoriaProducto:
        return self._categoria
    
    @property
    def stock(self) -> int:
        return self._stock
    
    @property
    def disponible(self) -> bool:
        """PROPIEDAD CALCULADA"""
        return self._stock > 0
    
    @property
    def ventas_totales(self) -> int:
        return self._ventas_totales
    
    # IMPLEMENTACIÓN DE INTERFAZ DESCUENTABLE
    def aplicar_descuento(self, porcentaje: float) -> float:
        """Aplica descuento al producto"""
        if 0 <= porcentaje <= 100:
            descuento = self._precio_original * (porcentaje / 100)
            self._precio_actual = self._precio_original - descuento
            return self._precio_actual
        return self._precio_actual
    
    def obtener_precio_original(self) -> float:
        return self._precio_original
    
    def restaurar_precio_original(self):
        """Restaura el precio original eliminando descuentos"""
        self._precio_actual = self._precio_original
    
    # GESTIÓN DE INVENTARIO
    def reducir_stock(self, cantidad: int) -> bool:
        """Reduce el stock del producto"""
        if self._stock >= cantidad:
            self._stock -= cantidad
            self._ventas_totales += cantidad
            return True
        return False
    
    def reponer_stock(self, cantidad: int):
        """Repone stock del producto"""
        self._stock += cantidad
    
    # SOBRECARGA DE OPERADORES
    def __eq__(self, other) -> bool:
        """Sobrecarga del operador == para comparar productos"""
        if isinstance(other, Producto):
            return self._id == other._id
        return False
    
    def __lt__(self, other) -> bool:
        """Sobrecarga del operador < para comparar por precio"""
        if isinstance(other, Producto):
            return self._precio_actual < other._precio_actual
        return NotImplemented
    
    def __str__(self) -> str:
        return f"{self._nombre} (${self._precio_actual:.2f}) - Stock: {self._stock}"
    
    def __repr__(self) -> str:
        return f"Producto(id='{self._id}', nombre='{self._nombre}', precio={self._precio_actual})"

# HERENCIA - PRODUCTOS ESPECIALIZADOS
class ProductoElectronico(Producto):
    """
    Producto electrónico con características específicas.
    Demuestra HERENCIA y especialización.
    """
    
    def __init__(self, nombre: str, precio: float, stock: int, marca: str, 
                 garantia_meses: int, descripcion: str = ""):
        super().__init__(nombre, precio, CategoriaProducto.ELECTRONICA, stock, descripcion)
        self._marca = marca
        self._garantia_meses = garantia_meses
    
    @property
    def marca(self) -> str:
        return self._marca
    
    @property
    def garantia_meses(self) -> int:
        return self._garantia_meses
    
    def extender_garantia(self, meses_adicionales: int):
        """Método específico de productos electrónicos"""
        self._garantia_meses += meses_adicionales
    
    def __str__(self) -> str:
        return f"{super().__str__()} - {self._marca} (Garantía: {self._garantia_meses} meses)"

class ProductoRopa(Producto):
    """
    Producto de ropa con tallas y colores.
    Demuestra HERENCIA y especialización.
    """
    
    def __init__(self, nombre: str, precio: float, stock: int, talla: str, 
                 color: str, material: str, descripcion: str = ""):
        super().__init__(nombre, precio, CategoriaProducto.ROPA, stock, descripcion)
        self._talla = talla
        self._color = color
        self._material = material

    @property
    def talla(self) -> str:
        return self._talla

    @property
    def color(self) -> str:
        return self._color

    @property
    def material(self) -> str:
        return self._material

    def __str__(self) -> str:
        return f"{super().__str__()} - {self._talla} - {self._color} - {self._material}"

if __name__ == "__main__":
    print("Bienvenido al sistema de tienda online")
    # Crear productos de ejemplo
    prod1 = ProductoElectronico("Smartphone", 1200.0, 10, "Samsung", 24)
    prod2 = ProductoRopa("Camiseta", 25.0, 50, "M", "Azul", "Algodón")
    print(prod1)
    print(prod2)
    # Aplicar descuento y mostrar resultado
    prod1.aplicar_descuento(10)
    print(f"Precio con descuento: {prod1.precio}")