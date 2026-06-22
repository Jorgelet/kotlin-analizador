// Algoritmo 1: mensajes y promedio (List, if, funcion sin retorno)
fun mostrarMensaje(nombre: String) {
    println("Hola")
    println(nombre)
}

fun main() {
    val nombres: List = listOf("Ana", "Luis", "Carlos")
    val cantidad: Int = 3
    var suma: Int = 10 + 20 + 30
    val promedio: Double = 20.5

    if (promedio >= 7.0 && cantidad > 0) {
        println("Aprobado")
    }

    mostrarMensaje("Ana")
    println(nombres)
    println(suma)
}
