// Errores semanticos:
// (1) la condicion de if/while debe ser Boolean
// (2) llamada a una funcion no declarada
fun main() {
    val x: Int = 5
    if (x + 1) {
        println("hola")
    }
    inexistente(x)
}