package com.example.abdemo

import kotlin.random.Random

/**
 * Логика выбора A/B-варианта - вынесена отдельно от Activity,
 * чтобы её можно было покрыть обычным unit-тестом (без эмулятора).
 */
enum class AbVariant(val buttonText: String) {
    A("Купить"),
    B("Купить сейчас со скидкой");

    companion object {
        fun random(random: Random = Random.Default): AbVariant =
            if (random.nextBoolean()) A else B
    }
}
