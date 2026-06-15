// Algoritmo 3: funciones con y sin retorno, y estructuras de datos

fun sumar(a: Int, b: Int): Int {
    return a + b
}

fun esAprobado(nota: Int): Boolean {
    return nota >= 7 || nota == 6
}

fun main() {
    val resultado: Int = sumar(4, 8)
    println("La suma es: ")
    println(resultado)

    val nombres: List = listOf("Ana", "Luis", "Carlos")
    println(nombres)

    print("Ingrese su nota: ")
    val nota: Int = 9
    if (esAprobado(nota) && nota <= 10) {
        println("Aprobado")
    } else {
        println("Reprobado")
    }
}