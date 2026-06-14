/*
 Algoritmo 2: suma de los numeros del 1 al limite usando un bucle while
*/

fun main() {
    val limite: Int = 10
    var contador: Int = 1
    var suma: Int = 0

    while (contador <= limite) {
        suma = suma + contador
        contador = contador + 1
    }

    print("La suma total es: ")
    println(suma)

    val promedio: Double = 5.5
    val activo: Boolean = true
    if (activo && promedio > 5.0) {
        println("Promedio aprobado")
    }
}