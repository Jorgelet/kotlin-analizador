// Algoritmo 2: clasificacion con arreglo y entrada de datos
// (Array, if-else, funcion con retorno, readln)
fun calcularDoble(x: Int): Int {
    return x * 2
}

fun main() {
    val numeros: Array = arrayOf(1, 2, 3, 4)
    var total: Int = 0
    total = total + 100 - 25

    print("Ingrese un valor: ")
    val entrada: String = readln()

    val activo: Boolean = true
    if (total >= 50 || activo == true) {
        println("Mayor o activo")
    } else {
        println("Menor")
    }

    val doble: Int = calcularDoble(total)
    println(numeros)
    println(doble)
}
