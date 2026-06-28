// Errores semanticos:
// (1) variable usada sin declarar
// (2) redeclaracion de un nombre en el mismo ambito
fun main() {
    val x: Int = 5
    val x: Int = 10
    y = 20
}
