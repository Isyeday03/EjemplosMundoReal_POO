from abc import ABC, abstractmethod
from datetime import datetime, timedelta
from typing import List, Dict, Optional

# ==============================================================================
# CLASE BASE ABSTRACTA - DEMOSTRACIÓN DE ABSTRACCIÓN
# ==============================================================================

class Libro(ABC):
    """
    Clase abstracta que define la estructura básica de un libro.
    
    Esta clase demuestra el concepto de ABSTRACCIÓN en POO al definir
    una interfaz común para todos los tipos de libros, sin implementar
    detalles específicos que varían según el tipo.
    
    Atributos:
        _titulo: Título del libro (privado)
        _autor: Autor del libro (privado)
        _isbn: Código ISBN único (privado)
        _año_publicacion: Año de publicación (privado)
        _disponible: Estado de disponibilidad (privado)
        _fecha_prestamo: Fecha del préstamo actual (privado)
        _usuario_actual: Usuario que tiene el libro prestado (privado)
    """
    
    def __init__(self, titulo: str, autor: str, isbn: str, año_publicacion: int):
        """
        Constructor de la clase base Libro.
        
        Demuestra ENCAPSULACIÓN usando atributos privados (prefijo _)
        para proteger los datos internos del objeto.
        """
        # ENCAPSULACIÓN: Atributos privados para proteger los datos
        self._titulo = titulo
        self._autor = autor
        self._isbn = isbn
        self._año_publicacion = año_publicacion
        self._disponible = True
        self._fecha_prestamo = None
        self._usuario_actual = None
        
        print(f"📚 Libro creado: {titulo} por {autor}")
    
    # PROPIEDADES - IMPLEMENTACIÓN DE ENCAPSULACIÓN
    @property
    def titulo(self) -> str:
        """Getter para el título del libro"""
        return self._titulo
    
    @property
    def autor(self) -> str:
        """Getter para el autor del libro"""
        return self._autor
    
    @property
    def isbn(self) -> str:
        """Getter para el ISBN del libro"""
        return self._isbn
    
    @property
    def año_publicacion(self) -> int:
        """Getter para el año de publicación"""
        return self._año_publicacion
    
    @property
    def disponible(self) -> bool:
        """Getter para el estado de disponibilidad"""
        return self._disponible
    
    @property
    def usuario_actual(self):
        """Getter para el usuario actual que tiene el libro"""
        return self._usuario_actual
    
    @property
    def fecha_prestamo(self) -> Optional[datetime]:
        """Getter para la fecha de préstamo"""
        return self._fecha_prestamo
    
    # MÉTODOS ABSTRACTOS - POLIMORFISMO
    @abstractmethod
    def calcular_dias_prestamo(self) -> int:
        """
        Método abstracto que debe ser implementado por las clases hijas.
        
        Returns:
            int: Número de días permitidos para el préstamo
        """
        pass
    
    @abstractmethod
    def obtener_tipo(self) -> str:
        """
        Método abstracto que retorna el tipo específico de libro.
        
        Returns:
            str: Tipo de libro (Físico o Digital)
        """
        pass
    
    @abstractmethod
    def obtener_informacion_especifica(self) -> str:
        """
        Método abstracto para obtener información específica del tipo de libro.
        
        Returns:
            str: Información específica del libro
        """
        pass
    
    # MÉTODOS CONCRETOS COMUNES
    def prestar(self, usuario) -> bool:
        """
        Presta el libro a un usuario específico.
        
        Args:
            usuario: Usuario al que se le presta el libro
            
        Returns:
            bool: True si el préstamo fue exitoso, False en caso contrario
        """
        if self._disponible:
            self._disponible = False
            self._fecha_prestamo = datetime.now()
            self._usuario_actual = usuario
            print(f"✅ Préstamo realizado: {self._titulo} para {usuario.nombre}")
            return True
        else:
            print(f"❌ El libro {self._titulo} no está disponible")
            return False
    
    def devolver(self) -> tuple:
        """
        Devuelve el libro y calcula días de retraso si los hay.
        
        Returns:
            tuple: (días_retraso, usuario_que_devolvio)
        """
        if not self._disponible:
            dias_prestado = (datetime.now() - self._fecha_prestamo).days
            dias_limite = self.calcular_dias_prestamo()
            dias_retraso = max(0, dias_prestado - dias_limite)
            
            # Guardar referencia del usuario antes de limpiar
            usuario_devolvio = self._usuario_actual
            
            # Restaurar estado del libro
            self._disponible = True
            self._fecha_prestamo = None
            self._usuario_actual = None
            
            if dias_retraso > 0:
                print(f"📅 Libro devuelto con {dias_retraso} días de retraso")
            else:
                print(f"✅ Libro devuelto a tiempo: {self._titulo}")
            
            return dias_retraso, usuario_devolvio
        else:
            print(f"⚠️  El libro {self._titulo} no estaba prestado")
            return 0, None
    
    def obtener_estado(self) -> str:
        """
        Obtiene el estado actual del libro.
        
        Returns:
            str: Estado del libro (disponible o prestado)
        """
        if self._disponible:
            return "Disponible"
        else:
            dias_prestado = (datetime.now() - self._fecha_prestamo).days
            return f"Prestado hace {dias_prestado} días a {self._usuario_actual.nombre}"
    
    def __str__(self) -> str:
        """Representación en cadena del libro"""
        return f"{self.obtener_tipo()}: '{self._titulo}' por {self._autor} - {self.obtener_estado()}"
    
    def __repr__(self) -> str:
        """Representación técnica del libro"""
        return f"Libro(titulo='{self._titulo}', isbn='{self._isbn}', disponible={self._disponible})"

