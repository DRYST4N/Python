
import sys

tareas = []
class Task():
    def __init__(self, nombre, descripcion, completada = False):
        self.nombre = nombre
        self.descripcion = descripcion
        self.completada = completada
class ToDoList():
    def añadirTareas(nombre, descripcion, completada = False):
        tarea = Task(nombre, descripcion, completada)
        tareas.append(tarea)
    def recuperarTarea(nombre):
        for tarea in tareas:
            if (tarea.nombre == nombre):
                return tarea
        return None;
    def eliminarTareas(tarea):
        tareas.remove(tarea)
    def mostrarTareas(tarea):
        print(f"{tarea.nombre}: {tarea.completada}")
        print(f"Descripcion: {tarea.descripcion}")
    def editarTarea():
            nombre = input("Que tarea quiere editar:")
            tarea_encontrada = ToDoList.recuperarTarea(nombre)
            
            if  tarea_encontrada:
                print("Tarea encontrada:")
                print(f"Nombre: {tarea_encontrada.nombre}")
                print(f"Descripción: {tarea_encontrada.descripcion}")
                print("")
                
                print("¿Qué desea modificar?")
                print("1.- Nombre")
                print("2.- Descripción")
                opcion = input("Elija una opción: ")
                if opcion == "1":
                    nuevo_nombre = input("Ingrese el nuevo nombre: ")
                    tarea_encontrada.nombre = nuevo_nombre
                elif opcion == "2":
                    nueva_descripcion = input("Ingrese la nueva descripción: ")
                    tarea_encontrada.descripcion = nueva_descripcion
                
                print("Tarea modificada:")
                print(f"Nombre: {tarea_encontrada.nombre}")
                print(f"Descripción: {tarea_encontrada.descripcion}")
            else:
                print(f"No se encontró la tarea con nombre '{nombre}'.")
def main():
    print("Bienvenido a ToDoList")
    while True:
        print("Menu principal")
        print("1.- Agregar nueva tarea")
        print("2.- Ver la lista de tareas")
        print("3.- Completar una tarea")
        print("4.- Editar una tarea")
        print("5.- Eliminar una tarea")
        print("0.- Salir")
        opcion = input("Elija una opcion")
        if (opcion == "1"):
               nombre = input("Cual es el nombre de la tarea:")
               descripcion = input("Describe la tarea:")
               ToDoList.añadirTareas(nombre,descripcion)
               input("Pulse <INTRO> para continuar...")
        elif (opcion == "2"):
            for tarea in tareas:
                print(" ")
                ToDoList.mostrarTareas(tarea)
                print(" ")
            input("Pulse <INTRO> para continuar...")
        elif (opcion == "3"):
                nombre = input("Que tarea sera completada:")
                tarea_encontrada = ToDoList.recuperarTarea(nombre)
                tarea_encontrada.completada = True
                input("Pulse <INTRO> para continuar...")
        elif (opcion == "4"):
            ToDoList.editarTarea()
            input("Pulse <Intro> para continuar...")
        elif (opcion == "5"):
            nombre = input("Que tarea quiere eliminar: ")
            ToDoList.eliminarTareas(ToDoList.recuperarTarea(nombre))
            print("Se ha eliminado la tarea")
            input("Pulse <INTRO> para continuar...")
        elif (opcion == "0"):
                print("HASTA PRONTO!!!!")
                sys.exit()

main()