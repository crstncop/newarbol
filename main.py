from Base import BinaryTreeNode

TOTAL_OPERACIONES_FUSION = 0


class medicamento:
    def __init__(self, id, nombre, stock, año, precio):
        self.id = id
        self.nombre = nombre
        self.stock = stock
        self.año = año
        self.precio = precio
        

    def __str__(self):
        return (f"ID: {self.id} | Nombre: {self.nombre} | "f"Stock: {self.stock} | Vence: {self.año} | "f"Precio: {self.precio:.2f}")


class arbol:
    def __init__(self):
        self.raiz = None
        self.alertas_stock = 0
        self.valor_total_inventario = 0.0
        self.venta_exitosa_total = 0.0
        self.eliminados_izquierda = 0
    def buscar(self, id):
        actual = self.raiz
        

        while actual is not None:
            if id == actual.data.id:
                return actual.data
            elif id < actual.data.id:
                actual = actual.leftchild
            else:
                actual = actual.rightchild

        return None

    def insertar(self, nodo, nuevo):
        if nodo is None:
            return BinaryTreeNode(nuevo)

        if nuevo.id < nodo.data.id:
            nodo.leftchild = self.insertar(nodo.leftchild, nuevo)
        elif nuevo.id > nodo.data.id:
            nodo.rightchild = self.insertar(nodo.rightchild, nuevo)

        return nodo

    def registrar(self, nuevo):
        if self.buscar(nuevo.id) is not None:
            print("El medicamento ya existe")
            return

        if nuevo.stock < 0 or nuevo.precio < 0:
            print("El stock y el precio no pueden ser negativos")
            return

        if nuevo.id % 2 == 0:
            nuevo.precio *= 0.90

        self.raiz = self.insertar(self.raiz, nuevo)

        if nuevo.stock < 5:
            self.alertas_stock += 1

        self.valor_total_inventario += nuevo.precio * nuevo.stock

        print("Medicamento registrado correctamente")

#CAMBIO 1 VENDER SIN IMPORTAR SI LA CANTIDAD ES MAYOR AL STOCK
    def busqueda_venta(self, id, cantidad):
        if cantidad <= 0:
            return "La cantidad debe ser mayor que cero"

        producto = self.buscar(id)

        if producto is None:
            return "Medicamento no encontrado"

        if producto.stock <= 0:
            sustituto = self.sugerir_sustituto(id)

            if sustituto is None:
                return "Medicamento agotado. No hay sustitutos disponibles."

            return f"Medicamento agotado. Sustituto sugerido:\n{sustituto}"

        stock_anterior = producto.stock
        vendidas = min(cantidad, producto.stock)

        producto.stock -= vendidas

        dinero = vendidas * producto.precio
        self.venta_exitosa_total += dinero
        self.valor_total_inventario -= dinero

        if stock_anterior >= 5 and producto.stock < 5:
            self.alertas_stock += 1

        return (f"Unidades vendidas: {vendidas}\n"f"Dinero recaudado: ${dinero:.2f}\n"f"Ingresos acumulados: ${self.venta_exitosa_total:.2f}")

    def nodo_mas_profundo(self, nodo):
        actual = nodo

        while actual.leftchild is not None:
            actual = actual.leftchild

        return actual

    def eliminar(self, id, nodo, actualizar=True):
        if nodo is None:
            return None

        if id < nodo.data.id:
            nodo.leftchild = self.eliminar(id, nodo.leftchild, actualizar)

        elif id > nodo.data.id:
            nodo.rightchild = self.eliminar(id, nodo.rightchild, actualizar)

        else:
            if actualizar:
                if nodo.data.stock < 5:
                    self.alertas_stock -= 1

                self.valor_total_inventario -= (nodo.data.precio * nodo.data.stock)

            if nodo.leftchild is None and nodo.rightchild is None:
                return None
            
            if nodo.leftchild is None:
                return nodo.rightchild

            elif nodo.rightchild is None:
                return nodo.leftchild

            else:
                sucesor = self.nodo_mas_profundo(nodo.rightchild)
                nodo.data = sucesor.data
                nodo.rightchild = self.eliminar(sucesor.data.id, nodo.rightchild, False)

        return nodo

    def eliminar_id(self, id):
        if self.buscar(id) is None:
            print("Medicamento no encontrado")
            return

        self.raiz = self.eliminar(id, self.raiz)
        print("Medicamento eliminado correctamente")

    def mostrar_estado(self):
        print("Alertas de stock:", self.alertas_stock)
        print(f"Valor total del inventario: "f"${self.valor_total_inventario:.2f}")