# ==============================================================================
# CLASES DERIVADAS - DEMOSTRACIÓN DE HERENCIA Y POLIMORFISMO
# ==============================================================================

class LibroFisico(Libro):
    """
    Clase que representa un libro físico en la biblioteca.
    
    Demuestra HERENCIA al extender la clase Libro y POLIMORFISMO
    al implementar métodos abstractos de manera específica.
    
    Atributos adicionales:
        _ubicacion: Ubicación física en la biblioteca
        _estado_fisico: Estado de conservación del libro
        _numero_paginas: Cantidad de páginas
    """
    
    def __init__(self, titulo: str, autor: str, isbn: str, año_publicacion: int,
                 ubicacion: str, estado_fisico: str = "Bueno", numero_paginas: int = 0):
        """
        Constructor de LibroFisico.
        
        Llama al constructor de la clase padre y agrega atributos específicos.
        """
        # Llamar al constructor de la clase padre
        super().__init__(titulo, autor, isbn, año_publicacion)
        
        # Atributos específicos de libros físicos
        self._ubicacion = ubicacion
        self._estado_fisico = estado_fisico
        self._numero_paginas = numero_paginas
        
        print(f"📍 Libro físico ubicado en: {ubicacion}")
    
    # PROPIEDADES ESPECÍFICAS
    @property
    def ubicacion(self) -> str:
        """Getter para la ubicación del libro"""
        return self._ubicacion
    
    @property
    def estado_fisico(self) -> str:
        """Getter para el estado físico del libro"""
        return self._estado_fisico
    
    @property
    def numero_paginas(self) -> int:
        """Getter para el número de páginas"""
        return self._numero_paginas
    
    # IMPLEMENTACIÓN DE MÉTODOS ABSTRACTOS - POLIMORFISMO
    def calcular_dias_prestamo(self) -> int:
        """
        Los libros físicos tienen un período de préstamo de 14 días.
        
        Returns:
            int: 14 días para libros físicos
        """
        return 14
    
    def obtener_tipo(self) -> str:
        """
        Identifica el tipo como libro físico.
        
        Returns:
            str: "Libro Físico"
        """
        return "Libro Físico"
    
    def obtener_informacion_especifica(self) -> str:
        """
        Información específica de libros físicos.
        
        Returns:
            str: Información de ubicación y estado físico
        """
        return f"Ubicación: {self._ubicacion}, Estado: {self._estado_fisico}, Páginas: {self._numero_paginas}"
    
    # MÉTODOS ESPECÍFICOS DE LIBROS FÍSICOS
    def cambiar_ubicacion(self, nueva_ubicacion: str) -> None:
        """
        Cambia la ubicación física del libro en la biblioteca.
        
        Args:
            nueva_ubicacion: Nueva ubicación del libro
        """
        ubicacion_anterior = self._ubicacion
        self._ubicacion = nueva_ubicacion
        print(f"📦 Libro reubicado de {ubicacion_anterior} a {nueva_ubicacion}")
    
    def actualizar_estado_fisico(self, nuevo_estado: str) -> None:
        """
        Actualiza el estado de conservación del libro.
        
        Args:
            nuevo_estado: Nuevo estado físico del libro
        """
        estado_anterior = self._estado_fisico
        self._estado_fisico = nuevo_estado
        print(f"🔄 Estado físico actualizado de '{estado_anterior}' a '{nuevo_estado}'")
    
    def necesita_mantenimiento(self) -> bool:
        """
        Determina si el libro necesita mantenimiento.
        
        Returns:
            bool: True si el estado es "Malo" o "Regular"
        """
        return self._estado_fisico.lower() in ["malo", "regular"]

