// Algoritmo 1: clasificar un numero como par o impar y mayoria de edad
// Ejercita: val/var, tipos, if/else, operadores aritmeticos y de comparacion

fun main() {
    val edad: Int = 20
    var numero: Int = 7

    if (edad >= 18) {
        println("Es mayor de edad")
    } else {
        println("Es menor de edad")
    }

    val residuo: Int = numero - (numero / 2) * 2
    if (residuo == 0) {
        println("El numero es par")
    } else {
        println("El numero es impar")
    }
}