#CAMBIO 3 CADUCADOS
    def limpiar_caducados(self, año, nodo, izquierda=False):
        if nodo is None:
            return

        self.limpiar_caducados(año, nodo.leftchild, izquierda)
        self.limpiar_caducados(año, nodo.rightchild, izquierda)

        if nodo.data.año <= año:
            if izquierda:
                self.eliminados_izquierda += 1

            self.raiz = self.eliminar(nodo.data.id, self.raiz)

    def reporte_caducidad(self, año):
        self.eliminados_izquierda = 0

        if self.raiz is not None:
            raiz_original = self.raiz

            self.limpiar_caducados(año, raiz_original.leftchild, True)
            self.limpiar_caducados(año, raiz_original.rightchild, False)

            if raiz_original.data.año <= año:
                self.raiz = self.eliminar(raiz_original.data.id, self.raiz)

        print("Limpieza de caducados completada")

    def visualizar_inverso(self, nodo):
        if nodo is not None:
            self.visualizar_inverso(nodo.rightchild)
            print(nodo.data)
            self.visualizar_inverso(nodo.leftchild)

    def consultar_rango(self, minimo, maximo, nodo):
        if nodo is None or minimo > maximo:
            return

        if nodo.data.id > minimo:
            self.consultar_rango(minimo, maximo, nodo.leftchild)

        if minimo <= nodo.data.id <= maximo:
            print(nodo.data)

        if nodo.data.id < maximo:
            self.consultar_rango(minimo, maximo, nodo.rightchild)

    def sucesor_inorder(self, id):
        actual = self.raiz
        sucesor = None

        while actual is not None:
            if actual.data.id > id:
                sucesor = actual.data
                actual = actual.leftchild
            else:
                actual = actual.rightchild

        return sucesor

    def predecesor_inorder(self, id):
        actual = self.raiz
        predecesor = None

        while actual is not None:
            if actual.data.id < id:
                predecesor = actual.data
                actual = actual.rightchild
            else:
                actual = actual.leftchild

        return predecesor

    def sugerir_sustituto(self, id):
        sustituto = self.sucesor_inorder(id)

        if sustituto is None:
            sustituto = self.predecesor_inorder(id)

        return sustituto

    def fusionar(self, id_origen, id_destino):
        global TOTAL_OPERACIONES_FUSION

        if id_origen == id_destino:
            print("Los IDs deben ser diferentes")
            return

        origen = self.buscar(id_origen)
        destino = self.buscar(id_destino)

        if origen is None or destino is None:
            print("Uno de los medicamentos no existe")
            return

        stock_origen = origen.stock
        stock_destino = destino.stock

        destino.stock += stock_origen
        self.valor_total_inventario += destino.precio * stock_origen

        if stock_destino < 5 and destino.stock >= 5:
            self.alertas_stock -= 1

        self.raiz = self.eliminar(id_origen, self.raiz)

        TOTAL_OPERACIONES_FUSION += 1

        print("Fusión realizada correctamente")
        print("Total de fusiones:", TOTAL_OPERACIONES_FUSION)
        
        
#CAMBIO 2 RETORNAR CUANTOS NODOS HAY DE PRECIO MENOR O IGUAL 
# AL PRESUPUESTO INGRESADO Y EL DE PRECIO MAX
    def analizar_presupuesto(self, presupuesto, nodo):
        if nodo is None:
            return 0, 0

        cantidad_izq, precio_izq = self.analizar_presupuesto(presupuesto, nodo.leftchild)

        cantidad_der, precio_der = self.analizar_presupuesto(presupuesto, nodo.rightchild)

        cantidad = cantidad_izq + cantidad_der
        precio_maximo = max(precio_izq, precio_der)

        if nodo.data.precio <= presupuesto:
            cantidad += 1
            precio_maximo = max(precio_maximo, nodo.data.precio)

        return cantidad, precio_maximo
    
    def consultar_presupuesto(self, presupuesto):
        cantidad, precio = self.analizar_presupuesto(presupuesto, self.raiz)

        print("Medicamentos que puedes comprar:", cantidad)

        if cantidad == 0:
            print("No hay medicamentos dentro del presupuesto")
        else:
            print(f"Precio más alto: ${precio:.2f}")
    
    
    
    def menu(self):
        while True:
            print("\n--- INVENTARIO DE FARMACIA ---")
            print("1. Registrar medicamento")
            print("2. Vender medicamento")
            print("3. Eliminar por ID")
            print("4. Limpiar medicamentos caducados")
            print("5. Consultar estado global")
            print("6. Mostrar inventario inverso")
            print("7. Consultar rango de IDs")
            print("8. Fusionar medicamentos")
            print("9. Analizar presupuesto")
            print("10. Consultar auditoría")
            print("11. Salir")

            opcion = input("Seleccione una opción: ")

            if opcion == "1":
                id = int(input("ID: "))
                nombre = input("Nombre: ")
                stock = int(input("Stock: "))
                año = int(input("Año de vencimiento: "))
                precio = float(input("Precio: "))

                nuevo = medicamento(id, nombre, stock, año, precio)
                self.registrar(nuevo)

            elif opcion == "2":
                id = int(input("ID del medicamento: "))
                cantidad = int(input("Cantidad a vender: "))
                print(self.busqueda_venta(id, cantidad))

            elif opcion == "3":
                id = int(input("ID a eliminar: "))
                self.eliminar_id(id)

            elif opcion == "4":
                año = int(input("Ingrese el año actual: "))
                self.reporte_caducidad(año)

            elif opcion == "5":
                self.mostrar_estado()

            elif opcion == "6":
                if self.raiz is None:
                    print("El inventario está vacío")
                else:
                    self.visualizar_inverso(self.raiz)

            elif opcion == "7":
                minimo = int(input("ID mínimo: "))
                maximo = int(input("ID máximo: "))

                if minimo > maximo:
                    print("El ID mínimo no puede superar al máximo")
                else:
                    self.consultar_rango(minimo, maximo, self.raiz)

            elif opcion == "8":
                origen = int(input("ID de origen: "))
                destino = int(input("ID de destino: "))
                self.fusionar(origen, destino)

            elif opcion == "9":
                presupuesto = float(input("Presupuesto máximo: "))
                self.consultar_presupuesto(presupuesto)

            elif opcion == "10":
                print(
                    "Medicamentos eliminados del subárbol izquierdo:",
                    self.eliminados_izquierda
                )

            elif opcion == "11":
                print("Saliendo del sistema")
                break

            else:
                print("Opción inválida")
if __name__ == "__main__":
    sistema = arbol()
    sistema.menu()