class LibroDigital(Libro):
    """
    Clase que representa un libro digital en la biblioteca.
    
    Demuestra HERENCIA y POLIMORFISMO con características específicas
    de libros digitales como formato, tamaño y descargas.
    
    Atributos adicionales:
        _formato: Formato del archivo (PDF, EPUB, etc.)
        _tamaño_mb: Tamaño del archivo en megabytes
        _url_descarga: URL para descargar el libro
        _descargas: Contador de descargas realizadas
    """
    
    def __init__(self, titulo: str, autor: str, isbn: str, año_publicacion: int,
                 formato: str, tamaño_mb: float, url_descarga: str):
        """
        Constructor de LibroDigital.
        
        Llama al constructor de la clase padre y agrega atributos específicos.
        """
        # Llamar al constructor de la clase padre
        super().__init__(titulo, autor, isbn, año_publicacion)
        
        # Atributos específicos de libros digitales
        self._formato = formato.upper()
        self._tamaño_mb = tamaño_mb
        self._url_descarga = url_descarga
        self._descargas = 0
        
        print(f"💾 Libro digital en formato {formato} ({tamaño_mb} MB)")
    
    # PROPIEDADES ESPECÍFICAS
    @property
    def formato(self) -> str:
        """Getter para el formato del archivo"""
        return self._formato
    
    @property
    def tamaño_mb(self) -> float:
        """Getter para el tamaño en MB"""
        return self._tamaño_mb
    
    @property
    def url_descarga(self) -> str:
        """Getter para la URL de descarga"""
        return self._url_descarga
    
    @property
    def descargas(self) -> int:
        """Getter para el contador de descargas"""
        return self._descargas
    
    # IMPLEMENTACIÓN DE MÉTODOS ABSTRACTOS - POLIMORFISMO
    def calcular_dias_prestamo(self) -> int:
        """
        Los libros digitales tienen un período de préstamo de 7 días.
        
        Returns:
            int: 7 días para libros digitales
        """
        return 7
    
    def obtener_tipo(self) -> str:
        """
        Identifica el tipo como libro digital.
        
        Returns:
            str: "Libro Digital"
        """
        return "Libro Digital"
    
    def obtener_informacion_especifica(self) -> str:
        """
        Información específica de libros digitales.
        
        Returns:
            str: Información de formato, tamaño y descargas
        """
        return f"Formato: {self._formato}, Tamaño: {self._tamaño_mb} MB, Descargas: {self._descargas}"
    
    # MÉTODOS ESPECÍFICOS DE LIBROS DIGITALES
    def registrar_descarga(self) -> None:
        """
        Registra una descarga del libro digital.
        """
        self._descargas += 1
        print(f"⬇️  Descarga registrada. Total: {self._descargas}")
    
    def obtener_estadisticas_descarga(self) -> Dict[str, any]:
        """
        Obtiene estadísticas de descarga del libro.
        
        Returns:
            dict: Diccionario con estadísticas de descarga
        """
        return {
            'total_descargas': self._descargas,
            'formato': self._formato,
            'tamaño_mb': self._tamaño_mb,
            'popularidad': 'Alta' if self._descargas > 50 else 'Media' if self._descargas > 10 else 'Baja'
        }
    
    def es_formato_compatible(self, dispositivo: str) -> bool:
        """
        Verifica si el formato es compatible con un dispositivo.
        
        Args:
            dispositivo: Tipo de dispositivo (kindle, tablet, etc.)
            
        Returns:
            bool: True si es compatible
        """
        compatibilidad = {
            'kindle': ['MOBI', 'AZW', 'PDF'],
            'tablet': ['PDF', 'EPUB', 'MOBI'],
            'ereader': ['EPUB', 'PDF'],
            'computadora': ['PDF', 'EPUB', 'MOBI', 'TXT']
        }
        
        return self._formato in compatibilidad.get(dispositivo.lower(), [])

