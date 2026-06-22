// Algoritmo 3: tabla y bucle (Map, while, funcion de una expresion, booleanas)
fun cuadrado(n: Int): Int = n * n

fun main() {
    val edades: Map = mapOf("Ana" to 20, "Luis" to 25)
    var contador: Int = 1
    var acumulado: Int = 0

    while (contador <= 5) {
        acumulado = acumulado + cuadrado(contador)
        contador = contador + 1
    }

    val aprobado: Boolean = acumulado > 10 && !false
    if (aprobado || contador == 6) {
        println("Fin del ciclo")
    }

    println(edades)
    println(acumulado)
}