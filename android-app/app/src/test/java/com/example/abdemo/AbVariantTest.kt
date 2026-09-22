package com.example.abdemo

import org.junit.Assert.assertEquals
import org.junit.Assert.assertTrue
import org.junit.Test

class AbVariantTest {

    @Test
    fun `random distributes visitors across both variants`() {
        val seen = (1..200).map { AbVariant.random() }.toSet()
        assertEquals(setOf(AbVariant.A, AbVariant.B), seen)
    }

    @Test
    fun `button texts are distinct between variants`() {
        assertEquals("Купить", AbVariant.A.buttonText)
        assertEquals("Купить сейчас со скидкой", AbVariant.B.buttonText)
        assertTrue(AbVariant.A.buttonText != AbVariant.B.buttonText)
    }
}