# ==============================================================================
# JERARQUÍA DE USUARIOS - MÁS HERENCIA Y POLIMORFISMO
# ==============================================================================

class Usuario(ABC):
    """
    Clase abstracta base para usuarios de la biblioteca.
    
    Demuestra ABSTRACCIÓN al definir la estructura común de todos los usuarios
    y ENCAPSULACIÓN al proteger los datos del usuario.
    
    Atributos:
        _nombre: Nombre completo del usuario
        _identificacion: ID único del usuario
        _email: Correo electrónico
        _fecha_registro: Fecha de registro en el sistema
        _libros_prestados: Lista de libros actualmente prestados
        _historial_prestamos: Historial completo de préstamos
        _multa_acumulada: Multa total acumulada
    """
    
    def __init__(self, nombre: str, identificacion: str, email: str):
        """
        Constructor base para usuarios.
        
        Args:
            nombre: Nombre completo del usuario
            identificacion: Identificación única
            email: Correo electrónico
        """
        # ENCAPSULACIÓN: Atributos privados
        self._nombre = nombre
        self._identificacion = identificacion
        self._email = email
        self._fecha_registro = datetime.now()
        self._libros_prestados: List[Libro] = []
        self._historial_prestamos: List[Dict] = []
        self._multa_acumulada = 0.0
        
        print(f"👤 Usuario registrado: {nombre} ({identificacion})")
    
    # PROPIEDADES - ENCAPSULACIÓN
    @property
    def nombre(self) -> str:
        """Getter para el nombre del usuario"""
        return self._nombre
    
    @property
    def identificacion(self) -> str:
        """Getter para la identificación"""
        return self._identificacion
    
    @property
    def email(self) -> str:
        """Getter para el email"""
        return self._email
    
    @property
    def fecha_registro(self) -> datetime:
        """Getter para la fecha de registro"""
        return self._fecha_registro
    
    @property
    def libros_prestados(self) -> List[Libro]:
        """Getter que retorna una copia de los libros prestados"""
        return self._libros_prestados.copy()
    
    @property
    def multa_acumulada(self) -> float:
        """Getter para la multa acumulada"""
        return self._multa_acumulada
    
    @property
    def total_prestamos_historicos(self) -> int:
        """Getter para el total de préstamos históricos"""
        return len(self._historial_prestamos)
    
    # MÉTODOS ABSTRACTOS - POLIMORFISMO
    @abstractmethod
    def limite_prestamos(self) -> int:
        """
        Límite de libros que puede tener prestados simultáneamente.
        
        Returns:
            int: Número máximo de libros prestados
        """
        pass
    
    @abstractmethod
    def calcular_multa_por_dia(self) -> float:
        """
        Multa por día de retraso en devolución.
        
        Returns:
            float: Cantidad de multa por día
        """
        pass
    
    @abstractmethod
    def obtener_tipo_usuario(self) -> str:
        """
        Tipo específico de usuario.
        
        Returns:
            str: Tipo de usuario
        """
        pass
    
    # MÉTODOS CONCRETOS
    def puede_prestar(self) -> bool:
        """
        Verifica si el usuario puede tomar más libros prestados.
        
        Returns:
            bool: True si puede prestar, False en caso contrario
        """
        dentro_limite = len(self._libros_prestados) < self.limite_prestamos()
        sin_multas = self._multa_acumulada == 0
        return dentro_limite and sin_multas
    
    def prestar_libro(self, libro: Libro) -> bool:
        """
        Realiza el préstamo de un libro al usuario.
        
        Args:
            libro: Libro a prestar
            
        Returns:
            bool: True si el préstamo fue exitoso
        """
        if self.puede_prestar() and libro.prestar(self):
            self._libros_prestados.append(libro)
            
            # Registrar en historial
            self._historial_prestamos.append({
                'libro_titulo': libro.titulo,
                'libro_isbn': libro.isbn,
                'fecha_prestamo': datetime.now(),
                'tipo_libro': libro.obtener_tipo(),
                'devuelto': False
            })
            
            print(f"📖 Préstamo exitoso: {libro.titulo} para {self._nombre}")
            return True
        else:
            motivo = "límite excedido" if len(self._libros_prestados) >= self.limite_prestamos() else "multas pendientes"
            print(f"❌ No se puede prestar libro: {motivo}")
            return False
    
    def devolver_libro(self, libro: Libro) -> float:
        """
        Devuelve un libro y calcula multa si hay retraso.
        
        Args:
            libro: Libro a devolver
            
        Returns:
            float: Multa aplicada por retraso
        """
        if libro in self._libros_prestados:
            dias_retraso, _ = libro.devolver()
            self._libros_prestados.remove(libro)
            
            # Actualizar historial
            for prestamo in reversed(self._historial_prestamos):
                if prestamo['libro_isbn'] == libro.isbn and not prestamo['devuelto']:
                    prestamo['devuelto'] = True
                    prestamo['fecha_devolucion'] = datetime.now()
                    prestamo['dias_retraso'] = dias_retraso
                    break
            
            # Calcular multa
            multa = 0.0
            if dias_retraso > 0:
                multa = dias_retraso * self.calcular_multa_por_dia()
                self._multa_acumulada += multa
                print(f"💰 Multa aplicada: ${multa:.2f} por {dias_retraso} días de retraso")
            
            return multa
        else:
            print(f"⚠️  El usuario {self._nombre} no tiene prestado el libro {libro.titulo}")
            return 0.0
    
    def pagar_multa(self, cantidad: float) -> float:
        """
        Permite al usuario pagar su multa.
        
        Args:
            cantidad: Cantidad a pagar
            
        Returns:
            float: Multa restante después del pago
        """
        if cantidad > 0:
            self._multa_acumulada = max(0, self._multa_acumulada - cantidad)
            print(f"💳 Pago de multa realizado: ${cantidad:.2f}. Multa restante: ${self._multa_acumulada:.2f}")
        return self._multa_acumulada
    
    def obtener_resumen(self) -> Dict[str, any]:
        """
        Obtiene un resumen completo del usuario.
        
        Returns:
            dict: Resumen con toda la información del usuario
        """
        return {
            'nombre': self._nombre,
            'tipo': self.obtener_tipo_usuario(),
            'identificacion': self._identificacion,
            'email': self._email,
            'fecha_registro': self._fecha_registro.strftime('%Y-%m-%d'),
            'libros_prestados_actual': len(self._libros_prestados),
            'limite_prestamos': self.limite_prestamos(),
            'total_prestamos_historicos': self.total_prestamos_historicos,
            'multa_acumulada': self._multa_acumulada,
            'puede_prestar': self.puede_prestar()
        }
    
    def __str__(self) -> str:
        """Representación en cadena del usuario"""
        return f"{self.obtener_tipo_usuario()}: {self._nombre} (ID: {self._identificacion})"
    
    def __repr__(self) -> str:
        """Representación técnica del usuario"""
        return f"Usuario(nombre='{self._nombre}', id='{self._identificacion}', tipo='{self.obtener_tipo_usuario()}')"

