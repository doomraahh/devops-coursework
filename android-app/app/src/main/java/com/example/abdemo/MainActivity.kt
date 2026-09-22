package com.example.abdemo

import android.os.Bundle
import android.widget.Button
import android.widget.TextView
import androidx.appcompat.app.AppCompatActivity

class MainActivity : AppCompatActivity() {

    private var clicks = 0

    override fun onCreate(savedInstanceState: Bundle?) {
        super.onCreate(savedInstanceState)
        setContentView(R.layout.activity_main)

        val variant = AbVariant.random()

        val variantLabel = findViewById<TextView>(R.id.variantLabel)
        val clickCountLabel = findViewById<TextView>(R.id.clickCountLabel)
        val buyButton = findViewById<Button>(R.id.buyButton)

        variantLabel.text = getString(R.string.variant_label, variant.name)
        buyButton.text = variant.buttonText

        buyButton.setOnClickListener {
            clicks += 1
            clickCountLabel.text = getString(R.string.click_count, clicks)
        }
    }
}
