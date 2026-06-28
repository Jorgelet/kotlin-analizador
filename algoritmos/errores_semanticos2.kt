// Errores semanticos:
// (1) reasignacion a un val (inmutable)
// (2) tipo incompatible en una declaracion con tipo explicito
fun main() {
    val nombre: String = 42
    val edad: Int = 18
    edad = 20
}