class Estudiante(Usuario):
    """
    Usuario tipo Estudiante con privilegios limitados.
    
    Demuestra HERENCIA al extender Usuario y POLIMORFISMO
    al implementar métodos específicos para estudiantes.
    
    Atributos adicionales:
        _carrera: Carrera que estudia
        _semestre: Semestre actual
    """
    
    def __init__(self, nombre: str, identificacion: str, email: str, carrera: str, semestre: int = 1):
        """
        Constructor de Estudiante.
        
        Args:
            nombre: Nombre del estudiante
            identificacion: ID del estudiante
            email: Email del estudiante
            carrera: Carrera que estudia
            semestre: Semestre actual
        """
        super().__init__(nombre, identificacion, email)
        self._carrera = carrera
        self._semestre = semestre
        
        print(f"🎓 Estudiante de {carrera}, semestre {semestre}")
    
    @property
    def carrera(self) -> str:
        """Getter para la carrera"""
        return self._carrera
    
    @property
    def semestre(self) -> int:
        """Getter para el semestre"""
        return self._semestre
    
    # IMPLEMENTACIÓN DE MÉTODOS ABSTRACTOS - POLIMORFISMO
    def limite_prestamos(self) -> int:
        """
        Los estudiantes pueden tener máximo 3 libros prestados.
        
        Returns:
            int: 3 libros para estudiantes
        """
        return 3
    
    def calcular_multa_por_dia(self) -> float:
        """
        Multa de $0.50 por día para estudiantes.
        
        Returns:
            float: $0.50 por día
        """
        return 0.50
    
    def obtener_tipo_usuario(self) -> str:
        """
        Identifica el tipo como estudiante.
        
        Returns:
            str: "Estudiante"
        """
        return "Estudiante"
    
    # MÉTODOS ESPECÍFICOS DE ESTUDIANTES
    def avanzar_semestre(self) -> None:
        """Avanza al siguiente semestre"""
        self._semestre += 1
        print(f"📚 {self._nombre} avanzó al semestre {self._semestre}")
    
    def cambiar_carrera(self, nueva_carrera: str) -> None:
        """
        Cambia la carrera del estudiante.
        
        Args:
            nueva_carrera: Nueva carrera
        """
        carrera_anterior = self._carrera
        self._carrera = nueva_carrera
        print(f"🔄 {self._nombre} cambió de {carrera_anterior} a {nueva_carrera}")

class Profesor(Usuario):
    """
    Usuario tipo Profesor con mayores privilegios.
    
    Demuestra HERENCIA y POLIMORFISMO con reglas específicas
    para profesores universitarios.
    
    Atributos adicionales:
        _departamento: Departamento al que pertenece
        _titulo_academico: Título académico del profesor
    """
    
    def __init__(self, nombre: str, identificacion: str, email: str, 
                 departamento: str, titulo_academico: str = "Profesor"):
        """
        Constructor de Profesor.
        
        Args:
            nombre: Nombre del profesor
            identificacion: ID del profesor
            email: Email del profesor
            departamento: Departamento académico
            titulo_academico: Título académico
        """
        super().__init__(nombre, identificacion, email)
        self._departamento = departamento
        self._titulo_academico = titulo_academico
        
        print(f"👨‍🏫 {titulo_academico} del departamento de {departamento}")
    
    @property
    def departamento(self) -> str:
        """Getter para el departamento"""
        return self._departamento
    
    @property
    def titulo_academico(self) -> str:
        """Getter para el título académico"""
        return self._titulo_academico
    
    # IMPLEMENTACIÓN DE MÉTODOS ABSTRACTOS - POLIMORFISMO
    def limite_prestamos(self) -> int:
        """
        Los profesores pueden tener máximo 10 libros prestados.
        
        Returns:
            int: 10 libros para profesores
        """
        return 10
    
    def calcular_multa_por_dia(self) -> float:
        """
        Multa de $1.00 por día para profesores (mayor responsabilidad).
        
        Returns:
            float: $1.00 por día
        """
        return 1.00
    
    def obtener_tipo_usuario(self) -> str:
        """
        Identifica el tipo como profesor.
        
        Returns:
            str: "Profesor"
        """
        return "Profesor"
    
    # MÉTODOS ESPECÍFICOS DE PROFESORES
    def solicitar_libro_especializado(self, titulo: str) -> str:
        """
        Solicita la adquisición de un libro especializado.
        
        Args:
            titulo: Título del libro solicitado
            
        Returns:
            str: Número de solicitud
        """
        solicitud_id = f"SOL-{datetime.now().strftime('%Y%m%d%H%M%S')}"
        print(f"📋 Solicitud de libro especializado: {titulo} (ID: {solicitud_id})")
        return solicitud_id
    
    def cambiar_departamento(self, nuevo_departamento: str) -> None:
        """
        Cambia el departamento del profesor.
        
        Args:
            nuevo_departamento: Nuevo departamento
        """
        departamento_anterior = self._departamento
        self._departamento = nuevo_departamento
        print(f"🏢 {self._nombre} se trasladó de {departamento_anterior} a {nuevo_departamento}")

# ==============================================================================
# CLASE PRINCIPAL DEL SISTEMA - COMPOSICIÓN
# ==============================================================================

class Biblioteca:
    """
    Clase principal que gestiona toda la biblioteca.
    
    Demuestra COMPOSICIÓN al estar compuesta por múltiples objetos
    (libros, usuarios) y coordinar todas las operaciones del sistema.
    """